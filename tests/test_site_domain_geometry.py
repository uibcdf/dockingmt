"""Analytical offline recipes preserve source meaning and refuse unplaced use."""

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
from bindingmt._private.site_domain_geometry import (
    ASSURANCE,
    FIELDS,
    derive_geometry_box,
)
from bindingmt._private.smonitor import ArgumentError, CapabilityMismatchError

FROZEN = Path(__file__).parent / 'data/site_domain_geometry_compat/0835648'


def original(name='sphere'):
    raw = (FROZEN / (name + '.json')).read_bytes()
    manifest = json.loads((FROZEN / 'manifest.json').read_text())
    assert hashlib.sha256(raw).hexdigest() == manifest['records'][name]['sha256']
    return json.loads(raw)


def site(name='sphere'):
    return bmt.BindingSite.from_dict(original(name), experimental=True)


def box(name='sphere', **options):
    return derive_geometry_box(
        site(name),
        **{
            'method': 'sphere_enclosure' if name != 'box' else 'axis_aligned_box',
            **options,
        },
    )


@pytest.mark.parametrize('name,base', [('sphere', [1, 1, 1]), ('box', [2, 4, 6])])
@pytest.mark.parametrize(
    'padding,extra', [(None, 0), ('0 angstrom', 0), ('2 angstrom', 0.4)]
)
@pytest.mark.parametrize('form', ['pint', 'unyt'])
def test_analytical_lengths_units_request_and_exact_original_custody(
    name, base, padding, extra, form
):
    with puw.context(default_form=form, standard_units=['pm', 'fs']):
        before = puw.configure.report()
        declaration = site(name)
        domain = derive_geometry_box(
            declaration,
            method='sphere_enclosure' if name == 'sphere' else 'axis_aligned_box',
            padding=padding,
        )
        recipe = domain.derivation
        assert recipe['site'] == original(name) == declaration.to_dict()
        assert recipe['site_ref'] == {
            **declaration.definition_ref,
            'view_key': 'geometry',
        }
        np.testing.assert_allclose(
            puw.get_value(domain.center, to_unit='nm'),
            [-1, 2, 3],
            rtol=8 * np.finfo(float).eps,
            atol=0,
        )
        np.testing.assert_allclose(
            puw.get_value(domain.lengths, to_unit='nm'),
            np.array(base) + extra,
            rtol=8 * np.finfo(float).eps,
            atol=0,
        )
        assert puw.get_form(domain.center) == form
        assert (recipe['request']['padding'] is None) == (padding is None)
        assert recipe['assurance'] == ASSURANCE
        assert recipe['losses'] == {
            'support_relation': 'equal' if name == 'box' and extra == 0 else 'encloses',
            'added_support': 'none' if name == 'box' and extra == 0 else 'unquantified',
        }
        for sorted_keys in (False, True):
            record = json.loads(json.dumps(domain.to_dict(), sort_keys=sorted_keys))
            assert bmt.BoxRegion.from_dict(record).to_dict() == domain.to_dict()
        assert puw.configure.report() == before


@pytest.mark.parametrize('name', ['annotated', 'revised'])
def test_original_claim_associations_and_detached_ownership(name):
    declaration = site(name)
    domain = box(name)
    record = domain.to_dict()
    assert record['derivation']['site'] == original(name)
    assert declaration.evidence == record['derivation']['site']['evidence']
    record['derivation']['site']['definition']['claim'] = 'caller edit'
    detached = domain.derivation
    detached['assurance']['placement'] = 'match'
    assert domain.derivation['site'] == original(name)
    assert domain.derivation['assurance'] == ASSURANCE


@pytest.mark.parametrize('name', ['sphere', 'box'])
def test_backend_projection_refuses_unplaced_geometry_without_mutation(name):
    from bindingmt.engines.vina import _vina_box

    domain = box(name)
    before = domain.to_dict()
    for route in (
        lambda: domain.to_backend_box(unit='angstrom'),
        lambda: _vina_box(domain),
        lambda: domain.as_box_approximation().to_backend_box(),
    ):
        with pytest.raises(CapabilityMismatchError) as error:
            route()
        assert 'placement' in error.value.extra['capability']
        assert domain.to_dict() == before
    assert not hasattr(site(name), 'to_search_domain')


