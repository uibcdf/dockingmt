# ArgDigest, DepDigest and SMonitor receiving review — 2026-11-04

Owner: [#19](https://github.com/uibcdf/dockingmt/issues/19). Reviewed starting
source: `edf72ce8a5841c2aa7d033b2cb573ecf98797456`; the bounded installer-hint
correction is [#64](https://github.com/uibcdf/dockingmt/issues/64). This review
checks actual calls and behavior, rather than treating imports/declarations or
passing numerical tests as complete adoption. No molecular workflow is changed.

## Assessment

The table records the starting review. The core model/factory and bounded
preparation/addon diagnostic follow-ups below deliver those receiving blocks.
Prepared constructors, owned view arguments, dependency-audit receiving and
the SMonitor #59 provider limitation remain incomplete.

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

## Core model/factory receiving follow-up

Starting from `4cfbac66ba643276533c8574a85c3d9e5f809f9b`, #19 extends real
ArgDigest admission to DockingPose, DockingResult and DockingProblem constructors,
their record factories, BoxRegion's bounds/points/selection/record factories,
DockingProblem.for_redocking and VinaProtocol.from_dict. BoxRegion and
VinaProtocol constructors already used ArgDigest. Closed signatures refuse
unknown keywords before processing values.

The value contracts require optional positive integer pose ranks, optional text
identifiers, mapping metadata/context records, actual pose collections and
optional DockingProblem references. Lists of key/value pairs are not metadata
mappings. Generators of poses remain supported and are consumed once. A pose
constructor still accepts scores=None, and a result constructor problem=None;
with_scores(None) and dock(None) remain invalid. Record recovery still accepts
absent receptor/partner overrides when the record supplies the inputs.

Those differences use explicit decorator context (`native_constructor`,
`native_factory` and `record_factory`) supported by the selected older ArgDigest, rather than
depending on runtime subclass module names or the newer contract_owner option.
They do not add public keywords: callers cannot spoof that context. The shared
caller helper performs exact constructor-key matching. Inherited constructors,
a super-delegating override and inherited class factories are exercised with
classes declared in a different module namespace.

Existing numerical pose and box validators now supply the corresponding
digesters; constructors/factories do not repeat those same input checks in
their bodies. Mutable pose export, schema admission, score semantics, ranking
history and domain-derivation consistency checks remain in their independent
boundaries. Values normalized to nanometers retain the original numerical,
unit and snapshot contracts under a non-default session policy. Constructor
repr methods now handle pre-initialization tracing without spurious SMonitor
summary warnings; new admission tests treat RuntimeWarning as an error.

Molecular forms, selections, structure indices and chemical states keep their
MolSysMT route. Explicit pass-through digesters document that ownership; they
do not interpret or normalize provider values. The selection factory preserves
None/array selections, original structure/state objects and native provider
exception identity, including through inheritance. DockingMT checks only absent
required sources and its own domain/options. Invalid metadata/domain/guidance
or padding fails before molecular operations. A pre-existing state-selection
test used a removed private charge setter; it now assigns the same charges
through public msm.set, and explicitly imports the native fixture class so it
also runs independently of test import order. No molecular routine is added.

### Executed evidence

- The first 47 new controls reproduce **44 failures / 3 passes** before the
  implementation. The final model module contains **50 passing cases**,
  including the protocol factory and provider-delegation controls.
- Routine Python 3.14.7, editable ArgDigest `cd9c4f3` and MolSysMT `71fbe4f`:
  **477 cases pass**, 20.09 s. Seven legacy-H5MSM warnings remain; there are no
  new constructor-summary warnings. The model module uses its stricter
  RuntimeWarning policy.
- A managed, read-only export selects CI's exact ArgDigest
  `3d1ec53c374098016452abab74706e9d80df5462` and MolSysMT
  `00abb958fb93649131d5ce5fe5e12e90cf4900e9`: the same **477 cases pass**,
  19.88 s, seven legacy-H5MSM warnings. Import origins are asserted inside
  those exports, inspected provider file bytes match their Git objects, and
  DigestConfig is confirmed to lack contract_owner. Import metadata can still
  show the routine installed distribution's version; the verified source
  commits, not that string, identify this probe. Both exports are retired.

The 477-case selection comprises test_model_argument_contracts,
test_argument_contracts, test_pose_coordinates, test_result_contracts,
test_search_domain_contracts, test_serialization_contracts, test_problem,
test_results, test_protocol, test_search_domain, test_score_semantics,
test_result_audit, test_pose_audit, test_result_export_benchmark and
test_support_contracts (all under tests/, using --receptor=llm).

This qualifies the bounded source contracts on Python 3.14 with both selected
ArgDigest generations; it is not the complete CI environment, all supported
Python/platform lanes, a new installed artifact or public-minimum qualification.
No dependency floor/pin, scientific producer or frozen input changes. #19 stays
partial: prepared-object constructors and owned view arguments still need their
own receiving work; molecular content validation must use MolSysMT. Preparation/
addon diagnostics and the DepDigest inventory/scanner disposition remain next.

## Preparation and addon diagnostic receiving follow-up

Starting from `c957f52116c068ce27c57129aca64b150ca7f986`, #19 adds explicit
SMonitor orchestration signals to prepare_ligand/prepare_receptor, addon
lifecycle/context actions and public molecular-scene/domain adapters. Preparation
frames use context_extra with operation and provider=molsysmt. Molecular work
still goes through the existing MolSysMT operations; no preparation choice,
geometry kernel, source mapping, frame policy or provider exception is replaced.

Eight catalog identities (DMT-E004 through DMT-E011) distinguish corrections for
pose count, structure pairing, missing display inputs, pose position, foreign
shape ownership, missing scene state, unsupported Viewer capabilities and unknown
panel actions. Their wording lives in the catalog; typed occurrence facts include
operation/provider, resource, observed/expected counts, pose index/position,
shape tag and action ID. Existing ValueError/RuntimeError catch families remain
valid through catalog-backed subclasses. Published DMT-E001–E003/W001–W002
meanings are retained. New classes survive args-only rebuilding, pickle and
deepcopy; all thirteen codes render under the five supported profiles.

Panel action dispatch and state reads have shared signal boundaries inside their
existing recovery catches, so handled failures remain observable. Panel states
add error_code, preserve the original error text and clear the code after a
successful refresh. Provider failures retain their original identities, causes
and codes, including an uncoded native error when appropriate. Expected absence
of an unrendered domain/reference during ordinary refresh emits no error; an
attempt to operate on that absent visual remains a coded refusal. Domain handles,
failed-deletion retry state, subscriptions and molecular frame ordering retain
their previous contracts.

The frontend protocol examples now come from emitted production refresh states,
including nullable error_code and catalog-backed prerequisite wording. Only
these current developer examples change; frozen scientific/installed fixtures
and their declared hashes retain their original bytes.

### Source and protocol evidence

- A verified export of the starting DockingMT source reproduces **12 failures /
  one pass** in the original thirteen diagnostic controls. The final diagnostic
  module has fourteen cases, including a normal-threshold owned-error control.
- **44 routine source checks pass** for diagnostics, catalog contracts and
  Python/DOM protocol examples. A fresh application-configured process preserves
  the complete SMonitor configuration and warning hook across addon activation
  and an owned diagnostic. The SMonitor config CLI and canonical integration
  checker pass configuration, templates, rendering and reserved-name checks.
- The broader first routine selection gives 244 passes/19 failures: four stale
  protocol examples are corrected here. The remaining fifteen failures are
  reproduced unchanged against the starting DockingMT source: thirteen Viewer
  player receiving cases and two MolSysMT preparation/map profile cases. Routine
  clones are Viewer `73a6f388e09146650349dfe83564ae318ba20298` and MolSysMT
  `71fbe4f46d3c70e4e973c8025f01752a8c9b1084`; do not call that profile qualified
  or modify a provider contract to accommodate it.
- A separate managed export selects the exact existing CI ArgDigest
  `3d1ec53c374098016452abab74706e9d80df5462`, MolSysMT
  `00abb958fb93649131d5ce5fe5e12e90cf4900e9` and Viewer
  `78ede79e2e345593db5bfe80d246d3f6c70bd005` sources. Package import origins and
  inspected provider-file bytes are verified. **All 264 affected cases pass**,
  48.79 s, no skips; 59 existing provider warnings remain (42 legacy-H5MSM,
  14 off-axis attribute and three attribute-drop warnings). This includes actual
  Python player/widget receiving, preparation stages/maps, core argument
  contracts and addon state/reference/presentation behavior. Exports are retired.
- **21 DOM tests pass**, Node 26.3.1, using the actual extracted panel modules;
  the existing experimental VM-module warning remains. The initial sandboxed
  command could not spawn its Python extractor; the authorized local rerun passes.
  No browser/canvas, comm transport or human C4/C6 acceptance is claimed.

The 264-case selection comprises test_preparation_addon_diagnostics,
test_support_contracts, test_viewer_addon, test_viewer_state,
test_viewer_reference, test_viewer_presentation, test_viewer_player_receiving,
test_viewer_frontend_contract, test_preparation, test_ligand_preparation_stages,
test_preparation_map_consumption, test_argument_contracts and
test_model_argument_contracts, all under tests/ with --receptor=llm. SMonitor
is the routine source `ebdd0542156ed1dbe8df93141dbddbc74132a6f0` in these probes.
These source profiles are not complete installed/public dependency closure or
qualification of every supported Python/platform lane. The separate installed-
wheel diagnostic check and its exact file/source identity are recorded in #19;
it does not replace the previous installed-science receipts or public gates.

### Independently reproduced SMonitor limitation

[SMonitor #59](https://github.com/uibcdf/smonitor/issues/59) owns a newly observed
nested-signal defect, reproduced without DockingMT or ArgDigest: with application
threshold WARNING, a filtered inner DEBUG signal marks the exception emitted
and suppresses the outer ERROR event. At threshold DEBUG the one DEBUG event is
observable; nested ERROR at threshold WARNING produces one ERROR. All controls
preserve native exception identity/args/cause. The consumer-facing ArgDigest
wrapper uses DEBUG, so this matters for ordinary preparation failures.

Trace tests explicitly select DEBUG to inspect breadcrumbs. A separate owned
addon error is verified at the ordinary WARNING threshold. This does **not**
prove normal-threshold ERROR delivery for the affected ArgDigest composition.
No production threshold, decorator order, private emission marker or provider
implementation is changed to work around it. Receive the provider correction
under #19 before closing that broader diagnostic claim; the owner issue includes
ArgDigest/DockingMT relationships and the shared-impact handoff requirement.

The local diagnostic block is delivered. #19 remains partial for SMonitor #59
receiving, prepared-object/owned-view argument contracts and dependency inventory/
scanner receiving (DepDigest #47). Scientific producers, provider pins, prior
installed artifacts, public minimum claims and the deferred visual review retain
their independent identities and gates.
