# Versioned milestones toward 1.0.0

Owner: [DockingMT #73](https://github.com/uibcdf/dockingmt/issues/73).
Maintainer request: 2026-11-05. This is a **prospective release ladder**, not a
selected release candidate, a public version announcement or permission to infer
unexecuted gates. The [operational roadmap](ROADMAP.md#current-operational-plan),
[scientific MVP](MVP.md) and [Core acceptance map](CORE_MVP_STATUS.md) retain their
own authority. Existing scientific producers and package identities remain intact.
The maintainer has accepted **Core plus Extended MVP for 1.0.0** under
[DMT-045](DECISIONS.md#dmt-045--require-core-and-extended-mvp-for-100).
That target scope is settled; intermediate numeric identities and actual release
candidates remain prospective.

The maintainer's 2026-11-06 objective is complete functional delivery in
the prospective **0.5.0 milestone before stabilization**, reserving 1.0.0 for
afterwards. Stabilization can span as many further reviewed **0.x.0** milestones
as the actual work requires. There is no mandatory `0.9.0` release or fixed
upper minor before 1.0.0. A possible `0.23.0` illustrates that open sequence;
it is not a selected DockingMT version, candidate or release.
[DMT-046](DECISIONS.md#dmt-046--deliver-the-complete-functional-objective-before-stabilization)
and [DMT-048](DECISIONS.md#dmt-048--let-pre-10-versions-follow-verified-progress),
together with the [requirement/evidence plan](PRE_STABILIZATION_PLAN.md), preserve
every Core, Extended, scientific, reproducibility and public-delivery obligation.

## Why consolidate intermediate versions

DockingMT has meaningful software, workflow and scientific checkpoints worth
making easy to identify. A version should name a reviewed, reproducible scope
with explicit limitations. It need not claim the whole Core, general docking
accuracy or a public Conda package merely because a tag exists.

No remote tags or GitHub Releases are observed at this review's source
`37e3771a6540d66992f799e500fdb82e221377dd`. Development identities derived from
the `0.0.0` fallback are not previously published releases. No tag, Release,
package version or real `release_plan.toml` is created by this plan.

## Proposed ladder

The numbers are prospective identities attached to outcomes, not dates or a
requirement to manufacture every intermediate release. Combine milestones if their actual
evidence arrives together. Do not advance a number solely because time or commit
count has increased. Patch versions such as `0.1.1` describe reviewed corrections
within a declared scope; new capabilities or intentional pre-1.0 compatibility
changes get a reviewed minor milestone and migration notes.
Stabilization follows the same rule: choose each actual version from the
accepted increment and its evidence, rather than reserving a particular minor
as a compulsory final stage. Completing the functional objective does not by
itself establish stability or select the 1.0.0 candidate.

| Prospective version | Meaning | Completion evidence / owner |
| --- | --- | --- |
| `0.1.0` | First consolidated reproducible source baseline. | Exact candidate, truthful version metadata, qualified source dependency composition, executed applicable source/quality/policy/addon gates, source-use instructions and release notes. Bound the claim to delivered Vina/box/preparation/result/score/recovery behavior and existing evidence. State that public dependency pairing, whole-Core and visible C4/C6 remain unaccepted where applicable. #73/#28/#19/#33. |
| `0.2.0` | First independently installable public Conda delivery. | Covering real public providers, measured compatible minima/closure, the staged candidate's fifteen required native jobs and eight installed cells, exact-file archive/resource checks and same-byte promotion/public receiving. Matching release identity and availability notice. #30/#47. A partial/private solve cannot satisfy this milestone. |
| `0.3.0` | Core MVP accepted for its declared scientific profile. | All 35 C0–C6 criteria have explicit acceptance, including actual visible domain/reference/pose observation and a scientifically credible complete redocking workflow. Preserve refusals, preparation assumptions, score meaning and source/state/selection provenance. #4/#33/#49/#52/#60 and the Core map. |
| `0.4.0` | Bounded scientific qualification beyond the original worked example. | Admit a small transparent independent set before execution, with provider-owned source/chemistry/plausibility tools, explicit preparation hypotheses, informative search-versus-ranking controls and all adverse/unassessed outcomes. Prespecify scope, denominators, budgets and decision rules. Existing 5X72/3PTB repetitions are not new independent complexes. #33/#49 and the audit Q2–Q4 plan. |
| `0.5.0` | Complete Core-plus-Extended functional objective, before stabilization. | C0–C6 and E1–E5 have executed acceptance, bounded scientific qualification, independent reproducibility and actual public delivery/support evidence. Reuse existing APIs, receive provider-owned molecular tools and preserve failures/provenance. `PRE_STABILIZATION_PLAN.md` maps the whole objective; #73 owns the goal and #78 starts E1. |
| Further reviewed `0.x.0` milestones | Stabilization of the delivered Core-plus-Extended contract across the increments actually needed. | Verify C0–C6 and E1–E5 acceptance, public API/schema and compatibility promises, supported dependency/platform combination, reproducibility instructions, examples and remaining critical findings. Record each increment's scope, checks, remaining limits and next step. Freeze intended scope; close or explicitly defer work outside it. No Extended gate is deferred beyond 1.0 by default. Select actual minor/patch identities through their release records; neither `0.9.0` nor the illustrative `0.23.0` is prescribed. #73/#28/#30/#47. |
| `1.0.0` | Stable release of Core plus Extended MVP. | Accepted C0–C6 and E1–E5, bounded scientific qualification, reproducible public installation and workflows, relevant platform/minor qualification, stable documented API/schema/migration policy, complete exact-candidate delivery gates and published limitations. No unresolved critical defect may contradict that scope. Final release authority and evidence decide readiness, not this table. |

## Accepted boundary for 1.0.0 — 2026-11-05

The requested [Core/Extended reminder](CORE_EXTENDED_COMPARISON.md) lists every
C0–C6 and E1–E5 capability, its actual delivered pieces and remaining boundaries,
and records the maintainer's resulting decision.

The maintainer explicitly selects **Core plus Extended MVP**. Before 1.0.0,
both C0–C6 and E1–E5 must be accepted for the declared scientific profile, together
with public installation, platform/minor qualification, API/record stability and
documented scientific limits. Existing pieces such as `score` and `dock_many`
must be reused and qualified in complete workflows; their presence alone is not
gate acceptance.

In particular, missing clustering/interaction workflows and the independent
reproducibility audit remain pre-1.0 work. General molecular operations belong
to MolSysMT, specialized tools to their providers, and DockingMT owns scientific
orchestration, result interpretation and evidence. Concrete workflow/ownership
review still precedes implementation; accepting this target does not authorize
unbounded speculative frameworks or new scientific experiments.

Intermediate source/public/Core milestones can be released earlier with their
actual scope and limitations. Later advanced engines, receptor flexibility,
large campaigns and peer-guided protocols are not added to 1.0 by this decision.

## A source tag, a GitHub Release and a package are distinct events

Follow the [suite release policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_version_policy.md).
Public release identities and tags are exact `X.Y.Z`, without `v`, `alpha`, `beta`,
`rc` or local-version suffixes. GitHub Release title equals that same version.
Development-derived versions remain truthful development identities.

1. A canonical source/tag-only release can preserve a useful qualified baseline
   while explicitly stating that no package is public. It still has an owning
   release record, exact-candidate gates and a release-specific MolSysSuite notice.
2. The current Conda wrapper runs on GitHub `release: released` or a reviewed
   manual dispatch. A tag push alone does not trigger that wrapper; policy and
   ordinary source CI remain separate. Do not publish a GitHub Release as a
   supposedly harmless source marker and accidentally start an unplanned package
   attempt. Review the concrete route before the event. No wrapper is changed here.
3. A Conda package requires its own exact artifact, version/build/route, installation
   evidence and same-byte public receiving. Its current distribution route is
   Conda `uibcdf`. A source release does not advertise a PyPI route or a compatible
   public molecular minimum.

The first `0.1.0` is therefore a useful **next candidate to prepare**, not a tag
to push immediately. A source-only delivery could precede the first Conda package;
whether to use it is decided in the actual release record. If the public closure
arrives first, the source and package milestones can be consolidated instead.
An archive tag has a different historical purpose and is not this version ladder;
this repository's older policy caller has not adopted the archive-tag capability.

### Development checkpoint tags — review 2026-11-10

The maintainer asks whether useful progress should also have a tag without a
package or GitHub Release. An annotated `archive/<description>` is the suitable
historical marker for a finite development checkpoint. Choose a completed,
reviewable block, record its exact commit, purpose, owning #73 issue, passing
evidence and remaining limits, then keep the marker immutable. Do not add a tag
for every incremental commit. The current 03ed7676 H5MSM 1.0/comparison checkpoint
is a possible preserved commit; no name or tag publication is selected here.

Before the first archive push, adopt policy-v1.5.7 or a compatible newer caller
and change the unconditional policy trigger from `tags: ["*"]` to
`tags: ["**"]`. Inspect publisher/version routes and demonstrate refusal of an
archive identity before registry writes, as the suite release policy requires.
The inspected Conda publisher runs on `release: released` or explicit dispatch,
not tag push. Archive conformance must still execute; a tag is not a route for
silently dispatching the deferred full scientific CI. Prepare its actual event
and validation checkpoint deliberately before publishing it.

This proposal does not create a tag, Release or package, move the fixed private
0.1.0 candidate, select a numeric version, or claim whole-product qualification.
Archive preparation belongs to existing #73; a future canonical X.Y.Z source tag
keeps the distinct exact-candidate and release-notice requirements below.

Preparation is now concrete under [#74](https://github.com/uibcdf/dockingmt/issues/74):
the [0.1.0 candidate dossier](releases/0.1.0.md) fixes source `905abc9`, records
the private version/payload check and separates pending source/closure/gate
receiving from a public tag. Later evidence commits do not move that target.

## First-tag readiness checklist

- Select one clean full source commit, intended `0.1.0` identity, source-only or
  package route, scope and responsible release owner. Preserve every historical
  producer and never retag a published identity.
- Record every applicable required gate, complete immutable inputs, actual
  outcome and reuse/replacement decision before publication. Resolve pending
  exact-head CI; an earlier green head, successful test jobs or a queued coverage
  publisher is not a terminal passing release receipt. This plan waives no gate.
- Verify intended version generation/metadata and tag/parser/title consistency
  using a controlled candidate context. Leave ordinary development metadata and
  source pins unchanged until that candidate is actually prepared.
- For a source-only release, document the exact source dependency composition,
  reproducible supported installation/use route, tested scope and explicit
  absence of a public package. Public dependency minima and unsupported platforms
  stay unqualified. Select the GitHub event/publisher behavior deliberately.
- For a package, select and commit the real staged plan, acquire the exact
  public dependency closure, execute all required native and installed gates,
  build/inspect/stage once, qualify, and promote the same bytes. The current
  administrative example is not that plan.
- Prepare release notes and the release-specific central notice. Source-only
  releases are notified too; update that same notice when packages arrive.
  The maintainer's package-plus-Release availability announcement remains due.
  Other-repository issue work is currently deferred: do not publish a release
  now and silently omit its required handoff. This is a reporting obligation,
  not a new central permission gate.

## Current disposition — 2026-11-05

The [fresh package inventory](validation/data/public_readiness/registry_refresh_2026-11-05.json)
compares complete official package APIs and independent `main` solver indexes.
The previously inspected MolSysMT `0.23.0` Linux and Viewer `0.24.0` build-1
noarch files remain at the highest relevant version with the same hashes.
There is no new artifact covering the missing reader/graph or handle/player
boundary, so repeating their prior failed receiving is not informative.
SMonitor `0.22.1` is newly indexed; its presence alone qualifies neither its
runtime nor DockingMT's full dependency pairing. Public pins/minima remain.

No DockingMT package appears in the three queried `main` indexes; its package API
returns 404. This bounded availability observation is not the all-label,
exact-coordinate absence check required for a real candidate publication.
No new artifact download, environment, install, molecular/native operation,
build, tag, release or upload is performed.

The immediate progression is: retain the accepted Core-plus-Extended target,
receive later checkpoint CI under #28, complete the `0.1.0` source-event decision, and resume
actual public compatibility under #30/#47 only when covering provider bytes are
available. Molecular capabilities remain MolSysMT-owned; visual acceptance stays
deferred until the maintainer resumes it.

The [completed #74 private receiving](validation/data/source_0_1_0_2026-11-05/hosted_receiving.json)
now supplies all intended-version Linux minors 3.11–3.14 across two archive
populations, with the original resource interruptions retained. Candidate
`905abc9` remains fixed; a single-file/public/platform matrix, canonical tag and
required central notice are not inferred. The source event remains pending
under the existing other-repository deferral.
