# Installed 3PTB interaction workflow

Owner: [DockingMT #80](https://github.com/uibcdf/dockingmt/issues/80).
The [six-cell notebook](installed_3ptb_interactions.ipynb) composes existing public
MolSysMT tools for one retained docking pose. **Receiving has not passed.** The
first attempt lacks notebook tooling; the corrected-tooling attempt is stopped
by the RAM-reserve guard. The first hosted attempt completes preparation but
refuses XYZ coordinate extraction before detectors. No completed interaction analysis, scientific result
or E4 acceptance is reported.

A separate [hosted receiving registration](installed_3ptb_interactions_hosted_registration.md)
defines exact-source Linux/Python 3.14 normal/pm-fs execution and independent
saved readers. Its first failure and later unexecuted explicit-atom amendment
remain separate; the local computational hold stays active.

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

At that checkpoint the refinement is syntax/format checked and **its molecular
cells are unexecuted**. A small isolated standard-library control runs the actual journal
helper, terminates its own process with SIGTERM and retains one valid started
event. It verifies durable software evidence, not the molecular notebook.
It changes workflow evidence, not molecular operations or the six-call
denominator. Before another attempt, review the resource disposition and
register a fresh execution identity/budget; the missing final counter of the
interrupted attempt must not be turned into zero calls. No automatic retry is
scheduled by this guide.

The hosted variant adds explicit provider H correspondence and merged ligand
axes to the docking association, retaining the same six molecular cells and
progress evidence. Its source/notebook identities and new finite budget are
registered separately before dispatch. Source-provider persistence stores the
resolved site definition; the reader verifies `site_definition` rather than
assuming the caller's `profile` label is a persisted field. This is a client
contract correction, without a provider or molecular algorithm change.

## First hosted receiving and client amendment

Source `988d8a1cd9cc069d2d44d3bd229cd1ff10fc780f`, notebook SHA-256
`549d3216cc4f5ec810da95c0c292dafbe9b49f8eb9ca56f1647624b068ccee0a`, is
registered before [run 42203647830](https://github.com/uibcdf/dockingmt/actions/runs/42203647830).
The [durable receipt](data/interaction_hosted_receiving_2026-11-06.json)
retains its same-run archive, exact source/inputs, Python 3.14.10 composition,
original preparation outputs, final observer and nonpassing disposition.

Conda setup, exact sibling/consumer installation, routes and pip closure pass.
The preparation companion completes its 2,011/13-atom checks and controlled map
refusal. Next, `msm.get(pose.coordinates, coordinates=True)` selects the XYZ
system getter and raises `NotWithThisFormError`. The normal profile exits after
13.264 seconds without a resource stop. Its final observer confirms **zero
detector attempts**, all forbidden counters zero and unchanged consumer/source-
provider payloads. Pose H completion, assembly, analyses, persistence, fresh
readers and pm/fs are not reached. This is not evaluated-empty interaction data;
the overall unit-policy acceptance is not manufactured after the exception.

The original artifact has 31 entries; its 4,106,592-byte ZIP independently
matches GitHub digest `e4f12b46f1255141cefe621f9959c54c7432cb68ced49849ac35dddaed9a6700`.
It is retained locally before remote expiry. Existing local interrupted counts
remain unknown and separate from this verified hosted zero.
Seven byte-exact original registration/build/preparation/receiving/observer,
journal and diagnostic exports are also preserved compressed in Git, with both
compressed/original digests in the receipt. These do not duplicate the full ZIP
or pretend that missing interaction files exist.

[MolSysMT #610](https://github.com/uibcdf/molsysmt/issues/610) receives the exact
refusal and asks for the supported public delivery contract. Inspection at the
qualified pin finds the public atom-level getter and provider-owned rank-three
normalization. The amended notebook explicitly requests `element='atom'` in
that same public call. It adds no coordinate getter, reshaper or molecular
adapter here. Its SHA-256 is
`6c43428ea9053dde56039828e16cfb14884a65fc91d9b76eb1e8455000336c01`.
This amendment is unexecuted; register its exact published source and budget
before a new run. Preserve the failed run and do not rerun it automatically.

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
