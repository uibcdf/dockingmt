# dockingmt developer-guide instructions

Read `../AGENTS.md`, `reporting_protocol.md` and
[the common working-instruction policy](../MOLSYSSUITE_GUIDE.md#durable-working-instructions).
The common MolSysSuite layer required by the root `AGENTS.md` retains precedence;
this file refines only local rules within its directory.

For this repository's report lifecycle, use the actual paths and commands in
`reporting_protocol.md`. Regenerate local indexes with
`python devtools/devguide_index.py`, then verify them with `--check`.

For scientific/performance evidence and its presentation, follow
[DMT-044](DECISIONS.md#dmt-044--publish-evidence-through-a-staged-repository-first-route)
and [the local evidence publication policy](validation/evidence_publication_policy.md).
When changing the scientific overview or its declared inputs, regenerate its
derived outputs and run the documented `build_summary.py --check`. Keep frozen
observations/producers intact and record new calculations as separate populations;
unrelated guide edits do not require a scientific rerun.
