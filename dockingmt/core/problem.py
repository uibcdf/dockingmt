from __future__ import annotations

import hashlib
from numbers import Integral
from pathlib import Path
from typing import Any

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.search_domain import BoxRegion, SearchDomain


def _source_fingerprint(value: Any) -> dict[str, str] | None:
    """Fingerprint file bytes or literal molecular text at the input boundary."""
    if not isinstance(value, (str, Path)):
        return None
    raw = str(value)
    if '\n' not in raw:
        path = Path(raw)
        try:
            if path.is_file():
                digest = hashlib.sha256()
                with path.open('rb') as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b''):
                        digest.update(block)
                return {'kind': 'file', 'sha256': digest.hexdigest()}
        except OSError:
            pass
    return {'kind': 'literal', 'sha256': hashlib.sha256(raw.encode()).hexdigest()}


def _is_pdbqt_input(value: Any) -> bool:
    """Recognize the existing low-level Vina input until MolSysMT supports PDBQT."""
    if isinstance(value, (str, Path)) and str(value).lower().endswith('.pdbqt'):
        return True
    if not isinstance(value, str) or '\n' not in value:
        return False
    if 'ROOT\n' in value or 'ENDROOT' in value or 'TORSDOF' in value:
        return True
    records = [
        line for line in value.splitlines() if line.startswith(('ATOM', 'HETATM'))
    ]
    return bool(records) and all(
        len(line.split()) >= 13 and _has_pdbqt_charge(line) for line in records
    )


def _has_pdbqt_charge(line: str) -> bool:
    try:
        float(line.split()[-2])
    except (ValueError, IndexError):
        return False
    return True


def _normalize_input(
    value: Any,
    selection: Any,
    structure_index: int | None,
    name: str,
    structure_index_name: str | None = None,
) -> tuple[
    Any | None,
    list[int] | None,
    int | None,
    str,
    dict[str, Any] | None,
    int | None,
    str | None,
]:
    """Select one molecular structure and retain source atom indices."""
    from dockingmt.preparation import PreparedLigand, PreparedReceptor

    index_name = structure_index_name or f'{name}_structure_index'
    prepared = isinstance(value, (PreparedReceptor, PreparedLigand))
    backend_input = _is_pdbqt_input(value)
    if prepared or backend_input:
        if prepared and (
            (name == 'receptor' and not isinstance(value, PreparedReceptor))
            or (name == 'partner' and not isinstance(value, PreparedLigand))
        ):
            raise ArgumentError(
                arg_name=name,
                reason=f'A prepared {name} must use the matching PreparedReceptor or PreparedLigand type.',
            )
        if not (
            isinstance(selection, str) and selection == 'all'
        ) or structure_index not in (None, 0):
            raise ArgumentError(
                arg_name=name,
                reason='Selection and structure_index cannot be applied to an already prepared or PDBQT input.',
            )
        if backend_input:
            return None, None, None, 'backend:pdbqt', None, None, None
        source_molsys = getattr(value, 'source_molsys', None)
        if source_molsys is None:
            return None, None, None, 'prepared', None, None, None
        state_index, state_id = _structure_state(source_molsys, 0, name)
        return (
            source_molsys,
            list(range(value.n_atoms)),
            0,
            'prepared',
            None,
            state_index,
            state_id,
        )

    try:
        source_form = msm.get_form(value)
        source_molsys, report = msm.convert(
            value, to_form='molsysmt.MolSys', return_report=True
        )
        n_atoms, n_structures = msm.get(
            source_molsys, element='system', n_atoms=True, n_structures=True
        )
        if not n_atoms or not n_structures:
            raise ValueError('the molecular system needs atoms and coordinates')
        if structure_index is None:
            if n_structures != 1:
                raise ValueError(
                    f'the molecular system has {n_structures} structures; choose {index_name}'
                )
            structure_index = 0
        if (
            isinstance(structure_index, bool)
            or not isinstance(structure_index, int)
            or structure_index < 0
            or structure_index >= n_structures
        ):
            raise ValueError(f'{index_name} must be an integer in [0, {n_structures})')
        state_index, state_id = _structure_state(source_molsys, structure_index, name)
        atom_indices = sorted(
            int(index)
            for index in msm.select(
                source_molsys,
                selection=selection,
                structure_indices=structure_index,
                chemical_state='structure',
            )
        )
        if not atom_indices:
            raise ValueError(f'{name}_selection selected no atoms')
        if len(atom_indices) != len(set(atom_indices)):
            raise ValueError(f'{name}_selection contains duplicate atom indices')
        selected = msm.extract(
            source_molsys,
            selection=atom_indices,
            structure_indices=structure_index,
        )
        coordinates = msm.get(selected, element='atom', coordinates=True)
        if (
            coordinates is None
            or np.asarray(puw.get_value(coordinates)).shape != (1, len(atom_indices), 3)
            or not np.isfinite(puw.get_value(coordinates)).all()
        ):
            raise ValueError('the selected structure needs finite atom coordinates')
    except Exception as exc:
        raise ArgumentError(
            arg_name=name,
            reason=f'Cannot select a MolSysMT molecular system: {exc}',
        ) from exc
    report_info = {
        'outcome': report.outcome,
        'audited_scopes': list(report.audited_scopes),
        'is_exhaustive': report.is_exhaustive,
        'issues': [
            {
                'attribute': issue.attribute,
                'reason': issue.reason,
                'kind': issue.kind,
                'scope': issue.scope,
            }
            for issue in report.issues
        ],
    }
    return (
        selected,
        atom_indices,
        structure_index,
        str(source_form),
        report_info,
        state_index,
        state_id,
    )