@pytest.mark.parametrize(
    'padding', [True, 1, -1, '-1 nm', '[1,2] nm', '1 fs', 'nan nm', 'inf nm']
)
def test_invalid_padding_has_no_implicit_unit_shape_or_clipping(padding):
    with pytest.raises(ArgumentError):
        box(padding=padding)


@pytest.mark.parametrize(
    'change',
    [
        'rotated',
        'nearly_identity',
        'wrong_method',
        'wrong_view',
        'wrong_method_type',
        'no_geometry',
    ],
)
def test_unsupported_geometry_or_request_is_explicit(change):
    record = original('oriented' if change == 'rotated' else 'box')
    options = {'method': 'axis_aligned_box'}
    if change == 'nearly_identity':
        theta = 1e-8
        rotation = [
            [np.cos(theta), np.sin(theta), 0],
            [-np.sin(theta), np.cos(theta), 0],
            [0, 0, 1],
        ]
        record['views'][0]['payload']['axes'] = QuantityRecord.from_quantity(
            puw.quantity(rotation, 'dimensionless'),
            field='bindingmt.site.geometry.box_axes',
            kind='urn:bindingmt:site:box-axes',
        ).to_dict()
        record['content_sha256'] = _digest(record)
    if change == 'wrong_method':
        options['method'] = 'sphere_enclosure'
    if change == 'wrong_method_type':
        options['method'] = np.array(['axis_aligned_box'])
    if change == 'wrong_view':
        options['view'] = 'membership'
    declaration = bmt.BindingSite.from_dict(record, experimental=True)
    if change == 'no_geometry':
        declaration = bmt.BindingSite.from_atoms(
            source={'owner': 'caller', 'id': 'A'}, atom_indices=[1]
        )
    with pytest.raises((ArgumentError, CapabilityMismatchError)):
        derive_geometry_box(declaration, **options)


@pytest.mark.parametrize('name', ['sphere', 'box'])
def test_extent_overflow_refuses_without_clipping_or_source_mutation(name):
    declaration = site(name)
    before = declaration.to_dict()
    with pytest.raises(ArgumentError):
        derive_geometry_box(
            declaration,
            method='sphere_enclosure' if name == 'sphere' else 'axis_aligned_box',
            padding='1e308 nm',
        )
    assert declaration.to_dict() == before


@pytest.mark.parametrize(
    'damage',
    [
        'version',
        'format',
        'extra',
        'reference',
        'view',
        'method',
        'assurance',
        'loss',
        'site_digest',
        'source_scope',
        'current_geometry',
        'output',
        'resealed_output',
        'padding',
        'resealed_padding',
        'wrong_field',
        'wrong_unit',
        'wrong_shape',
        'negative_lengths',
    ],
)
def test_reader_recomputes_inputs_refs_outputs_and_assurance_before_admission(damage):
    record = box(padding='0.1 nm').to_dict()
    recipe = record['derivation']
    if damage == 'version':
        recipe['format_version'] = '9'
    elif damage == 'format':
        recipe['format'] = 'unknown'
    elif damage == 'extra':
        recipe['unexpected'] = True
    elif damage == 'reference':
        recipe['site_ref']['content_sha256'] = '0' * 64
    elif damage == 'view':
        recipe['request']['view'] = 'membership'
    elif damage == 'method':
        recipe['request']['method'] = 'axis_aligned_box'
    elif damage == 'assurance':
        recipe['assurance']['placement'] = 'match'
    elif damage == 'loss':
        recipe['losses']['added_support'] = 'none'
    elif damage == 'site_digest':
        recipe['site']['definition']['claim'] = 'changed'
    elif damage == 'source_scope':
        recipe['site']['views'][0]['scope']['source_structure_indices'] = [0]
        recipe['site']['content_sha256'] = _digest(recipe['site'])
    elif damage == 'current_geometry':
        record['lengths']['value'][0] += 0.1
    elif damage in ('output', 'padding'):
        target = (
            recipe['box']['lengths']
            if damage == 'output'
            else recipe['request']['padding']
        )
        target['digest'] = 'changed'
    elif damage in (
        'resealed_output',
        'wrong_field',
        'wrong_unit',
        'wrong_shape',
        'negative_lengths',
    ):
        value, unit, field = [2, 2, 2], 'nm', FIELDS['lengths']
        if damage == 'wrong_field':
            field = FIELDS['center']
        elif damage == 'wrong_unit':
            unit = 'fs'
        elif damage == 'wrong_shape':
            value = 2
        elif damage == 'negative_lengths':
            value = [-2, 2, 2]
        recipe['box']['lengths'] = QuantityRecord.from_quantity(
            puw.quantity(value, unit), field=field
        ).to_dict()
    elif damage == 'resealed_padding':
        recipe['request']['padding'] = QuantityRecord.from_quantity(
            puw.quantity(0.2, 'nm'), field=FIELDS['padding']
        ).to_dict()
    before = deepcopy(record)
    with pytest.raises((ArgumentError, CapabilityMismatchError, RecordError)):
        bmt.BoxRegion.from_dict(record)
    assert record == before


