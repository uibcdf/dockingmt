"""Small, inspectable MolSysMT reads shared by the Vina preparation adapters."""

import json
from collections import Counter
from copy import deepcopy
from typing import Any

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError


def autodock_element(atom_type: str) -> str:
    """Decode only the element identity carried by a known AutoDock atom type."""
    elements = {
        'A': 'C',
        'C': 'C',
        'N': 'N',
        'NA': 'N',
        'O': 'O',
        'OA': 'O',
        'S': 'S',
        'SA': 'S',
        'HD': 'H',
        'P': 'P',
        'F': 'F',
        'Cl': 'Cl',
        'Br': 'Br',
        'I': 'I',
    }
    if atom_type not in elements:
        raise ArgumentError(
            arg_name='atom_types',
            reason=f'Cannot recover an element from AutoDock type {atom_type!r}.',
        )
    return elements[atom_type]


def select_one_structure(molecular_system: Any, selection: Any) -> Any:
    """Prepare one chosen chemical state and structure from a molecular input."""
    molsys = msm.convert(molecular_system, to_form='molsysmt.MolSys')
    n_structures = msm.get(molsys, element='system', n_structures=True)
    if n_structures != 1:
        raise ArgumentError(
            arg_name='molecular_system',
            reason='Preparation requires exactly one selected structure.',
        )
    indices = msm.select(
        molsys, selection=selection, structure_indices=0, chemical_state='structure'
    )
    if not indices:
        raise ArgumentError(
            arg_name='selection',
            reason=f"Selection '{selection}' did not match any atoms.",
        )
    return msm.extract(molsys, selection=sorted(int(index) for index in indices))


def atom_metadata(
    molsys: Any, fallback_group: str
) -> tuple[list[str], list[str], list[int], list[str]]:
    """Read atom identity without assuming that the source has residue groups."""
    n_atoms = int(msm.get(molsys, element='system', n_atoms=True))
    if not msm.has_attribute(molsys, 'atom_type'):
        raise ArgumentError(
            arg_name='molecular_system',
            reason='Atomic elements are required to prepare a Vina input.',
        )
    elements = [
        str(x).strip()
        for x in msm.get(
            molsys,
            element='atom',
            atom_type=True,
            chemical_state='structure',
            structure_indices=0,
        )
    ]
    if msm.has_attribute(molsys, 'atom_name'):
        names = [str(x).strip() for x in msm.get(molsys, element='atom', name=True)]
    else:
        names = [f'{element}{index + 1}' for index, element in enumerate(elements)]
    # Temporary consumer guard for uibcdf/molsysmt#233: group-free systems
    # currently raise a raw IndexError when group_name is queried directly.
    if msm.has_attribute(molsys, 'group_name'):
        group_names = [
            str(x).strip() for x in msm.get(molsys, element='atom', group_name=True)
        ]
    else:
        group_names = [fallback_group] * n_atoms
    if msm.has_attribute(molsys, 'group_id'):
        group_ids = [int(x) for x in msm.get(molsys, element='atom', group_id=True)]
    else:
        group_ids = [1] * n_atoms
    return names, group_names, group_ids, elements


def source_partial_charges(molsys: Any, n_atoms: int) -> list[float] | None:
    """Return only a complete finite atomic charge array; never infer zero charges."""
    if not msm.has_attribute(molsys, 'partial_charge'):
        return None
    values = msm.get(molsys, element='atom', partial_charge=True)
    if puw.is_quantity(values):
        values = puw.get_value(values, to_unit='elementary_charge')
    charges = np.asarray(values, dtype=float)
    if charges.shape != (n_atoms,) or not np.isfinite(charges).all():
        raise ArgumentError(
            arg_name='molecular_system',
            reason='Atomic partial charges must be complete and finite.',
        )
    return charges.tolist()


def source_charge_assignment(molsys: Any) -> dict[str, Any] | None:
    """Detach the public native assignment after MolSysMT's checked extraction.

    Molecular binding validation belongs to the provider. ``select_one_structure``
    extracts explicit indices, so its public operation marks stale assignments.
    Legacy supplied charges have no named assignment and remain unattributed.
    """
    mechanics = molsys.molecular_mechanics
    report = getattr(mechanics, 'partial_charge_assignment', None)
    if report is None:
        return None
    if (
        report.get('schema') != 'molsysmt.partial_charge_assignment@1'
        or report.get('status') not in ('assigned', 'projected')
        or report.get('charge_unit') != 'elementary_charge'
    ):
        raise ArgumentError(
            arg_name='molecular_system',
            reason='Named partial-charge attribution is stale or unsupported; explicitly reassign charges with MolSysMT.',
        )

    def normalize(value):
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, np.generic):
            return value.item()
        raise TypeError(f'Unsupported assignment value: {type(value).__name__}')

    try:
        return json.loads(
            json.dumps(deepcopy(report), default=normalize, allow_nan=False)
        )
    except (TypeError, ValueError) as exc:
        raise ArgumentError(
            arg_name='molecular_system',
            reason='Named charge attribution must contain finite serializable evidence.',
        ) from exc


