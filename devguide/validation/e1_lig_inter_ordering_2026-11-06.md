# E1 received-case interaction-component ordering — 2026-11-06

Owner: [DockingMT #78](https://github.com/uibcdf/dockingmt/issues/78).
Status at prescription: **prospective**. The
[notebook](e1_lig_inter_ordering.ipynb) receives one finite study policy over
the [existing native observations](e1_native_rescoring_2026-11-06.md).
This is a case-specific external report, not a new public comparison API or a
change to `DockingResult.rank_by`, descriptors, pose ranks or ranking histories.
This is exploratory secondary analysis of scores already inspected. Registering
the reader before execution does not make the policy selection or molecular
predictions prospective, blinded or independently validated.

## Study question and direction

For the five newly completed conformations of the received ligand model against
the same supplied receptor, order the **reported `lig_inter` values, lower
first**, separately within Vina and Vinardo. This direction is the study's
explicit choice. Original descriptors retain `preferred_direction=null`.
The component concerns the receptor-interaction model; no affinity calibration,
total-score preference, physical validity, significance or cross-method scale
is inferred. The partial/unassessed receptor is admitted only as the same fixed
PDBQT input of this declared computational model.

The received `lig_inter` component does not subtract the unbound reference.
Its complete source evaluation/history must nevertheless be internally
consistent and documentarily complete. A missing reference record can stop this
documentary admission; it does not make `lig_inter` physically dependent on that
reference. Contradictory reference records remain inconsistent. This profile
does not receive total-score ordering, a common unrounded reference, historical
docking comparison or a Vina/Vinardo pool. Those are separate questions, not a
claim that all such future comparisons are universally impossible.

## Frozen roots and custody

The exact previously received manifest roots are:

- Complete-pose construction:
  `45b3665ba09b6979aa1bcdf1bea0ac3e8102f081fefbfc51348c55bc71405df3`.
- Native scoring:
  `bf214aa7e48f15a95051411ed3bd54969f78c811503050c6969d6f5aa2898e93`.

Verify every listed file and compressed/decoded identity, actual registrations,
and the native receipt's construction-root link before admitting any row.
The policy trusts this identified receiving population and its retained
producers. A newly supplied self-consistent manifest is not authentication of
another study. Candidate records/evidence must still bind exactly to these
received snapshots after semantic checks. Inspection JSON hashes are custody
checks, never a locally invented molecular fingerprint.

## Required evidence per row

Require exactly five unique expected pose IDs, source positions and unchanged
state declarations, with both complete original method evaluations retained.
No failed/incomplete member may silently turn into an ordered subset.

Consume the received full18, prepared13 and mapped-read13 correspondence
reports: complete axes and supplied identity candidates, one admitted candidate,
complete supplied-map search, declared-graph profile/rule, state index 0 and
their original producer digests. A null provider chemical-state label is valid
here; it is distinct from DockingMT's declared partner-state label. Compare
digests only within their own contracts. Do not equate correspondence-graph
digests with writer/mechanics chemical digests, recompute molecular identity,
decode a molecular model locally or run another matcher.

Read sealed charge quantity records through PyUnitWizard with explicit
elementary-charge expectations. Check aligned eighteen-/thirteen-atom charges,
types, original named methods, derived assignment axes, conservation evidence,
the single selected cut and both native/written trees/maps against this
received profile and the reference row. The derived typing report retains its
original eighteen-atom calculation count with thirteen projected source indices;
do not relabel it as a new thirteen-atom typing calculation. These are checks
of received mechanical evidence, not MM restoration or a fresh chemical audit.

The native writer map binds `native.pdbqt`; actual scoring captured
`dockingmt.pdbqt`. Keep their different hashes and use the already executed
field/tree receiving plus the retained associations to join them. Never attach
the native map's payload hash to the remark-bearing DockingMT text. Native tree
branch `(6,0)` and parsed written branch `(0,7)` belong to different axes.

Require exact received method/version/component/kind/unit, both state labels,
fixed receptor capture, box/frame lineage, reported weights/spacing, CPU/seed,
preparation policy and identified source/native producer. Keep every context
field. Different partner hashes are expected only after each actual capture is
bound to its own received complete pose; another unexpected context difference
refuses this case admission. A changed input means a broken receiving/capture
binding, not merely one of the five legitimate different conformation hashes.

This profile accepts the received kcal/mol representation. Other energy
representations remain outside this frozen profile rather than being declared
physically incompatible. No local unit converter is introduced. Repeating the
reader under normal and pm/fs/coulomb/kJ-per-mol policies must preserve the
original scalar values, contexts and resulting report bytes.

## Ordering and controls

Use `Decimal` of the published scalar representation to check the received
0.001-kcal/mol resolution. Reject booleans, nonfinite values and unexpected
extra precision; do not round a changed value into admission. Equal reported
values form a tie at the available resolution. Preserve source order only for
presentation inside that tie, with no chemical tie-break or superiority claim.
Produce groups and a display order separately for each method, retaining
original row values, full descriptors/contexts, input/evidence identities and
the study's direction. Four positive admissions are two methods repeated under
two reader policies, not four independent studies or molecular cases.

Prescribe 33 documentary controls per policy, 66 expected refusals total:
altered capture; unreceived partner; missing/changed witness; changed charges,
types, tree or export axis; changed receptor or either state; weights, box or
spacing; wrong dimensional label or other energy representation; duplicate ID;
nonfinite, boolean or excess-precision score; missing/contradictory reference;
total or mixed-method request; unknown context field; changed backend version
or typing method; missing assignment projection; wrong export-payload binding;
a coherently edited score; changed custody root or construction/scoring link;
and an incomplete population. These mutations concern copies of documentary
evidence, not newly prepared molecules or native observations.

Also receive a separate synthetic tie control and detached-report check under
each reader policy. Synthetic values are software examples, not new empirical
measurements. Retain both existing-public-method ranking refusals per policy
and verify the original collection/source files remain unchanged.

## Execution and limits

Register notebook/cell/input/prescription identities before a fresh process
executes four plain Python cells. Run serially on one allowed logical CPU,
nice 10, with one native/build worker. Admit and monitor an 8 GiB available-RAM
reserve, 1 GiB task RSS, 2 GiB address space, 60 CPU seconds and 90 seconds wall.
Unexpected outcomes stop the selection and preserve partial outputs; no
automatic resource restart or splicing across corrected attempts. Keep exact
positive/negative denominators and diagnostics under #78/#50; custody review
**2026-11-13**.

This reader makes no molecular-operation, Vina, preparation, docking or new
scoring call. Quantity decoding and saved-record audits remain explicit.
Optional engine/viewer imports must remain absent. Native source/build and
effective-grid observational limits remain as recorded; this policy compares
observations from the same identified executed artifact without upgrading those
limits. Its outcome can receive only this finite component-ordering policy;
representative installed acceptance, full E1 and the separate E4 hold remain.

## Executed offline policy receiving

Attempt 01 completes the four registered plain Python cells in **3.92 s**.
Its [registration](data/e1_lig_inter_ordering_2026-11-06/registration.json) binds
notebook SHA-256
`389412ed8f9005ec4b73b60e87d523cf0377cf1ce034fb348c8eb174f4260eea`.
The [frozen prescription](data/e1_lig_inter_ordering_2026-11-06/registered_prescription.md)
predates the reader run; the source predictions and exploratory policy selection
remain earlier observations, without a prospective/blinded science claim.
No Jupyter frontend/kernel session is qualified by this cell execution.

| Receiving | Actual outcome |
| --- | --- |
| Closed population | Both method-local five-pose populations are admitted under each reader policy: four admissions representing two component studies. |
| Documentary controls | All 33 controls refuse under each policy: 66 expected refusals. No failed member yields an ordered subset. |
| Source/audit binding | Twenty-two saved-record audit calls and 36 sealed charge-record readings stay within caps. Two audits concern coherently edited documentary controls: internal consistency does not authenticate a received score, so the final custody binding correctly rejects them. |
| Ties and ownership | Two synthetic tie controls retain source presentation inside an equal-value group. Two checks mutate the actual returned report and confirm its input snapshot remains unchanged. Synthetic values remain software examples. |
| Existing public API | Four `rank_by` requests on the selected described `lig_inter` scores still refuse, with the collection unchanged. No native descriptor, rank or ranking history is edited. |
| Units and custody | Corresponding positive report bytes are identical between normal and pm/fs/coulomb reader policies. Both frozen manifest roots and every source file remain unchanged. |
| Resources | One CPU, nice 10, one native/build worker; sampled peak RSS **75.43 MiB**, minimum available RAM **42.84 GiB**, no resource interruption or termination signal. |

The received orders are below. Source positions identify the new native-study
records in their original input order; they are not newly assigned pose ranks.
Every actual reported value is distinct within its method, so this population
has no empirical ties. The reports retain full original descriptors/contexts,
reference records, custody identities and the received molecular-evidence links.

| Case policy | Source positions, lower reported `lig_inter` first | Reported values in that order, kcal/mol |
| --- | --- | --- |
| Vina | 1 → 2 → 3 → 4 → 5 | -6.422, -6.258, -4.105, -4.007, -3.507 |
| Vinardo | 1 → 2 → 4 → 3 → 5 | -5.941, -5.676, -3.357, -3.214, -2.975 |

See the separate [Vina report](data/e1_lig_inter_ordering_2026-11-06/normal/vina_component_order.json.gz)
and [Vinardo report](data/e1_lig_inter_ordering_2026-11-06/normal/vinardo_component_order.json.gz).
The methods are not pooled or calibrated against one another. These conditional
empirical interaction orders do not establish an affinity order, total-score
policy, shared unrounded reference, uncertainty model, recovery result or
historical energy equivalence. The original `preferred_direction=null` fields
remain intact; direction belongs only to this external case policy.

The [receipt](data/e1_lig_inter_ordering_2026-11-06/receipt.json) retains all
denominators, scopes, versions and reader-policy outcomes. The
[manifest](data/e1_lig_inter_ordering_2026-11-06/manifest.json) binds both repeated
positive reports, all refusal diagnostics, synthetic controls, admission journal,
registered code/prescription and resources. Gzip is transport only; verify
compressed and decoded identities before restoring an original filename.
No empirical value is recalculated. The zero-new-operation statement follows
the inspected record-only routes rather than hidden molecular/native counters;
Vina, RDKit and MolSysViewer remain absent from the process module inventory.

This receives the stated finite comparison/ordering policy under #78. A
representative installed workflow and any decision to expose a broader reusable
interface remain separate work; this notebook is not a new runtime API. Source/
native build correspondence and effective-grid observations keep their existing
limits. Full E1 acceptance and the independent local E4 hold remain unchanged.
