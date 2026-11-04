# Scientific evidence organization and publication

Owner: [DockingMT #29](https://github.com/uibcdf/dockingmt/issues/29).
Decision: [DMT-044](../DECISIONS.md#dmt-044--publish-evidence-through-a-staged-repository-first-route),
accepted 2026-11-04. This local presentation decision follows existing suite
reporting, disclosure and qualification rules; it creates no shared suite policy.

## Initial route, readers and alternatives

Use this repository's maintained scientific overview and original records as the
initial publication, linked from the root README. GitHub renders Markdown and
provides access to notebooks/archives. A rendered notebook is not proof of a
completed experiment. Cite commit permalinks for frozen claims and `main` links
for navigation to maintained guidance.

| Reader | Question / entry |
| --- | --- |
| Scientist | Which finite recovery/ranking observations exist, with which limits? Start at the [scientific overview](scientific_evidence_overview_2026-11-04.md), then original prescriptions/records. |
| Reproducing user | Which input/composition/choices are needed, and which steps execute work? Follow the installed inspection/preparation/execution/evaluation guides and their actual artifact qualification. |
| Contributor | Is a discrepancy in the adapter, provider, model or reporting? Use owning issues, source/installed guards and retained failures. |
| Release maintainer | Which exact files/platforms are qualified? Use [public readiness](public_candidate_readiness.md) and artifact/native gates; a scientific table or CI badge is not a substitute. |

| Route | Benefit | Cost/limit | Disposition |
| --- | --- | --- | --- |
| Main documentation section now | Familiar user navigation and rendered examples. | This checkout has no documentation site/build; adding one only for evidence introduces infrastructure before a demonstrated need. | Next presentation destination when a user-documentation site exists. |
| Dedicated validation website now | Supports a large searchable or interactive collection. | Adds hosting/build/maintenance and duplicate-evidence risk; current needs do not establish that cost. | Deferred pending a specific reader/scale need and owned implementation proposal. |
| Staged repository-first presentation | Uses existing versioned records and a reproducible overview immediately. | GitHub navigation/rendering has limits; this is not the final user-documentation system. | Selected initial route; later pages consume/link the same records. |

Revisit when a documentation site is introduced, a demonstrated reader task cannot
be completed through this index, or measured archive/collection scale makes Git
storage/navigation unsuitable. Record the task, proposed route and maintenance
cost in an owning issue before introducing infrastructure. No arbitrary case
count, automatic site migration or hosting service is selected.

## Inventory and authoritative relationships

| Material | Current location | Role |
| --- | --- | --- |
| Strategy and scientific claims | `VALIDATION_STRATEGY.md`, audit, scope/model | Questions, admission and limits; not measured outcomes. |
| Case prescription/interpretation | `validation/<case>.md` and owning issue | Declared population, hypotheses, controls, decisions and interpretation. |
| Original producers/observations | Linked scripts/notebooks and `validation/data/<case>/` | Original input bytes, producer identity, outputs, warnings/failures and custody. |
| Software/artifact qualification | `tests/`, `dmt_test_support/`, CI/installed receipts | Correctness/integration evidence; test counts are not independent molecular cases. |
| Derived scientific overview | Dated overview plus frozen-input producer/summary manifest | Reader presentation; never a replacement molecular record or new producer for old outcomes. |
| Performance measurements | [Profiling](workflow_profiling.md), [result export](result_export.md) and their records | Defined time/memory/hardware/composition; not scientific accuracy. |
| Public/visual acceptance | Public readiness and #30/#47, #52/#60 | Actual delivery/interaction gates, separate from private composition and model suitability. |

Derived tables and future rendered pages refer to those sources. Do not duplicate
experiment archives merely to publish them or relabel old producers with a new
documentation commit. Label historical narrative-only evidence when selected
machine-readable receipts are unavailable. Recovering a missing receipt does not
authorize manufacturing replacement bytes.

## Minimum evidence for a new executed question

Retain each applicable item or an explicit unavailable/unassessed disposition:

- Owning issue, intended claim, registered prescription/amendments, original
  input/data origin, attribution, exact bytes/hashes and revision identities.
- Original producer/source changes and actual software/native artifacts and
  dependency composition, distinguished from later receivers or stale versions.
- States, preparation methods/reports, selected atom/frame populations, actual
  correspondence/export maps and allowed losses. Molecular operations stay in
  MolSysMT or the specialized provider; missing tools get provider feedback.
- Backend/score definitions, submitted inputs/box/settings, seed, CPU/hardware,
  requested/returned counts and resource/retention ownership.
- Metric, units, cutoff, frame/alignment/symmetry, reference identity and continuous
  observations; distinguish returned-set recovery from ordering.
- Selected/admitted/attempted/completed/returned/evaluated denominators, every
  failure/partial result, adverse controls and within-case repetitions.
- Original warnings, unknowns and limits; scientific validity, software/artifact
  qualification and performance observations classified separately.
- Reproduction instructions that identify record reading, molecular measurement,
  preparation and native execution as different operations.

Complexes, seeds, poses and repeated evaluations are different analysis units.
Do not pool incompatible criteria or strip evidence to pass the conservative
`summarize_redocking` policy. Juxtaposed tables can retain distinct populations
without claiming a pooled recovery probability, affinity or physical validity.

## Maintenance, reruns and retention

The contributor changing a case maintains its record/interpretation and affected
presentation; the owning issue carries unresolved work. DockingMT maintainers
review claims/composition, and the release maintainer owns separate delivery gates.
No new permanent benchmark-service role is created.

Before changing a source or summary, inspect original producer/input identities
and applicable controls. Preserve frozen observations; append dated corrections
or separately attributed receiving/run records. A corrected defect does not erase
the original failed population. Regenerate affected derived outputs and check
their exact source hashes. The current overview uses its case-specific
`build_summary.py --check`; unrelated guide edits do not require a new campaign.

Routine pushes do not automatically rerun stochastic/scientific experiments.
Rerun for a concrete changed backend, molecular contract, hypothesis or suspected
regression that needs informative evidence, after registering a new population,
budget and failure policy. Historical results remain historical when versions
advance. Existing suite CI/full-matrix/release cadence retains separate authority.

Keep the bounded current text/notebooks/compressed records in Git. If actual
size, sensitivity or availability needs outgrow it, propose an owned immutable
external store; retain repository manifests, exact digests, attribution, custody
and independently verified access. This decision selects no storage vendor,
relocation or DOI. Publish only authorized content/sanitized dispositions; local
logs/environments and public molecular evidence can have different disclosure.

Review resources at declared custody checkpoints. Cache cleanup must preserve
evidence still needed for reproduction/diagnosis. Archive resolved reports under
the existing reporting protocol. This publication decision closes no linked
scientific, provider, visual or public-distribution qualification task.
