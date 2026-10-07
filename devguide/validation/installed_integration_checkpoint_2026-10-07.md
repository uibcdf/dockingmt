# Installed consumer and hosted integration checkpoint — 2026-10-07

Owners: [#30](https://github.com/uibcdf/dockingmt/issues/30) (Python and installed
delivery), [#21](https://github.com/uibcdf/dockingmt/issues/21) (recurring CI),
[#42](https://github.com/uibcdf/dockingmt/issues/42) (chemical-history qualification),
[#45](https://github.com/uibcdf/dockingmt/issues/45) (declared marker) and
[#46](https://github.com/uibcdf/dockingmt/issues/46) (portable evaluation guard).

## Exact producers and artifacts

| Producer | Ordinary wheel | SHA-256 | Declared typing marker |
| --- | --- | --- | --- |
| `365668e30f5f519adf4abc5c5e5e387d50af00a1` | `dockingmt-0.0.0+131.g365668e-py3-none-any.whl` | `7a0c0dbefb6e134f20e3e9b8a4a56442114a13f45d94fd0557cf54a7ed0eb374` | Missing |
| `8741fb2e104814e6f1012e0cb7073689e710f982` | `dockingmt-0.0.0+132.g8741fb2-py3-none-any.whl` | `12f2ac10e0b6c44d2b1da8e9f3e100c394596897f0c1924d23a210fe82a8e1a6` | Present; installed bytes verified |

Each file was built once from its own separate clone with normal versioningit
and Python 3.14.7, using `python -m pip wheel --no-deps --no-build-isolation`.
Setuptools 84.0.0, wheel 0.48.0 and versioningit 3.3.0 were the existing build
tools. Ordinary installation used `pip install --no-deps WHEEL`; no Python
metadata override was used. The original file remains distinct from the corrected
producer's file. Files remain locally at
`/tmp/dockingmt-installed-PRODUCER-wheels/` under their abbreviated producer IDs;
they were not published to a package registry.

The [machine-readable checkpoint](data/installed_integration/checkpoint_2026-10-07.json)
records the exact payload and loaded-module inventories, JUnit digest, actual
dependency origins and native executed-step evidence. The corrected installed
consumer passes **986 tests, no failures or skips, in 366.95 seconds**, with 383
warning occurrences. All 64 inspected wheel members match installed bytes and
all 56 loaded consumer/addon modules resolve within the installed prefix.

The corrected artifact's consumer version matches distribution metadata;
its `Requires-Python` is parsed as `>=3.11,<3.15`. Installed payload members
match the corresponding wheel bytes, excluding the install-generated `RECORD`.
The declared `dockingmt/py.typed` marker is present. The single
`molsysviewer.addons` entry named `dockingmt` loads the installed addon module.
The marker is a resource-delivery assertion, not a claim of complete annotations.

## Installed execution boundary

The consumer and addon are ordinarily installed into a temporary virtual
environment. It inherits dependencies from `molsyssuite@uibcdf_3.14`; the
corrected checkpoint also installs Pandas 3.0.6 into that temporary prefix.
The full source test selection is copied with its fixtures, guide records,
configuration and developer helpers into a temporary harness. Both production
package directories are omitted. Git metadata identifies the producer for
development benchmark helpers, while its deliberately removed source directories
make that harness dirty. Those benchmark source hashes describe the harness;
the artifact receipt supplies installed-package identity.

Scientific tests execute from `/tmp` through the existing MolSysSuite
`devtools/scripts/installed_noarch.py::run_tests` operation. Its before/after
hooks require every loaded DockingMT module to come from the installed prefix.
The invocation uses `--import-mode=importlib`, `-o pythonpath=` to clear the
checkout's pytest source insertion, and `PYTHONSAFEPATH=1` for subprocesses.
`PYTHONPATH` supplies only the reviewed sibling archives and the source-free
harness, its tests and its developer-helper directory. The latter two paths
support existing bare test-helper and reporting imports. A final inventory also
checks every loaded addon module against the installed prefix.

Sibling sources remain exactly MolSysMT
`5bd893c85fe8d211663b2b1f865f5f1d2c382a90`, released ArgDigest 0.15.0
`1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e` and the reviewed Python 3.14
MolSysViewer `ec4c71e574d798b7c8675b7e7e983da878ce9889`. MolSysMT's preserved
`_rust.abi3.so` SHA-256 is
`c535c7d2f0e2a92b6ebf8298a60b19e4b5555467b4aa087e9563c6760619827e`;
this does not provide fresh native-build provenance. Other dependencies retain
their ambient installed/editable origins, including PyUnitWizard and Pytest
Receptor. This is installed-consumer evidence with a local dependency profile,
not clean public-channel dependency closure or exact Conda-artifact qualification.
Sibling runtime version strings can reflect inherited distribution metadata;
the reviewed source commits and earlier source-profile hashes identify the
exercised source. The receipt preserves those strings without using them to
authenticate a source revision.

## Failures retained and corrections bounded

- The original wheel lacks the declared resource (#45).
- Initial harness collection has 12 errors because existing bare test imports
  need the copied test directory. Adding that directory does not expose consumer
  source. The first complete original-wheel run passes 982 tests and fails three
  harness tests: two helpers need Git metadata and the reporting subprocess needs
  its helper directory under safe-path execution. After supplying those harness
  prerequisites, the same three tests pass in 10.93 seconds. This is combined
  evidence, not a single green 985-test run.
- [Original exact-head CI](https://github.com/uibcdf/dockingmt/actions/runs/37580554662)
  passes 984 tests and fails one H5MSM snapshot assertion on each required Linux
  minor. A Pandas 3.0.6 reproduction finds only two `str` to `string` changes in
  component text-column dtype labels. Values, null masks and all other state/history
  fields remain exact. The guard accepts those measured text labels while preserving
  full value/history equality. The corrected chemical-template selection passes
  all 15 tests with Pandas 3.0.6 in 37.56 seconds; local Pandas 2.3.3 coverage also
  passes (16 tests in 33.87 seconds during an exploratory parametrization).
- [Historical macOS matrix](https://github.com/uibcdf/dockingmt/actions/runs/37491745012)
  has one false first-pose recovery expectation and 886 passing tests in each
  representative arm64 lane. #46 now independently verifies live positional RMSDs
  from actual returned coordinates. It retains captured-input checks, the 2.5
  angstrom cutoff and the displaced-domain negative control. A separate guard
  preserves the historical positive observations. The corrected evaluation/reporting
  selection passes 46 tests in 65.73 seconds; production algorithms and search
  parameters are unchanged.
- Forcing nondefault legacy string inference in Pandas 3 exposes a different
  reader error, reported in [MolSysMT #349](https://github.com/uibcdf/molsysmt/issues/349).
  The current accepted workflow uses Pandas defaults; no reader workaround or
  sibling edit is introduced.

## Hosted recovery and remaining qualification

[Original manual matrix](https://github.com/uibcdf/dockingmt/actions/runs/37580610601)
executes and fails all four Linux cells at the same snapshot assertion. Its macOS
jobs have not started when the obsolete run is cancelled in favor of the corrected
producer. Cancelled or unexecuted cells are not passing evidence.

The corrected producer's [required CI](https://github.com/uibcdf/dockingmt/actions/runs/37581673369),
[suite policy](https://github.com/uibcdf/dockingmt/actions/runs/37581674154) and
[six-cell manual matrix](https://github.com/uibcdf/dockingmt/actions/runs/37581760344)
provide separate source integration, isolated ordinary-installed import and
administrative evidence. Full pytest in the existing hosted workflows runs from
the checkout and is not asserted to use installed consumer code throughout.
The separate local installed guard establishes that consumer boundary.

Required CI completes successfully on the corrected producer: quality plus
**986 tests without skips on each of Python 3.11, 3.12, 3.13 and 3.14**. All
ordinary-install and isolated metadata/import steps execute successfully.
These hosted shallow-checkout builds report version `0.0.0`; they are separate
files from the fully identified local wheel. The manual matrix also passes all
four Linux cells. Its macOS arm64 Python 3.13/3.14 jobs remain `pending`, with
no runner assigned and no explanatory GitHub annotation at inspection. Their
completion is still required under #46/#30; the whole six-cell run is not green.

Manual execution of the existing backlog detector recognizes corrected required
CI as the four-minor recovery watermark and finds zero skipped commits since
`8741fb2e104814e6f1012e0cb7073689e710f982`. This does not establish a scheduled
daily trigger or clear pending macOS qualification. #21 remains open for its
remaining acceptance conditions.

### Completion of queued macOS cells — 2026-10-07, 06:57 UTC

The same [manual matrix](https://github.com/uibcdf/dockingmt/actions/runs/37581760344)
finishes green on the original corrected producer `8741fb2`: all six scientific
cells actually execute 986 tests without skips. macOS arm64 Python 3.13 passes
in 197.41 s and Python 3.14 in 188.14 s, with 382 warnings each. The interpreter,
architecture, Vina 1.2.7 and ordinary installed-import checks also execute. The
administrative backlog detector is skipped by design for this manual dispatch;
it is not one of the six scientific gates. #46 is now resolved and archived.

The receipt appends completion evidence without replacing its earlier pending
observations. [Evidence-head CI](https://github.com/uibcdf/dockingmt/actions/runs/37582910814)
also passes quality and all 986 tests per required Linux minor at `7ac138b`.
Both original local wheels have exact byte copies under the ignored local
`dist/qualification/2026-10-07/` directory; their original identities and
SHA-256s are preserved. No new file is built to reinterpret either producer.

The inherited environment's `pip check` remains red for unrelated AmberTools
packages: missing `pdb2pqr` and incompatible NumPy/Biopython bounds. It is not a
clean dependency solve. Public package availability, installed Conda bytes on every
claimed cell, provider native-build provenance and suite admission remain owned
by #30. None of these internal results authorizes a public support claim or upload.
