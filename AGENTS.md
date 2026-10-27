# DockingMT contributor instructions

## Mandatory MolSysSuite instructions

Read and follow `MOLSYSSUITE_GUIDE.md` before working in this repository.

Within their stated scope, its common rules take precedence over this file
and any nested `AGENTS.md`. Local instructions may refine them; deviations
require the documented policy exception process.

The synchronized guide is owned by `uibcdf/molsyssuite`. It includes the
[reusable-tool ownership rules](MOLSYSSUITE_GUIDE.md#modular-reusable-tools)
and [working-instruction rules](MOLSYSSUITE_GUIDE.md#durable-working-instructions).
For work under `devguide/`, also read `devguide/AGENTS.md` and its local
reporting protocol. Keep repository-specific instructions below.

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

## Component qualification

Track this member's source qualification and public-delivery evidence in
`uibcdf/dockingmt#30`. The common Python/support
requirements and actual component metadata retain their separate authority.
