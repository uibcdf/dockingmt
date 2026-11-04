"""Reassess two saved Vina outputs; never execute a scientific engine.

Preserve/reproduce the failed original gate. Correct only unit spelling and
ephemeral-field exclusion, with unchanged exact numerical comparisons.
"""

import argparse
import gzip
import hashlib
import importlib.util
import json
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

import pyunitwizard as puw

HERE = Path(__file__).resolve().parent
OBSERVATIONS_SHA256 = 'c12ddf82559c057051c3ccf235dbf6379003dc876ab485b73f51dd8c552ba5e8'
PRODUCER_SHA256 = '38f4821166dfb0e2e914e2286d56ab76d095747f86b91daa88cbcbca580c9053'
FORBIDDEN = ('dockingmt', 'molsysmt', 'vina', 'molsysviewer', 'meeko')


def original_comparator():
    path = HERE / 'run_control.py'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == PRODUCER_SHA256
    spec = importlib.util.spec_from_file_location('frozen_fidelity_control', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare


def original_checks(record, comparator):
    """Run the frozen comparison, without invoking its native execution paths."""
    with tempfile.TemporaryDirectory(prefix='dmt-fidelity-offline-') as directory:
        root = Path(directory)
        for route, items in record['routes'].items():
            (root / route).mkdir()
            for name, item in items.items():
                (root / route / (name + '.json')).write_text(
                    json.dumps(item, allow_nan=False)
                )
        result = comparator(root)
    assert not root.exists()
    return result


def exact_score_unit(definitions):
    if set(definitions) != {'vina', 'inter', 'intra', 'torsion'}:
        return False
    target = puw.quantity(1.0, 'kcal/mol')
    for definition in definitions.values():
        candidate = puw.quantity(1.0, definition['unit'])
        if not puw.are_compatible(candidate, target):
            return False
        if puw.get_value(candidate, to_unit='kcal/mol', value_type=float) != 1.0:
            return False
    return True


def assess(record, comparator):
    checks = original_checks(record, comparator)['checks']
    infos = [
        record['routes'][route]['native']['engine_info']
        for route in ('adapter', 'direct')
    ]
    checks['same_engine_info'] = all(
        'rigid_receptor' in info and 'flex_receptor' in info for info in infos
    ) and {k: v for k, v in infos[0].items() if k != 'rigid_receptor'} == {
        k: v for k, v in infos[1].items() if k != 'rigid_receptor'
    }
    checks['normalized_score_units'] = exact_score_unit(
        record['routes']['adapter']['normalized']['score_definitions']
    )
    return {'checks': checks, 'passed': all(checks.values())}


def controls(record, comparator):
    """Adverse saved-data controls test strictness without new calculations."""
    cases = []

    def reject(name, mutate, required_failure):
        changed = deepcopy(record)
        mutate(changed)
        result = assess(changed, comparator)
        assert not result['passed'] and not result['checks'][required_failure], name
        cases.append({'mutation': name, 'rejected_by': required_failure})

    def change(path, value):
        def mutate(record):
            target = record
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value

        return mutate

    reject(
        'fifth native energy column',
        change(('routes', 'direct', 'native', 'energies', 0, 4), 1.0),
        'same_native_energies',
    )
    reject(
        'native numeric array entry',
        change(('routes', 'direct', 'native', 'coordinates', 0, 0, 0), 12345.0),
        'same_native_coordinate_array',
    )
    reject(
        'native PDBQT text byte',
        change(
            ('routes', 'direct', 'native', 'poses_pdbqt'),
            record['routes']['direct']['native']['poses_pdbqt'] + ' ',
        ),
        'same_native_pdbqt_bytes',
    )
    reject(
        'actual constructor seed',
        change(('routes', 'adapter', 'calls', 0, 'arguments', 'seed'), 8),
        'prescribed_adapter_calls',
    )
    reject(
        'actual map spacing',
        change(('routes', 'direct', 'calls', 3, 'arguments', 'spacing'), 0.5),
        'prescribed_direct_calls',
    )
    reject(
        'recorded input hash',
        change(
            ('routes', 'adapter', 'normalized', 'input_sha256', 'partner'), '0' * 64
        ),
        'recorded_input_hashes',
    )
    reject(
        'normalized score value',
        change(('routes', 'adapter', 'normalized', 'scores', 0, 'vina'), 0.0),
        'normalized_four_score_columns',
    )
    reject(
        'energy unit with different scale',
        change(
            ('routes', 'adapter', 'normalized', 'score_definitions', 'vina', 'unit'),
            'kJ/mol',
        ),
        'normalized_score_units',
    )
    reject(
        'incompatible unit dimension',
        change(
            ('routes', 'adapter', 'normalized', 'score_definitions', 'vina', 'unit'),
            'angstrom',
        ),
        'normalized_score_units',
    )
    reject(
        'engine scoring weight',
        change(('routes', 'direct', 'native', 'engine_info', 'weights', 0), 0.0),
        'same_engine_info',
    )
    reject(
        'unexpected flexible receptor',
        change(
            ('routes', 'direct', 'native', 'engine_info', 'flex_receptor'), 'unexpected'
        ),
        'same_engine_info',
    )

    def empty_outputs(changed):
        for route in ('adapter', 'direct'):
            native = changed['routes'][route]['native']
            native['coordinates'] = native['energies'] = []
            native['poses_pdbqt'] = ''
        normalized = changed['routes']['adapter']['normalized']
        normalized['n_poses'] = 0
        for key in ('scores', 'ranks', 'recorded_energies'):
            normalized[key] = []

    reject(
        'empty outputs on both routes', empty_outputs, 'nonempty_consistent_pose_counts'
    )
    alias = deepcopy(record)
    for definition in alias['routes']['adapter']['normalized'][
        'score_definitions'
    ].values():
        definition['unit'] = 'kcal/mol'
    assert assess(alias, comparator)['passed']
    return {'rejected_mutations': cases, 'equivalent_abbreviation_accepted': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    payload = (HERE / 'observations.json.gz').read_bytes()
    assert hashlib.sha256(payload).hexdigest() == OBSERVATIONS_SHA256
    record = json.loads(gzip.decompress(payload))
    comparator = original_comparator()
    assert not any(name in sys.modules for name in FORBIDDEN)
    original = original_checks(record, comparator)
    assert original == record['original_summary']
    assert {k for k, value in original['checks'].items() if not value} == {
        'same_engine_info',
        'normalized_score_units',
    }
    with puw.context(default_form='pint', default_parser='pint'):
        corrected = assess(record, comparator)
        negative = controls(record, comparator)
    assert corrected['passed']
    assert not any(name in sys.modules for name in FORBIDDEN)
    result = {
        'original_source': record['producer_source'],
        'original_gate_passed': original['passed'],
        'original_checks_passed': sum(original['checks'].values()),
        'observations_sha256': OBSERVATIONS_SHA256,
        'assessment_producer_sha256': hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        'assessment': corrected,
        'controls': negative,
        'original_search_attempts': 2,
        'new_search_attempts': 0,
        'optional_scientific_modules_loaded': [],
        'geometry_identity_and_physical_validity': 'not_assessed',
    }
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + '\n'
    output = HERE / 'offline_assessment.json'
    if args.check:
        assert output.read_text() == encoded
    else:
        output.write_text(encoded)
    print(
        json.dumps(
            {
                'original_gate': 'failed',
                'corrected_checks': sum(corrected['checks'].values()),
                'adverse_controls': len(negative['rejected_mutations']),
                'new_search_attempts': 0,
                'check': args.check,
            }
        )
    )


if __name__ == '__main__':
    main()
