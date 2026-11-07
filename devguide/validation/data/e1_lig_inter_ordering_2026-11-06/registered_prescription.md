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
