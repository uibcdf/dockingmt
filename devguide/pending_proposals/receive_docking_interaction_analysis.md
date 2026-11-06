---
summary: Receive MolSysMT structured interactions and associate them with existing docking poses for E4.
issue: uibcdf/dockingmt#80
status: active
opened: 2026-11-06
closed:
verification: inspected
area: [analysis, provenance, visualization, scientific-validation]
guard:
normative: devguide/MVP.md
blocked_by: []
supersedes: []
---

# Structured interaction analysis for docking poses

## Concrete workflow

E4 in the [complete functional plan](../PRE_STABILIZATION_PLAN.md) needs a minimal
structured analysis useful for filtering and eventual visualization. For a
selected existing pose, use a supported MolSysMT assembly of its known ligand
and receptor states, disjoint ligand/receptor selections and the original
Cartesian frame, with explicit structure selection and `pbc=False`.

The first profile considers hydrogen bonds (`baker_hubbard`/`nitrogen_oxygen`)
and hydrophobic typed proximity (`atom_pair_distance`/`smarts_hydrophobic_atoms`).
Preserve the provider's exact definitions, cutoffs/inequalities, units, chemistry
and H inventory. These experimental molecular definitions are not interaction
energies, affinity or biological validation, and do not imply all families.

## Existing provider tools

The [dated inspection](../validation/extended_provider_scope_2026-11-06.md)
identifies public detectors, sparse `molsysmt.Interactions`, explicit coverage,
source maps, queries and typed interchange. Their availability in source does
not establish actual qualified receiving. No missing-detector proposal is
warranted by this inspection; reuse delivered MolSysMT #252 and existing tools.

MolSysMT owns assembly, chemical state/site recognition, molecular geometry,
detection and molecular serialization. PharmacophoreMT owns pharmacophore model
interpretation. MolSysViewer owns generic rendering/communication. DockingMT
selects its scientific population, associates provider results with actual
docking records and supplies docking-specific interpretation/filtering policy.

## Receiving and association

1. Prove the actual public molecular assembly/projection route on the qualified
   dependency, preserving source atom maps, frame/state and H inventory. Report
   uncovered reusable needs in MolSysMT; do not add a merger, coordinate editor,
   atom matcher, typing rule or interaction engine here. Existing #49 bridges
   retain their receiving/removal obligations.
2. Preserve the complete provider analysis with participant roles/source indices,
   structure/state coverage, assumptions, method/profile, original versions and
   bibliography. Evaluated-empty, unevaluated and unsupported are distinct.
   Missing H or failed chemical admission cannot establish biological absence.
3. Link the new analysis to its actual result/pose, receptor/partner states and
   coordinate/input identities. Preserve original scores and producer identities.
   Use the provider's supported typed interchange/persistence; `to_dict()` and
   `to_page()` are inspection projections, not complete persistence codecs.
4. Register the bounded representative calculation and informative positive,
   adverse and empty controls before execution. Receive actual provider calls,
   filtering, nondefault units, immutability, source/installed provenance and
   detached records, keeping molecular numerical and consumer-association
   evidence distinct.
5. Pass structured data to the addon through supported provider contracts.
   Actual comm/canvas acceptance remains #52/#60 and the maintainer's scheduling
   decision; no Python object or static export proves it.

## Current disposition

The concrete scope and existing tools are inspected. The
[six-cell installed notebook](../validation/installed_3ptb_interactions.ipynb) and
[finite prescription](../validation/installed_3ptb_interactions_registration.md)
are implemented but not yet executed. The route reuses the prepared native
source's retained virtual H counts and MolSysMT's delivered fixed-state H tool;
it does not infer missing chemistry or introduce a molecular reconstruction
algorithm in DockingMT. Actual receiving remains unproven.

Selected detector signatures exist at the
qualified pin, but current main has internal coordinate-delivery changes.
Unchanged signatures do not prove behavioral equivalence. Receive the actual
selected profile before changing a provider pin or making E4 acceptance claims.

