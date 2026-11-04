# Small redocking panel: design and admission boundary — 2026-11-04

Owner: [DockingMT #33](https://github.com/uibcdf/dockingmt/issues/33), following
questions Q2/Q3 and risks R3/R6 of the [library audit](../library_audit_2026-11-04.md).
Evidence presentation remains [#29](https://github.com/uibcdf/dockingmt/issues/29).
Reviewed consumer: `71287ce86db365c9063846ae7d904c9586a99354`.

**Status: proposed design; not execution-ready or a registered experiment.**
The [first source inspection](scientific_panel_admission_2026-11-04.md) now
preserves four PDB/CIF inputs and provider-built assembly observations. Revision,
template, state and environment decisions remain pending; no case is admitted.
No admitted docking preparation, scoring, search or RMSD was executed. No results are
predicted here. The specific unresolved decisions below must be frozen before
search, rather than filled in after observing outcomes.

The [environment/template continuation](scientific_panel_environment_2026-11-04.md)
now records provider water shells, ligand-copy separations, observed protein
boundaries and the OXT prerequisite. MolSysMT #557 owns the requested reusable
CCD/template route. These observations do not resolve state/environment admission.

The [subsequent terminal software control](scientific_panel_terminal_probe_2026-11-04.md)
executes one unadmitted reconstruction, with its own counter and provider map/history
request #558. It neither adds a search row nor qualifies a prepared receptor.

## Question and intended claim

For two additional public complexes within an explicitly admitted one-state,
rigid-protein/small-molecule profile, does the existing Vina workflow return
near-reference poses, and does its returned ordering place them first?

Separate preparation admission, returned-set coverage and ranking. The first
panel deliberately starts from observed bound heavy geometry and compares a
rigid ligand with explicit ligand cuts. It tests local redocking with known-site
information, not de novo conformer recovery, blind docking, affinity or screening.
Two complexes constitute a diagnostic pilot, not a population success-rate estimate.
There is no requirement that either candidate yield favorable docking results.

## Case roles and candidates

| Role | Cases | Reason and admission boundary |
| --- | --- | --- |
| Existing development/regression evidence | 181L, 1IEP, 5X72 and 3PTB | Retain original producers, populations, references and cutoffs. Consult their observations without rerunning or pooling them into the new denominator. |
| New candidate A | [RCSB 1HSG](https://www.rcsb.org/structure/1HSG), ligand MK1 | Protease/inhibitor complex; RCSB lists a dimeric biological assembly. Review both protein chains and the specific ligand instance, chemistry and catalytic-site state before admitting a rigid receptor. |
| New candidate B | [RCSB 1STP](https://www.rcsb.org/structure/1STP), ligand BTN | Streptavidin/biotin complex; RCSB lists a tetrameric assembly and a difference between deposited and modeled residue counts. Establish the relevant complete binding environment and classify missing segments; do not silently use an isolated asymmetric-unit chain. |

Entry descriptions and identities above were read on 2026-11-04. No occurrence
of these two IDs was found in the inspected DockingMT tests, validation records or
test-support sources at the reviewed head. This is a local development-corpus
observation, not proof that the cases are unseen by Vina's developers, training
sets, other tools or published benchmarks. Their different receptor contexts are
a deliberate diagnostic choice, not random or representative sampling.

The candidates are selected before observing DockingMT outcomes. If admission
fails, preserve the failure and its reason. Do not replace a difficult case with
an easier successful case. A replacement requires a dated pre-search design
amendment with its rationale and a preserved candidate ledger.

## Admission work before any search

For each candidate, produce an inspectable case declaration using public MolSysMT
operations. The declaration must resolve all rows below; a PDB ID alone is not an
executable scientific prescription.

| Item | Required decision/evidence | Current state |
| --- | --- | --- |
| Input identity | Exact downloaded entry/assembly and CCD files, revision/acquisition identities, SHA-256, usage attribution and immutable local copies. | Entry PDB/CIF bytes acquired and hashed; exact revision/CCD/template admission pending. |
| Receptor context | Assembly and chain/operator identities, one coordinate structure, retained protein atoms, termini/disulfides, alternate locations, missing sites and any allowed exclusions. | Provider assembly 1 observed; state/environment/truncation acceptance pending. |
| Ligand/reference | One named ligand instance, original observed heavy coordinates, complete declared graph, atom map, stereochemistry and reference population. Symmetry-generated copies are not independent cases. | Provider source axes observed (45/16 atoms); complete chemistry, maps and instance admission pending. |
| Chemical hypothesis | Explicit ligand protonation/tautomer and receptor residue states, including scientifically consequential catalytic-site choices. Record basis and uncertainty; no inferred experimental pH. | Pending case-specific review; no generic state default selected. |
| Environment | Explicit disposition for waters, ions, cofactors and other occupants; justify the chosen bounded model or reject it as outside scope. | Pending inspection; no automatic deletion justified by this design. |
| Preparation | Named provider template/H/charge/type methods and versions, original/expanded/projected maps, allowed losses, complete required fields and native export/readback. | Reuse the supported profile only where its applicability is demonstrated. |
| Flexibility | Explicit selected-source bond pairs and their provider classification/rigid fragments, frozen before search. Rigid and cut arms share the same initial molecular state and coordinates. | Pending graph admission; do not infer cuts locally. |
| Software | Exact installed consumer/provider/native artifacts, origins and dependency closure; qualified scientific tools and source scripts. | Existing private qualification is context, not automatic admission of this new experiment. |
| Resource/record custody | Output destination, owner, storage limit, timeout behavior, cleanup and retention of every failure/partial result. | Register with the executable producer before launching. |

Unresolved heavy-atom identity, unsupported chemistry, incomplete binding-site
structure or unavailable provider assembly/reading operations stop admission.
Peripheral unresolved segments need an explicit justified boundary, not silent
repair. Report whether a refusal is data, provider capability or scientific-scope
related. Missing reusable tools go to their provider issues.

## Proposed execution matrix

Freeze these choices with the admitted declarations and producer before execution:

- Two admitted cases, two ligand arms (rigid / explicitly cut), seeds
  `[7, 42, 2026]`, exhaustiveness `[1, 8]`: **at most 24 new searches**.
- Fixed loop order: candidate A, then B; rigid, then cut; listed seed; then effort.
  A refused case/arm remains in the planned ledger as not attempted.
- Vina scoring, CPU 1, at most nine returned poses, energy range `3 kcal/mol`,
  captured backend inputs, no provisional-preparation bypass. Freeze the actual
  engine version, map spacing, clustering and other resolved native defaults.
- One native box per case, derived from the reference-heavy-atom bounds with
  `8 angstrom` padding on each side through `BoxRegion.from_selection`. Freeze
  actual axes and physical/backend box values. If a dimension exceeds 30 angstrom,
  review budget/scope before admission; never resize after search outcomes.
- Use the same admitted role bytes within each case/arm across seeds and effort.
  Between arms, record the exact expected torsion/tree/order differences and
  verify common source geometry/chemical fields through the provider maps.
- No standalone fixed-pose scoring, ligand/reference alignment, hidden
  pre-optimization, outcome-selected root ordering, ensemble or rescoring arm.
  Normal Vina internal search/refinement remains part of the recorded backend call.
- Proposed execution ceiling: 600 s wall time per search, serial CPU 1; at most
  four hours of search time if all 24 hit that ceiling, excluding explicitly
  recorded preparation/reporting overhead. This is a proposed resource bound,
  not a measured runtime prediction. Freeze it before executing any row.
- One attempt per row. Preserve native errors/timeouts and any durable partial
  artifacts; do not retry for a favorable pose. A software defect stops the affected
  experiment for a separately attributed amendment, not a reset of its denominator.

At most 216 poses can be returned, but seeds, poses and repeated arms remain
within-case observations. A direct-backend differential rerun or displaced-box
control would add calculations and requires a separate declared population; it
is not implicitly included in these 24 searches.

## Evaluation and interpretation

Primary measurements use **all originally observed ligand heavy atoms**, mapped
through actual provider source/export/pose correspondence into the original
receptor frame. No fit and no symmetry correction in the primary endpoint.
Proposed near-reference criterion: positional RMSD **<= 2 angstrom**. Preserve
continuous values and the exact population; do not compare this threshold with
historical 2.5-angstrom outcomes as if they were one benchmark.

For every returned result report first-pose RMSD, minimum returned RMSD, top-1,
top-5 and any-returned recovery, number of returned poses, original rank/position,
score descriptors and input/settings identity. A result with fewer than five poses
has an explicit considered count. Empty successful results are observed nonrecovery;
failed or missing evaluations have unknown recovery, not invented zero RMSD.

Use existing `evaluate_redocking` with the declared heavy-atom comparison views,
preserving the full original poses. Optional chemically constrained symmetry RMSD
may be reported separately only after provider admission of its exact chemistry/H
representation; it must not replace or retroactively rescue the primary criterion.
Unmeasured source H coordinates must never masquerade as returned-pose geometry.

Show each case/arm/effort separately. Preserve selected, admitted, attempted,
completed, returned and evaluated denominators plus failure stage. Use
`summarize_redocking` only where its exact method/protocol/preparation compatibility
contract is satisfied. Do not strip state-specific preparation reports to force
different cases through that API. A case-level presentation table may juxtapose
the original reports without claiming a pooled success probability.

Decision rules:

1. Near-reference poses returned but consistently not ranked first motivate
   ranking/model diagnosis; they are not evidence that sampling never reached a
   useful region.
2. No near-reference returned pose leaves sampling, preparation, scoring and
   output filtering as possible contributors. Increasing effort alone does not
   uniquely diagnose or fix the cause.
3. A changed result between rigid/cut arms characterizes those declared search
   spaces; it does not establish a universal torsion policy or justify comparing
   their total scores as binding free energies.
4. RMSD recovery and provider plausibility outcomes remain separate. Failed
   plausibility is informative; unavailable checks are unassessed. The missing
   general assessment contract is tracked in [MolSysMT #555](https://github.com/uibcdf/molsysmt/issues/555).
5. With two selected complexes, publish descriptive results and limits, not a
   general recovery rate, calibrated confidence or superiority claim.

## Human workflow and continuation

Keep four small steps: source/admission notebook, recorded execution, saved-result
evaluation, and interpretation. Reuse the current public APIs and separate output
records; notebooks express scientific choices rather than implementing molecular
parsers, geometry or generic workflow infrastructure. No new campaign scheduler
is needed. Visual review stays separately deferred.

**Next executable step is admission/source inspection, not docking.** Complete
the case declarations, immutable input inventory, exact composition and resource
record; then register the final matrix and producer under #33 before searching.
Any change to the draft must be recorded before outcome inspection. The
[provider inventory](molecular_plausibility_inventory_2026-11-04.md) can progress
independently and does not make a missing molecular capability a local implementation.
