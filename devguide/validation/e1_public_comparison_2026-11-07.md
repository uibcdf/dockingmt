# E1 public interaction-component comparison — 2026-11-07

Owner: [BindingMT #78](https://github.com/uibcdf/bindingmt/issues/78), with
resource/custody coordination in [#50](https://github.com/uibcdf/bindingmt/issues/50).
Status at prescription: **prospective; no execution or new measurements recorded**.
Custody review: **2026-11-14**.

Receive the bounded public `compare_scores` operation described in the
[comparison contract](score_comparison.md), using the existing five-pose E1
population. The [receiving notebook](e1_public_comparison_receiving.ipynb) and
its supervisor must be frozen and registered before execution. This prescription
does not report their completion.

## Question, population and trust

For the five previously scored, newly completed ligand conformations, request
an external comparison of the reported `lig_inter` components, lower first,
separately for Vina and Vinardo 1.2.7. Receive the public
`vina_1.2.7_same_axis@1` profile, including actual prepared-input binding,
provider-supported chemical correspondence and conservative refusals. The
existing [finite ordering study](e1_lig_inter_ordering_2026-11-06.md) supplies
regression expectations, not a replacement public implementation or new
authentication authority.

Use these independently retained input roots:

| Input population | Manifest SHA-256 |
| --- | --- |
| [Complete-pose construction](data/e1_complete_pose_2026-11-06/manifest.json) | `45b3665ba09b6979aa1bcdf1bea0ac3e8102f081fefbfc51348c55bc71405df3` |
| [Native scoring](data/e1_native_rescoring_2026-11-06/manifest.json) | `bf214aa7e48f15a95051411ed3bd54969f78c811503050c6969d6f5aa2898e93` |

Verify both manifest bytes and every listed stored/decoded identity before
molecular loading. Check the recorded construction-to-scoring relationship.
Consume `normal/pose_1/full18_chemical_only.h5msm.gz` through
`normal/pose_5/full18_chemical_only.h5msm.gz` from construction and
`scored_collection.json.gz` from scoring. Preserve all five original positions,
IDs, state declarations, raw scores, histories and collection provenance. No
member is replaced, discarded or relabelled as an independently new complex.

These trusted roots identify this receiving's historical inputs. They are not
embedded in the public API as authentication of arbitrary caller data. The
public report checks supplied records and current molecular views; hashes do
not authenticate a producer or prove historical chemical preparation.

## Runtime and registration

The supervisor registers `BINDINGMT_COMPARISON_ROOT` and a fresh
`BINDINGMT_COMPARISON_OUTPUT`, exact notebook/cell and prescription identities,
all harness files, source revisions and runtime/API file hashes before launch.
It records the actual Python executable, versions and loaded module origins,
including the public `bindingmt.compare_scores` implementation, MolSysMT,
PyUnitWizard and assignment/correspondence providers. Record the actual native
provider identities and any private/borrowed runtime scope. A checkout HEAD
alone does not identify uncommitted runtime changes or prove installed delivery.
The observed source HEAD while drafting is
`59d3f2ebcc4b817572e8410de503fa42e021cc8e`; registration must identify the
actual complete candidate used, including any reviewed working-tree files.

This is reception of molecular preparation and comparison over saved energies.
Guard against `bindingmt.dock`, `bindingmt.score`, importing Vina and hydrogen
generation. No new search, energy, minimization or visualization operation is
authorized. RDKit may execute the explicitly registered fresh charge/type
assignments and the provider's declared-graph capability. Preserve all provider
warnings without local suppression.

## Reproduce five matching prepared inputs

Load each complete eighteen-atom chemical/structural H5 model through public
MolSysMT conversion, exactly once. H5 is chemical/structural authority here;
its absent full MM payload is not repaired by decoding inspection sidecars.
Existing local H coordinates remain as received: request zero new hydrogens.

On each actual source axis, use public MolSysMT selection to resolve
`atom_name in ['C3', 'C1']`. Require exactly two distinct endpoints; do not infer
correspondence or transport literal indices between axes. First call public
`msm.build.assign_partial_charges(source, method='gasteiger_marsili')`, then
`msm.build.assign_autodock_atom_types(charged, typing_scheme='autodock4',
method='chemical_environment')`, once each per full18 source. Call
`prepare_ligand(typed, selection='all', ...)` once per source with that explicit
cut and the exact partner state declared by the saved scored collection.
Do not pass H, charge or typing options to this final preparation: it consumes
the five new preassigned models without calculating another assignment.
Require the received thirteen-atom, one-cut representation and its explicit
nonidentity written traversal. The five new assignment observations retain
their actual current producers; they are not the producers of the old energies.

Pair every preparation with the exact received receptor bytes, scoring domain
and saved partner/receptor state declarations in its own `DockingProblem`.
Use the existing construction contract for receptor and box, checking its
identities against the selected scoring histories. Preserve named source and
derived assignments, maps, quantities and preparation lineage. In particular,
the derived charge report's `parameters.source_calculation` already carries
the original calculation policy; inspect actual fields rather than assuming
that a top-level aggregation method has lost Gasteiger/RDKit attribution.

Static review corrected this operation order before registration or scientific
execution; no failed run prompted the change. The historical export includes
`REMARK BINDINGMT_ATOM_TYPES` with `source_status='projected'`: its named typing
preceded the real selection/extraction performed by `prepare_ligand`. Assigning
inside preparation options would instead occur after extraction and retain
`source_status='assigned'`, changing the exact bytes despite equivalent chemical
fields. The explicit public sequence above reproduces the actual projection
operation. It does not edit a status, restore a report or relabel a new producer
as historical. All five charge/type calculations remain new observations.

Before any comparison, export each prepared input once through its public
`to_pdbqt`. Require exact SHA-256 **and byte equality** with that pose's actual
captured ligand input. Verify the captured inputs using the public integrity
operation. A numerically similar or differently remarked export does not pass
this exact-input gate. Keep these five exports and all original capture hashes.
If a gate fails, retain the attempt and stop; do not rewrite PDBQT, override a
hash or recalculate the historical scores.

## Positive public comparison receiving

Run two whole-call repetitions under explicit caller unit policies: normal
nm/ps/elementary-charge and pm/fs/coulomb, retaining the caller's energy policy
and restoring the caller configuration after each completed context. Under
each policy call `compare_scores` once for `vina.lig_inter` and once for
`vinardo.lig_inter`, with all five matching problems in original order and
`ascending=True`. Thus there are four positive calls, two method-specific
decisions repeated under two reader policies, over one five-pose population.

Save each returned report immediately and exclusively, before assertions,
presentation or the next call. Retain every actual export map, current
molecular correspondence report, selected-evaluation audit, charge audit,
original and checked/projected assignments, source-record identity and decision
policy. Each positive call must receive all five rows. Public extraction with
explicit indices validates and projects legitimate derived assignments on the
actual exported molecular view; preserve the original and checked reports as
distinct producers. Native and written axes retain their own maps and trees.
Never compare correspondence-graph digests with writer/MM chemical digests.

The expected source-position display orders, taken from the old finite report,
are Vina `[1,2,3,4,5]` and Vinardo `[1,2,4,3,5]`. These are prospective regression
checks against already inspected scalar observations, not blinded predictions
or measurements made by this prescription. Equal reported values must remain
ties; source order is only their display convention. Do not alter units,
descriptors, original pose ranks or `ranking_history` to obtain an order.

Across caller policies require the same original scalar observations, decision
policy, groups, order, physical prepared quantities, molecular evidence and
original input identities. Newly generated inspection/producer fields retain
their actual declarations. A different valid QuantityRecord/unit representation
is not grounds for demanding literal whole-report byte identity. Check physical
quantities through public unit-aware operations; do not add a local converter.

Require JSON roundtrip of every saved report and a synthetic control that edits
the actual returned report while the source result, prepared objects and a
pristine saved report remain unchanged. This checks report independence; it is
not another empirical or molecular case. Record the observed control outcome.

## Refusal population

Apply the following six detached documentary controls **once under the normal
policy**, each as a separate public call. Preserve all unaffected input fields
and require an actionable refusal before molecular work:

1. Duplicate a pose ID.
2. Change a partner-state declaration.
3. Request the unsupported total-score component.
4. Remove the first pose's selected scoring history.
5. Change the selected current score without changing its recorded evaluation.
6. Change the first row's shared weights coherently in its selected current
   descriptor and corresponding evaluation descriptor, retaining internally
   valid documentary evidence but disagreement with the other four rows.

The changed-weights control must reach comparison-context refusal rather than
passing through an unrelated malformed-record failure. Record the actual
reason and the absence of molecular work for every documentary control.

Add two separate prepared-input controls under normal policy:

7. Supply a detached first prepared input with `source_molsys=None`. Require
   refusal before any export, extraction, charge audit or correspondence.
8. Change one coordinate of a detached first prepared input by `0.01 nm`.
   Require one actual export followed by captured-input hash refusal, before
   extraction, charge audit or correspondence. Do not mutate the original
   prepared source or pose and do not change the saved energy or capture.

There are twelve comparison calls in total: four positive returns and eight
expected refusals. An unexpected success, refusal reason, count or provider
failure stops receiving; no successful subset becomes a passing population.

## Exact direct-operation budgets

Counters distinguish call attempts, returns and checked outputs. They are
scoped to the named preparation/gate/comparison routes; they do not claim to
count every internal MolSysMT getter, extraction or writer validation.

| Operation | Registered count/cap |
| --- | --- |
| H5 source loads | 5 |
| Public ligand preparations | 5 |
| Fresh charge assignments / type assignments | 5 / 5 |
| Comparison calls / positive returns / expected refusals | 12 / 4 / 8 |
| Pre-comparison gate exports | 5 |
| Comparison exports | 21: twenty positive rows plus one changed-coordinate control |
| Total gate/comparison exports | 26 |
| Explicit comparison assignment-validation extractions | 20 |
| Comparison graph-correspondence calls | 20 |
| Comparison charge audits | 20 |
| Selected-evaluation audits | 35: twenty positive rows, five shared-weights rows, five missing-source rows and five changed-coordinate rows |
| Fixed-score geometry admission reads | 20 |
| Existing-helper native inspection snapshots | 30: five full18 and five prepared13 models at initial, post-positive and final boundaries |
| Returned-report detachment controls / strict JSON roundtrips | 4 / 4 |
| Detached prepared-coordinate controls | 1 |
| New docking / fixed-score / H-generation calls and Vina imports | 0 |

The other five documentary controls must stop before selected-evaluation audit.
The two prepared-input controls complete all five selected-evaluation audits
before entering molecular admission, but stop on their first prepared row.
Save diagnostics for any deviation; do not change caps after observing a failed
attempt without a separately registered amendment.

## Nonmutation, resources and failure custody

Keep read-only pre/post snapshots of all five original pose records, original
scores/ranks/histories and collection metadata. Inspect source/native
coordinates, chemistry, mechanical values and named reports through existing
public contracts, with quantities carrying explicit units. Native inspection
records are evidence, not a new molecular/MM restoration format. Include actual
correspondence results in the received chemistry evidence. Avoid extra exports
for snapshots that would violate the declared export denominator.

At completion verify the original source/input file hashes, registered runtime
and API bytes and relevant provider/native identities again. Assert no mutation
of the original result, problems, prepared sources or caller unit policy.
Retain original and newly generated assignment reports independently, and keep
all outputs detached from live scientific objects.

Run scientific work serially on CPU 0, nice 10, one logical CPU and one native
worker, including heavy descendants. Check available RAM before launch and
monitor an **8 GiB reserve**, **1 GiB owned-group RSS**, **2 GiB address space**,
**60 CPU seconds** and **90 wall seconds**. Stop only owned work on a threatened
bound; retain partial outputs, diagnostics and interrupted counts. Do not
automatically restart after a resource interruption, repeat successful molecular
work to repair reporting, or splice outputs across attempts. Use a fresh output
directory; preserve started/returned/checked/failed and not-attempted states.

Keep the registration, frozen inputs/source, notebook/harness identities,
operation journal, returned reports, refusals, physical/unit checks, warnings,
resource receipts and partial attempts under #78/#50 until the stated custody
review. Public delivery and later publication remain separately reviewed.

## Acceptance and limits

Acceptance requires four complete public reports with the expected physical
decisions, all eight informative refusals at their declared phase, exact input
binding, received provider chemistry/mechanics evidence, JSON/independence and
nonmutation controls, and operation/resource compliance. Record actual results
separately after execution; this document contains no passing outcome.

This receives one bounded public comparison profile using five historical E1
score records and five freshly reproduced matching preparations. It does not
receive the missing multipose **original docking result → reconstruction →
repreparation → additive rescoring** continuity route, restore historical
prepared13/H identity, authenticate old producers, establish affinity/accuracy,
pool Vina with Vinardo, admit total-score/common-reference ordering, qualify a
public installation/platform matrix or accept full E1. Separate E4 scheduling
and broader E1/E5 owners retain their existing scope.

## Preserved artifact preflight rejection

Before molecular receiving, the first private wheel built from `3b1853a`
contains all 64 required runtime paths but also 62 historical Python paths from
the untracked migration tree. Its SHA-256 is
`eaa5b04adc6e60e8b21f96b3f67056f69af18bbcd1ade3826e8234210f1cf263`.
Installation completes, but full payload ownership rejects the artifact; this
is not a passing private-consumer qualification. No scientific cell has run.

The local package-discovery correction is tracked under
[#30](../pending_proposals/adopt_required_python_314.md): use exact package roots
and dot-delimited descendants. Preserve the wheel, installed copy and rejection
independently. Build the replacement from a fresh committed source tree, verify
its entire payload (including unexpected namespaces) and register its actual
consumer/source identities before any molecular operation. The source migration
bundle and existing build/cache material are retained without modification.

## Executed private installed receiving

The corrected consumer is built from
`a7422dfb9f8c3b1c8ede3d852e202dc33e4beefe` in a fresh sparse Git worktree.
Wheel `bindingmt-0.0.0+298.ga7422df-py3-none-any.whl`, SHA-256
`93d76f898575fb64b39520f33ceded25708270c8042c2a53c9a451acd834bcdd`,
contains exactly 64 runtime paths and its own distribution metadata, with no
foreign namespace. All 63 nongenerated paths match that source commit; installed
bytes and generated version match the wheel. The new private target has 3,867
files, borrowing the retained support/provider composition. Old targets remain
unchanged. Build attempt 02 stops because the new sparse worktree index is not
yet materialized; attempt 03 builds after that administrative setup correction.
Neither that failed setup nor the rejected first artifact executes science.

The [preserved manifest](data/e1_public_comparison_2026-11-07/manifest.json),
SHA-256 `88c84da8f4fd4a3f48125e167536127207b41f7f703cfa4d0c3ddf4956ff5f37`,
contains 157 bounded records/harness inputs, 2,432,932 stored bytes. Compression
is transport only; stored/decoded hashes preserve original bytes. Private
wheels/native dependencies/environments remain separately retained.

| Boundary | Actual outcome |
| --- | --- |
| Prepared-input gates | Five fresh named charge/type assignments and five preparations exactly reproduce both captured ligand inputs per pose. Zero new H. |
| Public comparisons | Four complete returns: two methods under two caller unit policies, five rows each. Vina positions 1–2–3–4–5; Vinardo 1–2–4–3–5. |
| Evidence | Twenty provider correspondences, twenty explicit assignment-validation extractions, twenty charge audits/geometry reads and 35 selected-evaluation audits pass. Original derived and newly checked projected reports remain separate. |
| Controls | All eight refusals occur at the registered phase/reason. Thirty source/prepared snapshots, four actual-return detachment checks and four finite JSON roundtrips pass. Original records/preparations/caller unit policy survive. |
| Resource receiving | 24.37 s, sampled peak group RSS 352.29 MiB, CPU 0/nice 10. No interruption or signal. |
| Installed/support | Designated runtime roots resolve privately; pre/post complete target hashes agree. Declared shared support staging validates source/SDK bindings and retires resources/imports. |
| Independent saved reader | Fresh standard-library process receives four reports/twenty rows and eight refusal records in 0.61 s/34.30 MiB, with identical report bytes/decisions and zero molecular operations. |

The [generation receipt](data/e1_public_comparison_2026-11-07/attempts/receiving-01/output/receipt.json.gz),
[resources](data/e1_public_comparison_2026-11-07/attempts/receiving-01/resource-outcome.json.gz),
[fresh reader](data/e1_public_comparison_2026-11-07/attempts/json-reader-01/output/receipt.json.gz),
[wheel inspection](data/e1_public_comparison_2026-11-07/assembly/wheel-inspection-02.json.gz)
and [rejected artifact](data/e1_public_comparison_2026-11-07/assembly/artifact-rejection-01.json.gz)
retain their distinct producers/outcomes. Source software passes 193 tests;
distribution controls pass 19. Initial collection/build/setup/rejection records
remain in the archive. Independent architecture/evidence reviews find no further
blocking discrepancy within this scope.

This receives the bounded public comparison profile with a privately installed
consumer and borrowed providers/dependencies. Twenty graph witnesses concern
five existing conformations, not twenty independent molecular cases. RDKit
assignment/native files are identified after execution; this does not qualify
every borrowed native dependency or its complete before/after state. Zero
energies, searches or H-generation operations occur. Historical preparation
authentication, affinity/accuracy, total/common-reference ordering, multi-pose
original-result reconstruction/additive continuity, public platform delivery,
full E1/E5 and the separate E4 hold remain pending. Remote CI stays deferred
under `[skip ci]`; it is not a passing checkpoint.
