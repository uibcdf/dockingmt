"""Finite #33/#49 consumer receiving of MolSysMT #558, explicitly selected only.

These software controls do not admit a panel receptor or assign its chemistry.
All molecular construction, selection, generation, mapping and storage are
provider-owned. The controller stages this module/data through the shared SDK.
"""

import gzip
import hashlib
import json
import os
import warnings
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

from dmt_test_support.qualify_chemical_templates import snapshot
from dockingmt.preparation._molsys import detached_provider_report


def _save(name, data):
    output = Path(os.environ['DMT_TERMINAL_OUTPUT'])
    output.mkdir(parents=True, exist_ok=True)
    with (output / (name + '.json')).open('x') as stream:
        json.dump(detached_provider_report(data), stream, indent=2, allow_nan=False)
        stream.write('\n')


def _journal(kind, **data):
    path = Path(os.environ['DMT_TERMINAL_OUTPUT']) / 'calls.jsonl'
    existing = (
        [json.loads(line) for line in path.read_text().splitlines()]
        if path.exists()
        else []
    )
    if kind == 'terminal_attempt':
        assert sum(row['kind'] == kind for row in existing) < 10
    with path.open('a') as stream:
        stream.write(json.dumps({'kind': kind, **data}) + '\n')


def _complete(source, **options):
    options = {
        'N_terminal': None,
        'C_terminal': None,
        'pH': 7.4,
        'keep_ids': True,
        'engine': 'MolSysMT',
        'return_report': True,
        **options,
    }
    _journal('terminal_attempt', options=options)
    try:
        result = msm.build.add_missing_terminal_cappings(source, **options)
    except BaseException as error:
        _journal('terminal_error', error_type=type(error).__name__)
        raise
    _journal('terminal_return')
    return result


def _snapshot(source):
    return {
        'molecular': snapshot(source),
        'occupancy': source.structures.occupancy,
        'b_factor': (
            puw.get_value(source.structures.b_factor, to_unit='nm**2')
            if source.structures.b_factor is not None
            else None
        ),
        'observation_units': {'b_factor': 'nm**2', 'occupancy': 'dimensionless'},
        'molecular_mechanics_present': source.molecular_mechanics is not None,
    }


def _detached_snapshot(source):
    return detached_provider_report(_snapshot(source))


def _history(source):
    return detached_provider_report(source.chemical_states.get_preparation_history())


def _geometry(source, output, report):
    forward, inverse = (
        report['source_to_output_atom_indices'],
        report['output_to_source_atom_indices'],
    )
    assert forward.dtype == inverse.dtype == np.int64
    assert forward.shape == (source.get_n_atoms(),)
    assert inverse.shape == (output.get_n_atoms(),)
    np.testing.assert_array_equal(inverse[forward], np.arange(source.get_n_atoms()))
    np.testing.assert_array_equal(inverse[report['generated_atom_indices']], -1)
    before = puw.get_value(source.structures.coordinates, to_unit='nm')
    mapped = puw.get_value(output.structures.coordinates, to_unit='nm')[:, forward]
    np.testing.assert_allclose(mapped, before, rtol=0, atol=1e-15)
    assert report['coordinate_unit'] == 'nm'
    assert report['complete_chemical_state_assigned'] is False
    return {
        'unit': 'nm',
        'absolute_tolerance': 1e-15,
        'max_absolute_delta': float(np.max(np.abs(mapped - before))),
        'exactly_equal': bool(np.array_equal(mapped, before)),
    }


def _warned_complete(source, expected, **options):
    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter('always')
        result = _complete(source, **options)
    assert observed and {type(w.message).__name__ for w in observed} == {expected}
    return result, [
        {'category': type(w.message).__name__, 'message': str(w.message)}
        for w in observed
    ]


@pytest.fixture(scope='module')
def small_source():
    _journal('peptide_factory')
    peptide = msm.build.build_peptide('AA', engine='MolSysMT')
    peptide = msm.remove(peptide, selection='atom_type=="H" or atom_name=="OXT"')
    source = msm.merge([peptide, peptide], keep_ids=False)
    source.molecular_mechanics = None
    source = msm.append_structures(source, source, in_place=False)
    assert source.get_n_atoms() == 20 and source.structures.n_structures == 2
    return source


