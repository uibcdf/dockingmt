# Integrated 5X72 control evidence — 2026-11-05

Owner: [DockingMT #70](https://github.com/uibcdf/dockingmt/issues/70), following
the finite scientific questions in #17/#6/#33 and the DMT-044 evidence policy.
This retrospective synthesis incorporates seven already executed stages. It
adds no search, score, molecular measurement, optimization or independent case.
The original producers, archives and receiving corrections remain authoritative.

The complete chain supports a more specific interpretation than the original
ROOT-order challenge alone. Fixed companion occupancy changes P59's search and
same-geometry score preferences in the declared model. The reciprocal P69
control improves returned-set coverage while its first/minimum-score recovery
remains absent. Reference, rigid-geometry, distance and displacement controls
further restrict explanations without establishing a physical cause, a chemical
preparation defect or an automatic remedy.

## Source inventory and operation ledger

The [machine-readable synthesis](data/5x72_synthesis_2026-11-05/summary.json)
retains seven exact compressed/uncompressed input hashes, each original consumer
base/source-map fingerprint/provider/version record, dependency edges and
historical source-proof flags. Its presentation helper has a separate identity;
it does not replace any original scientific producer. The
[generated tables](data/5x72_synthesis_2026-11-05/tables.md) preserve per-stage
operation counts and all twelve ligand/receptor/ROOT recovery strata.

| Stage / original evidence | Original operations and populations | Reuse and scientific role |
| --- | --- | --- |
| [ROOT order](5x72_root_order_workflow.md) | 24 searches, 99 returned poses; both ligands and both ROOT orders. | Single-ligand searches omit the other experimental occupant. Establishes the initial returned-set/ordering distinction. |
| [P59 with fixed P69](5x72_occupancy_workflow.md) | 24 searches, 78 returned poses (50 sham, 28 occupied); 256 fixed evaluations. | The 256 include 156 evaluations of new search poses plus 100 original/sham serialization evaluations on the 50 historical P59 poses. Those historical geometries are reused, not extra searches. |
| [P69 with fixed P59](5x72_reciprocal_workflow.md) | 24 searches, 78 returned poses (49 sham, 29 occupied); 254 fixed evaluations. | The 254 include 156 new-pose evaluations plus 98 serialization evaluations on 49 historical P69 poses. The reciprocal bounds the favorable P59 inference. |
| [Experimental-heavy reference](5x72_reference_workflow.md) | Eight new fixed evaluations; zero searches. | Reuses 156 returned poses and 312 fixed evaluations from the two occupancy studies, with full recorded contrasts. Generated H and original chemistry assumptions remain explicit. |
| [Original-rigid geometry](5x72_rigid_workflow.md) | Eight new fixed evaluations; zero searches. | Reuses those same 156 poses/312 evaluations. Two constructed conformers retain original rigid-fragment geometry/H while adopting reference torsions and placement. They are not returned poses. |
| [Saved-input distances](5x72_contact_workflow.md) | Eight matrices, 298,700 distances; zero scores/searches. | Reads exact inputs captured by the preceding 16 fixed evaluations. Descriptive proximity bins do not classify interactions or identify pair energies. |
| [Seven positional offsets](5x72_displacement_workflow.md) | 28 constructed points, 112 fixed evaluations: 16 fresh zero anchors and 96 nonzero evaluations; zero searches/optimizations. | Zero anchors match old bytes/components. All six nonzero 0.25 Å offsets per point remain, including unfavorable/no-improvement results. |

These are original stage-specific operation counts. Repeated appearances of
the same geometries or evaluations do not create new independent evidence.
The later sham trajectories match the corresponding historical P59/P69 poses;
their repetition controls serialization, not independent-complex replication.
All seven stages concern the same complex. P59/P69 occupy different sites and
are not an affinity or stereoselectivity dataset. No pooled success rate is used.

## Occupancy separates environmental context, coverage and ordering

All search matrices retain seeds 7/42/2026 and exhaustiveness 1/8 with CPU 1,
five requested poses, original ROOT orders and the fixed box. Original positional
RMSD uses 24 experimental heavy atoms, inclusive cutoff 2.5 Å, no alignment or
symmetry correction. Each row below contains six evaluated runs, preserving
the two ROOT arms separately.

| Searched ligand / search receptor | ROOT | First recovered | Any returned recovered | Recorded lowest fixed-score recovery in sham / occupied context |
| --- | --- | ---: | ---: | --- |
| P59 / sham | native | 0/6 | 3/6 | 0/6 / 3/6 |
| P59 / sham | first-fixed | 0/6 | 4/6 | 0/6 / 4/6 |
| P59 / occupied by fixed P69 | native | 5/6 | 5/6 | 5/6 / 5/6 |
| P59 / occupied by fixed P69 | first-fixed | 5/6 | 5/6 | 5/6 / 5/6 |
| P69 / sham | native | 0/6 | 0/6 | 0/6 / 0/6 |
| P69 / sham | first-fixed | 0/6 | 0/6 | 0/6 / 0/6 |
| P69 / occupied by fixed P59 | native | 0/6 | 4/6 | 0/6 / 0/6 |
| P69 / occupied by fixed P59 | first-fixed | 0/6 | 3/6 | 0/6 / 0/6 |

The fixed-score columns reproduce the original declared retained-set diagnostic,
with original-rank tie breaking. They do not change public result ranks or
general score-comparability policy. Search receptor and evaluation receptor
are distinct variables: these columns score the same retained geometries in
two contexts, without moving or resampling them.

For P59, all seven sham sets containing recovered poses prefer a recovered
geometry under occupied fixed scoring. This identifies a model-conditional
environmental preference effect independently of new sampling. Searching with
the occupied receptor separately improves first recovery to five of six cells
in each ROOT arm. A matched same-writer sham controls the receptor serialization
change; original-versus-sham fixed components and corresponding trajectories
agree in the measured populations.

For P69, the occupied searches retain recovered poses in four/six native and
three/six first-fixed cells, but the first pose and the original lowest-fixed
diagnostic remain unrecovered. Occupancy alone therefore does not resolve the
P69 ordering discrepancy. Absence from a returned set does not establish which
unretained states Vina visited.

## Score modes and reference/geometry controls

The docking totals used by [#69's P59 diagnostic](p59_score_diagnostic_2026-11-05.md)
come from the recorded `Vina.energies` docking result. The fixed controls use
`Vina.score` and retain eight components. Both have declared kcal/mol units,
but their numerical totals and component definitions are not equated. Comparisons
below stay inside their original ligand/order/receptor/fixed-score context.
No terms are recombined into a new score and no cross-ligand ranking is inferred.

The experimental-heavy/generated-H reference has fixed totals of −10.534 for
P59 and −10.499 kcal/mol for P69 in their respective occupied contexts. No
retained P59 geometry has a lower occupied fixed total than its experimental
reference. Ten P69 occupied retained geometries do, all originally first-ranked
and outside the positional criterion. Recovered P69 occupied pose-minus-reference
totals remain positive (+0.179 to +0.505 kcal/mol). Thus introducing the reference
does not by itself restore the P69 preference under this model.

The original-rigid constructions attain positional RMSD 0.513138 Å (P59) and
0.679452 Å (P69), retaining their original fragment geometry/H. Their occupied
fixed totals are respectively +1.983 and +7.832 kcal/mol above the earlier
experimental-heavy/generated-H references. This demonstrates finite geometric
placement near the reference, without establishing global search reachability
or a chemically correct conformation. Original/generated H differences and
unrelaxed geometry remain confounded between coordinate arms.

The distance control finds short protein pairs in both ligands. P59 and P69
each have two original-rigid heavy pairs below the descriptive 2.5 Å bin, with
different score contrasts. A threshold count is not an energy explanation.
The fixed companion's heavy-pair minima exceed 3 Å, which does not exclude
other pair or H effects. No clash, hydrogen-bond or atom-pair energy classifier
is introduced.

All seven prescribed positional offsets remain in the displacement record.
For original-rigid occupied P69, −x lowers the total by 2.554 kcal/mol relative
to its zero anchor, while moving every ligand–environment pair. Even that
finite minimum remains 5.278 kcal/mol above the earlier-reference zero. The
occupied P59 earlier-reference arm has no strictly lower nonzero point. These
positive and negative observations describe finite positional sensitivity,
not an optimum, gradient, barrier, pair cause or optimization policy.

## Consequences for the audit and remaining work

The original protein-only challenge and #69 remain valid within their declared
populations. The combined record adds controlled environmental and geometry
evidence that the original overview did not synthesize. The audit's current
E5/E6/E7 assessment must include these controls, while keeping its original
dated observations and all original producers intact.

The evidence supports traceable within-case model sensitivity and a persistent
P69 preference discrepancy. It does not establish general predictive accuracy,
affinity, cooperativity, experimental chemical states, preparation readiness or
systematic output plausibility. Charge/parser admission and low RMSD do not
resolve those questions. Generated H, environmental assumptions and the absence
of relaxation remain explicit.

The executed chain now ends at the displacement control; its earlier reference,
rigid or contact follow-ups should not be scheduled as missing experiments.
Any new sensitivity/causal question requires a separate declared intervention,
budget and provider-supported operations. Molecular inspection/transformation,
geometry and chemical assessment remain MolSysMT-owned. New independent-panel
admission, provider/public delivery and live C4/C6 retain their existing owners
and deferrals. No production preparation/ranking default changes follow.

## Reproduction and historical proof scope

```bash
python -m dmt_test_support.synthesize_5x72_controls --check
```

The standard-library helper authenticates all seven compressed archives before
parsing, checks recorded dependency hashes and complete search cells, and
projects original operation/reuse counts and recovery summaries. It checks
recorded recovery against saved scalar RMSD, without measuring coordinates.
The new [manifest](data/5x72_synthesis_2026-11-05/manifest.json) binds both outputs
to the input bytes and presentation-helper fingerprint. Running without
`--check` regenerates only the two derived presentation files and manifest.

The original source-proof flags vary by historical loader scope. In particular,
the contact/displacement records retain `original_sources_verified=False` in
their historical dependencies. The later displacement receiving verified
tracked original Git/source identities separately; it did not rewrite those
flags or freshly verify every historical generated-version runtime byte.
This synthesis authenticates archived evidence, preserving that distinction.
It performs no new source/native/artifact qualification of the old producers.

No molecular/engine/plotting imports are required. Original archives and the
earlier four-input overview, #67 and #69 numerical outputs remain unchanged.

The [21 controls](../../tests/test_5x72_control_synthesis.py) pass through the
shared support stager's 589 exact file declarations with the owner root excluded
from Python paths. They exercise archive/link corruption, incomplete cells,
invalid recovery values, dependent reuse, negative outcomes, historical false
proof flags, stale outputs and fresh scientific-import blocking. Four shared
integrity checks pass and managed resources/imports retire. The private staging
area is workspace-owned; this verifies import/source isolation, not a filesystem
location outside the checkout or an installed DockingMT artifact.
Another 24 reporting/distribution/support controls pass: 45 affected tests in
total with published Pytest Receptor 1.2.2 on Python 3.14. Ruff, report indexes,
all three earlier saved-evidence reproducers and shared publication/resource
preflights pass. Final-head hosted observation remains #28; the earlier
`ae2a9a9` checkpoint is independently green in all four workflows.
