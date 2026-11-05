# ArgDigest, DepDigest and SMonitor receiving review — 2026-11-04

Owner: [#19](https://github.com/uibcdf/dockingmt/issues/19). Reviewed starting
source: `edf72ce8a5841c2aa7d033b2cb573ecf98797456`; the bounded installer-hint
correction is [#64](https://github.com/uibcdf/dockingmt/issues/64). This review
checks actual calls and behavior, rather than treating imports/declarations or
passing numerical tests as complete adoption. No molecular workflow is changed.

## Assessment

The table records the starting review. The follow-ups below deliver core model/
factory admission, preparation/addon diagnostics, the accepted SMonitor #59/#61
source corrections, prepared-constructor admission and owned view arguments.
The later dependency block reconciles the local inventory/routes and proposes
the shared audit correction for owner review. Accepted scanner and public
support-provider qualification remain incomplete. Development continues against
the selected editable providers while their publishers prepare public files
independently, currently through the uibcdf Conda channel.

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

## SMonitor filtered-signal source receiving

The ordinary SMonitor #59 correction is now integrated independently in provider
commit `b1241ef`, received here from accepted main
`82dad5a7e26e0fba712e30657a6739188d770d79`. A filtered inner observation no longer
acknowledges the exception before the outer ERROR can report it. An already
accepted DEBUG observation still wins; this does not promote every nested event.
DockingMT keeps its ordinary signal/ArgDigest composition without a local marker
reset, decorator-order change or application-policy override.

The frozen [control producer](data/smonitor59_receiving_2026-11-04/control.py)
and [source matrix receipt](data/smonitor59_receiving_2026-11-04/receiving.json)
record consumer runtime `656cacb10a432f77c9a9f4b8bef21136e1270cd3` and producer
SHA-256 `7e137ea466fb58dfd6c26cdeffff22ff6f72507ce9c742fc231ab2b6a74d2110`.
Each selected profile exercises the real public prepare_ligand/prepare_receptor
wrappers with a controlled provider refusal: WARNING/ERROR thresholds, native
and foreign catalog exceptions, plus metadata-only opaque values. It requires
one correctly attributed ERROR, unchanged exception identity/args/cause and
foreign code/context, no opaque string/repr access, and unchanged application
configuration. The controlled refusal replaces only the existing selection
call, restored afterward; no molecular inspection, manipulation or docking runs.

| SMonitor source | ArgDigest source | Passing / total |
| --- | --- | --- |
| `a3fd6d9858973b887e7a8ef0ed1b44f1dd1f2a1d` | `3d1ec53c374098016452abab74706e9d80df5462` | 0 / 10, expected adverse control |
| Same old provider | `cd9c4f3ab80e892075fc5bee9b4ae9ce0ab5e018` | 0 / 10, expected adverse control |
| Accepted `82dad5a7e26e0fba712e30657a6739188d770d79` | `3d1ec53c374098016452abab74706e9d80df5462` | 10 / 10 |
| Same accepted provider | `cd9c4f3ab80e892075fc5bee9b4ae9ce0ab5e018` | 10 / 10 |

The matrix verifies selected import origins before running; temporary source
exports are retired. These are two ArgDigest generations, not the entire CI
dependency composition. After fast-forwarding the clean SMonitor sibling to the
accepted source and reinstalling its editable without dependencies, the routine
environment independently passes **10/10** with no provider override. Its
[profile identities](data/smonitor59_receiving_2026-11-04/routine-profile.json)
and [observations](data/smonitor59_receiving_2026-11-04/routine-receiving.json)
are separate from the matrix. Run the frozen producer from the repository root
using the selected Python/provider environment, with a disposable output file:

```bash
python devguide/validation/data/smonitor59_receiving_2026-11-04/control.py /tmp/receiving.json
```

The routine environment still fails pip check on the separately owned
MolSysSuite #82 dependency-closure findings. This receiving does not qualify
that whole environment, public files/minima, other Python/platform lanes, prior
installed artifacts or visible C4/C6. Scientific provider pins and frozen inputs
remain unchanged; molecular work stays in MolSysMT.

### Separate callback follow-up and provider handoff

Additional independent controls find a narrower residual bug on accepted main:
a diagnostic emitted by exception formatting or manager template resolution can
acknowledge a different, filtered event. **18/20** independent controls pass on
that source; these two callback cases fail. The owning
[SMonitor #61](https://github.com/uibcdf/smonitor/issues/61) and owner-review
[PR #60](https://github.com/uibcdf/smonitor/pull/60) retain this follow-up, rather
than treating the ordinary #59 fix as missing.

Proposal head `11116e25581f9eb46f561ed9d891040a52c08edd` extends the accepted
implementation with invocation-bound receipts and message construction before
capture. Its full provider suite passes **813 tests**, no skips; Ruff, generated
indexes, all fifteen distribution preflights and the docs build pass. A private
wheel built from that exact head passes **44 installed regressions** and a CLI
smoke check; one pytest pre-import rewrite warning remains. Its SHA-256 is
`60831f4bc97caece9f20017ec1382e94e1e466a6dbad20ad96f977c2ba5242d9`.
This proposal was published for owner review. During receiving, the provider
maintainer integrated the runtime correction independently as `5ee88c1` and
retained the final guards/owner record in accepted main
`ccdcace55ba5caf431b4a6a6904d8d18173114a3`. Runtime code differs from the proposal
only in a comment. PR #60 is superseded by that integration; its parallel branch
is not represented as merged. The original matrix above still identifies the
earlier accepted source `82dad5a7`, without relabeling its observations.

An independent full provider run on accepted `ccdcace` passes **812 tests**,
no skips, with required collective E2E enabled. Its CI `41951351240`, QA CI
`41951351174` and policy `41951351465` succeed, inspected through GH Run Receptor.
After a second clean sibling fast-forward/editable reinstall, the frozen
DockingMT producer passes **10/10** again with no source override; separate
[accepted-main identities](data/smonitor59_receiving_2026-11-04/accepted-main-profile.json)
and [observations](data/smonitor59_receiving_2026-11-04/accepted-main-routine.json)
retain this later profile. These checks qualify accepted source, not a new
public artifact or the earlier proposal's private wheel as another producer.

Advance shared impact/receiving is coordinated in
[MolSysSuite #163](https://github.com/uibcdf/molsyssuite/issues/163), related to
#106, and [ArgDigest #49](https://github.com/uibcdf/argdigest/issues/49). Other
registered consumers are candidates for their own receiving, not qualified by
DockingMT's controls. #19 remains partial for prepared constructors, owned-view
arguments, dependency inventory/scanner receiving (DepDigest #47) and actual
public dependency qualification.

## Prepared declaration and owned view argument receiving

Starting from `4cba4b8665f1e122d7d6a247adf1405fc9b83267`, #19 adds ArgDigest to
PreparedLigand/PreparedReceptor construction. State identifiers require nonempty
text; metadata requires a mapping; declared columns require ordered iterables,
preserving generators and NumPy vectors. Bare strings, mappings and unordered
sets cannot silently become atom-axis columns. Ligand group defaults remain
optional without relaxing the required receptor group columns. Integer torsion
counts normalize without boolean/fractional coercion; the existing independent
tree/count invariant remains in the constructor. A supplied private tree must
have the declared local TorsionTree type. Initialization-safe repr avoids
diagnostic warnings before constructor fields exist.

These are declaration/container contracts. Prepared coordinates and source
objects pass through unchanged, including coordinates=None for metadata-only
preparation assessment. MolSysMT retains molecular interpretation, coordinate/
representation validation on use, chemical classification, graph operations and
export. The constructor neither certifies preparation nor selects a chemical
model. Native sources, mappings, charges and the established writer route retain
their existing behavior.

`view()` now digests its own item/result/problem/domain and one-based pose
position through a closed `_resolve_view_inputs` boundary before importing
rendering adapters, creating a widget, enabling the addon or loading a molecular
scene. Invalid owned inputs, conflicting positional/named objects and positions
outside a supplied result are refused before scene changes. Position remains
collection order, independent of scientific pose.rank; NumPy integers normalize
to Python integers. The existing duck-typed item route, same-object repetitions,
optional defaults and existing-widget reuse are preserved.

The closed helper is deliberate: public view's open kwargs belong to MolSysViewer.
They bypass DockingMT's registry entirely, including names also used by local
digesters, a literal kwargs key and the provider's skip_digestion option. That
provider option cannot bypass the separate owned-argument boundary. Viewer
options are not copied into a local domain or reinterpreted; provider exceptions
retain identity. Receptor, partner and reference values likewise stay provider-
owned. No shared ArgDigest policy, contract_owner generation, decorator order or
provider implementation is changed.

### Measured source evidence

- The final **60** controls in `tests/test_prepared_view_argument_contracts.py`
  reproduce **52 failures / eight passes** against a verified managed export of
  the starting DockingMT source. Final test-producer SHA-256 is
  `05d62f9f69f5a847733d69317e486ee5b5fefc8c0fe72366098dd4a55ee1d440`.
- **170 routine source cases pass**, 2.97 s: the new module plus
  test_model_argument_contracts, test_argument_contracts and
  test_preparation_assessment. Inherited/overridden constructors preserve optional
  semantics and opaque molecular values while molecular operations are forbidden.
  Controlled viewer factories/adapters observe admission before side effects,
  provider-option identity, alias behavior and original provider exceptions.
- **355 affected source cases pass**, 45.20 s, no skips, with development
  ArgDigest `7e09e974c36bcf5cace99a7b898d0f5f7a9d3ff2`, SMonitor
  `ccdcace55ba5caf431b4a6a6904d8d18173114a3` and verified exports of existing CI
  MolSysMT `00abb958fb93649131d5ce5fe5e12e90cf4900e9` / Viewer
  `78ede79e2e345593db5bfe80d246d3f6c70bd005`. The 62 provider warnings remain:
  45 legacy-H5MSM, 14 off-axis and three attribute-drop warnings.
- **208 bounded compatibility cases pass**, 2.28 s, selecting exact CI ArgDigest
  `3d1ec53c374098016452abab74706e9d80df5462` with the same molecular/Viewer exports.
  These cover the first six modules in the selection below. Package origins and
  inspected file bytes are verified; all managed exports/caches are retired.

The 355-case selection comprises test_prepared_view_argument_contracts,
test_model_argument_contracts, test_argument_contracts, test_preparation_assessment,
test_preparation_addon_diagnostics, test_support_contracts, test_preparation,
test_ligand_preparation_stages, test_preparation_map_consumption,
test_molecular_delegation, test_viewer_addon, test_viewer_state,
test_viewer_reference, test_viewer_presentation and test_viewer_player_receiving,
all under tests/ with --receptor=llm on Python 3.14.7. These checks include existing
preparation/export and real Python Viewer receiving; controlled adapter tests
do not establish browser/comm/canvas or visible C4/C6 acceptance.

An initially ambiguous consumer digester registration was corrected locally by
naming its value parameter explicitly when declaring extra context. Its provider
diagnostic incorrectly attributes that consumer mistake to an internal ArgDigest
defect and loses function/argument context. An independent registry-only control
is handed to [ArgDigest #50](https://github.com/uibcdf/argdigest/issues/50).
That diagnostic improvement does not block this receiving or require a local
copy of provider logic.

The runtime changes use the development checkouts and the existing compatible
CI generation. Public package preparation proceeds in the providers; no release,
minimum/pin change or scientific experiment is required for this source block.
Frozen scientific/installed producers retain their identities. #19 remains
partial for dependency inventory/scanner receiving (DepDigest #47), wider
developer-tool adoption and actual public dependency qualification. The routine
environment's separate dependency-closure findings remain MolSysSuite #82.

## Dependency ownership, channels and scoped audit receiving

Starting from `6305b2bb2f997c9eca16966684ee247337536329`, #19 reconciles the
DepDigest inventory with DockingMT's actual direct runtime and optional extras.
The required dependencies remain NumPy, MolSysMT, PyUnitWizard, ArgDigest,
DepDigest and SMonitor. The directly owned optional capabilities are Vina's
Python API and MolSysViewer integration. RDKit, OpenMM and PDBFixer are removed
from this runtime inventory: molecular tools are selected and checked by
MolSysMT. RDKit's test extra and the declared RDKit/OpenMM scientific CI tools
retain their existing, separate purposes. No environment/recipe, dependency
floor, CI source pin or molecular implementation changes.

| Capability | Owner / route and boundary |
| --- | --- |
| Docking and fixed-pose scoring | Vina Python API, guarded by DepDigest on VinaBackend.dock/score; no CLI route or automatic backend substitution is added. |
| Molecular forms, preparation and optional molecular engines | MolSysMT; DockingMT passes the explicit workflow/options through its existing provider calls. |
| Widget, player and panels | MolSysViewer; public view is guarded, and explicitly selecting the addon requires its Viewer contracts. |
| Saved records and declaration assessment | DockingMT; fresh import/empty-result roundtrip works with Vina, Viewer, RDKit, OpenMM, PDBFixer and Meeko blocked. |

`VinaBackend.is_available` documents discovery, matching DepDigest's find_spec
check. Discovery is distinct from loading a native extension, solving its
dependencies or scientific qualification. Existing provider exceptions remain
separate from diagnosed absence.

### Current installation guidance

The maintainer confirms that our current public package route is **Conda,
channel uibcdf**, for now. The four support-library entries join the already
corrected MolSysMT/Viewer entries: all six explicitly disable PyPI and advertise
their own uibcdf Conda names. NumPy and the third-party Vina provider retain
their existing routes. Source/editable installation remains the development
route; package publication proceeds independently. Root instructions and the
README retain this current route and its future provider-handoff condition.

The [route observation](data/depdigest47_receiving_2026-11-04/installation-routes.json)
retains inspected provider README source identities and the four official PyPI
API responses (HTTP 404, 2026-11-05 UTC / local 2026-11-04). This is dated route
evidence, not a claim about future channels or a qualified public dependency set.
The earlier #64 two-entry correction retains its original measurements; this
block completes the four support-library hints under #19.

The initial inventory/guard selection gives **one failure / 30 passes**: the
runtime inventory contains three provider-owned tools absent from the actual
runtime extras. The six-route control then reproduces **four failures / two
passes** before the four hint corrections. Afterward **121 source cases pass**,
4.17 s: test_support_contracts, test_bootstrap, test_preparation_assessment and
test_prepared_view_argument_contracts, all under tests/ with --receptor=llm.
Inventory checks compare real installed package requirements/extras with
DepDigest's introspection rather than duplicating a hard-coded dependency list.
Their packaging requirement parser is declared in the test extra; the maintained
Conda test environment already supplies it. Runtime requirements stay unchanged.
The guard selection now covers both Vina dock and score plus missing Viewer;
fresh-process isolation also executes an empty-result saved roundtrip.

### Provider correction and exact addon scope

The relative-import false positive remains in accepted DepDigest main `9dc5621`
(the runtime file is unchanged from `0884f0c`). The narrow correction is proposed
in [DepDigest #48](https://github.com/uibcdf/depdigest/pull/48), for
[owner #47](https://github.com/uibcdf/depdigest/issues/47), at exact source
`23c028c1bafe6b8241e0a3d57b1df1773afa2322`. It classifies ImportFrom.level in
DepDigest; DockingMT adds no scanner implementation or core-file exemption.
The 27 owning controls reproduce fifteen failures/twelve passes before repair.
The proposal passes **332 provider tests**, no skips, including supplied
shared-SDK and sibling integration gates, Ruff/index/format checks and all
twenty configured distribution routes.

A private wheel from that exact source passes **27 installed owning tests**
and CLI smoke. Its [package receipt](data/depdigest47_receiving_2026-11-04/package-receipt.json)
retains the original file/SHA-256 and explicitly unpublic state. The
[consumer producer](data/depdigest47_receiving_2026-11-04/control.py) and
[observations](data/depdigest47_receiving_2026-11-04/receiving.json) retain the
consumer base, actual inventory/producer hashes and three separate profiles:
old provider **5/7**, proposal source **7/7**, installed proposal **7/7**.
Original import origins are checked before execution. All controlled fixtures
are retired; no docking or molecular operation runs in these audit controls.

The raw addon finding is real and remains visible:
`molsysviewer_dockingmt/panels/_base.py` imports AddonPanelWidget at definition
time because its local panel inherits that Viewer class. This is an explicitly
selected Viewer integration, reached after requesting the addon/panels; core
DockingMT import stays independent. The supported exact-file exception is scoped
only to this class-definition boundary. Owner: #19; review by 2026-11-11; remove
or revise it if panel ownership, import reachability or the provider's class
construction contract changes. A new absolute import in another addon file
still produces a failing finding. No directory exemption or allow-violations
mode is used for the consumer's scoped pass.

With the proposal selected explicitly, run from the repository root:

```bash
depdigest audit --src-root dockingmt --soft-deps vina,molsysviewer --json
depdigest audit --src-root molsysviewer_dockingmt --soft-deps vina,molsysviewer --exempt-file molsysviewer_dockingmt/panels/_base.py --json
```

Both scoped checks pass on the proposal; raw addon audit retains one finding.
The scanner remains a syntax check, with its documented dynamic-import and
reachability limits. Fresh import, runtime guard tests and science keep their
own evidence. No new CI gate relies on the unmerged provider fix.

Shared advance notice and candidate consumers are tracked in
[MolSysSuite #166](https://github.com/uibcdf/molsyssuite/issues/166). The original
sibling clones are preserved. Source acceptance, receiving in the routine
provider clone and eventual public files/floors remain separate: #48 is an open
owner-review proposal, not accepted main or a public package. #19 stays partial
for that acceptance/receiving, wider developer-tool adoption and actual public
compatibility. Development against source checkouts continues; original
scientific/installed producers and deferred visual C4/C6 remain unchanged.
