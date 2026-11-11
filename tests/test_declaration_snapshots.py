"""Saved declarations are independent observations of live prepared inputs."""

from copy import deepcopy

import numpy as np
import pytest
import pyunitwizard as puw

import bindingmt as bmt
from bindingmt.exceptions import ArgumentError


class MolecularSource:
    def __deepcopy__(self, memo):
        pytest.fail('A declaration snapshot copied the live molecular source')


def prepared(role):
    options = dict(
        state_id=role,
        atom_names=['C1'],
        coordinates=puw.quantity([[0, 0, 0]], 'angstrom'),
        atom_types=['C'],
        charges=[0.125],
        metadata={'nested': {'steps': ['original']}},
    )
    if role == 'ligand':
        return bmt.PreparedLigand(**options, group_name='LIG')
    return bmt.PreparedReceptor(**options, group_names=['REC'], group_ids=[1])


def problem(**options):
    domain = bmt.BoxRegion('[0,0,0] angstrom', '[10,10,10] angstrom')
    return bmt.DockingProblem('unused-rec.pdbqt', 'unused-lig.pdbqt', domain, **options)


@pytest.mark.parametrize('role', ['ligand', 'receptor'])
@pytest.mark.parametrize(
    'field', ['atom_names', 'group_names', 'group_ids', 'atom_types', 'charges']
)
@pytest.mark.parametrize('direction', ['export', 'live'])
def test_prepared_columns_are_independent(role, field, direction):
    item = prepared(role)
    record = item.to_dict()
    before = deepcopy(record)
    if direction == 'export':
        record[field][0] = 'changed'
        assert item.to_dict() == before
    else:
        getattr(item, field)[0] = 'changed'
        assert record == before


@pytest.mark.parametrize('role', ['ligand', 'receptor'])
@pytest.mark.parametrize('direction', ['export', 'live'])
def test_prepared_metadata_is_recursive_and_source_is_not_copied(role, direction):
    item = prepared(role)
    source = MolecularSource()
    item.source_molsys = source
    record = item.to_dict()
    before = deepcopy(record)
    target = record['metadata'] if direction == 'export' else item.metadata
    target['nested']['steps'].append('changed')
    assert (item.to_dict() if direction == 'export' else record) == before
    assert item.source_molsys is source
    assert 'coordinates' not in record and 'source_molsys' not in record


@pytest.mark.parametrize('role', ['ligand', 'receptor'])
def test_prepared_python_metadata_keeps_types_cycles_and_internal_aliases(role):
    item = prepared(role)
    shared = ['original']
    cycle = []
    cycle.append(cycle)
    item.metadata.update(
        a=shared,
        b=shared,
        array=np.array([1, 2]),
        pair=(1, 2),
        labels={'a'},
        cycle=cycle,
    )
    record = item.to_dict()['metadata']
    assert record['a'] is record['b'] and record['a'] is not shared
    assert isinstance(record['pair'], tuple) and isinstance(record['labels'], set)
    assert record['cycle'][0] is record['cycle'] and record['cycle'] is not cycle
    np.testing.assert_array_equal(record['array'], item.metadata['array'])
    record['array'][0] = 99
    assert item.metadata['array'][0] == 1


@pytest.mark.parametrize('field', ['metadata', 'constraints', 'search_guidance'])
@pytest.mark.parametrize('direction', ['export', 'live'])
def test_problem_declarations_are_independent(field, direction):
    item = problem(**{field: {'nested': ['original']}})
    record = item.to_dict()
    before = deepcopy(record)
    target = record[field] if direction == 'export' else getattr(item, field)
    target['nested'].append('changed')
    assert (item.to_dict() if direction == 'export' else record) == before


def test_problem_export_preserves_aliases_within_its_own_snapshot():
    shared = ['original']
    item = problem(metadata={'shared': shared}, constraints={'shared': shared})
    record = item.to_dict()
    assert record['metadata']['shared'] is record['constraints']['shared']
    assert record['metadata']['shared'] is not shared


@pytest.mark.parametrize('legacy', [False, True])
@pytest.mark.parametrize('field', ['metadata', 'constraints', 'search_guidance'])
@pytest.mark.parametrize('direction', ['record', 'live'])
def test_problem_reader_detaches_supported_and_legacy_records(legacy, field, direction):
    record = problem(**{field: {'nested': ['original']}}).to_dict()
    if legacy:
        del record['schema_version']
    before = deepcopy(record)
    restored = bmt.DockingProblem.from_dict(record)
    expected = deepcopy(restored.to_dict())
    target = record[field] if direction == 'record' else getattr(restored, field)
    target['nested'].append('changed')
    assert (restored.to_dict() if direction == 'record' else record) == (
        expected if direction == 'record' else before
    )


def test_problem_prepared_declarations_detach_while_explicit_inputs_stay_borrowed():
    receptor, ligand = prepared('receptor'), prepared('ligand')
    domain = bmt.BoxRegion('[0,0,0] angstrom', '[10,10,10] angstrom')
    item = bmt.DockingProblem(receptor, ligand, domain)
    receptor.source_molsys = ligand.source_molsys = MolecularSource()
    record = item.to_dict()
    record['partner']['value']['metadata']['nested']['steps'].append('edited export')
    assert ligand.metadata['nested']['steps'] == ['original']
    # Explicit input reconstruction normally resolves molecular states. Remove
    # this sentinel only for construction; no source/renderer is serialized.
    receptor.source_molsys = ligand.source_molsys = None
    restored = bmt.DockingProblem.from_dict(
        item.to_dict(), receptor=receptor, partner=ligand
    )
    assert restored.receptor is receptor and restored.partner is ligand


@pytest.mark.parametrize('model', [bmt.PreparedLigand, bmt.PreparedReceptor])
def test_prepared_subclass_inherits_snapshot_ownership(model):
    class Extension(model):
        pass

    item = prepared('ligand' if model is bmt.PreparedLigand else 'receptor')
    item.__class__ = Extension
    record = item.to_dict()
    record['metadata']['nested']['steps'].append('extension export')
    assert item.metadata['nested']['steps'] == ['original']


@pytest.mark.parametrize('kind', ['schema', 'domain'])
def test_problem_reader_admits_schema_before_copying_metadata(kind):
    class MustNotCopy:
        def __deepcopy__(self, memo):
            pytest.fail('Unsupported schema copied metadata before admission')

    record = problem().to_dict()
    record['metadata']['payload'] = MustNotCopy()
    if kind == 'schema':
        record['schema_version'] = '999.0'
    else:
        record['search_domain']['schema_version'] = '999.0'
    with pytest.raises(ArgumentError):
        bmt.DockingProblem.from_dict(record)


@pytest.mark.parametrize('field', ['extra', 'receptor', 'partner'])
def test_problem_reader_does_not_copy_ignored_or_replaced_payloads(field):
    class IgnoredPayload:
        def __deepcopy__(self, memo):
            pytest.fail('A payload unused by restoration was copied')

    record = problem().to_dict()
    options = {}
    if field == 'extra':
        record[field] = IgnoredPayload()
    else:
        record[field] = {'type': 'object', 'value': IgnoredPayload()}
        options[field] = (
            'unused-rec.pdbqt' if field == 'receptor' else 'unused-lig.pdbqt'
        )
    restored = bmt.DockingProblem.from_dict(record, **options)
    assert restored.receptor == 'unused-rec.pdbqt'
    assert restored.partner == 'unused-lig.pdbqt'
