# Provider compatibility checkpoint — 2026-10-13

Owner: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49).
[Prospective registration](https://github.com/uibcdf/dockingmt/issues/49#issuecomment-6141557097)
binds the candidate composition before tests or consumer adoption.

## Composition and executed boundary

Consumer source: `1acab23cb81f28a4ff5c4441045b823ad20d5b31`.

| Provider | Candidate commit | Installed version |
| --- | --- | --- |
| MolSysMT | `a462b49c5566e8de993f83825576dc3860e9cfb1` | `0.23.0+65.ga462b49c5` |
| ArgDigest | `3d1ec53c374098016452abab74706e9d80df5462` | `0.15.0+5.g3d1ec53` |
| MolSysViewer | `a61b75bc994e3ad674c3e7eafe53bb6b2a989c5f` | `0.24.0+76.ga61b75bc` |

The shared MolSysSuite environment operation creates a task-owned Python 3.14.8
Conda prefix from the declared test manifest. Independent detached Git source
copies are installed with normal `pip install --no-deps` directory builds and
ordinary build isolation. MolSysMT's Rust extension is compiled from the candidate;
its installed SHA-256 is
`feb001379201b92690eadf04fd0be6b710cdfe50bad240feba26cf666e19b41b`.
DockingMT is editable only in this task prefix. There is no scientific source
overlay, copied old native binary or sibling branch update.

The immutable dependency SDK `738fe8dd731abb99dac421b0bb2acc8564110180`
verifies each provider's clean clone, HTTPS origin, commit, installed version and
PEP 610 directory origin. Imports resolve to the candidate prefix. These checks
establish source composition; scientific tests remain separate.

All 251 Conda packages originate from the two declared channels: 245 from
conda-forge and six from uibcdf. Conda nevertheless considered an additional
ambient channel. This nonblocking shared-tool observation is reported in
[MolSysSuite #108](https://github.com/uibcdf/molsyssuite/issues/108#issuecomment-6141735585).
The Vina Conda record omits setuptools and wheel although its Python metadata
requires them. Installing those declared requirements in the task prefix completes
`pip check`. The receipt records this augmentation; the manifest alone is not a
claim of complete Python dependency closure. PyUnitWizard 0.28.1, Vina 1.2.7,
NumPy 2.5.4 and pandas 3.0.6 are actual installed dependencies.

## Consumer and scientific compatibility

The focused selection passes **270 tests, zero skips, 330.62 seconds**. It covers
molecular composition and source-free conversion, native prepared serialization,
named/required charges and typing, explicit torsions and fragments, templates and
chemical readiness, native formats, Viewer reconstruction, 181L preparations,
1IEP flexibility, 5X72 occupancy and 3PTB admission/saved-pose geometry.

All 167 saved 3PTB poses are reevaluated with no new search, preparation or native
scoring inside the receiving test. Both ordinary and nondefault pm/fs policies are
exercised. Original search/admission/evaluation archives and producers retain their
bytes, including the original 24 reporting failures and later receiving correction.
This checkpoint does not replace their scientific producer identity.

A separate receiving admission repeats the declared molecular workflow without
scoring or search. Coordinates, full-source atom maps, native parser admission,
boxes and containment match the original. Entire PDBQT digests differ: the first
two provenance remarks record the candidate MolSysMT version. Parsed remark records
are otherwise exactly equal; every subsequent line, including all engine atoms,
charges, types and torsion records, is identical. The 24 population rows differ only
in the two input digests bound to those truthful version remarks. Both old and new
digests remain in the comparison; neither is substituted into the original archive.

The selected run retains 704 warnings: 587 pandas deprecations, 82 off-axis
attribute warnings, 29 legacy H5MSM warnings and six explicit atom-expansion
attribute-loss warnings. A minimal public two-system merge reproduces eight pandas
warnings while preserving 44 output atoms. Provider improvement is reported in
[MolSysMT #386](https://github.com/uibcdf/molsysmt/issues/386); DockingMT adds no
warning filter or molecular merger.

## Local decision before hosted qualification

The complete local run executes all 1,125 cases: **1,124 pass and one fails in
815.81 seconds**, with 844 retained warnings. Its sole failure is the governance
guard's literal assertion of the old source pins after the candidate route change.
The guard now reads declared checkout inputs from the maintained inventory;
the existing independent workflow/context mutation tests still reject pin drift.
All six governance/reporting cases pass on rerun. This is combined local evidence,
not a single green full-suite run. No scientific implementation changed after the
passing functional cases. The final four-minor hosted matrix must provide the
complete successful exact-head checkpoint.

The initial 24 distribution/coverage/reporting controls pass (2.89 seconds);
the final 29-case selection includes governance and passes (2.77 seconds). Ruff
lint/format, declared and installed-context preflight, reporting/index and
synchronized-guide checks qualify the changed administrative scope.

Adopt the three exact candidate source revisions in the required and recurring
source workflows and dependency inventory. Both existing Viewer contexts now
select the same source; their identifiers and conditional routing remain intact.
The environment explicitly supplies Vina's declared setuptools/wheel requirements.
The shared source-dependency mechanism remains tracked by MolSysSuite #31.
Required interpreter matrices, scientific commands and public publication routes
retain their contracts. Before considering this adoption qualified, inspect the
unskipped exact-head CI and its measured coverage upload.

Evidence: [qualification receipt](data/provider_compatibility/qualification_2026-10-13.json),
[receiving admission](data/provider_compatibility/admission_2026-10-13.json.gz),
[comparison producer](data/provider_compatibility/receiving_comparison_2026-10-13.py.txt),
[full local result](data/provider_compatibility/full_suite_2026-10-13.txt),
[corrected governance result](data/provider_compatibility/governance_correction_2026-10-13.txt)
and [environment](data/provider_compatibility/environment_2026-10-13.txt).
The receiving admission has no fabricated historical producer field; its current
import/source/native identity is bound by the separate receipt.

DepDigest's guide is synchronized without local content changes from canonical
`1b746ece24587e920e49ea20f2bfebde7c3efc24`. SMonitor's current remote guide at
`020b6bf7012281efae9a1a16ddec11cdcd49c1fd` already matches this repository; its
older local provider clone is excluded as a synchronization authority. Guide
synchronization does not adopt DepDigest's new optional DeclaredRegistry API.

All task installs target the temporary prefix. A before/after routine-environment
freeze comparison detects concurrent editable Git-head changes in PharmacophoreMT
and Sabueso; other rows match at that observation. This task does not mutate those
checkouts or the routine prefix, and makes no whole-global-environment closure claim.

General projection, export maps, native multi-pose/permutation and symmetry remain
owned by the existing MolSysMT issues. A passing current composition does not prove
those proposals delivered or establish scientific model/scoring validity. Public
installed pair/channel qualification stays under [#30](https://github.com/uibcdf/dockingmt/issues/30)
and [#47](https://github.com/uibcdf/dockingmt/issues/47). A source checkout and compiled
provider wheel are distinct from an admitted public Conda artifact.

The next human workflow must execute through Python/Jupyter from an ordinary
installed distribution with recorded imports, units, preparations, captured backend
inputs and replayed outputs. The general vertical-pilot principle is human
orchestration before agent orchestration; this public checkpoint includes no private
scientific pilot content.


## Source-history correction before CI admission

The first published source candidate `a7f753a` starts CI
[38374178868](https://github.com/uibcdf/dockingmt/actions/runs/38374178868).
A receiving versioning probe of the exact ArgDigest source shows that its shallow
Git checkout produces `0.0.0`, while the full source clone produces
`0.15.0+5.g3d1ec53`. The former violates MolSysMT's declared ArgDigest >=0.13.0
requirement. Scientific tests and direct consumer floor checks do not establish
transitive installed-metadata compatibility. This run is superseded before
admission; successful preliminary quality/governance gates stay bounded evidence.

Both source workflows now fetch complete history for each scientific provider and
execute `python -m pip check` before source tests. The existing declared-route
control also checks full-history checkout inputs and dependency-check ordering.
Exact source commits, scientific code, matrices and commands are unchanged. The
[correction receipt](data/provider_compatibility/ci_history_correction_2026-10-13.json)
and [version reproduction](data/provider_compatibility/shallow_version_2026-10-13.txt)
preserve the observed failure. The corrected unskipped head requires fresh complete
CI, including its installed dependency check, before source adoption is qualified.
The reusable sibling-source mechanism and this versioning requirement belong to
[MolSysSuite #31](https://github.com/uibcdf/molsyssuite/issues/31).


## Terminal source qualification — 2026-10-13

The corrected source adoption is qualified at
`06e2d84b92b6c44caa1108d5ef2cfcccc6b16d4e` by
[CI 38375329396](https://github.com/uibcdf/dockingmt/actions/runs/38375329396),
attempt 1: all seven jobs succeed. Every Linux Python 3.11–3.14 cell executes
**1,125 tests without skips**, with independent installed source/context
verification, ordinary installed consumer import and `pip check` before science.
The real three provider versions match the normally installed local composition.
Python 3.11 uses NumPy 2.4.6; the other three use 2.5.4.

[Policy 38375330236](https://github.com/uibcdf/dockingmt/actions/runs/38375330236)
and [publication governance 38375330332](https://github.com/uibcdf/dockingmt/actions/runs/38375330332)
also pass on that exact head. Native run/attempt/job/step facts and full logs are
preserved in the [terminal receipt](data/provider_compatibility/terminal_2026-10-13.json).
The measured Python 3.14 artifact is downloaded and its single report uploaded:
37,197 compressed bytes, followed by `Upload queued for processing complete`.
This establishes actual upload; subsequent Codecov processing is separate.

This fulfills the source checkpoint required above. The initial local old-pin
failure and cancelled first CI remain diagnostic records. The ordinary installed
consumer import in CI does not replace a source-free scientific receiving test or
public Conda file/pair admission. DockingMT #49 remains partial for missing provider
operations; #30/#47 retain installed/public qualification scope. Original 3PTB
producer/archive bytes and the no-new-search boundary remain unchanged.
