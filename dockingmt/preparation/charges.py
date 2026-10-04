"""Inspect charge consumption and rounding in DockingMT preparation records."""

import hashlib
import json
from collections.abc import Mapping
from math import fsum, isfinite

import numpy as np
from argdigest import arg_digest

from dockingmt._private.smonitor import ArgumentError, signal


def _values_digest(values):
    """Bind the consumer's numeric array, independently of molecular chemistry."""
    return hashlib.sha256(np.asarray(values, dtype='<f8').tobytes()).hexdigest()


def _charge_projection(
    assignment, source_charges, retained, transfers, prepared_charges
):
    """Record the existing hydrogen transfers without recalculating chemistry."""
    if assignment is None:
        return None
    source_indices = assignment['atom_source_indices']
    return {
        'schema_version': '1.0',
        'charge_unit': 'elementary_charge',
        'policy': 'retain_polar_merge_nonpolar',
        'selected_source_atom_indices': source_indices.copy(),
        'retained_source_atom_indices': [source_indices[i] for i in retained],
        'selected_total_charge': fsum(source_charges),
        'retained_before_merge_total_charge': fsum(source_charges[i] for i in retained),
        'transfers': [
            {
                'omitted_source_atom_index': source_indices[donor],
                'recipient_source_atom_index': source_indices[recipient],
                'charge': source_charges[donor],
            }
            for donor, recipient in transfers
        ],
        'prepared_total_charge': fsum(prepared_charges),
        'prepared_values_sha256': _values_digest(prepared_charges),
        'total_charge_tolerance': 1e-6,
    }


@signal(tags=['api', 'preparation'])
@arg_digest()
def audit_preparation_charges(prepared):
    """Inspect current prepared charges, conservation evidence and PDBQT rounding.

    Accept a PreparedLigand or PreparedReceptor. Numeric charges are declared in
    elementary charge by these objects. Return detached finite JSON, with fixed
    units, current totals, provider attribution and the existing H-transfer map.
    A changed numeric binding is inconsistent; absent attribution is unassessed.
    PDBQT observations follow the actual atom order and three-decimal formatter.

    This does not read or validate a molecular graph, calculate a charge model,
    render PDBQT, or certify AutoDock typing or scoring compatibility. Molecular
    assignment and its validity remain MolSysMT operations. Call again after
    editing a preparation; this is an observation of the current values.
    """
    from .ligand import PreparedLigand
    from .receptor import PreparedReceptor

    if not isinstance(prepared, (PreparedLigand, PreparedReceptor)):
        raise ArgumentError(arg_name='prepared', reason='Use a DockingMT preparation.')
    try:
        values = np.asarray(prepared.charges, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ArgumentError(
            arg_name='prepared', reason='Use numeric prepared charges.'
        ) from exc
    if values.shape != (prepared.n_atoms,) or not np.isfinite(values).all():
        raise ArgumentError(
            arg_name='prepared', reason='Prepared charges must be complete and finite.'
        )
    # The producer has already normalized arrays/scalars. Strict JSON admission
    # prevents silently recording a mutated nonfinite or nonserializable report.
    if not isinstance(prepared.metadata, Mapping):
        raise ArgumentError(
            arg_name='prepared', reason='Preparation metadata must be a mapping.'
        )
    try:
        assignment = json.loads(
            json.dumps(
                prepared.metadata.get('partial_charge_assignment'), allow_nan=False
            )
        )
        projection = json.loads(
            json.dumps(prepared.metadata.get('charge_projection'), allow_nan=False)
        )
    except (TypeError, ValueError) as exc:
        raise ArgumentError(
            arg_name='prepared', reason='Charge evidence must be finite JSON.'
        ) from exc
    total = fsum(values)
    status = 'unassessed'
    matches = None
    difference = None
    if assignment is not None or projection is not None:
        if (
            not isinstance(assignment, dict)
            or assignment.get('schema') != 'molsysmt.partial_charge_assignment@1'
            or assignment.get('status') not in ('assigned', 'projected')
            or assignment.get('charge_unit') != 'elementary_charge'
            or not isinstance(projection, dict)
            or projection.get('schema_version') != '1.0'
            or projection.get('charge_unit') != 'elementary_charge'
            or projection.get('policy') != 'retain_polar_merge_nonpolar'
            or projection.get('total_charge_tolerance') != 1e-6
            or not isinstance(projection.get('prepared_values_sha256'), str)
            or type(projection.get('selected_total_charge')) not in (int, float)
            or not isfinite(projection['selected_total_charge'])
            or not isinstance(projection.get('retained_source_atom_indices'), list)
            or len(projection['retained_source_atom_indices']) != prepared.n_atoms
        ):
            raise ArgumentError(
                arg_name='prepared',
                reason='Charge evidence is incomplete or unsupported.',
            )
        matches = _values_digest(values) == projection['prepared_values_sha256']
        difference = total - projection['selected_total_charge']
        status = (
            'consistent'
            if matches and abs(difference) <= projection['total_charge_tolerance']
            else 'inconsistent'
        )
    order = (
        prepared.pdbqt_atom_indices
        if isinstance(prepared, PreparedLigand)
        else list(range(prepared.n_atoms))
    )
    rounded = [float(f'{values[i]:6.3f}') for i in order]
    return {
        'schema_version': '1.0',
        'scope': 'prepared_charge_consumption',
        'charge_unit': 'elementary_charge',
        'assessment': status,
        'n_atoms': prepared.n_atoms,
        'total_charge': total,
        'matches_preparation_values': matches,
        'selected_total_charge_difference': difference,
        'partial_charge_assignment': assignment,
        'charge_projection': projection,
        'pdbqt': {
            'decimal_places': 3,
            'prepared_atom_indices': order,
            'source_atom_indices': [
                projection['retained_source_atom_indices'][i] for i in order
            ]
            if projection is not None
            else None,
            'charges': rounded,
            'total_charge': fsum(rounded),
            'rounding_difference': fsum(rounded) - total,
            'total_rounding_bound': prepared.n_atoms * 0.0005,
        },
    }


def _charge_remark(prepared):
    """Guard named consumer binding and write bounded, original attribution."""
    if prepared.metadata.get('partial_charge_assignment') is None:
        return []
    report = audit_preparation_charges(prepared)
    if report['assessment'] != 'consistent':
        raise ArgumentError(
            arg_name='prepared',
            reason='Prepared charges no longer match their named assignment projection; prepare again with MolSysMT-assigned charges.',
        )
    assignment = report['partial_charge_assignment']
    payload = {
        'method': assignment['method'],
        'engine': assignment['engine'],
        'software': assignment['software'],
        'charge_unit': 'elementary_charge',
        'calculated_n_atoms': assignment['n_atoms'],
        'written_n_atoms': prepared.n_atoms,
        'pre_round_total_charge': report['total_charge'],
        'decimal_places': 3,
        'hydrogen_policy': report['charge_projection']['policy'],
    }
    return [
        'REMARK DOCKINGMT_PARTIAL_CHARGES '
        + json.dumps(payload, sort_keys=True, separators=(',', ':'))
    ]
