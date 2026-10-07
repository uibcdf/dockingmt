# DockingMT development controls

Owner: uibcdf/dockingmt#47; suite distribution coordination: uibcdf/molsyssuite#45.
Scientific source tests and release decisions stay with DockingMT.

## Dependency routes and immutable scientific clones

`check_dependency_routes.py` is a thin loader for the accepted shared source SDK
`738fe8dd731abb99dac421b0bb2acc8564110180` (uibcdf/molsyssuite#109). It checks
SDK identity/cleanliness and actual import origin before calling the provider.
Use `.molsyssuite/sdk` or explicitly set `DOCKINGMT_SUITE_ROOT` to that clean
immutable clone. Parser tools are administrative dependencies; the science jobs
put them in `.molsyssuite-tools`, which is used only in the preflight process.

```bash
python devtools/check_dependency_routes.py --declared-only
python devtools/check_dependency_routes.py --context ci-3.14 \
  --source-root argdigest-source=.molsyssuite/argdigest \
  --source-root molsysmt-source=.molsyssuite/molsysmt \
  --source-root viewer-py314=.molsyssuite/molsysviewer
```

The first command reviews nine declarations and makes no installed claim.
The second runs in the actual resolved Python 3.14 interpreter after installing
the original normal directory sources. For older supported minors use their
`ci-3.MINOR` context and `viewer-base` binding. Exactly the three selected source
IDs/roots are required; the SDK checks Git root/origin/full commit/cleanliness,
normal PEP610 directory origin and actual required versions. Editable origins,
wrong/dirty clones and missing/extra bindings fail. Source provenance does not
prove public dependency closure or scientific compatibility.

`dependency_routes.toml` owns one new recipe, the unchanged test environment,
seven workflows, four original source records and four Python contexts. ArgDigest
and MolSysMT supply omitted runtime requirements; Viewer is an optional integration
provider, with its original lane-specific pins. Existing source installs, test
commands, matrix, schedules and skipped-commit recovery remain unchanged. Current
metadata owns public requirements; compatible bootstrap floors are not invented
as new scientific API minima.

When a route changes, review its actual inputs/commands/conditions and update its
inventory hash deliberately. The provider does not interpret arbitrary shell;
consumer tests additionally compare actual checkout selections with contexts.
Do not refresh hashes automatically to silence drift.

## Local administrative checks

Use the qualified `molsyssuite@uibcdf_3.14` environment and the accepted SDK:

```bash
python devtools/devguide_index.py --check
python devtools/check_dependency_routes.py --declared-only
python -m pytest --receptor=llm -o addopts= devtools/tests/test_distribution_contract.py tests/test_reporting_protocol.py
ruff check .
ruff format --check .
```

These checks import no scientific component. A separate Python 3.14 CI job runs
them independently of the existing scientific jobs. Their passing result clears
neither scientific backlog nor candidate publication gates. The common provider
owns reusable operations/negative guards; this repository owns source bindings,
packaging selection and candidate/installed profiles.

See [the Conda route](conda-build/README.md) for release preparation. Temporary
fixture directories use managed cleanup; retain evidence while needed and remove
obsolete owner resources, preserving active/dirty work.

## Annotated source identity correction — 2026-10-07

First CI 37595722752 correctly rejects the ArgDigest input as the expected HEAD:
original immutable checkout ref 1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e is an
annotated tag object, pointing to commit 57447cc4ec1f7ce85078f8a939892efd075bc919.
Its source directory actually has that commit as HEAD. The SDK requires the
commit; the owner inventory now records that actual commit and separately keeps
checkout_ref as owner-only original input. Existing checkout commands/pins are
unchanged. Consumer guards bind original checkout_ref to workflow inputs; the SDK
checks actual HEAD/origin/installed directory. A real annotated-tag fixture
rejects the tag as HEAD and accepts its exact target. No tag or scientific source
is altered, and no publication policy permits tag-object substitution for a
producer commit. The first failure and corrected hosted evidence remain separate.
