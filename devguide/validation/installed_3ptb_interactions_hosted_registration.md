# Hosted 3PTB interaction receiving — registered scope

Owner: [DockingMT #80](https://github.com/uibcdf/dockingmt/issues/80), with
#73/#28/#50. Date: **2026-11-06**. Status at registration: **prospective; not executed**.
This is a new receiving population after the
[interrupted local attempt](installed_3ptb_interactions.md). Its local resource
hold remains active; no local molecular replay or dependency solve is authorized
by this registration. Preserve the original prescription, inputs and diagnostics.

## Exact producer and scientific scope

Before dispatch, publish and register the full main source commit on #80.
The manual [workflow](../../.github/workflows/qualify-3ptb-interactions.yml)
requires that exact hash as `expected_source_sha`; dispatch, checkout and runtime
registration must agree before setup or calculation. The source commit's
[operator](../../devtools/qualify_3ptb_interactions.py) verifies all five inputs:

| Input | SHA-256 |
| --- | --- |
| Interaction notebook | `549d3216cc4f5ec810da95c0c292dafbe9b49f8eb9ca56f1647624b068ccee0a` |
| Preparation notebook | `c6c5a6660b8b5d46df01cde6960129a7bc65db81d551b3ad0a4d763fc0907da9` |
| 3PTB source | `75b1b8e73b4c197b7dcb217fbcfdd39c451860c0fd5a86cdef587c4dbd9972be` |
| Original admission declarations | `79e9283236ebbb645cd75d7c3341d457a8078361466b7a26458c814d8041cd53` |
| Original compressed result | `4b1f51cdeb135fd6785a181f6bb09a0d0f631ec3d9de7c169c88703748924249` |

The notebook differs from `5032664` only by retaining the explicit provider
atom correspondence and merged ligand axes in the docking association. It keeps
the same six molecular code cells, progress journal, first original pose,
chemical declarations and [six-call prescription](installed_3ptb_interactions_registration.md).
The notebook variants at `45b15e8` and `5032664` retain their own identities.
The original five-pose result/producer and fixed private 0.1.0 candidate are
unchanged. No positive pose selection, search, energy call or optimization occurs.

All preparation, H generation, selection, assembly, coordinate editing,
interaction recognition/geometry, filtering and molecular persistence use public
MolSysMT APIs. DockingMT's operator binds its own records, source/archive identities
and finite execution. A missing molecular operation or provider defect is reported
in MolSysMT, without a DockingMT replacement.

## Installed composition

Use one GitHub-hosted Linux x86_64/Python 3.14 runner. The reviewed Conda
[E4 environment](../../devtools/conda-envs/e4_env.yaml) supplies scientific and
notebook tooling with strict `uibcdf`, `conda-forge` priority. It selects SMonitor
0.22.1, DepDigest 0.15.2, PyUnitWizard 0.29.0, RDKit 2026.03.1, IPython 9.17.1,
nbformat 5.11.1 and public Pytest Receptor 1.2.2. Other resolved files/versions
are observed, not retrospectively asserted identical to the local Python 3.12
closure. Existing ordinary-CI directory source routes remain exact:

| Provider | Source commit |
| --- | --- |
| ArgDigest | `3d1ec53c374098016452abab74706e9d80df5462` |
| MolSysMT | `00abb958fb93649131d5ce5fe5e12e90cf4900e9` |
| MolSysViewer | `78ede79e2e345593db5bfe80d246d3f6c70bd005` |
| Dependency SDK | `738fe8dd731abb99dac421b0bb2acc8564110180` |

Build one ordinary private DockingMT wheel from that exact source, verify its
63 declared runtime payloads against source (62 tracked plus generated version),
metadata, license and addon entry point, then install those same archive bytes.
Each scientific process uses isolated Python outside the checkout, checks
installed origins and archive binding, and compares DockingMT plus the three
source-provider payload sets before/after. This does not verify every native file
in the entire environment. Retain pip inspection, Conda inventory/explicit
resolution and before/after pip closure separately.

The new test-only environment changes no public runtime floor, dependency edge,
Conda release recipe or installed-support fixture snapshot. Runtime-bearing
routes and reviewed workflow hashes are in `devtools/dependency_routes.toml`.
The local workflow follows existing micromamba/manual/read-only/failure-retention
patterns. The measured need is #80's shared-machine RAM stop. Retire this bounded
caller after receiving #80 or receiving an accepted common scientific route;
[MolSysSuite #31](https://github.com/uibcdf/molsyssuite/issues/31) separately owns
replacement of the source-acquisition variation.

## Finite execution and failure policy

Run **normal**, then **pm/fs**, serially. Each profile has six detector calls,
followed by a separate fresh process reading saved provider files without
preparation, H addition, detection, Vina, scoring or visualization. The new maximum
is **12 detector calls**, not 12 independent cases. The interrupted local
attempt's final counters are unknown: conservatively reserve its whole six-call
budget separately, yielding at most **18 cumulative** local-unknown plus hosted
calls. The earlier pre-cell tooling failure has observed zero molecular calls.

Use one logical CPU, low priority and one native/build worker. Each profile has
300 seconds; each reader has 120 seconds. Keep a **1 GiB hosted RAM reserve** and
64 MiB owned output limit per profile; the workflow has a 60-minute total bound
including solve/build. This new cloud budget does not relax the old local reserve.
Stop only owned children on a threatened bound. No automatic retry, rerun,
fallback provider, replacement pose or execution on the shared workstation occurs.
A failed normal profile stops before pm/fs; failed readers also stop the sequence.
Retain started/completed/failed states, warnings and partial output. Amend and
register any changed contract or new attempt before further calculation.

## Receiving and custody

Acceptance needs all four profile/reader operations completed, exactly six
observed detector calls per profile, no forbidden calls, preserved input/runtime
bytes and caller policy, passing analytic/adverse controls and full typed/H5MSM
roundtrips. Fresh readers check named methods/site definitions/PBC, units,
coverage/filtering, original pose/states/scores, atom maps, coordinates and file
digests. Empty observations, missing coverage and incomplete execution remain
distinct. Software gates alone do not establish molecular acceptance.

Retain the same-run wheel, registration, observer/reader receipts, journals,
association, four H5MSM files per completed profile and diagnostics as an
attempt-qualified Actions artifact for 14 days, including nonpassing outcomes.
Retrieve the needed evidence before expiry; archive a sanitized durable receiving
record in this repository and cross-link #80. Custody review: **2026-11-13**.
No public package, platform/minor matrix, independent panel, live-canvas
acceptance, complete E4 or functional-release claim follows from this bounded run.

## First disposition and explicit-atom amendment

Initial producer `988d8a1cd9cc069d2d44d3bd229cd1ff10fc780f` is
[registered before execution](https://github.com/uibcdf/dockingmt/issues/80#issuecomment-6682811593).
[Run 42203647830](https://github.com/uibcdf/dockingmt/actions/runs/42203647830)
fails after preparation and before detectors because omitted-element XYZ
coordinate extraction selects an unavailable system getter. Its final observer
verifies zero detector attempts, passing pip closure and unchanged payloads;
normal reader and pm/fs are not reached. Preserve the full
[receiving record](data/interaction_hosted_receiving_2026-11-06.json).

The client amendment explicitly supplies `element='atom'` to public `msm.get`,
using the provider's existing atom getter/rank normalization, source-inspected
at the same qualified pin. [MolSysMT #610](https://github.com/uibcdf/molsysmt/issues/610)
owns clarification of the public XYZ composition/default behavior. No provider
pin, model, scientific population, molecular operation or six-call denominator
changes. New notebook SHA-256:
`6c43428ea9053dde56039828e16cfb14884a65fc91d9b76eb1e8455000336c01`.

This is an unexecuted amendment. Publish/register the new full source on #80
before dispatching one new attempt; do not rerun the old producer. The twelve-call
new hosted maximum plus the original unknown six-call local reserve remains
eighteen: the first hosted attempt has a verified zero and releases its unused
detector budget. All other scientific/resource/retention/failure conditions above
remain. A proposed composition and successful preparation do not accept E4.
