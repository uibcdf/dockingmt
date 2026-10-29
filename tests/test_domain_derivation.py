"""Selection-domain recipes retain the executed context without molecular copies."""

import hashlib
import json
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from test_engines import MINIMAL_LIG_PDBQT, MINIMAL_REC_PDBQT
from test_problem import _multi_structure_redocking_source

import dockingmt as dmt
from devtools.qualify_chemical_templates import snapshot
from dockingmt._private.smonitor import ArgumentError


def _box():
    source, _ = _multi_structure_redocking_source()
    return dmt.BoxRegion.from_selection(
        source,
        selection=[2, 3],
        structure_indices=1,
        padding=puw.quantity(2, 'angstrom'),
    )


@pytest.mark.parametrize('unit', ['nm', 'pm'])
def test_selection_recipe_retains_actual_axes_and_detaches_source_and_records(
    unit, monkeypatch
):
    source, coordinates = _multi_structure_redocking_source()
    before = snapshot(source)
    indices = np.array([2, 3])
    select, get = msm.select, msm.get
    calls = []

    def selected(item, **options):
        calls.append((item, options))
        return select(item, **options)

    monkeypatch.setattr(msm, 'select', selected)
    with puw.context(standard_units=[unit, 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        box = dmt.BoxRegion.from_selection(
            source,
            selection=indices,
            structure_indices=1,
            padding=puw.quantity(2, 'angstrom'),
        )
        saved = box.to_dict()
        recovered = dmt.BoxRegion.from_dict(json.loads(json.dumps(saved)))
        assert recovered.to_dict() == saved
        assert puw.configure.report() == policy
    recipe = box.derivation
    assert recipe['source'] == {
        'form': 'molsysmt.MolSys',
        'n_atoms': len(coordinates[0]),
        'fingerprint': None,
    }
    assert recipe['selection'] == recipe['atom_indices'] == [2, 3]
    assert recipe['structure_indices'] == 1 and recipe['structure_position'] == 0
    assert recipe['structure_chemical_state'] == {
        'index': 1,
        'id': 'selected-second-state',
    }
    assert recipe['selection_chemical_state'] == 'reference'
    assert recipe['padding'] == {'value': pytest.approx(0.2), 'unit': 'nm'}
    np.testing.assert_allclose(
        puw.get_value(box.center, to_unit='angstrom'),
        coordinates[1, [2, 3]].mean(axis=0),
        rtol=0,
        atol=1e-12,
    )
    assert any(
        item is source and options['structure_indices'] == 1 for item, options in calls
    )
    indices[0] = 0
    recipe['atom_indices'][0] = 0
    saved['derivation']['selection'][0] = 0
    assert box.derivation['selection'] == box.derivation['atom_indices'] == [2, 3]
    assert snapshot(source) == before
    # Later caller edits do not silently rebind the historical domain.
    msm.set(source, coordinates=get(source, coordinates=True) + puw.quantity(1, 'nm'))
    assert box.derivation['atom_indices'] == [2, 3]


def test_multiple_requested_frames_keep_the_existing_first_returned_policy():
    source, coordinates = _multi_structure_redocking_source()
    box = dmt.BoxRegion.from_selection(
        source,
        selection=[2, 3],
        structure_indices=[1, 0],
        padding=puw.quantity(2, 'angstrom'),
    )
    assert box.derivation['structure_indices'] == [1, 0]
    assert box.derivation['structure_position'] == 0
    assert box.derivation['structure_chemical_state']['index'] == 1
    np.testing.assert_allclose(
        puw.get_value(box.center, to_unit='angstrom'),
        coordinates[1, [2, 3]].mean(axis=0),
        rtol=0,
        atol=1e-12,
    )


@pytest.mark.parametrize('kind', ['native', 'file'])
def test_redocking_records_original_source_not_the_reindexed_temporary_view(kind):
    source, _ = _multi_structure_redocking_source()
    frame = 1
    if kind == 'file':
        source = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
        frame = 0
    problem = dmt.DockingProblem.for_redocking(
        source,
        receptor_selection=[0, 1],
        partner_selection=[2, 3],
        structure_index=frame,
        padding=puw.quantity(2, 'angstrom'),
    )
    recipe = problem.search_domain.derivation
    assert recipe['method'] == 'redocking_partner_bounds'
    assert recipe['source']['n_atoms'] > 2
    assert recipe['atom_indices'] == problem.partner_atom_indices == [2, 3]
    assert recipe['selection'] == [2, 3] and recipe['structure_indices'] == frame
    assert recipe['selection_chemical_state'] == 'structure'
    expected = (
        {
            'kind': 'file',
            'sha256': hashlib.sha256(Path(source).read_bytes()).hexdigest(),
        }
        if kind == 'file'
        else None
    )
    assert recipe['source']['fingerprint'] == expected
    saved = problem.to_dict()
    restored = dmt.DockingProblem.from_dict(saved, receptor=source, partner=source)
    assert restored.search_domain.to_dict() == saved['search_domain']


def test_explicit_and_legacy_boxes_keep_absent_derivation():
    box = dmt.BoxRegion(puw.quantity([0, 0, 0], 'nm'), puw.quantity([2, 2, 2], 'nm'))
    assert box.derivation is None
    saved = box.to_dict()
    assert 'derivation' not in saved
    assert dmt.BoxRegion.from_dict(saved).to_dict() == saved


@pytest.mark.parametrize(
    'damage',
    [
        'schema',
        'method',
        'count',
        'atoms',
        'fingerprint',
        'frame',
        'padding',
        'state',
        'basis',
        'nan',
    ],
)
def test_malformed_or_changed_geometry_binding_is_rejected(damage):
    saved = _box().to_dict()
    recipe = saved['derivation']
    if damage == 'schema':
        recipe['schema'] = 'unknown@2'
    elif damage == 'method':
        recipe['method'] = 'guessed'
    elif damage == 'count':
        recipe['source']['n_atoms'] = 0
    elif damage == 'atoms':
        recipe['atom_indices'] = [10**9]
    elif damage == 'fingerprint':
        recipe['source']['fingerprint'] = {'kind': 'file', 'sha256': 'bad'}
    elif damage == 'frame':
        recipe['structure_indices'] = True
    elif damage == 'padding':
        recipe['padding']['value'] = -1
    elif damage == 'state':
        recipe['structure_chemical_state']['index'] = True
    elif damage == 'basis':
        saved['center']['value'][0] += 1
    else:
        recipe['box']['center'][0] = float('nan')
    with pytest.raises(ArgumentError, match='derivation'):
        dmt.BoxRegion.from_dict(saved)


def test_mutated_live_geometry_cannot_retain_old_derivation():
    box = _box()
    box.center[0] = puw.quantity(42, 'nm')
    for operation in [box.to_dict, box.to_backend_box]:
        with pytest.raises(ArgumentError, match='no longer matches'):
            operation()


def test_file_change_during_construction_is_not_silently_bound(tmp_path, monkeypatch):
    source = tmp_path / 'source.h5msm'
    source.write_bytes(
        Path(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']).read_bytes()
    )
    get = msm.get

    def changed(item, **options):
        value = get(item, **options)
        if item == source and options.get('n_atoms'):
            with source.open('ab') as stream:
                stream.write(b'changed-caller-bytes')
        return value

    monkeypatch.setattr(msm, 'get', changed)
    with pytest.raises(ArgumentError, match='Source bytes changed'):
        dmt.BoxRegion.from_selection(
            source, selection=[2, 3], padding=puw.quantity(2, 'angstrom')
        )


def test_provider_selection_failure_propagates_without_geometry_fallback(monkeypatch):
    source, _ = _multi_structure_redocking_source()

    def refuse(*args, **kwargs):
        raise RuntimeError('provider selection refusal')

    monkeypatch.setattr(msm, 'select', refuse)
    with pytest.raises(RuntimeError, match='provider selection refusal'):
        dmt.BoxRegion.from_selection(source)


def test_backend_result_keeps_recipe_alongside_actual_projection_without_native_search(
    monkeypatch,
):
    import vina

    calls = []

    class FakeVina:
        def __init__(self, **options):
            pass

        def set_receptor(self, **options):
            pass

        def set_ligand_from_string(self, value):
            pass

        def compute_vina_maps(self, center, box_size):
            calls.append((center, box_size))

        def dock(self, exhaustiveness, n_poses):
            pass

        def energies(self, n_poses, energy_range):
            return np.zeros((1, 5))

        def poses(self, n_poses, energy_range, coordinates_only):
            return (
                np.array([[[0.0, 0, 0], [1.5, 0, 0]]])
                if coordinates_only
                else MINIMAL_LIG_PDBQT
            )

        def info(self):
            return {'weights': [1.0], 'box_spacing': 0.375}

    monkeypatch.setattr(vina, 'Vina', FakeVina)
    box = _box()
    result = dmt.dock(
        dmt.DockingProblem(
            receptor=MINIMAL_REC_PDBQT, partner=MINIMAL_LIG_PDBQT, search_domain=box
        ),
        dmt.VinaProtocol(exhaustiveness=1, n_poses=1, cpu=1),
    )
    saved = result.to_dict()
    recipe = box.derivation
    assert saved['problem_info']['search_domain']['derivation'] == recipe
    assert saved['provenance']['search_domain']['derivation'] == recipe
    backend = result.provenance['backend_box']
    assert calls == [(backend['center'], backend['size'])]
    expected = box.to_backend_box(unit='angstrom')
    np.testing.assert_allclose(backend['center'], expected['center'], rtol=0, atol=1e-6)
    assert (
        dmt.DockingResult.from_dict(saved).provenance['search_domain']['derivation']
        == recipe
    )


def test_literal_input_records_actual_bytes_without_inventing_native_identity():
    text = 'pdbqt_text:' + MINIMAL_LIG_PDBQT
    box = dmt.BoxRegion.from_selection(text, padding=puw.quantity(2, 'angstrom'))
    assert box.derivation['source']['form'] == 'string:pdbqt_text'
    assert box.derivation['source']['fingerprint'] == {
        'kind': 'literal',
        'sha256': hashlib.sha256(text.encode()).hexdigest(),
    }
    assert box.derivation['structure_chemical_state'] is None
    assert dmt.BoxRegion.from_dict(box.to_dict()).to_dict() == box.to_dict()


def test_redocking_preserves_absent_padding_on_a_nonflat_source():
    from molsysmt.native import MolSys

    source = MolSys(n_atoms=4)
    msm.set(
        source,
        atom_id=['1', '2', '3', '4'],
        atom_name=['C1', 'C2', 'C3', 'C4'],
        atom_type=['C'] * 4,
        coordinates=puw.quantity(
            [[[0.0, 0, 0], [1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]]], 'nm'
        ),
    )
    problem = dmt.DockingProblem.for_redocking(
        source, receptor_selection=[0], partner_selection=[1, 2, 3], padding=None
    )
    assert problem.search_domain.derivation['padding'] is None
    np.testing.assert_allclose(
        puw.get_value(problem.search_domain.lengths, to_unit='nm'), [1, 1, 1]
    )
