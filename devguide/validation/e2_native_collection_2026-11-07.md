# E2 serial native collection and study comparison — 2026-11-07

Owner: [DockingMT #81](https://github.com/uibcdf/dockingmt/issues/81).
Registration status: **prospective**. Qualification base: `78b0664`.
Custody: `.molsyssuite/e2-native-collection-20261107`, reviewed under #50 on
**2026-11-14**. Preserve [the complete functional objective](../PRE_STABILIZATION_PLAN.md).

## Question and population

Receive a real serial public `dock_many(..., on_error='record')` study with two
distinct admitted ligand states, a capability refusal between them, all
original outcomes and an explicitly delimited empirical comparison. This is
functional collection evidence, not potency, affinity, stereoselectivity,
enrichment, convergence or independent-panel qualification.

P59(R)/P69(S) are two declared stereochemical entities from one 5X72 complex
at two experimental sites, without activity labels. Use the
[admitted sources](e2_source_admission_2026-11-07.md) and
[received rigid preparations](e2_preparation_receiving_2026-11-07.md).
Their raw starting conformations are not experimental reference poses. Do not
generate H, optimize, fit or translate to a reference, or borrow historical
fixed-companion receptor arms.

Study ID: `e2-5x72-rigid-20261107`. Positions, run IDs, ligand/state IDs and
result-local pose IDs retain separate meanings.

| Position | Run ID | Ligand/state | Requested role |
| --- | --- | --- | --- |
| 0 | `p59-main` | P59 / `e2-5x72-p59` | Native scientific item |
| 1 | `p59-unsupported-intent-control` | Same admitted P59 state | Nonempty constraints marker; expected Vina refusal |
| 2 | `p69-main` | P69 / `e2-5x72-p69` | Native scientific item after the refusal |

The control requests `constraints=[{'kind': 'e2_unsupported_intent_control'}]`.
It is not a third compound, inactive, invalid chemical state or pharmacophore.
It must produce `CapabilityMismatchError` / `DMT-E003` without native
initialization, maps or search. Preserve its error and the later outcome.

## Immutable source and prepared-input gate

Freeze candidate inventory SHA-256
`898b26fa60561bb99f823d2dd0c27216cc5771ac7dceacdb103760fed2e22284`,
source archive `a5a60b65715b466bd04dc5e2bdb41a73489fdf9a13254552870628d387221b8d`
and preparation archive
`bd4f34c7c696efa1c864c9ea410630398b5ec164726eeaaf6462ea9d9b78d326`.
Verify stored/decoded members and exact raw bytes before molecular work.

Reproduce both SDF/native/RDKit/native authorities, comparing actual fields to
their corresponding admitted initial/new interpretations. Then make two fresh
named Gasteiger–Marsili / AutoDock4 chemical-environment assignments and rigid
preparations, with declared neutral total `puw.quantity(0, 'elementary_charge')`
and `active_torsion_bonds=[]`. Keep actual conversion/assignment/projection
reports. Compare prepared chemistry, geometry and parameters with the admitted
observations without inventing fields or restoring MM from JSON. Require both
exact newly exported PDBQT hashes before importing/using Vina:

| State | PDBQT SHA-256 |
| --- | --- |
| P59 | `ae0e9d3beb4d14363ea6edb1bff591c56d53b02295082bae8c281d9284d84b9e` |
| P69 | `1cbe49d31e1859e34b7cc71af1a8514fef9314401401b2b76b6a7e07dfc7ebaa` |

The common protein-only receptor `tests/data/vina_torsions/5x72_receptor.pdbqt`
has SHA-256 `25d4e9b5f3932bc2953152dffc2d9dadf13726ae029e5e88712a0dc9525361e6`.
The box authority `5x72_receptor.box.txt` has SHA-256
`e1e87f640b1976109f7358e871e8e63b6f965ad7e76a54b9e848c10518ac3354`:
center `[-15, 15, 129]` angstrom, size `[30, 24, 24]` angstrom. Authenticate
the actual native box/grid in this frame. The joint domain covers different
sites; external receptor preparation and chemical validity remain unassessed.

## Frozen protocol and operation caps

Use Vina **1.2.7**, scoring `vina`, CPU **1**, seed **42 for each scientific
item**, exhaustiveness **1**, maximum **3 poses**, energy range
`puw.quantity(3, 'kcal/mol')`, `capture_backend_inputs=True`,
`collect_timings=True`, `allow_provisional_preparation=False`, and no protocol
torsion cuts. Both supplied ligands are already rigid. No index-derived seed,
reseeding, retry or effort adaptation.

Effort 1 is selected before new results for this finite functional question.
Historical ROOT-order effort-1 searches take about three seconds in their own
composition, while effort-8 samples take tens of seconds. These saved times are
resource context, not new measurements, portable guarantees or convergence.
Retain actual native defaults, grid spacing, minimum pose separation and
evaluation policy through resolved call/info records.

The inspected pinned wrapper declares weights
`[-0.035579, -0.005156, 0.840245, -0.035069, -0.587439, 50, 0.05846]`,
`no_refine=False`, spacing `0.375 angstrom`, `force_even_voxels=False`,
`min_rmsd=1.0 angstrom` and `max_evals=0`. Receive those actual defaults without
new setter or calculation calls; numeric transport normalization is not a
change of scientific value.

| Direct request | Complete-selection cap |
| --- | ---: |
| Each SDF/native, native/RDKit, RDKit/native bridge | 2 each |
| Named charge assignments / type assignments / rigid preparations | 2 each |
| Explicit prepared-byte gate exports | 2 |
| Public batch iterator / requested items | 1 / 3 |
| Native constructor / receptor binding / ligand-string binding | 2 each |
| Native map construction / dock / energies retrieval | 2 each |
| Original coordinate / text pose retrieval | At most 2 each |
| Native info observations from existing adapter calls | 4 |
| Public saved-outcome reconstruction | 3 |
| Existing public result-integrity audit | 2 |
| Fixed score, optimize, randomize, H generation, H5/MM persistence | 0 |

The backend exports the same two supplied preparations when submitting them;
observe those separately from the two gate exports. Internal getters/conversions
and the two requested provider H projections are not new caller cases.
The frozen notebook additionally registers the two pure result-integrity audits;
they perform no molecular or native calculation.

Observe actual public Vina methods with preserved signatures and original
returns, without another calculation or replacement backend. The adapter
already saves all five `total/inter/intra/torsions/intra_best_pose` native
columns and four public scores. Preserve every native row, actual info/weights,
resolved parameters, coordinate/text return, exact input capture and public
provider pose-reader/map evidence. The fifth column remains its own run's
reference; no fixed `Vina.score()` components are substituted. Compare JSON
normalized reports, since native info contains tuple values.

## Execution and acceptance

Advance serially and save each original outcome/result before assertions.
Collect all ordinary failures/empty results before complete-selection judgment.
Submitted, reached, attempted, native-invoked, terminal, successful, expected-
refused, unexpected-failed, successful-empty, returned-pose and representative
denominators are separate. Memory/process/source-iterator failures propagate,
preserving earlier data. No retry, extra ligand or favorable replacement.

Two nonempty scientific successes surrounding the expected refusal establish
the intended control. Otherwise preserve all outcomes and declare it incomplete.
Native counters and submitted bytes must remain unchanged during the refusal.
Receive owned staged-file retirement, original sources/prepared objects,
protocol/problem declarations, detached records and caller-policy nonmutation.
After preserving all outcomes, receive `DockingOutcome.from_dict` on the three
actual records, including error/success payloads, original scores/IDs and
physical coordinates under the caller policy. Preserve the original records;
this public persistence control performs no molecular or native calculation.

## Prespecified caller-owned study policy

Freeze the finite study policy/hash before execution. Select only the unique
original rank-1 pose of each nonempty scientific success. Missing/duplicate
rank 1 is unranked; no `top_pose` fallback, best minimum, seed or reference-based
selection. Bind each value to `(run_id, pose_id)`, original index/rank, result
digest and native row.

The [frozen policy](data/e2_native_study_policy_2026-11-07.json) has SHA-256
`d7bae710203402d37fb1a0378ea2d5c14c1d427bde5575f378cb25552648a34e`.
It registers exact inputs, protocol/defaults, caps, three public outcome
restores, representative/missing/tie/context rules and the report schema.

Require method/version, canonical energy unit, weights, fixed receptor/domain/
grid, protocol and preparation profile to match the policy. Keep each ligand's
legitimately different state/hash and complete original descriptor. Contexts
include `partner_sha256`, so full-context equality is not a cross-ligand gate.
Preserve each search's fifth reference without requiring equality or inventing/
subtracting a shared unbound reference.

Order eligible representatives by reported native `vina` total, lower first,
in `kcal/mol`; physical conversion is presentation only. Exact equality is a
tie, with input position only for stable display. No post hoc epsilon or
zero/infinite imputation. Missing, nonfinite, unknown-definition, missing-
reference, incompatible, failed, refused and successful-empty records remain
unranked with reasons. Fewer than two representatives leaves the two-ligand
comparison incomplete even if its outcome ledger is readable.

Save this decision separately without changing original scores/ranks/histories
or concatenating ligands into one result. Do not call E1 `compare_scores` or
`rank_by` across states. This is empirical preference under the joint-domain
model, without affinity or stereoselectivity inference. Existing composition
suffices; no runtime API or campaign framework is selected.

## Runtime, resources and independent receiving

Reuse consumer source `a7422df`, wheel SHA-256
`93d76f898575fb64b39520f33ceded25708270c8042c2a53c9a451acd834bcdd`,
3,867-file private target, borrowed MolSysMT
`9e1f1b1ad8bf09446374ab6f04ca7208e2717936` and support SDK
`95f693be10c9205ab9b912cb53453710a207bf45`. Reuse the received 103-path
Vina/Boost overlay. Vina artifact SHA-256 is
`9a337ada583bf92635f34211c7c3dc47249b0bd85b912432a53b46f4e795d824`;
Boost 1.86 artifact SHA-256 is
`a17ae9fd2af96eac7c29072b3e345ec3c2af42f18e33102633ab4440c1168ef7`.
No install/rebuild or routine Boost replacement. Verify payloads, metadata,
import/native origins and both input archives before/after. Shared staged test
support stays outside runtime.

One complete selection uses pm/fs/coulomb caller policy with explicit boundary
units and restoration. CPU 0, nice 10, one native/build worker including
descendants, 8 GiB monitored available-RAM reserve, 1 GiB owned-group RSS,
2 GiB address space, 60 CPU seconds and 90 wall seconds per process. Check
headroom before launch/cells and monitor throughout. Stop only owned work on
limits; preserve interruptions without automatic restart. Freeze exact notebook/
cells, policy, prescription, harnesses, sources/artifacts/support and limits
before launch. Preserve every attempted/not-attempted stage and producer.

After passing native receiving, a fresh standard-library reader checks sealed
bytes, policies, source/state/run/pose bindings, outcome denominators, all five
native columns/four public scores, representatives/ties, context/reference
limits and runtime/resource/custody controls. It imports no scientific package
and recalculates no molecule, score or energy. It receives saved evidence,
without authenticating a producer or revalidating chemistry.

Whole E2 needs criterion-by-criterion acceptance of the actual workflow and
public composition. The independent scientific panel, remaining Core/E3/E4/E5,
public dependency/artifact delivery, exact-head hosted gates, stabilization and
1.0 retain their scope. Preserve E4/live-visual holds and the original untracked
migration snapshot. Controlled private receiving is not public package delivery.

## Frozen execution material

The reviewed [collection notebook](e2_ligand_collection_receiving.ipynb) has
SHA-256 `e34d6c12ce6d80679ad054d93bb9a1caeb491e5e885e0bdf256e91b31108d9be`:
one Markdown cell and three unexecuted Python cells. AST, Ruff lint/format and
independent static API review pass before launch. All case report code is
embedded. Public PyUnitWizard conversion receives physical unit aliases;
literal native tuples/list representations do not decide semantic equality.

Numerical native arrays are retained first as original NumPy NPY returns,
with explicit physical unit, shape, dtype and digest receipts, before finite
JSON views. Text poses and input bytes are retained unchanged. The observer
holds detached data and weak instance IDs, preserving bounded native lifetime.
Policy dictionaries and all original result records have nonmutation checks.
Normal process completion and complete-selection acceptance retain separate
outcomes; successful-empty results cannot clear the functional requirement.

## Original native selection received — 2026-11-07

`native-01` passes the complete registered selection and original live checks.
Both authorities and fresh named preparations match their admitted chemistry,
geometry, mechanics and exact byte gates before Vina import. One public serial
iterator returns success/refusal/success: P59 returns three poses, the explicit
constraint control reports `DMT-E003` without any additional native or writer
call, and P69 then returns two poses. No retries or extra searches occur.

Two constructors, receptor/ligand bindings, maps, docking calls and existing
energy retrievals, four original pose retrievals and four info calls meet the
caps. All five native columns and twenty public scalar scores remain associated
with the five original poses. Two gate exports plus two backend staging exports
match the admitted inputs. Both provider known-source pose readers, two public
result audits and three public saved-outcome reconstructions pass. Original
scores/ranks/histories, live molecular/prepared objects, problem/protocol and
policy dictionaries, raw input files and both admitted archives are unchanged.

| Run | Outcome | Returned poses | Selected original pose | Native total (kcal/mol) | Own fifth reference (kcal/mol) |
| --- | --- | ---: | --- | ---: | ---: |
| `p59-main` | Success | 3 | `pose_1`, rank 1 | -11.462 | 0.000 |
| `p59-unsupported-intent-control` | Expected capability refusal | 0 | Unranked | — | — |
| `p69-main` | Success | 2 | `pose_1`, rank 1 | -10.787 | 0.000 |

The prespecified report receives both representatives and presents P59 before
P69 under this native-total policy. There is no tie in these reported totals.
Each fifth reference is retained separately; equal reported zeros do not
establish a shared internal/unbound reference. This is not an affinity or
stereoselectivity conclusion, and the joint two-site domain remains material.
All five energy columns, full descriptors and original histories stay
in the immutable records; no new score is inserted or result reranked.

The process takes 28.21 wall seconds with sampled peak owned-group RSS
652.48 MiB, no interruption or signal. The two native docking intervals are
1.247 and 1.066 seconds in their own provenance. These local timing samples
include different scopes; the overall process includes imports, input gates,
hashes and receiving. They are not throughput or portable speed evidence; the
original harness records CPU/affinity and artifacts but not a CPU hardware-model
inventory. Preserve that missing context rather than infer a benchmark claim.

All 3,867 private consumer/provider payload files, 103 overlay paths and overlay
metadata, actual import/native-library origins, routine environment metadata
and 594 shared support files pass before/after controls. Both observed receptor
staging files and the task temporary support are retired; owned temporary files
remaining are zero. The original stderr retains the expected 77-byte capability
diagnostic; stdout is empty. The original 166-member phase manifest is SHA-256
`975c8222650d5d6948fe023c51a70a277b59c4e34d993de897d5ef7b01ff294b`.

## Independent receiving and bounded acceptance

`reader-01` passes against all 166 native phase members and the 80 source/120
preparation archive members. It verifies exact original bytes, strict numeric
NPY witnesses and JSON views, native calls/defaults, five columns/four public
scores, pose/run/state associations, original rank-1 representatives, study
counts/order, public roundtrips, source nonmutation and private/runtime/support
provenance. It imports only the standard library and performs zero molecular,
scoring, search or public outcome-restoration operations. This is record
receiving, not producer authentication or new chemical validation.

The reader takes 3.80 seconds and 51.78 MiB sampled peak owned-group RSS, with
no interruption. Its original 20-member phase manifest is SHA-256
`bfbebaa3d62e0c4142b1350764c76aa30e847c7bc14bb0e936f8aca1b5f5fb42`.
Reader source SHA-256 is
`1430cb6335eee1892af93e52dc0b836d746677bf5c671d5949f8dc4fa2261851`.
The [193-member immutable native archive](data/e2_native_collection_2026-11-07/manifest.json)
contains 1,684,688 stored and 9,028,905 decoded bytes, plus its manifest, at
SHA-256 `4535ecab26c9fbe4d80bf50fabb48ec3a74ae067979f4e970f5523f703c98e46`.

Eleven existing software guard cases pass for ordinary failure isolation and
unsupported Vina intent refusal before hooks/execution. The
[software receipt](data/e2_collection_guard_receiving_2026-11-07.json) preserves
the first collection-route failure (missing optional Vina Python path) and the
complete corrected selection using the existing received overlay. No package
is installed, scientific input/protocol changed or native search repeated.

The [archived #81 acceptance](../archive/qualify_small_ligand_collection.md#bounded-acceptance-and-resolution--2026-11-07)
maps all five original criteria to this concrete received workflow and names
the relevant guard. The finite rigid25 joint-domain question is resolved;
arbitrary ligand profiles, unobserved tie/empty/incompatibility branches,
screening effectiveness, public delivery and the full #73 objective remain
outside that acceptance. The next independent Extended workflow is #79/
MolSysMT #604 pose comparison/clustering. Preserve E4/live-observation holds.

Thirteen applicable local checks pass for notebook AST/lint/format, archived
report/guard addressability and indexes, maintained links, stored/decoded archive
hashes, dependency/publication contracts and shared resources, including a fresh
source export with the exact final changes. Publication also requires a fresh
export of the actual committed source. Exact-head hosted evidence remains missing under
#28 and `[skip ci]`; no manual remote workflow is dispatched.

## Short reviewed public route

With the admitted `prepared_ligands`, `receptor_path` and physical `domain`, the
ordinary composition uses existing public operations:

```python
protocol = dmt.VinaProtocol(
    cpu=1,
    seed=42,
    exhaustiveness=1,
    n_poses=3,
    energy_range=puw.quantity(3, 'kcal/mol'),
    capture_backend_inputs=True,
    collect_timings=True,
)
problems = [
    dmt.DockingProblem(
        receptor=receptor_path,
        partner=ligand,
        search_domain=domain,
        metadata={'ligand_id': ligand_id, 'partner_state_id': ligand.state_id},
    )
    for ligand_id, ligand in prepared_ligands.items()
]
records = [
    outcome.to_dict()
    for outcome in dmt.dock_many(problems, protocol=protocol, on_error='record')
]
restored = dmt.DockingOutcome.from_dict(records[0])
```

This excerpt is reviewed against the executed composition, not a separately
executed experiment or observed usability test. The qualification additionally
declares stable run/study/receptor identities and its intentional middle
control. Save every outcome independently before analysis; adopt an explicit
study policy before comparing different ligands. The longer notebook owns
qualification instrumentation, not a required ordinary-user interface.