def source_aromaticity(molsys: Any, n_atoms: int) -> list[bool] | None:
    if not msm.has_attribute(
        molsys, 'atom_is_aromatic', chemical_state='structure', structure_indices=0
    ):
        return None
    values = msm.get(
        molsys,
        element='atom',
        atom_is_aromatic=True,
        chemical_state='structure',
        structure_indices=0,
    )
    if len(values) != n_atoms:
        raise ArgumentError(
            arg_name='molecular_system',
            reason='Atomic aromaticity must have one value per atom.',
        )
    return [bool(x) for x in values]


def _residue_coverage_summary(report: dict[str, Any]) -> dict[str, Any]:
    """Project provider evidence onto counts, preserving exact template identity."""
    groups = report['groups']
    templates = {}
    for group in groups:
        template = group['template']
        if template is None:
            continue
        name = template['group_name']
        if name not in templates:
            templates[name] = {
                'resource': template['resource'],
                'packaged_sha256': template['provenance']['packaged_sha256'],
                'n_groups': 0,
            }
        templates[name]['n_groups'] += 1
    return {
        'provider_schema': report['schema'],
        'method': report['method'],
        'rule_version': report['rule_version'],
        'group_axis': 'selected_source_before_hydrogen_projection',
        'n_groups': len(groups),
        'status_counts': dict(report['summary']),
        'reason_counts': dict(
            Counter(reason for group in groups for reason in group['reason_codes'])
        ),
        'check_status_counts': {
            name: dict(Counter(group[name]['status'] for group in groups))
            for name in ('heavy_atoms', 'hydrogens', 'connectivity', 'protonation')
        },
        'template_usage': templates,
        'unassessed_checks': list(report['unassessed_checks']),
        'software': dict(report['software']),
    }


def chemistry_evidence(
    molsys: Any, *, include_residue_coverage: bool = False
) -> dict[str, Any]:
    """Record compact provider coverage without certifying docking readiness.

    Coverage refers to the selected source before hydrogen projection. Retain
    counts rather than duplicating the provider's atom/bond values in every run.
    The full source-index diagnostic remains available through MolSysMT's API.
    """
    completeness = msm.get(
        molsys,
        connectivity_completeness=True,
        chemical_state='structure',
        structure_indices=0,
    )
    residue_summary = None
    if include_residue_coverage and msm.get(molsys, n_groups=True):
        coverage = msm.build.get_residue_chemical_coverage(
            molsys, chemical_state='structure', structure_indices=0
        )
        report = coverage['chemical_readiness']
        residue_summary = _residue_coverage_summary(coverage)
    else:
        report = msm.physchem.get_chemical_readiness(
            molsys, chemical_state='structure', structure_indices=0
        )
        if include_residue_coverage:
            residue_summary = {
                'status': 'unassessed',
                'reason_code': 'no_group_domain',
                'n_groups': 0,
                'group_axis': 'selected_source_before_hydrogen_projection',
            }
    fields = {}
    for name, field in report['fields'].items():
        summary = {
            'status': field['status'],
            'n_assessed': len(field['indices']),
            **{
                f'n_{category}': len(field[f'{category}_indices'])
                for category in ('present', 'missing', 'unsupported', 'conflict')
            },
            'origin_counts': dict(Counter(field['origin'].tolist())),
        }
        if 'unit' in field:
            summary['unit'] = field['unit']
        fields[name] = summary
    connectivity = report['connectivity']
    evidence = {
        'connectivity_completeness': list(completeness)
        if completeness is not None
        else None,
        'bond_order_available': msm.has_attribute(
            molsys,
            'bond_order',
            chemical_state='structure',
            structure_indices=0,
        ),
        'chemical_readiness': {
            'provider_schema': report['schema'],
            'method': report['method'],
            'rule_version': report['rule_version'],
            'atom_axis': 'selected_source_before_hydrogen_projection',
            'n_atoms': report['n_atoms'],
            'structure_index': report['structure_index'],
            'chemical_state_index': report['chemical_state_index'],
            'chemical_state_status': report['chemical_state_status'],
            'state_provenance_index': report['state_provenance_index'],
            'fields': fields,
            'connectivity': {
                'declared_completeness': connectivity['declared_completeness'],
                'n_examined_bonds': len(connectivity['examined_bond_indices']),
                'n_invalid_bonds': len(connectivity['invalid_bond_indices']),
                'n_crossing_bonds': len(connectivity['crossing_bond_indices']),
            },
            'n_explicit_hydrogens': len(report['explicit_hydrogen_atom_indices']),
            'unassessed_checks': list(report['unassessed_checks']),
            'software': dict(report['software']),
        },
    }
    if include_residue_coverage:
        evidence['residue_coverage'] = residue_summary
    return evidence
