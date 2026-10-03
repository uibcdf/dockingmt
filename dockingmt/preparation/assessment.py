"""Inspect declared preparation evidence independently of engine execution."""

from collections.abc import Mapping

from argdigest import arg_digest

from dockingmt._private.smonitor import ArgumentError, signal

from .ligand import PreparedLigand
from .receptor import PreparedReceptor


@signal(tags=['api', 'preparation'])
@arg_digest()
def assess_preparation(prepared):
    """Report known provisional preparation without reading a molecular system.

    Parameters
    ----------
    prepared : PreparedLigand, PreparedReceptor, str, pathlib.Path or renderer
        A DockingMT preparation or an external PDBQT representation. External
        representations include text, paths and objects with a callable
        ``to_pdbqt`` method; they are always unassessed. No file or renderer is
        read or executed, and no molecular conversion or engine call occurs.

    Returns
    -------
    dict
        Detached JSON-compatible report with schema version ``1.0``, scope
        ``declared_preparation_metadata``, assessment, provisional reason codes
        and descriptions, and declared charge/type sources. ``provisional``
        means that DockingMT's known placeholder or heuristic markers were
        found. Otherwise the assessment is ``unassessed``, including missing
        markers or externally declared parameterization methods.

    Notes
    -----
    This inspects declarations, not charge values, molecular chemistry or
    scoring compatibility. Zero charge values alone do not imply placeholders.
    An unassessed report does not certify readiness for docking. Chemical
    coverage and validation remain MolSysMT operations (dockingmt#5).
    """
    evidence = {'charge_source': None, 'atom_type_source': None}
    if isinstance(prepared, (PreparedLigand, PreparedReceptor)):
        if not isinstance(prepared.metadata, Mapping):
            raise ArgumentError(
                arg_name='prepared', reason='Preparation metadata must be a mapping.'
            )
        for name in evidence:
            value = prepared.metadata.get(name)
            if value is not None and not isinstance(value, str):
                raise ArgumentError(
                    arg_name='prepared',
                    reason=f'Preparation metadata {name} must be a string or None.',
                )
            evidence[name] = value

    return _assessment_from_sources(evidence)


def _assessment_from_sources(evidence):
    """Build the declaration-only report shared by assessment and offline audit."""
    codes = []
    reasons = []
    if evidence['charge_source'] == 'zero_placeholder':
        codes.append('zero_placeholder_charges')
        reasons.append('zero-placeholder partial charges')
    if 'heuristic' in (evidence['atom_type_source'] or ''):
        codes.append('heuristic_atom_types')
        reasons.append('heuristic AutoDock atom types')
    return {
        'schema_version': '1.0',
        'scope': 'declared_preparation_metadata',
        'assessment': 'provisional' if reasons else 'unassessed',
        'provisional_reason_codes': codes,
        'provisional_reasons': reasons,
        'evidence': evidence,
    }