def test_synthetic_insertions_map_geometry_and_dockingmt_transport(small_source):
    before = _detached_snapshot(small_source)
    result = _complete(small_source, attribute_policy='strict')
    output, report = result['molecular_system'], result['report']
    assert report['schema'] == 'molsysmt.terminal_completion@1'
    assert output.get_n_atoms() == 22
    np.testing.assert_array_equal(
        report['source_to_output_atom_indices'], np.r_[np.arange(10), np.arange(11, 21)]
    )
    np.testing.assert_array_equal(report['generated_atom_indices'], [10, 21])
    np.testing.assert_array_equal(report['structure_indices'], [0, 1])
    np.testing.assert_array_equal(
        report['introduced_bond_atom_pairs'], [[8, 10], [19, 21]]
    )
    assert report['bond_index_scope'] == 'output'
    geometry = _geometry(small_source, output, report)
    transported = detached_provider_report(report)
    assert json.loads(json.dumps(transported, allow_nan=False)) == transported
    composed = msm.compose_atom_maps([report])
    np.testing.assert_array_equal(
        composed['source_to_output_atom_indices'],
        report['source_to_output_atom_indices'],
    )
    assert set(composed['generated_output_atom_indices']) == {10, 21}
    transported['source_to_output_atom_indices'][0] = -99
    assert report['source_to_output_atom_indices'][0] == 0
    assert _detached_snapshot(small_source) == before
    _save(
        'synthetic-map',
        {
            'report': report,
            'geometry': geometry,
            'source_before': before,
            'source_after': _snapshot(small_source),
        },
    )


def test_synthetic_history_and_h5msm_keep_original_operation_axes(
    small_source, tmp_path
):
    before = _history(small_source)
    result = _complete(small_source, attribute_policy='strict')
    output, report = result['molecular_system'], result['report']
    first = _history(output)
    assert first[: len(before)] == before and first[-1][
        'report'
    ] == detached_provider_report(report)
    noop = _complete(output, selection=[], attribute_policy='strict')
    current = noop['molecular_system']
    history = _history(current)
    assert history[: len(first)] == first
    assert history[-1]['report']['n_source_atoms'] == 22
    assert first[-1]['report']['n_source_atoms'] == 20
    path = tmp_path / 'completion.h5msm'
    msm.convert(current, to_form=str(path), format_version='1.0')
    restored = msm.convert(path)
    assert _history(restored) == history
    assert _history(small_source) == before
    _save(
        'history-persistence',
        {'history': history, 'restored_history': _history(restored), 'report': report},
    )


def test_synthetic_empty_selection_returns_independent_identity(small_source):
    before = _detached_snapshot(small_source)
    result = _complete(small_source, selection=[], attribute_policy='strict')
    output, report = result['molecular_system'], result['report']
    assert output is not small_source and report['status'] == 'unchanged'
    np.testing.assert_array_equal(
        report['source_to_output_atom_indices'], np.arange(20)
    )
    assert report['generated_atom_indices'].size == 0
    assert report['coordinate_evidence'] == 'not_generated'
    _geometry(small_source, output, report)
    assert _detached_snapshot(small_source) == before
    _save('empty-selection', {'report': report})


def test_synthetic_strict_loss_refusal_preserves_input(small_source):
    source = small_source.copy()
    source.structures.occupancy = np.ones((2, 20))
    before = _detached_snapshot(source)
    with pytest.raises(Exception) as caught:
        _complete(source, attribute_policy='strict')
    assert type(caught.value).__name__ == 'StructuralInconsistencyError'
    assert _detached_snapshot(source) == before
    _save(
        'strict-loss-refusal',
        {
            'error_type': type(caught.value).__name__,
            'source_before': before,
            'source_after': _snapshot(source),
        },
    )


