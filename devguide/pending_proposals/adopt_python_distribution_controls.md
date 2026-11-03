---
summary: Adopt distribution controls and the agreed first noarch Conda route.
issue: uibcdf/dockingmt#47
status: partial
opened: 2026-10-07
closed:
verification: measured
area: [governance, distribution, compatibility]
guard: devtools/tests/test_distribution_contract.py
normative:
blocked_by: []
supersedes: []
---

# Distribution control adoption

## PEP 639 metadata migration in qualification — 2026-11-03

The maintainer accepts the local migration under MolSysSuite #162. The MIT
expression and explicit `LICENSE` replace the deprecated table/classifier;
Setuptools >=77.0.3 is aligned across build metadata, recipe, test bootstrap and
administrative CI. The dependency inventory reclassifies the changed CI tooling
floor; scientific pins/steps and runtime dependencies retain their authority.
All 24 administrative guards and declaration preflight pass before building.

New private wheel/sdist and sdist-to-wheel builds will test both the selected
minimum backend and the development backend in isolated build-only prefixes.
Exact metadata, license bytes, version, entry point and all 63 package resources
need actual archive verification before this bounded subtask is accepted. The
original `376679c` wheel is preserved, not relabelled or rebuilt. Full scientific,
public dependency/platform, real Conda archive and C6 gates remain separate.

## Additional test-only frontend workflow — 2026-11-03

The #60 [DOM checkpoint](../validation/addon_dom.md) adds one reviewed Node/jsdom
workflow with standard-library-only Python extraction. The original Python CI,
full matrix, publication workflows, four source records and scientific contexts
are unchanged. The declaration inventory now contains ten routes; its existing
exact count guard reflects that one additional classified workflow. All 24
administrative controls pass in the final 78-case selection. npm tools are private
development-only third-party dependencies, outside registered-member graph edges
and Python/Conda runtime manifests. The future actual release plan must review
this additional product gate; the example plan and old artifacts remain unchanged.

## Private addon wheel receiving — 2026-11-03

The [new receiving checkpoint](../validation/addon_installed_receiving.md)
builds one private wheel from producer `376679c2fe77298eda7a80edd311335c2cfa205b`,
then installs it in a genuinely independent Linux/Python 3.14.8 prefix with the
unchanged controlled provider wheels. Exact archive/version/PEP 610 identity,
63 resources, installed core/addon/provider origins and the public widget resolver
are checked. Dependency closure passes before and after **1,430 passing installed
tests**, zero skips; all consumer files and loaded module origins recheck. That result and
five-cell real-kernel 3PTB proof are retained separately from earlier artifacts.
Failed receiver/kernel setup attempts are preserved with their corrections.

This fulfills only the recorded private receiving scope. Public coordinates,
actual published minima, Conda candidate/archive gates and the remaining installed
platform cells stay open. No release/tag/publication/promotion occurs. Setuptools
license-metadata deprecations are a tracked cleanup for a future candidate; the
qualified wheel is not rewritten or rebuilt. This proposal stays partial.

## Addon inventory correction — 2026-11-03

