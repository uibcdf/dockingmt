"""Consume real chemical correspondence without fitting or changing baselines."""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_named_types import declared_source, explicit_source
from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.results import _molecular_atom_keys


def pose(source, *, cycle=False, distance=0, order=None):
    heavy = msm.select(source, selection='atom_type!="H"')
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom')[
        0, heavy
    ].copy()
    if cycle:
        coordinates = np.roll(coordinates, -1, axis=0)
    coordinates[:, 2] += distance
    keys = [_molecular_atom_keys(source)[i] for i in heavy]
    if order is not None:
        coordinates = coordinates[order]
        keys = [keys[i] for i in order]
    return dmt.DockingPose(
        puw.quantity(coordinates, 'angstrom'),
        rank=7,
        metadata={'pose_atom_order': 'verified_pdbqt_order', 'source_atom_keys': keys},
    )


def evaluate(result, reference, **kwargs):
    return dmt.evaluate_redocking(
        result,
        reference,
        rmsd_cutoff=puw.quantity(0.2, 'angstrom'),
        **kwargs,
    )


def test_opt_in_preserves_baseline_and_unaligned_negative_control(monkeypatch):
    source = explicit_source('c1ccccc1')
    before = puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom').copy()
    result = dmt.DockingResult([pose(source, cycle=True), pose(source, distance=4)])
    original = evaluate(result, source)
    saved = deepcopy(result.to_dict())
    calls = []
    native = msm.structure.get_symmetry_corrected_rmsd

    def observed(*args, **kwargs):
        calls.append(kwargs)
        return native(*args, **kwargs)

    monkeypatch.setattr(msm.structure, 'get_symmetry_corrected_rmsd', observed)
    report = evaluate(result, source, symmetry_options={'molecular_system': source})
    corrected = report.pop('symmetry_evaluation')
    assert report == original
    assert len(calls) == 2
    assert all(call['correspondences'] is calls[0]['correspondences'] for call in calls)
    assert corrected['criterion']['alignment'] == 'none'
    assert corrected['criterion']['search_scope'] == 'all_chemical_correspondences'
    assert corrected['criterion']['unselected_coordinates'] == (
        'unchanged_context_not_pose_geometry'
    )
    assert [row['rmsd'] for row in corrected['poses']] == pytest.approx([0, 4])
    assert corrected['poses'][0]['raw_rmsd'] > 1
    assert original['top_n'][0]['recovered'] is False
    assert corrected['top_n'][0]['recovered'] is True
    assert result.to_dict() == saved
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom'), before
    )
    assert (
        corrected['correspondences']['rule_version'] == 'declared_graph_isomorphism@1'
    )
    assert corrected['evaluator']['references']


def test_permuted_pose_axis_nondefault_units_and_detached_maps():
    source = declared_source('c1ccccc1')
    result = dmt.DockingResult([pose(source, cycle=True, order=[2, 0, 5, 1, 4, 3])])
    options = {'molecular_system': source, 'tie_tolerance': puw.quantity(1e-8, 'pm')}
    with puw.context(standard_units=['pm', 'fs']):
        report = evaluate(result, source, symmetry_options=options)
    corrected = report['symmetry_evaluation']
    assert corrected['poses'][0]['rmsd'] == pytest.approx(0, abs=1e-12)
    assert corrected['criterion']['unit'] == 'angstrom'
    assert corrected['criterion']['tie_tolerance_angstrom'] == pytest.approx(1e-10)
    corrected['correspondences']['atom_correspondences'][0][0][0] = -1
    again = evaluate(result, source, symmetry_options=options)
    assert (
        again['symmetry_evaluation']['correspondences']['atom_correspondences'][0][0][0]
        >= 0
    )


def test_non_equivalent_same_element_sites_are_not_exchanged():
    source = declared_source('CCO')
    reference = msm.copy(source)
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom')
    msm.set(source, coordinates=puw.quantity(coordinates[:, [1, 0, 2]], 'angstrom'))
    result = dmt.DockingResult([pose(source)])
    report = evaluate(result, reference, symmetry_options={'molecular_system': source})
    row = report['symmetry_evaluation']['poses'][0]
    assert row['rmsd'] == pytest.approx(row['raw_rmsd'])
    assert row['rmsd'] > 0.2


