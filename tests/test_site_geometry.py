"""Elementary support preserves physical meaning without molecular placement."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest
import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord, RecordError

import bindingmt as bmt
from bindingmt._private.interface_records import _digest
from bindingmt._private.site_geometry import AXES_KIND, FIELDS

SOURCE = {'owner': 'caller', 'id': 'source-A', 'revision': '1'}
FRAME = {'id': 'frame-A', 'coordinate_policy': 'cartesian', 'pbc': False}
ROTATION = np.array([[0.0, 1, 0], [-1, 0, 0], [0, 0, 1]])
FROZEN = Path(__file__).parent / 'data/site_geometry_compat/e1e6a33'


def declare(kind='sphere', **options):
    args = {
        'source': deepcopy(SOURCE),
        'frame': deepcopy(FRAME),
        'center': '[-1,2,3] nm',
        **options,
    }
    if kind == 'sphere':
        return bmt.BindingSite.from_sphere(**{'radius': '0.5 nm', **args})
    return bmt.BindingSite.from_box(**{'lengths': '[2,4,6] nm', **args})


def restored(record):
    record['content_sha256'] = _digest(record)
    return bmt.BindingSite.from_dict(record, experimental=True)


@pytest.mark.parametrize('kind', ['sphere', 'box'])
def test_physical_declaration_is_not_membership_or_placement(kind, tmp_path):
    site = declare(kind, structure_indices=[2], chemical_state_indices=[1])
    assert site.to_dict()['format_version'] == '0.3'
    assert site.inspect()['membership'] == {
        'state': 'not_supplied',
        'entry_count': None,
    }
    assert site.inspect()['geometry'] == {
        'state': 'declared',
        'kind': kind,
        'frame': FRAME,
        'placement_assurance': 'not_assessed',
    }
    assert site.inspect()['molecular_resolution'] == 'not_performed'
    assert not site.inspect()['capabilities']['domain_placement']
    assert site.definition['binding_support'] == 'unknown' and site.inspect()[
        'realization_coverage'
    ] == {'state': 'not_requested'}
    geometry = site.geometry
    np.testing.assert_allclose(
        puw.get_value(geometry['center'], to_unit='nm'),
        [-1, 2, 3],
        rtol=8 * np.finfo(float).eps,
        atol=0,
    )
    assert geometry['frame'] == FRAME and kind in site.describe()
    if kind == 'sphere':
        assert float(puw.get_value(geometry['radius'], to_unit='nm')) == 0.5
    else:
        np.testing.assert_array_equal(geometry['axes'], np.eye(3))
        np.testing.assert_array_equal(
            puw.get_value(geometry['lengths'], to_unit='nm'), [2, 4, 6]
        )
    site.save(tmp_path / 'geometry.json')
    assert (
        bmt.BindingSite.read(tmp_path / 'geometry.json', experimental=True).to_dict()
        == site.to_dict()
    )
    assert site.copy().to_dict() == site.to_dict()


@pytest.mark.parametrize('kind', ['sphere', 'box'])
@pytest.mark.parametrize('form', ['pint', 'unyt'])
def test_equivalent_units_and_application_policy_are_preserved(kind, form):
    with puw.context(default_form=form, standard_units=['pm', 'fs']):
        before = puw.configure.report()
        args = {'center': puw.quantity([-10, 20, 30], 'angstrom')}
        args.update(
            {'radius': '5 angstrom'}
            if kind == 'sphere'
            else {'lengths': '[20,40,60] angstrom'}
        )
        site = declare(kind, **args)
        geometry = site.geometry
        np.testing.assert_allclose(
            puw.get_value(geometry['center'], to_unit='nm'),
            [-1, 2, 3],
            rtol=8 * np.finfo(float).eps,
            atol=0,
        )
        key = 'radius' if kind == 'sphere' else 'lengths'
        expected = 0.5 if kind == 'sphere' else [2, 4, 6]
        np.testing.assert_allclose(
            puw.get_value(geometry[key], to_unit='nm'),
            expected,
            rtol=8 * np.finfo(float).eps,
            atol=0,
        )
        assert puw.get_form(geometry['center']) == form
        assert puw.configure.report() == before


@pytest.mark.parametrize(
    'axes', [ROTATION, ROTATION.tolist(), ROTATION.astype(np.float32)]
)
def test_oriented_box_axes_are_retained_not_replaced_by_a_search_box(axes):
    site = declare('box', axes=axes)
    np.testing.assert_array_equal(site.geometry['axes'], ROTATION)
    raw = site.to_dict()
    saved = bmt.BindingSite.from_dict(
        json.loads(json.dumps(raw, sort_keys=True)), experimental=True
    )
    assert saved.to_dict() == raw and not isinstance(site, bmt.BoxRegion)
    assert not site.inspect()['capabilities']['domain_placement']


@pytest.mark.parametrize('kind', ['sphere', 'box'])
def test_geometry_and_evidence_are_detached_through_interpretation(kind):
    frame = deepcopy(FRAME)
    site = declare(kind, frame=frame)
    before = site.to_dict()
    geometry = site.geometry
    frame['id'] = 'changed'
    geometry['center'][0] = puw.quantity(99, 'nm')
    geometry['frame']['id'] = 'edited'
    if kind == 'box':
        geometry['axes'][0, 0] = 99
    assert site.to_dict() == before
    observed = site.with_evidence(
        key='annotation',
        source={'owner': 'curator', 'id': 'support'},
        observation={'reported_support': 'geometry'},
        attribution={'producer': 'curator'},
    )
    revised = observed.with_definition(
        claim='Retain support only',
        criterion={'kind': 'manual_rule'},
        reason='Explicit interpretation',
    )
    assert (
        revised.evidence == observed.evidence
        and revised.evidence[0]['original_claim_ref'] == site.definition_ref
    )
    assert revised.definition['evidence_refs'] == [] and revised.views == site.views
    assert revised.to_dict()['format_version'] == '0.3'


@pytest.mark.parametrize('kind', ['sphere', 'box'])
@pytest.mark.parametrize(
    'center',
    [None, [1, 2, 3], '[1,2] nm', '[1,2,3] ps', '[nan,2,3] nm', '[[1,2,3]] nm'],
)
def test_invalid_center_shape_units_or_value_refuse(kind, center):
    with pytest.raises(bmt.exceptions.ArgumentError):
        declare(kind, center=center)


@pytest.mark.parametrize(
    'radius', [None, 1, '0 nm', '-1 nm', '[1] nm', '1 ps', 'nan nm']
)
def test_invalid_sphere_extent_refuses(radius):
    with pytest.raises(bmt.exceptions.ArgumentError):
        declare(radius=radius)


@pytest.mark.parametrize(
    'lengths', [None, [1, 2, 3], '[0,1,2] nm', '[-1,1,2] nm', '[1,2] nm', '[1,2,3] ps']
)
def test_invalid_full_box_lengths_refuse(lengths):
    with pytest.raises(bmt.exceptions.ArgumentError):
        declare('box', lengths=lengths)


@pytest.mark.parametrize(
    'axes',
    [
        np.diag([-1, 1, 1]),
        np.eye(3) * 2,
        np.zeros((3, 3)),
        np.array([[1, 0.1, 0], [0, 1, 0], [0, 0, 1]]),
        np.ones((2, 3)),
        np.eye(3, dtype=bool),
        [['1', 0, 0], [0, 1, 0], [0, 0, 1]],
        puw.quantity(np.eye(3), 'radians'),
    ],
)
def test_invalid_orientation_refuses_without_repair_or_unit_stripping(axes):
    with pytest.raises(bmt.exceptions.ArgumentError):
        declare('box', axes=axes)


def test_orientation_does_not_coerce_arbitrary_objects():
    calls = []

    class Fake:
        def __float__(self):
            calls.append('coerced')
            return 1.0

    with pytest.raises(bmt.exceptions.ArgumentError):
        declare('box', axes=[[Fake(), 0, 0], [0, 1, 0], [0, 0, 1]])
    assert calls == []


@pytest.mark.parametrize(
    'frame',
    [
        {},
        {'id': '', 'coordinate_policy': 'cartesian', 'pbc': False},
        {'id': 'x', 'coordinate_policy': 'cartesian', 'pbc': 0},
        {'id': 'x', 'coordinate_policy': 'fractional', 'pbc': False},
        {'id': 'x', 'coordinate_policy': 'cartesian', 'pbc': True},
    ],
)
def test_frame_is_explicit_and_unsupported_placement_is_not_downgraded(frame):
    with pytest.raises(
        (bmt.exceptions.ArgumentError, bmt.exceptions.CapabilityMismatchError)
    ):
        declare(frame=frame)


@pytest.mark.parametrize('indices', [[2, 0], [2, 2], [2, 0, 2]])
def test_one_saved_geometry_does_not_manufacture_a_multi_occurrence_ensemble(indices):
    with pytest.raises(
        bmt.exceptions.ArgumentError, match='one source-structure occurrence'
    ):
        declare(structure_indices=indices)


@pytest.mark.parametrize(
    'field,quantity',
    [('center', '[1,2] nm'), ('center', '[1,2,3] ps'), ('radius', '-1 nm')],
)
def test_resealed_quantity_still_needs_field_dimension_shape_and_positive_extent(
    field, quantity
):
    record = declare().to_dict()
    record['views'][0]['payload'][field] = QuantityRecord.from_quantity(
        puw.quantity(quantity), field=FIELDS[field]
    ).to_dict()
    with pytest.raises((bmt.exceptions.ArgumentError, RecordError)):
        restored(record)


def test_named_quantity_fields_and_semantic_axis_kind_cannot_be_swapped():
    record = declare().to_dict()
    record['views'][0]['payload']['center'] = record['views'][0]['payload']['radius']
    with pytest.raises(RecordError):
        restored(record)
    record = declare('box').to_dict()
    record['views'][0]['payload']['axes'] = QuantityRecord.from_quantity(
        puw.quantity(np.eye(3), 'dimensionless'),
        field=FIELDS['box_axes'],
        kind='urn:other:quantity',
    ).to_dict()
    with pytest.raises(RecordError):
        restored(record)
    assert AXES_KIND == 'urn:bindingmt:site:box-axes'


def test_root_content_digest_does_not_replace_the_shared_quantity_seal():
    record = declare().to_dict()
    record['views'][0]['payload']['radius']['digest'] = 'corrupted'
    with pytest.raises(RecordError):
        restored(record)


@pytest.mark.parametrize('version', ['0.1', '0.2'])
def test_geometry_cannot_be_disguised_as_an_older_profile(version):
    record = declare().to_dict()
    record['format_version'] = version
    with pytest.raises(bmt.exceptions.ArgumentError, match='0.3'):
        restored(record)


@pytest.mark.parametrize('name', ['atoms.json', 'groups.json', 'cited.json'])
def test_actual_original_02_membership_remains_unchanged_readable(name):
    manifest = json.loads((FROZEN / 'manifest.json').read_text())
    path = FROZEN / name
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == manifest['records'][name]['sha256']
    record = json.loads(raw)
    site = bmt.BindingSite.from_dict(
        json.loads(json.dumps(record, sort_keys=True)), experimental=True
    )
    assert site.to_dict() == record and site.geometry is None
    assert (
        path.read_bytes() == raw
        and site.to_dict()['producer'] == manifest['records'][name]['original_producer']
    )


@pytest.mark.parametrize('route', ['box_region', 'sphere', 'site_box'])
@pytest.mark.parametrize(
    'error',
    [
        MemoryError('authored memory'),
        OSError(12, 'authored OS allocation'),
        PermissionError('authored IO'),
    ],
)
def test_length_resource_exception_preserves_original_identity(
    monkeypatch, route, error
):
    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(puw, 'ensure_quantity', fail)
    with pytest.raises(type(error)) as observed:
        if route == 'box_region':
            bmt.BoxRegion(center='[0,0,0] nm', lengths='[1,1,1] nm')
        else:
            declare('sphere' if route == 'sphere' else 'box')
    assert observed.value is error
