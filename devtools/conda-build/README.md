# First guarded Conda route

Owner: uibcdf/dockingmt#47. Shared publication SDK:
`2d32048457c6d37093ae509f5626d00a5cda121b`. Dependency/source SDK:
`738fe8dd731abb99dac421b0bb2acc8564110180`. These are separate accepted pins.

## Applicability and current status

The recipe declares `noarch: python`: both Python namespaces and py.typed carry
no bundled native binaries. Third-party native Vina/OpenMM/RDKit stay separately
distributed; Vina/Viewer are optional features, not new required runtime packages.
`resources.toml` requires all 58 current tracked package paths plus the generated
version file (59 paths). Bounded setuptools discovery excludes administration/tests.
No actual archive, public dependency closure or platform qualification is claimed.

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
   requires fourteen jobs across routine CI, six-cell full compatibility, policy
   and Conda controls. Successful administration or a debt probe with skipped
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
a candidate and stay with DockingMT; MolSysSuite administrative passes do not
repair or clear them. The Python badge/admission remains uibcdf/dockingmt#30.

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
the installed addon. The broader shared multi-import-root guard need is owned by
uibcdf/molsyssuite#110; this receiving control stays linked until a reviewed shared
replacement covers the boundary. No global installer/pytest profile is altered.

Run offline recipe and resource review using the accepted SDK and example plan;
these are declarations/synthetic negative guards, not release evidence. Future
resource changes update the inventory and require a new exact candidate's archive
and installed validation. The full common route and recovery contracts live in
MolSysSuite devguide/noarch_conda_workflow.md and dependency_route_preflight.md.
