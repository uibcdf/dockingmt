# ArgDigest, DepDigest and SMonitor receiving review — 2026-11-04

Owner: [#19](https://github.com/uibcdf/dockingmt/issues/19). Reviewed starting
source: `edf72ce8a5841c2aa7d033b2cb573ecf98797456`; the bounded installer-hint
correction is [#64](https://github.com/uibcdf/dockingmt/issues/64). This review
checks actual calls and behavior, rather than treating imports/declarations or
passing numerical tests as complete adoption. No molecular workflow is changed.

## Assessment

| Tool | Actual adoption | Remaining work |
| --- | --- | --- |
| ArgDigest | Strict registry configuration and real digesters protect dock/score/batch/evaluation/summary, VinaProtocol, BoxRegion and selected preparation/result methods. | DockingPose/Result/Problem constructors, prepared-object constructors, record factories and view's DockingMT-owned arguments are not uniformly covered. |
| DepDigest | Vina and Viewer execution paths have real guards, local diagnostics and delayed optional imports. Fresh core import loads none of Vina/Viewer/RDKit/OpenMM. | Installer metadata advertised nonexistent/default routes; #64 corrects two suite entries. Reconcile other declarations with directly owned versus MolSysMT-delegated capabilities. |
| SMonitor | Package-local config, ensure_configured, catalog exceptions/warnings and DiagnosticBundle are active; five codes render across profiles and survive rebuilding. Existing application config is preserved. | Preparation orchestration lacks explicit signals; addon-owned validation still raises uncoded ValueError/RuntimeError. Add useful structured context where needed, retaining original provider failures. |

The overall state is **partial adoption with working representative boundaries**.
Neither missing optional advanced features nor a different supported ArgDigest
layout is automatically a defect. The registry style is supported: ElastNetMT
also uses it. MolSysMT's larger argument/function/domain hierarchy addresses its
own form-agnostic and extensible-keyword contracts; copying that whole tree is
not required for DockingMT's mostly closed signatures.

## Comparison with our sibling implementations

The inspected MolSysMT source is `71fbe4f46d3c70e4e973c8025f01752a8c9b1084`,
clean and 93 commits behind the fetched branch. Its current fetched ArgDigest
configuration retains the same relevant structure. Public MolSys/native and
get_distances entry points compose signal plus arg_digest; private numerical
consistency checks remain private. Caller-specific digesters express meaningful
optional arguments. Controlled delegation uses skip_digestion only where its
argument contracts are already satisfied.

TopoMT explicitly declares disabled distribution routes and executable-versus-
Python capabilities. ElastNetMT demonstrates strict registry-style digestion.
These are inspected source patterns, not new whole-component qualifications.
Their local worktrees are preserved, including TopoMT's existing modified
`_version.py`; no sibling code is changed by this review.

DockingMT should apply the same separation: digest public inputs, keep necessary
mutable-object/output invariants inside models, and delegate molecular work to
MolSysMT. The finite-real guards added in #63 remain necessary for snapshot
integrity; their presence does not complete constructor ArgDigest adoption.
Adding decorators requires actual digesters/caller semantics: for example,
DockingPose accepts scores=None, while with_scores requires a mapping. Inherited
constructors and selected ArgDigest generations need explicit receiving checks.

The view keyword passthrough is already scoped under #19: Viewer options remain
provider-owned. Validate DockingMT's own options without inventing the downstream
converter/widget keyword domain. Do not add skip flags indiscriminately: some
delegated public calls have stronger or still-unvalidated arguments.

## Executed checks and limits

- Original argument/support/coordinate selection: **70 pass**, 1.24 s.
- Installed routine SMonitor CLI validates DockingMT's config; the provider's
  canonical checker passes config/templates/profile rendering/reserved names.
  Existing tests cover args-only rebuilding, pickle/copy and warning filters.
- A fresh application-configured process preserves its complete SMonitor config
  after importing DockingMT; optional scientific imports remain absent. Runtime
  digestion-plan inspection confirms the covered/uncovered examples above.
- Raw DepDigest scans report one core and one addon finding. The core is a
  **false positive** for `from .vina import VinaBackend`, which names our adapter,
  not external Vina. A three-case managed probe reproduces relative-import
  failure, correct absolute-import detection and correct lazy-function acceptance.
  The owning shared correction is [DepDigest #47](https://github.com/uibcdf/depdigest/issues/47).
  The addon widget-base import is a separate selected-feature boundary, requiring
  a narrow explicit audit disposition; neither finding proves eager core import.

These are source/current-environment checks. They do not replace exact installed
wheel verification, public dependency closure, all Python/platform lanes or
complete support-library adoption. Existing scientific/provider pins remain;
shared-environment closure remains MolSysSuite #82. No new scientific run is made.

## Bounded installer-hint correction

The starting configuration enabled pip and default conda-forge for MolSysMT and
Viewer. The [maintained Viewer installation instructions](https://github.com/uibcdf/molsysviewer/blob/main/README.md#installation)
explicitly say public Conda, not PyPI. Existing #30/#47 observations retain the
MolSysMT public-file/route facts. The old test incorrectly required pip advice.
Three corrected controls fail before the fix. #64 uses supported DepDigest fields
to disable PyPI and select uibcdf Conda for those two entries; Vina routes remain.
The updated argument/support/coordinate selection passes **72 cases**.

This advertises actual acquisition routes, not a compatible public provider set.
Our Viewer #294 source work is received; its covering public artifact still needs
scope/frozen files/qualification/publication in that repository. Current 0.24.0
does not provide both required scene-handle/player contracts. No provider release,
installation, version floor, scientific pin or new API is selected here.

## Next bounded adoption work

1. Integrate model constructors/factories with caller-correct ArgDigest contracts,
   reusing invariant helpers and preserving mutation/export checks, inheritance,
   optional values, units and original records. Qualify the selected provider.
2. Complete preparation/addon diagnostic tracing and catalog-backed owned errors;
   preserve native/provider exception identity and causes where appropriate.
3. Correct the shared scanner in DepDigest #47 and record the selected-addon
   import disposition before treating its raw output as a complete consumer gate.
   Review remaining dependency inventory against real ownership/acquisition.

Use our owning repositories for reusable fixes and #19 for DockingMT receiving;
source access permits coordinated implementation without duplicating providers.