def test_benzamidinium_nitrogen_roles_are_not_normalized_by_resonance():
    reference = declared_source('NC(=[NH2+])c1ccccc1')
    query = msm.copy(reference)
    coordinates = puw.get_value(msm.get(query, coordinates=True), to_unit='angstrom')
    msm.set(
        query,
        coordinates=puw.quantity(
            coordinates[:, [2, 1, 0, 3, 4, 5, 6, 7, 8]], 'angstrom'
        ),
    )
    report = evaluate(
        dmt.DockingResult([pose(query)]),
        reference,
        symmetry_options={'molecular_system': query},
    )['symmetry_evaluation']
    for table in report['correspondences']['atom_correspondences']:
        assert table[0] == [0, 0]
        assert table[2] == [2, 2]
    assert report['poses'][0]['rmsd'] > 0.2


@pytest.mark.parametrize('missing_stereo', [None, 'unknown'])
def test_template_context_retains_stereo_and_rejects_missing_declarations(
    missing_stereo,
):
    from molsysmt._private.smonitor import StructuralInconsistencyError

    from devtools.qualify_3ptb_admission import DATA, expand
    from devtools.qualify_chemical_templates import snapshot, template_options

    source = msm.convert(
        DATA / '3PTB.pdb.gz', to_form='molsysmt.MolSys', get_missing_bonds=False
    )
    reference = msm.extract(source, selection="group_name=='BEN'")
    template = declared_source('NC(=[NH2+])c1ccccc1')
    options = template_options(
        template,
        np.column_stack((np.arange(9), [8, 6, 7, 0, 1, 2, 3, 4, 5])),
        identity='Explicit declared benzamidinium',
        uri='smiles:NC(=[NH2+])c1ccccc1',
        hydrogen_policy='stored_counts',
    )
    applied = msm.physchem.apply_chemical_template(
        reference, **options, connectivity_policy='complete_from_template'
    )['molecular_system']
    context, _ = expand(applied, receptor=False)
    result = dmt.DockingResult([pose(context)])
    before, saved = snapshot(context), result.to_dict()
    assert (
        list(msm.get(context, element='atom', atom_stereochemistry=True))
        == ['unspecified'] * 18
    )
    report = evaluate(result, context, symmetry_options={'molecular_system': context})
    assert report['symmetry_evaluation']['poses'][0]['rmsd'] == pytest.approx(0)
    maps = np.asarray(
        report['symmetry_evaluation']['correspondences']['atom_correspondences']
    )
    assert maps.shape == (2, 9, 2)
    np.testing.assert_array_equal(maps[:, 7:, 1], [[7, 8], [7, 8]])

    incomplete = msm.copy(context)
    msm.set(incomplete, atom_stereochemistry=[missing_stereo] * 18)
    with pytest.raises(StructuralInconsistencyError, match='stereochemistry'):
        evaluate(result, incomplete, symmetry_options={'molecular_system': incomplete})
    assert snapshot(context) == before and result.to_dict() == saved


@pytest.mark.parametrize('query_smiles', ['C[NH2+]C', 'CNC'])
def test_incompatible_chemical_state_or_h_encoding_propagates(query_smiles):
    from molsysmt._private.smonitor import StructuralInconsistencyError

    reference = explicit_source('CNC')
    context = declared_source(query_smiles)
    with pytest.raises(StructuralInconsistencyError):
        evaluate(
            dmt.DockingResult([pose(reference)]),
            reference,
            symmetry_options={'molecular_system': context},
        )


def test_provider_bound_failure_is_not_replaced_with_positional_success():
    from molsysmt._private.smonitor import UnsupportedHeavyOperationError

    source = declared_source('c1ccccc1')
    with pytest.raises(UnsupportedHeavyOperationError):
        evaluate(
            dmt.DockingResult([pose(source)]),
            source,
            symmetry_options={'molecular_system': source, 'max_matches': 1},
        )


@pytest.mark.parametrize('options', [{}, {'fit': True}, True, [], 42])
def test_invalid_options_fail_explicitly(options):
    source = declared_source('CCO')
    with pytest.raises(ArgumentError, match='symmetry_options'):
        evaluate(dmt.DockingResult([pose(source)]), source, symmetry_options=options)


def test_complete_reference_is_required_and_ordinary_empty_results_remain_supported():
    source = declared_source('CCO')
    item = pose(source)
    with pytest.raises(ArgumentError, match='complete declared molecular reference'):
        evaluate(
            dmt.DockingResult([item]),
            item.coordinates,
            symmetry_options={'molecular_system': source},
        )
    assert evaluate(dmt.DockingResult([]), source)['n_poses'] == 0
    with pytest.raises(ArgumentError, match='mapped pose population'):
        evaluate(
            dmt.DockingResult([]), source, symmetry_options={'molecular_system': source}
        )
