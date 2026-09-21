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
Conda test job is such a dependency-driven variation: it installs the fixed MolSysMT
0.21.0 source because the channel lacks a Python 3.13 build. Replacing that fallback with
a common sibling-dependency mechanism is tracked by `uibcdf/molsyssuite#31`.

## Local gates

Run these before committing:

```bash
ruff check .
ruff format --check .
pytest --receptor=llm
python devtools/devguide_index.py --check
```

Use `pytest-receptor` (`--receptor=llm` locally) for compact test reports, and
`gh-run-receptor` (`gh run-receptor inspect RUN_ID --receptor=llm`) to inspect
remote workflow runs.

Routine development uses Python 3.13; the supported user range is Python 3.11 to 3.13.

## External tooling guides

The synchronized root guides are read-only copies owned by their named repositories.
Read the guide for every shared tool touched by a change:

- `SMONITOR_GUIDE.md`
- `DEPDIGEST_GUIDE.md`
- `ARGDIGEST_GUIDE.md`
- `PYUNITWIZARD_GUIDE.md`
- `GH_RUN_RECEPTOR_GUIDE.md`