The first #60 implementation head `1c96052` omitted `_presentation.py` from
`devtools/conda-build/resources.toml`. Its
[distribution job](https://github.com/uibcdf/dockingmt/actions/runs/41689015547/job/126102325478)
passes 23 controls and fails the complete source/resource inventory assertion.
The previous 104-case source selection did not include this separate gate.

The maintained inventory now includes `_presentation.py`, `_scene.py` and
`panels/_base.py`. The unchanged complete-inventory guard and all 24 scoped
administrative tests pass with SDK `738fe8dd731abb99dac421b0bb2acc8564110180`.
The second addon slice and its exact-head CI remain tracked on #60. This corrects
the declaration; it does not build, qualify, publish or replace an artifact.
The historical receipts and payload counts below retain their original sources.

## What

Under uibcdf/molsyssuite#45, the maintainer accepts preparation of the shared
noarch route and existing-source controls. Whole adoption remains partial until
actual candidate/archive/installed/public evidence and closure are qualified.

## How

Source baseline 7b11391e153f77f340fd039bc799352f90da83d3 is reviewed in the
central immutable inspection receipt. One recipe preserves six unbounded core
requirements and Python >=3.11,<3.15; optional Vina/Viewer stay optional. All
58 tracked core/addon paths and the generated version are inventoried. Four
wrappers pin publication SDK 2d32048457c6d37093ae509f5626d00a5cda121b.
The example plan names fourteen executed candidate jobs and eight installed
cells with all four installation/resource/science/provenance steps. It is not a
release decision and the actual plan remains absent.

The source SDK 738fe8dd731abb99dac421b0bb2acc8564110180 qualifies original
normal directory installations, with four source records/four contexts/nine
routes. Original scientific pins, install/test commands, environment, matrix,
triggers and recovery remain intact. The new independent admin job runs on 3.14;
preflight in each scientific interpreter verifies the selected clone origins and
actual bounds before existing science. The provider is qualified under
uibcdf/molsyssuite#109 with 416 native tests. Existing source API minima remain
component-owned; the controls invent no new scientific dependency floor.

## Why

Guide synchronization is not distribution adoption. Guard required closure,
packaging/resources/version, actual source provenance and exact qualification
before public mutation. Ordinary internal push flexibility is preserved.

## What was refuted

Noarch does not prove platform support, and normal directory installs do not
prove public closure. Changing scientific source transport to fit the earlier
checker would change the receiving route; the optional shared directory profile
preserves it. A missing first publisher is not proof of unauthorized prior uploads.

## Measured scope and remaining work

Local administrative guards exercise actual shared operations and synthetic
archives without importing or running science. Recipe omission/Python widening,
missing addon/core/typing/version resources, changed routes/floors, source pin
binding drift and inherited pytest source paths are guarded. Installed selection
explicitly clears the source pythonpath; broader multi-root provenance remains
uibcdf/molsyssuite#110. Native exact-source administrative evidence is recorded
at delivery; configuring a gate is not executing it.

Remaining: actual source-free production/development closure, successful exact
candidate science/full compatibility, real plan/access, staged archive and all
installed/public evidence. Python admission stays uibcdf/dockingmt#30; existing
scientific native format integration stays uibcdf/dockingmt#33. No build, install
of science, environment update, tag, upload, promotion or installed dispatch is
performed by this preparation. Public availability/access remains unknown.

## Scope and exclusions

Metadata-bound recipe/resource controls, immutable source adapter, existing-route
inventory, separate administrative CI and publication examples/wrappers. Scientific
algorithms, optional API stabilization, release version choice and active MolSysMT/
MolSysViewer science stay with their development teams.

## Acceptance criteria

Keep candidate controls and local/native guards addressable. Qualify actual
maintained route claims and original installed/public bytes before whole-policy
adoption; record a bounded exception for a justified unresolved condition.

## Provenance

2026-10-07, Linux x86_64, molsyssuite@uibcdf_3.14 / Python 3.14.7. Existing seven
pip-check conflicts remain uibcdf/molsyssuite#82; no global closure is claimed.
The primary clone is preserved; implementation uses an isolated committed-source
clone. SDK availability, source adoption and artifact qualification are separate.

## Local control checkpoint — 2026-10-07

Eighteen distribution guards and the existing reporting/index test pass (19).
The inherited source-pythonpath reproducer fails its addon-origin assertion
before the declared installed override; the corrected profile passes through
the actual shared runner. Ruff/format across 126 files, actionlint, scoped mypy
of the one adapter, declaration preflight and source conformance pass. The
original scientific environment is byte-identical (SHA-256
cc6424fe742b4cf11b96d796baf72b839d0e8b5d26eb3bfee951478012e595ce).
Programmatic old/new workflow review proves every original source scientific
step/pin, matrix, trigger and recovery job is retained; exactly three preflight
steps are added per scientific job. No local scientific suite was executed.

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

## Bounded ordinary-wheel receiving — 2026-10-13

The ordinary `ef8ee2e` wheel is installed outside the source checkout into the
qualified task-owned Python 3.14.8 receiver. Its exact bytes, PEP 610 identity,
59 resources, core/addon import origins and dependency closure are checked. The
shared installed-test operation executes 158 passing cases without skips, with
one explicitly replaced source-bound case; all 24 saved 3PTB rows and 167 poses
replay without new native work. The
[pause handoff](../validation/pause_handoff_2026-10-13.md) links receipts, producer
scripts, limits and retained original-wheel resources. This fulfills that bounded
receiving gate; public channel/file/pair admission and the full installed
scientific/platform/browser scope remain open. This report stays partial.
