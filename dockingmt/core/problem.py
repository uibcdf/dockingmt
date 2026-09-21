from __future__ import annotations

from typing import Any

from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.search_domain import BoxRegion, SearchDomain


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
    """

    def __init__(
        self,
        receptor: Any,
        partner: Any,
        search_domain: SearchDomain,
        constraints: list[Any] | dict[str, Any] | None = None,
        search_guidance: list[Any] | dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
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
        self._search_domain = search_domain
        self._constraints = constraints if constraints is not None else []
        self._search_guidance = search_guidance if search_guidance is not None else []
        self._metadata = dict(metadata) if metadata is not None else {}

    @property
    def receptor(self) -> Any:
        """Molecular representation of the receptor."""
        return self._receptor

    @property
    def partner(self) -> Any:
        """Molecular representation of the docking partner."""
        return self._partner

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
        if isinstance(self._receptor, str):
            serialized_receptor = {'type': 'string', 'value': self._receptor}
        elif hasattr(self._receptor, 'to_dict'):
            serialized_receptor = {'type': 'object', 'value': self._receptor.to_dict()}
        else:
            serialized_receptor = {'type': 'repr', 'value': repr(self._receptor)}

        serialized_partner: Any
        if isinstance(self._partner, str):
            serialized_partner = {'type': 'string', 'value': self._partner}
        elif hasattr(self._partner, 'to_dict'):
            serialized_partner = {'type': 'object', 'value': self._partner.to_dict()}
        else:
            serialized_partner = {'type': 'repr', 'value': repr(self._partner)}

        return {
            'schema_version': '1.0',
            'receptor': serialized_receptor,
            'partner': serialized_partner,
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

        rec = (
            receptor if receptor is not None else data.get('receptor', {}).get('value')
        )
        part = partner if partner is not None else data.get('partner', {}).get('value')

        return cls(
            receptor=rec,
            partner=part,
            search_domain=search_domain,
            constraints=data.get('constraints'),
            search_guidance=data.get('search_guidance'),
            metadata=data.get('metadata'),
        )

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