def test_stale_live_box_cannot_retain_offline_derivation():
    domain = box()
    domain.lengths[0] += puw.quantity(0.1, 'nm')
    with pytest.raises(ArgumentError):
        domain.to_dict()
    with pytest.raises(ArgumentError):
        domain.to_backend_box()


@pytest.mark.parametrize('field', ['center', 'lengths'])
def test_current_box_shape_is_not_accepted_through_broadcasting(field):
    domain = box()
    getattr(domain, field).shape = (1, 3)
    with pytest.raises(ArgumentError):
        domain.to_dict()


@pytest.mark.parametrize('route', ['padding', 'saved_quantity'])
@pytest.mark.parametrize(
    'error',
    [MemoryError('authored'), OSError(12, 'authored'), PermissionError('authored')],
)
def test_original_resource_exception_identity_is_preserved(monkeypatch, route, error):
    declaration = site()
    saved = box().to_dict()

    def fail(*args, **kwargs):
        raise error

    if route == 'padding':
        monkeypatch.setattr(puw, 'ensure_quantity', fail)
    else:
        monkeypatch.setattr(QuantityRecord, 'to_quantity', fail)
    with pytest.raises(type(error)) as observed:
        if route == 'padding':
            derive_geometry_box(
                declaration, method='sphere_enclosure', padding='0.1 nm'
            )
        else:
            bmt.BoxRegion.from_dict(saved)
    assert observed.value is error


def test_ordinary_problem_and_result_records_preserve_unassessed_recipe():
    domain = box('revised', padding='1 angstrom')
    problem = bmt.DockingProblem('unused_rec.pdbqt', 'unused_lig.pdbqt', domain)
    saved = problem.to_dict()
    restored = bmt.DockingProblem.from_dict(
        json.loads(json.dumps(saved, sort_keys=True))
    )
    assert restored.search_domain.to_dict() == domain.to_dict()
    result = bmt.DockingResult(
        [], problem_info=saved, provenance={'search_domain': domain.to_dict()}
    )
    loaded = bmt.DockingResult.from_dict(
        json.loads(json.dumps(result.to_dict(), sort_keys=True))
    )
    assert loaded.problem_info['search_domain'] == domain.to_dict()
    assert loaded.provenance['search_domain'] == domain.to_dict()
    with pytest.raises(CapabilityMismatchError):
        restored.search_domain.to_backend_box()


def test_public_backend_route_refuses_before_preparation_and_native_engine(monkeypatch):
    import importlib.abc
    import sys

    from depdigest.core import checker

    from bindingmt.engines import vina as backend

    def forbidden(*args, **kwargs):
        pytest.fail('Unassessed geometry reached preparation or a native engine')

    class ForbidEngine(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            if fullname.split('.')[0] in ('vina', 'meeko'):
                forbidden()

    monkeypatch.delitem(sys.modules, 'vina', raising=False)
    monkeypatch.setattr(sys, 'meta_path', [ForbidEngine(), *sys.meta_path])
    available = checker.is_installed
    monkeypatch.setattr(
        checker,
        'is_installed',
        lambda name: True if name == 'vina' else available(name),
    )
    monkeypatch.setattr(backend, 'prepare_receptor', forbidden)
    monkeypatch.setattr(backend, 'prepare_ligand', forbidden)
    problem = bmt.DockingProblem('unused_rec.pdbqt', 'unused_lig.pdbqt', box())
    with pytest.raises(CapabilityMismatchError):
        bmt.dock(problem, bmt.VinaProtocol(cpu=1, seed=1))
