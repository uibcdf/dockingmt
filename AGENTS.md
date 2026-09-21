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

## Language and scope

Use English in code, documentation, issues and commits. Keep changes focused, test
user-visible behavior, preserve human work and never commit secrets.

Do not overdesign: the existence of a concept in `devguide/` does not authorize code
until a concrete accepted workflow requires it.

## Local gates

Run these before committing:

```bash
ruff check .
ruff format --check .
pytest --receptor=llm
```

Use `pytest-receptor` (`--receptor=llm` locally) for compact test reports, and
`gh-run-receptor` (`gh run-receptor inspect RUN_ID --receptor=llm`) to inspect
remote workflow runs.

Routine development uses Python 3.13; the supported user range is Python 3.11 to 3.13.
