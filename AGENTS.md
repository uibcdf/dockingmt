# DockingMT contributor instructions

Read [`MOLSYSSUITE_GUIDE.md`](MOLSYSSUITE_GUIDE.md) before making changes. It routes
suite-wide policy, compatibility, tooling and cross-component proposals to
`uibcdf/molsyssuite` while this repository remains authoritative for its implementation
and product behavior. That file is a synchronized, read-only copy: propose changes at its
canonical source, never in this repository.

## MolSysSuite membership

DockingMT is a native MolSysSuite scientific component, providing the molecular docking
layer of the suite.

Keep DockingMT-specific implementation, tests, releases and product issues here. Report
suite-wide rules, shared tooling problems and cross-repository proposals in
`uibcdf/molsyssuite`. When work here exposes a limitation in a sibling component, file the
evidence in that provider component and cross-link it, as
[`cross_component_feedback.md`](https://github.com/uibcdf/molsyssuite/blob/main/devguide/cross_component_feedback.md)
requires.

`devguide/` contains the frozen architectural and scientific seed of DockingMT. Treat
those documents as the living design authority.

`GH_RUN_RECEPTOR_GUIDE.md` is the synchronized copy of the guide governing
GitHub Actions inspection. Propose changes at its canonical source repository.

Before filing or closing durable local work, read `devguide/reporting_protocol.md`.
Open the owning issue first, regenerate report indexes, synchronize GitHub state and
archive resolved records instead of deleting them.

## Language and scope

Use English in code, documentation, issues and commits. Keep changes focused, test
user-visible behavior, preserve human work and never commit secrets.

Do not overdesign: the existence of a concept in `devguide/` does not authorize code
until a concrete accepted workflow requires it.

Start CI and maintenance workflows from the current MolSysSuite starter-kit patterns.
Keep a local variation only when DockingMT has a measured need, document that reason and
link its removal condition. If the variation could help sibling components, propose it
in `uibcdf/molsyssuite` instead of letting repositories drift independently. The current
Conda test job is such a dependency-driven variation: it installs exact compatible
ArgDigest, MolSysMT and MolSysViewer source commits because the channel lacks Python 3.13
builds for the integrated set and the published ArgDigest/MolSysMT generations are not
mutually compatible. Replacing that fallback with a common sibling-dependency mechanism
is tracked by `uibcdf/molsyssuite#31`.

## Local gates

Choose local gates before committing by the changed code, inputs and scope:

- Documentation, instructions and evidence require applicable reporting/index,
  link and synchronized-guide checks; prose changes alone do not require the
  scientific suite.
- Executable behavior, dependency, metadata, packaging and integration changes
  require relevant code/contract tests and applicable lint, format and local
  type checks. Broaden validation when the affected boundary requires it.
- Scientific exploration requires informative hypothesis cases and explicit
  limits; an administrative check does not establish scientific equivalence.

Available commands (select applicable checks and test scope):

```bash
ruff check .
ruff format --check .
pytest --receptor=llm
python devtools/devguide_index.py --check
```

Use `pytest-receptor` (`--receptor=llm` locally) for compact test reports, and
`gh-run-receptor` (`gh run-receptor inspect RUN_ID --receptor=llm`) to inspect
remote workflow runs.

Routine development uses the Conda environment `molsyssuite@uibcdf_3.14`
(Python 3.14); the required source range is Python 3.11 to 3.14.
Install this checkout in that environment with `python -m pip install --no-deps
--editable .`, and run the local gates with its interpreter and tools.

## External tooling guides

The synchronized root guides are read-only copies owned by their named repositories.
Read the guide for every shared tool touched by a change:

- `SMONITOR_GUIDE.md`
- `DEPDIGEST_GUIDE.md`
- `ARGDIGEST_GUIDE.md`
- `PYUNITWIZARD_GUIDE.md`
- `PYTEST_RECEPTOR_GUIDE.md`
- `GH_RUN_RECEPTOR_GUIDE.md`

## Direct pushes and scoped local validation

Follow [the common checkpoint policy](MOLSYSSUITE_GUIDE.md#direct-pushes-and-validation-checkpoints)
for authorized internal direct pushes by `dprada` and `LMMV`. Batch focused local
commits when remote visibility is unnecessary; a permitted interim CI skip is
conditional, never the default after every locally checked change. Retain local
results while tested code, inputs, environment and scope remain applicable.
Normally finish with an unskipped head and inspect its applicable CI, or explicitly
execute and verify those exact-head gates manually. Record missing evidence,
untested scope, owning issue and recovery route; administrative checks do not
clear full-suite backlog. External PRs, admission and publication require all
mandatory executed gates for the exact candidate and required installed file.
An authorized manual qualification retains the original producer and artifact
bytes/digest; a marker alone neither waives a gate nor disqualifies that evidence.

## Modular reusable tools

Before adding a feature, inspect existing tools and identify the owning module or
component. Implement or extend independently useful operations as documented reusable
tools in that owner, with their own contracts and tests; have consumers call them.
Keep task-specific decisions local and report missing sibling capabilities to the
provider with linked consumer evidence. Follow
[MOLSYSSUITE_GUIDE.md#modular-reusable-tools](MOLSYSSUITE_GUIDE.md#modular-reusable-tools)
for applicability, compatibility, performance and tracked exceptions.

## Durable working instructions

Keep technical findings in owning issues, fixes, tests and maintained guidance.
Place only accepted lasting contributor actions in root or appropriately scoped
instructions, following
[the common policy](MOLSYSSUITE_GUIDE.md#durable-working-instructions).
For work under `devguide/`, also read [devguide/AGENTS.md](devguide/AGENTS.md)
and its local reporting protocol. Shared instruction proposals belong in
`uibcdf/molsyssuite`; cross-MOLI contracts belong in `uibcdf/moli`.


## Required Python support

The required source contract is Python 3.11–3.14; routine development uses
`molsyssuite@uibcdf_3.14`. Qualification and public delivery are tracked in
`uibcdf/dockingmt#30`.
Keep metadata, recipe, required CI and recovery evidence aligned. Normal
installed evidence must not bypass `Requires-Python`; public support claims
remain tied to the suite's recorded admission.
