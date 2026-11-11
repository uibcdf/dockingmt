# bindingmt developer-guide instructions

Read `../AGENTS.md`, `reporting_protocol.md` and
[the common working-instruction policy](../MOLSYSSUITE_GUIDE.md#durable-working-instructions).
The common MolSysSuite layer required by the root `AGENTS.md` retains precedence;
this file refines only local rules within its directory.

For this repository's report lifecycle, use the actual paths and commands in
`reporting_protocol.md`. Regenerate local indexes with
`python devtools/devguide_index.py`, then verify them with `--check`.

For each implementation or qualification increment, update its owning contract/
report and the applicable current checkpoint in `ROADMAP.md`,
`PRE_STABILIZATION_PLAN.md` and `MACHINE_HANDOFF.md`. Keep the resumption route
in `README.md`/`DOCUMENT_MAP.md` accurate when ownership or paths change. State
implemented versus received behavior, exact source/artifact evidence, applicable
checks and missing remote evidence, unresolved limits, and the next concrete
action. Retain resource/custody information when needed. A fresh contributor
must be able to resume from these files without recovering the conversation.

For scientific/performance evidence and its presentation, follow
[BMT-044](DECISIONS.md#bmt-044--publish-evidence-through-a-staged-repository-first-route)
and [the local evidence publication policy](validation/evidence_publication_policy.md).
When changing the scientific overview or its declared inputs, regenerate its
derived outputs and run the documented `build_summary.py --check`. Keep frozen
observations/producers intact and record new calculations as separate populations;
unrelated guide edits do not require a scientific rerun.
