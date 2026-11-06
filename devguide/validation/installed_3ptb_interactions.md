# Installed 3PTB interaction workflow

Owner: [DockingMT #80](https://github.com/uibcdf/dockingmt/issues/80).
The [six-cell notebook](installed_3ptb_interactions.ipynb) composes existing public
MolSysMT tools for one retained docking pose. **Receiving has not passed.** The
first attempt lacks notebook tooling; the corrected-tooling attempt is stopped
by the RAM-reserve guard. No completed interaction analysis, scientific result
or E4 acceptance is reported.

## Inputs and executed work

Use the five explicit inputs of the
[preparation companion](installed_3ptb_preparation.md), plus:

```bash
export DOCKINGMT_INTERACTIONS_PREPARATION_NOTEBOOK="installed_3ptb_preparation.ipynb"
export DOCKINGMT_INTERACTIONS_PREPARATION_NOTEBOOK_SHA256="c6c5a6660b8b5d46df01cde6960129a7bc65db81d551b3ad0a4d763fc0907da9"
export DOCKINGMT_INTERACTIONS_RESULT="native_result_2026-10-20.json.gz"
export DOCKINGMT_INTERACTIONS_RESULT_SHA256="4b1f51cdeb135fd6785a181f6bb09a0d0f631ec3d9de7c169c88703748924249"
export DOCKINGMT_INTERACTIONS_OUTPUT="new-interaction-output"
```

The original [five-pose result](data/human_3ptb/native_result_2026-10-20.json.gz)
and preparation source/declarations retain their bytes and producers. Expected
hashes come from the trusted original records, not a fresh self-approval hash.
Use an ordinary installed scientific environment with IPython/Jupyter and
`nbformat` plus its dependencies available. No repository/data harness or SDK
import is required. The qualified installation here is private; these commands
are not a public DockingMT installation/release claim.

Run All replays the trusted preparation notebook once, then selects the first
stored pose. It uses the known prepared native ligand source and checks the
explicit thirteen-atom identity axis through MolSysMT getters. Public setters
place its actual coordinates; delivered fixed-state H addition materializes the
five virtual nonpolar H retained by the provider's projection. Existing pose
atoms and polar-H coordinates must remain. The new H are local generated
geometry, not environment refinement or atoms returned by docking.

Public `msm.merge` assembles ligand and full receptor context. A separate +60
angstrom ligand translation supplies a geometry control, not another native
pose. The named hydrogen-bond and hydrophobic-proximity criteria are evaluated
for each model, with explicit state, disjoint between selections and `pbc=False`.
Two independent declared water geometries control positive/adverse hydrogen-bond
behavior. The [registration](installed_3ptb_interactions_registration.md) defines
six detector calls per profile, controls, units and failure/resource boundaries.
No search, scoring, minimization, alignment or viewer is part of this notebook.

Complete provider analyses use `InteractionsDict` and attached H5MSM. The separate
association manifest binds provider file identities to the original pose, states,
coordinates and scores. Inspection pages/dictionaries are not substituted for
the molecular persistence codec. All chemical interpretation, geometry, H
generation, detection, filtering and molecular serialization stay in MolSysMT.

## Observed attempts — 2026-11-06

The [receiving record](data/interaction_receiving_2026-11-06.json) distinguishes
the registered producer, fixed private consumer and unchanged providers:

| Attempt | Actual disposition |
| --- | --- |
| Initial file-audit setup | Four stops expose wrong assumptions about pip versus Conda file authority and generated entry points. Corrected read-only checks distinguish active installers, source overlays and unsealed generated files. No molecular workflow runs in these checks. |
| Normal profile | IPython fails to import `nbformat` before notebook cells. Observer records zero H/merge/set/translation/detector attempts. |
| Isolated-tooling amendment | Seven cached Conda tool packages supply 208 individually verified files outside the scientific prefix. Python dependencies, native Python-3.12 rpds import and notebook validation pass. |
| Normal with tooling | RAM-reserve guard terminates the owned process after 5.270 seconds. The initial output directory exists; no final observer, association or provider-analysis file exists. Final molecular call counts are unverified. |
| pm/fs profile | Not attempted after the resource stop. |

The stop enforces the shared-machine budget; it is not a detector refusal or
biological observation. Only owned work is terminated. There is no automatic
heavy restart, replacement pose selection or inference of empty interactions.
The full E4 and functional-release requirements remain unproven.

## Observability refinement after the stop

The originally attempted notebook at `45b15e8` retains SHA-256
`b6a0d8269403acae5b242ced9cc7d65ce42430b002ddbd263407554d309f1b07` in
Git and frozen task inputs. It is not relabelled with the later refinement.
The maintained notebook now writes `registration.json` and append-only,
flushed `progress.jsonl` before preparation and each detector phase. Completed,
failed and started-without-completion states remain distinct after interruption.
Partial directories are retained; an existing output directory is refused.

This refinement is syntax/format checked and **its molecular cells are not
executed**. A small isolated standard-library control runs the actual journal
helper, terminates its own process with SIGTERM and retains one valid started
event. It verifies durable software evidence, not the molecular notebook.
It changes workflow evidence, not molecular operations or the six-call
denominator. Before another attempt, review the resource disposition and
register a fresh execution identity/budget; the missing final counter of the
interrupted attempt must not be turned into zero calls. No automatic retry is
scheduled by this guide.

## Remaining acceptance

Receive the actual molecular route, named criteria, original-pose association,
complete typed/H5MSM roundtrips, independent analytic controls, nondefault units
and detached fresh readers. Then qualify the actual current consumer/provider
candidate and applicable supported/public profiles. Neither source availability,
an installed old candidate nor this interrupted attempt substitutes for those
gates. Preparation suitability remains `unassessed`; affinity, independent
scientific-panel and live-canvas acceptance retain their own owners.

Custody is #80/#50, review **2026-11-13**. Preserve original inputs, qualified
bases, exact notebook variants, isolated tools and unique diagnostics. Retire
only verified owned runtime/cache scratch; operational details remain local.