def test_synthetic_intersection_reports_actual_loss(small_source):
    source = small_source.copy()
    source.structures.occupancy = np.ones((2, 20))
    before = _detached_snapshot(source)
    result, observed = _warned_complete(
        source, 'StructuralAttributeDropWarning', attribute_policy='intersection'
    )
    output, report = result['molecular_system'], result['report']
    assert report['dropped_attributes'] == ['occupancy']
    assert output.structures.occupancy is None
    geometry = _geometry(source, output, report)
    assert _detached_snapshot(source) == before
    _save(
        'intersection-loss',
        {'report': report, 'warnings': observed, 'geometry': geometry},
    )


def test_synthetic_default_still_returns_native_system(small_source):
    before = _detached_snapshot(small_source)
    output = _complete(small_source, return_report=False, attribute_policy='strict')
    assert msm.get_form(output) == 'molsysmt.MolSys'
    assert output.get_n_atoms() == 22
    assert _detached_snapshot(small_source) == before
    _save(
        'default-return',
        {'form': msm.get_form(output), 'n_atoms': output.get_n_atoms()},
    )


@pytest.fixture(scope='module')
def original_source(tmp_path_factory):
    archive = (
        Path(__file__).resolve().parents[1]
        / 'devguide/validation/data/panel_admission_2026-11-04/1HSG.pdb.gz'
    )
    packed = archive.read_bytes()
    assert (
        hashlib.sha256(packed).hexdigest()
        == 'eef33be911e35b27f49b1ce97cde422ef4bb792af452959dd0c662957f7c2b3a'
    )
    raw = gzip.decompress(packed)
    assert (
        hashlib.sha256(raw).hexdigest()
        == 'd430675c358060808ef614002cfdcfcfa824714d89f1240adf5749d2ba60fed2'
    )
    path = tmp_path_factory.mktemp('original') / 'source.pdb'
    path.write_bytes(raw)
    source = msm.convert(path, get_missing_bonds=False)
    protein = msm.extract(source, selection='group_type=="amino acid"')
    assert protein.get_n_atoms() == 1514
    yield protein
    assert path.read_bytes() == raw and archive.read_bytes() == packed


def test_original_declared_only_backbone_remains_unassessed(original_source):
    before = _detached_snapshot(original_source)
    result, observed = _warned_complete(
        original_source,
        'UnassessedPeptideBackboneWarning',
        attribute_policy='intersection',
    )
    output, report = result['molecular_system'], result['report']
    assert output.get_n_atoms() == 1514 and report['status'] == 'unchanged'
    assert [entry['chain_index'] for entry in report['unassessed']] == [0, 1]
    assert report['generated_atom_indices'].size == 0
    _geometry(original_source, output, report)
    assert _detached_snapshot(original_source) == before
    _save(
        'original-unassessed',
        {
            'report': report,
            'warnings': observed,
            'source_before': before,
            'source_after': _snapshot(original_source),
        },
    )


def test_original_inferred_backbone_preserves_maps_history_and_observations(
    original_source,
):
    original_before = _detached_snapshot(original_source)
    _journal('covalent_inference')
    inferred = msm.build.infer_covalent_bonds(original_source, structure_indices=0)
    assert _detached_snapshot(original_source) == original_before
    before, history = _detached_snapshot(inferred), _history(inferred)
    with pytest.raises(Exception) as caught:
        _complete(inferred, attribute_policy='strict')
    assert type(caught.value).__name__ == 'StructuralInconsistencyError'
    assert _detached_snapshot(inferred) == before
    result, observed = _warned_complete(
        inferred, 'StructuralAttributeDropWarning', attribute_policy='intersection'
    )
    output, report = result['molecular_system'], result['report']
    assert output.get_n_atoms() == 1516
    np.testing.assert_array_equal(report['generated_atom_indices'], [757, 1515])
    np.testing.assert_array_equal(
        report['source_to_output_atom_indices'],
        np.r_[np.arange(757), np.arange(758, 1515)],
    )
    assert report['dropped_attributes'] == ['b_factor', 'occupancy']
    geometry = _geometry(inferred, output, report)
    assert _history(output)[: len(history)] == history
    assert _history(output)[-1]['report'] == detached_provider_report(report)
    assert _detached_snapshot(inferred) == before
    _save(
        'original-mapped',
        {
            'report': report,
            'warnings': observed,
            'geometry': geometry,
            'source_before': before,
            'source_after': _snapshot(inferred),
        },
    )
