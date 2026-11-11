# First guarded Conda route

Owner: uibcdf/bindingmt#47. Reviewed publication/build/upload/promotion and
publication-governance SDK: `95f693be10c9205ab9b912cb53453710a207bf45`
(MolSysSuite #87, Conda provider v2.3.0). The installed-scientific caller adopts
that same immutable revision after full private-wheel receiving of the isolated
test-support profile under #47/MolSysSuite #110/#117. Actual staged/public artifact
and eight-cell receiving remain pending. Dependency/source
SDK remains `738fe8dd731abb99dac421b0bb2acc8564110180`. These scopes are reviewed
separately, not a blanket helper-pin replacement.

The [public readiness review](../../devguide/validation/public_candidate_readiness.md)
records current registry/archive evidence, required provider handoffs and the
release stop condition. No real plan/version, build, upload or promotion is
selected by the shared-caller adoption.

## Applicability and current status

The recipe declares `noarch: python`: both Python namespaces and py.typed carry
no bundled native binaries. Third-party native Vina/OpenMM/RDKit stay separately
distributed; Vina/Viewer are optional features, not new required runtime packages.
`resources.toml` requires all 67 current runtime paths, including the generated
version file. Bounded setuptools discovery excludes administration/tests.
No actual Conda archive, public dependency closure or platform qualification is claimed.

The local [PEP 639 checkpoint](../../devguide/validation/license_metadata.md)
aligns Setuptools >=77.0.3 in build metadata/recipe/bootstrap, preserves the MIT
license and qualifies new private wheel/sdist files against minimum/development
backends. Those Python archive checks do not qualify this Conda publication route.

`release_plan.example.toml` is administrative onboarding only. Its version/build
are examples and do not select a release. There is no real release_plan.toml;
the publisher rejects a missing real plan. Access is unknown: the new wrappers
map the expected `ANACONDA_UIBCDF_TOKEN` secret to the common `ANACONDA_TOKEN`,
but no secret was created, read or verified. The authorized owner must confirm
its mapping/access before any publication.

## Candidate preparation owned by the developer

1. Review required metadata, ordinary public dependency closure and optional test
   tools; choose the canonical version/new immutable build and responsible owner.
2. Commit the actual release_plan.toml with the reviewed recipe/resource/platform
   profile. The first Conda route uses staging. Preserve any already registered
   source and bytes; never overwrite an occupied coordinate.
3. Execute every candidate gate at that exact full source commit. The example
   requires fifteen jobs across routine CI, six-cell full compatibility, policy,
   Conda controls and the shipped addon's DOM workflow. Successful administration or a debt probe with skipped
   science cannot authorize a build. Existing weekly/manual routes remain; the
   developer selects the real qualification execution when ready.
4. Dispatch build_and_upload_conda_packages.yaml with the candidate SHA/version.
   Shared preflight verifies native gates and immutable availability; it builds
   one file, checks version/resources before upload and retains receipts.
5. Qualify that exact staging filename/SHA-256 through
   test_installed_conda_package.yaml. The proposed eight cells cover Linux and
   macOS arm64 Python 3.11–3.14, with exact install, installed files, whole existing
   tests and final dependency provenance. Original source fallbacks are forbidden
   in installed/public closure. Current source macOS coverage is only 3.13/3.14;
   configuring eight installed cells is not executed evidence for older macOS.
6. Dispatch promote_conda_package.yaml only after all required installed evidence
   is reviewed. Normally qualification equals candidate; an explicitly reviewed
   different qualification_sha preserves the original producer/file/digest.
   Promotion adds the public label to those same bytes and verifies public poststate.

No real version, plan, build, scientific dispatch, upload, promotion or tag was
selected by this control preparation. Component-owned scientific failures block
a candidate and stay with BindingMT; MolSysSuite administrative passes do not
repair or clear them. The Python badge/admission remains uibcdf/bindingmt#30.

## Installed selection and import isolation

The selection retains the entire existing tests tree. Exact Vina 1.2.7, RDKit
2026.03.1 and OpenMM 8.6.1 test tools were observed across the existing Linux
source CI 37589149276. Their declaration is a proposed tool profile, not a new
core API floor or a solved eight-cell matrix. Review them with the real candidate;
optional missing integrations retain their explicit tests' behavior and do not
certify the optional Viewer feature. The shared SDK selects its own standard
pytest/receptor tools; an actual receiving run must qualify that combination.

The source pytest profile adds the owner root. The installed profile explicitly
uses `-o pythonpath=` so collection cannot inherit that source route. A regression
runs the actual shared runner against separate installed/source addon fixtures:
the original inherited configuration selects source; the declared override selects
the installed addon. The adopted shared #110 verifier independently clears that
route and checks every loaded core/addon root inferred from the actual payload.
The compatible explicit override stays in the descriptor. No global installer/
pytest profile is altered.

Scientific helpers use the unshipped `bmt_test_support` namespace. The optional
shared #117 declaration selects 30 Python files and 564 explicit fixture/text
files with exact SHA-256. Keep it synchronized when changing an input; new
receiving reports are not recursively included. The shared operation validates,
stages, checks and retires those files without exposing the owner/staging parent
on Python paths. Original producer programs remain preserved, with byte-identical
inert text copies for fingerprint-only use. Runtime discovery excludes support.
Live guide/notebook fixture sources are stored as inert snapshots under
`tests/data/installed_support/b74b4ad/`; their staged paths/bytes remain the
qualified originals. Run the shared resource preflight after final guide edits
and on a fresh committed export before pushing, keeping administrative checks
independent of scientific imports.

The [complete private receiving](../../devguide/validation/installed_support_receiving.md)
passes 1,450 tests on Linux/Python 3.14.8 with the original controlled providers
and consumer wheel. Its first full 1,448-pass/one-failure run and corrected
source attribution remain separately recorded. This source adoption does not
qualify a staged Conda archive, public closure or all eight installed cells.

Run offline recipe and resource review using the accepted SDK and example plan;
these are declarations/synthetic negative guards, not release evidence. Future
resource changes update the inventory and require a new exact candidate's archive
and installed validation. The full common route and recovery contracts live in
MolSysSuite devguide/noarch_conda_workflow.md and dependency_route_preflight.md.