def _structure_state(
    molsys: Any, structure_index: int, name: str
) -> tuple[int | None, str | None]:
    """Resolve the chemical state represented by one selected structure."""
    n_states = msm.get(molsys, element='system', n_chemical_states=True)
    if not n_states:
        return None, None
    indices = msm.get(
        molsys,
        element='system',
        structure_indices=structure_index,
        structure_chemical_state_index=True,
    )
    state_index = indices[0] if indices is not None and len(indices) else None
    if not isinstance(state_index, Integral):
        raise ValueError(
            f'{name} structure {structure_index} has no resolved chemical-state association'
        )
    state_ids = msm.get(molsys, element='system', chemical_state_id=True)
    state_id = state_ids[int(state_index)] if state_ids is not None else None
    return int(state_index), str(state_id) if state_id not in (
        None,
        'None',
        '',
    ) else None


def _serialize_selection(selection: Any) -> Any:
    if isinstance(selection, np.ndarray):
        return selection.tolist()
    if isinstance(selection, tuple):
        return list(selection)
    return selection


class DockingProblem:
    """The scientific docking problem specification.

    Describes scientific intent independently of backend file formats or docking engines.
    Captures the receptor, docking partner(s), search domain, constraints, search guidance,
    and associated scientific context.

    Parameters
    ----------
    receptor : Any
        Molecular representation of the receptor system (e.g. MolSysMT system, file path,
        or molecular state).
    partner : Any
        Molecular representation of the docking partner (e.g. ligand, MolSysMT system,
        file path, or molecular state).
    search_domain : SearchDomain
        Spatial domain where docking poses will be searched.
    constraints : list[Any] | dict[str, Any] | None, optional
        Scientific constraints restricting admissible solutions (e.g. pharmacophoric points,
        covalent attachments, distance boundaries).
    search_guidance : list[Any] | dict[str, Any] | None, optional
        Information guiding or biasing sampling without necessarily defining the hard spatial
        boundary (e.g. pocket topology, interaction fields).
    metadata : dict[str, Any] | None, optional
        Scientific metadata and identities (e.g. ligand_id, receptor_state_id, campaign tags).
    receptor_selection, partner_selection : Any, default 'all'
        Independent MolSysMT atom selections in each source system.
    receptor_structure_index, partner_structure_index : int | None
        Structure to dock. Required when the input has multiple structures.
    """

    def __init__(
        self,
        receptor: Any,
        partner: Any,
        search_domain: SearchDomain,
        constraints: list[Any] | dict[str, Any] | None = None,
        search_guidance: list[Any] | dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        receptor_selection: Any = 'all',
        partner_selection: Any = 'all',
        receptor_structure_index: int | None = None,
        partner_structure_index: int | None = None,
    ):
        if receptor is None:
            raise ArgumentError(
                arg_name='receptor',
                reason="'receptor' must be provided and cannot be None.",
            )
        if partner is None:
            raise ArgumentError(
                arg_name='partner',
                reason="'partner' must be provided and cannot be None.",
            )
        if search_domain is None or not isinstance(search_domain, SearchDomain):
            raise ArgumentError(
                arg_name='search_domain',
                reason=f"'search_domain' must be an instance of SearchDomain, got {type(search_domain)}.",
            )

        self._receptor = receptor
        self._partner = partner
        self._receptor_fingerprint = _source_fingerprint(receptor)
        self._partner_fingerprint = _source_fingerprint(partner)
        self._receptor_selection = receptor_selection
        self._partner_selection = partner_selection
        (
            self._receptor_molsys,
            self._receptor_atom_indices,
            self._receptor_structure_index,
            self._receptor_form,
            self._receptor_conversion_report,
            self._receptor_chemical_state_index,
            self._receptor_chemical_state_id,
        ) = _normalize_input(
            receptor, receptor_selection, receptor_structure_index, 'receptor'
        )
        (
            self._partner_molsys,
            self._partner_atom_indices,
            self._partner_structure_index,
            self._partner_form,
            self._partner_conversion_report,
            self._partner_chemical_state_index,
            self._partner_chemical_state_id,
        ) = _normalize_input(
            partner, partner_selection, partner_structure_index, 'partner'
        )
        self._search_domain = search_domain
        self._constraints = constraints if constraints is not None else []
        self._search_guidance = search_guidance if search_guidance is not None else []
        self._metadata = dict(metadata) if metadata is not None else {}

    @classmethod
    def for_redocking(
        cls,
        complex_system: Any,
        receptor_selection: Any,
        partner_selection: Any,
        padding: Any,
        structure_index: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DockingProblem:
        """Use one ligand selection and structure for both docking and its box.

        A source with multiple structures requires an explicit ``structure_index``.
        """
        selected, _, _, _, _, _, _ = _normalize_input(
            complex_system,
            partner_selection,
            structure_index,
            'partner',
            structure_index_name='structure_index',
        )
        if selected is None:
            raise ArgumentError(
                arg_name='complex_system',
                reason='Redocking requires a MolSysMT molecular input with coordinates.',
            )
        domain = BoxRegion.from_selection(
            selected,
            padding=padding,
        )
        return cls(
            receptor=complex_system,
            partner=complex_system,
            search_domain=domain,
            receptor_selection=receptor_selection,
            partner_selection=partner_selection,
            receptor_structure_index=structure_index,
            partner_structure_index=structure_index,
            metadata=metadata,
        )

    @property
    def receptor(self) -> Any:
        """Molecular representation of the receptor."""
        return self._receptor

    @property
    def partner(self) -> Any:
        """Molecular representation of the docking partner."""
        return self._partner

    @property
    def receptor_molsys(self) -> Any | None:
        """Selected receptor MolSys, if the input has a molecular representation."""
        return self._receptor_molsys

    @property
    def partner_molsys(self) -> Any | None:
        """Selected partner MolSys, if the input has a molecular representation."""
        return self._partner_molsys

    @property
    def receptor_atom_indices(self) -> list[int] | None:
        """Indices of selected atoms in the original receptor input."""
        return (
            list(self._receptor_atom_indices)
            if self._receptor_atom_indices is not None
            else None
        )

    @property
    def partner_atom_indices(self) -> list[int] | None:
        """Indices of selected atoms in the original partner input."""
        return (
            list(self._partner_atom_indices)
            if self._partner_atom_indices is not None
            else None
        )

    @property
    def receptor_structure_index(self) -> int | None:
        return self._receptor_structure_index

    @property
    def partner_structure_index(self) -> int | None:
        return self._partner_structure_index

    @property
    def receptor_chemical_state_index(self) -> int | None:
        return self._receptor_chemical_state_index

    @property
    def partner_chemical_state_index(self) -> int | None:
        return self._partner_chemical_state_index

    @property
    def receptor_selection(self) -> Any:
        return self._receptor_selection

    @property
    def partner_selection(self) -> Any:
        return self._partner_selection

    @property
    def search_domain(self) -> SearchDomain:
        """The spatial search domain."""
        return self._search_domain

    @property
    def constraints(self) -> list[Any] | dict[str, Any]:
        """Scientific constraints restricting docking solutions."""
        return self._constraints

    @property
    def search_guidance(self) -> list[Any] | dict[str, Any]:
        """Information guiding or biasing sampling."""
        return self._search_guidance

    @property
    def metadata(self) -> dict[str, Any]:
        """Scientific metadata, state identities, and provenance annotations."""
        return self._metadata

    def to_dict(self) -> dict[str, Any]:
        """Serialize DockingProblem specification to a versioned machine-readable dictionary."""
        serialized_receptor: Any
        if isinstance(self._receptor, (str, Path)):
            serialized_receptor = {'type': 'string', 'value': str(self._receptor)}
        elif hasattr(self._receptor, 'to_dict'):
            serialized_receptor = {'type': 'object', 'value': self._receptor.to_dict()}
        else:
            serialized_receptor = {'type': 'external', 'value': None}

        serialized_partner: Any
        if isinstance(self._partner, (str, Path)):
            serialized_partner = {'type': 'string', 'value': str(self._partner)}
        elif hasattr(self._partner, 'to_dict'):
            serialized_partner = {'type': 'object', 'value': self._partner.to_dict()}
        else:
            serialized_partner = {'type': 'external', 'value': None}

        return {
            'schema_version': '1.0',
            'receptor': serialized_receptor,
            'partner': serialized_partner,
            'molecular_inputs': {
                'receptor': {
                    'form': self._receptor_form,
                    'selection': _serialize_selection(self._receptor_selection),
                    'structure_index': self._receptor_structure_index,
                    'atom_indices': self.receptor_atom_indices,
                    'chemical_state_index': self._receptor_chemical_state_index,
                    'chemical_state_id': self._receptor_chemical_state_id,
                    'conversion_report': self._receptor_conversion_report,
                    'source_fingerprint': self._receptor_fingerprint,
                },
                'partner': {
                    'form': self._partner_form,
                    'selection': _serialize_selection(self._partner_selection),
                    'structure_index': self._partner_structure_index,
                    'atom_indices': self.partner_atom_indices,
                    'chemical_state_index': self._partner_chemical_state_index,
                    'chemical_state_id': self._partner_chemical_state_id,
                    'conversion_report': self._partner_conversion_report,
                    'source_fingerprint': self._partner_fingerprint,
                },
            },
            'search_domain': self._search_domain.to_dict(),
            'constraints': self._constraints,
            'search_guidance': self._search_guidance,
            'metadata': self._metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        receptor: Any | None = None,
        partner: Any | None = None,
    ) -> DockingProblem:
        """Reconstruct DockingProblem from a serialized dictionary.

        If receptor or partner are not provided as arguments, the serialized string/value
        from data is used.
        """
        domain_dict = data['search_domain']
        domain_type = domain_dict.get('type')
        if domain_type == 'BoxRegion':
            search_domain = BoxRegion.from_dict(domain_dict)
        else:
            raise ArgumentError(
                arg_name='search_domain',
                reason=f"Unsupported search domain type '{domain_type}' for deserialization.",
            )

        rec_data = data.get('receptor', {})
        part_data = data.get('partner', {})
        if (receptor is None and rec_data.get('type') != 'string') or (
            partner is None and part_data.get('type') != 'string'
        ):
            raise ArgumentError(
                arg_name='receptor/partner',
                reason='Serialized molecular objects require explicit receptor and partner inputs for reconstruction.',
            )
        rec = receptor if receptor is not None else rec_data.get('value')
        part = partner if partner is not None else part_data.get('value')
        if rec is None or part is None:
            raise ArgumentError(
                arg_name='receptor/partner',
                reason='Receptor and partner inputs are required for reconstruction.',
            )
        input_info = data.get('molecular_inputs', {})
        rec_info = input_info.get('receptor', {})
        part_info = input_info.get('partner', {})

        for label, source, source_info in (
            ('receptor', rec, rec_info),
            ('partner', part, part_info),
        ):
            expected = source_info.get('source_fingerprint')
            actual = _source_fingerprint(source)
            if expected is not None and actual is not None and expected != actual:
                raise ArgumentError(
                    arg_name=label,
                    reason='Molecular source content has changed since the problem was recorded.',
                )

        reconstructed = cls(
            receptor=rec,
            partner=part,
            search_domain=search_domain,
            constraints=data.get('constraints'),
            search_guidance=data.get('search_guidance'),
            metadata=data.get('metadata'),
            receptor_selection=rec_info.get('selection', 'all'),
            partner_selection=part_info.get('selection', 'all'),
            receptor_structure_index=rec_info.get('structure_index'),
            partner_structure_index=part_info.get('structure_index'),
        )
        actual_inputs = reconstructed.to_dict()['molecular_inputs']
        for label, recorded in (('receptor', rec_info), ('partner', part_info)):
            for field in (
                'atom_indices',
                'structure_index',
                'chemical_state_index',
                'chemical_state_id',
            ):
                if field in recorded and recorded[field] != actual_inputs[label][field]:
                    raise ArgumentError(
                        arg_name=label,
                        reason=(
                            f'Reconstructed {label} {field} differs from the '
                            'recorded molecular selection.'
                        ),
                    )
        return reconstructed

    def __repr__(self) -> str:
        rec_repr = (
            self._receptor
            if isinstance(self._receptor, str)
            else type(self._receptor).__name__
        )
        part_repr = (
            self._partner
            if isinstance(self._partner, str)
            else type(self._partner).__name__
        )
        return (
            f'DockingProblem(receptor={rec_repr!r}, partner={part_repr!r}, '
            f'search_domain={self._search_domain!r})'
        )
