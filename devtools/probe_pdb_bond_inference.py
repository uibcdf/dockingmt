"""Retain reader-policy and native-candidate evidence without changing inputs.

Run in molsyssuite@uibcdf_3.14 with the qualified MolSysMT source on PYTHONPATH.
OpenMM is needed only for the comparison profile. Native candidates are not
applied or treated as validated chemistry. This command writes a new evidence
record; it does not overwrite the earlier preparation benchmark.
"""

import builtins
import hashlib
import importlib.metadata as metadata
import json
import sys
from collections import Counter
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from pathlib import Path

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def _without_openmm():
    original_import = builtins.__import__

    def blocked(name, *args, **kwargs):
        if name == 'openmm' or name.startswith('openmm.'):
            raise ModuleNotFoundError('OpenMM blocked for reader-policy reproduction')
        return original_import(name, *args, **kwargs)

    builtins.__import__ = blocked
    try:
        yield
    finally:
        builtins.__import__ = original_import


def _pairs(source):
    return {
        tuple(sorted(map(int, pair)))
        for pair in msm.get(source, inner_bonded_atom_pairs=True)
    }


def probe():
    """Compare explicit-only, unavailable-engine and native candidate profiles."""
    cases = []
    for name, path in (
        ('181L', Path(msm.systems['T4 lysozyme L99A']['181l.pdb'])),
        ('1IEP', ROOT / 'tests/data/vina_torsions/1iep_receptorH.pdb'),
    ):
        original_bytes = path.read_bytes()
        with _without_openmm():
            unavailable = msm.convert(str(path), to_form='molsysmt.MolSys')
        handler = msm.convert(str(path), to_form='molsysmt.PDBFileHandler')
        try:
            explicit = msm.convert(
                handler, to_form='molsysmt.MolSys', get_missing_bonds=False
            )
        finally:
            handler.close()
        assert _pairs(unavailable) == _pairs(explicit)
        reference = msm.convert(str(path), to_form='molsysmt.MolSys')
        file_flag_false = msm.convert(
            str(path), to_form='molsysmt.MolSys', get_missing_bonds=False
        )
        report = msm.build.get_residue_chemical_coverage(
            unavailable, chemical_state='structure', structure_indices=0
        )
        # Reuse explicit source indices: connectivity changes molecule membership,
        # so separately evaluating the same molecule selection is not comparable.
        indices = msm.select(reference, selection="molecule_type=='protein'")
        selected = msm.extract(explicit, selection=indices)
        selected_reference = msm.extract(reference, selection=indices)
        assert msm.get(selected, n_atoms=True) > 0
        for attribute in ('atom_name', 'atom_type', 'atom_id'):
            np.testing.assert_array_equal(
                msm.get(selected, element='atom', **{attribute: True}),
                msm.get(selected_reference, element='atom', **{attribute: True}),
            )
        before_pairs = _pairs(selected)
        before_coordinates = puw.get_value(
            msm.get(selected, element='atom', coordinates=True), to_unit='nm'
        ).copy()
        stdout = StringIO()
        with _without_openmm(), redirect_stdout(stdout):
            candidates = msm.build.get_missing_bonds(
                selected, engine='MolSysMT', pbc=False
            )
        assert _pairs(selected) == before_pairs
        np.testing.assert_array_equal(
            puw.get_value(
                msm.get(selected, element='atom', coordinates=True), to_unit='nm'
            ),
            before_coordinates,
        )
        candidate_graph = before_pairs | {
            tuple(sorted(map(int, pair))) for pair in candidates
        }
        reference_graph = _pairs(selected_reference)
        assert path.read_bytes() == original_bytes
        cases.append(
            {
                'case': name,
                'source_sha256': hashlib.sha256(original_bytes).hexdigest(),
                'source_atoms': msm.get(explicit, n_atoms=True),
                'without_openmm_bonds': len(_pairs(unavailable)),
                'explicit_handler_bonds': len(_pairs(explicit)),
                'openmm_bonds': len(_pairs(reference)),
                'file_get_missing_bonds_false_bonds': len(_pairs(file_flag_false)),
                'without_openmm_summary': report['summary'],
                'without_openmm_reason_counts': dict(
                    Counter(
                        reason
                        for group in report['groups']
                        for reason in group['reason_codes']
                    )
                ),
                'comparison_selection': "Explicit indices from the reference molecule_type=='protein' selection, reused on explicit-only input",
                'selected_source_atom_indices': [int(index) for index in indices],
                'pair_axis': 'extracted_selection_atom_indices',
                'selected_atoms': msm.get(selected, n_atoms=True),
                'native_candidate_bonds': len(candidate_graph),
                'openmm_comparison_bonds': len(reference_graph),
                'native_only_pairs': sorted(candidate_graph - reference_graph),
                'openmm_only_pairs': sorted(reference_graph - candidate_graph),
                'native_stdout': stdout.getvalue(),
                'native_stdout_lines': len(stdout.getvalue().splitlines()),
            }
        )
    provider_root = Path(msm.__file__).parent
    return {
        'evidence': 'Read-only source-specific candidate comparison, not independent chemical validation or a performance benchmark',
        'provider_reference_source': 'e8e4fff22d0df0d26a3b91d80ea5a85c04981aef',
        'provider_import': msm.__file__,
        'python': sys.version.split()[0],
        'interpreter': sys.executable,
        'versions': {
            name: metadata.version(name) for name in ('openmm', 'numpy', 'pandas')
        },
        'implementation_sha256': {
            name: hashlib.sha256((provider_root / name).read_bytes()).hexdigest()
            for name in (
                'build/get_missing_bonds.py',
                'form/file_pdb/to_molsysmt_MolSys.py',
                'form/molsysmt_PDBFileHandler/to_molsysmt_MolSys.py',
                '_private/residue_chemical_coverage.py',
            )
        },
        'cases': cases,
    }


def main():
    payload = probe()
    destination = ROOT / 'devguide/validation/data/pdb_bond_inference/probe.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2) + '\n')
    print(destination)
    for case in payload['cases']:
        print(
            case['case'],
            'explicit:',
            case['explicit_handler_bonds'],
            'OpenMM:',
            case['openmm_bonds'],
            'native-only:',
            len(case['native_only_pairs']),
            'OpenMM-only:',
            len(case['openmm_only_pairs']),
        )


if __name__ == '__main__':
    main()
