# Current Core MVP acceptance map

Owner: [#28](https://github.com/uibcdf/dockingmt/issues/28); workflow follow-up:
[#4](https://github.com/uibcdf/dockingmt/issues/4). Runtime baseline:
`8f1711621170c64f6256545e2d38b327cfdc9beb`, 2026-11-03. The unchanged runtime
retains the preceding review; new notebook evidence is identified separately below.
This maintained map supersedes the *next-action list* of the
[2026-10-28 audit](validation/core_mvp_audit_2026-10-28.md), preserving that
audit, its findings at its original source and all scientific/artifact receipts.
The criteria in [MVP.md](MVP.md) remain unchanged.

## Scope and interpretation

The supported starting profile is a declared single-state small molecule and
rigid protein, explicit preparation choices, a physical box and Vina. See the
[preparation/provenance contract](validation/preparation_profile.md) for source,
hydrogen, charge, type, torsion and input-profile limits. No experimental pH,
affinity, general model suitability or automatic preparation policy is inferred.

**Supported** below means implementation and named evidence exist within that
profile. **Partial** identifies an actual remaining boundary. **Deferred** means
the required observation is intentionally unperformed. These are evidence
descriptions, not new report statuses or blanket acceptance of a whole gate.
Core MVP completion is not declared: visible C4/C6, bounded scientific/profile
questions and the stated public-boundary review retain their owners.

Broader molecular persistence, every input dialect and all future chemistry are
not prerequisites for demonstrating the declared workflow. A source-qualified
private wheel is also distinct from a publicly admitted distribution.

## Evidence used

| Key | Evidence and actual boundary |
| --- | --- |
| S | [Original 3PTB searches](validation/3ptb_search.md): 24 searches / 167 poses; original reporting failures and separate successful receiving are preserved. This is original scientific evidence, not a new experiment on the current composition. |
| H | [Original human workflow](validation/human_3ptb_workflow_2026-10-20.ipynb): five poses, original producer `1decee5` and original provider. |
| P | [Declared profile](validation/preparation_profile.md): recorded recipe, admission and explicit scientific limits; [prepared recovery](validation/prepared_recovery.md) binds supplied inputs to declarations and available submitted bytes. |
| D | [Domain derivation](validation/domain_derivation.md) and [guard](../tests/test_domain_derivation.py): selection/frame/source/padding recipe, geometry binding, legacy readability and serialization. #55 is resolved. |
| C | [ChemicalStates receiving](chemical_domain_receiving.md): current source and qualified wheel producers remain distinct; chemical operations stay in MolSysMT. |
| R | [Saved-case recovery](validation/saved_human_case_recovery.md): authenticates the bounded original bundle and returns a detached result; no molecular restoration or search. |
| I | [Installed record inspection](validation/installed_result_inspection.md): eight public-API cells pass for original and missing-capture records, with units, refusal controls and installed provenance. It reads records without authenticating the entire original bundle or restoring a molecular problem. |
| W | [Installed preparation/admission](validation/installed_3ptb_preparation.md): nine public-API cells pass under normal and pm/fs policies, recreating explicit 2,011/13-atom inputs and admitting two planned problems. Its own scope has no search/evaluation/viewer calls; actual execution is separate evidence E. |
| E | [Installed two-search execution](validation/installed_3ptb_execution.md): separately registered workflow source `1ef85cb`, unchanged consumer/provider archives, native/displaced attempted once each and 5+4 full poses. Saved-record audits/captures, refusal controls and nondefault-policy inspection pass; no RMSD/recovery or affinity claim. |
| V | [Player receiving](validation/player_notifications_receiving.md): exact Viewer `78ede79e`, real Python widgets, immediate navigation, full private installed gate and five-cell kernel replay. [DOM tests](validation/addon_dom.md) separately exercise shipped JavaScript with a model double. Browser comm/pixels remain unobserved. |

The V receiving uses original DockingMT wheel producer
`50d8e33f4ccb3354a8d27aea9fa9010c1b13e9a9` / version `0.0.0+225.g50d8e33`,
and separate qualification harness `1c343924b4a144058685796783d72c174b032651`.
Its [manifest](validation/data/addon_player/manifest_2026-11-03.json) binds exact
consumer/provider archives, environment, 1,449 passing installed tests with zero
skips, and kernel receipts. The 62 nongenerated runtime files equal reviewed
source. Reusing that proof for this documentation review does not change its
producer, interpreter/platform or scientific scope. Final-head hosted observations
and recovery remain on [#60](https://github.com/uibcdf/dockingmt/issues/60);
queued/in-progress lanes are not passing evidence.

## All 35 Core criteria

Numbering follows the bullet order of each gate in `MVP.md`: 32 C0–C5 criteria
plus three C6 criteria. Public source/test links identify current implementation;
the evidence keys above identify executed results and their limits.

| Criterion | Current implementation / evidence | Remaining boundary and owner |
| --- | --- | --- |
| C0.1 Implementable concepts | Supported: problem, protocol, pose/result and box models; H/P/V. | Present profile only; no speculative ontology required (#28). |
| C0.2 Isolated Vina | Supported: [backend](../dockingmt/engines/base.py), [Vina adapter](../dockingmt/engines/vina.py). | No second engine is needed to demonstrate this gate. |
| C0.3 Files are not the model | Supported: independent problem/domain/result records; H/P/R. | PDBQT is a partial representation, not native chemistry (#33/#49). |
| C0.4 Molecular identity | Supported for complete one-state sources: provider export/map/reader chain; C/P/V. | Partial/reference reading remains MolSysMT #521 under #49/#33. |
| C0.5 Run provenance | Supported by original result and linked source/admission bundle; H/P/R. | Arbitrary prepared-source/replay coverage stays #4. |
| C0.6 Capability validation | Supported: backend checks and [guards](../tests/test_backend_contracts.py). | Unsupported intent rejects; fields do not imply execution support. |
| C0.7 Physical quantities | Supported: explicit conversion/display units and nondefault-policy guards; D/P/V. | No new global unit policy or unitless numerical boundary is introduced. |
| C0.8 ArgDigest boundaries | Supported representative paths: [argument guards](../tests/test_argument_contracts.py). | Complete public-surface/adoption review stays #19. |
| C0.9 Optional dependencies | Supported: [DepDigest/lazy-import guards](../tests/test_support_contracts.py). | Availability does not certify scientific suitability. |
| C0.10 Diagnostics | Supported: SMonitor catalog/errors and support guards. | Exhaustive public diagnostic/adoption review remains #19. |
| C0.11 Inspectable defaults | Supported: serialized protocol, resolved native calls and score context; S/H. | Defaults are versioned execution choices, not universal recommendations. |
| C1.1 Inputs/transforms | Supported: declared source/state/template/H/model choices and original reports; P/H. | Experimental state/model suitability is unassessed (#33). |
| C1.2 Prepared-state identity | Supported: explicit receptor/ligand state IDs, axes and source maps; P/H/C. | Labels do not establish environmental protonation. |
| C1.3 Traceable representation | Supported: actual export map, submitted bytes/hashes and source binding; P/H/R. | Standalone prepared JSON is not a molecular snapshot (#4). |
| C1.4 Preparation failures | Supported: missing Q/types, unknown H, conflicts and provider errors reject; P/C. | #5's unsafe placeholder mechanisms are resolved; scientific follow-up stays #33. |
| C2.1 Multiple normalized poses | Supported: S has 167 poses; H/R/V retain the five-pose case; E adds two current-composition searches and nine full poses. | E has its own finite denominator; V remains a saved-case receiving. |
| C2.2 Scores/ranks | Supported: named descriptors, ranking history and distinct position/rank; S/H/V. | No implicit rescoring, arbitrary score substitution or fabricated rank. |
| C2.3 Reference RMSD | Supported: [evaluation API](../dockingmt/evaluation.py), original positional criterion and separate optional symmetry; S/H. | Reference, correspondence, units and policy must be explicit; panel navigation computes no RMSD. |
| C2.4 Molecular/receptor state | Supported: declared states and original frame retained; P/H/C/V. | State selection is not automatic chemical validation (#33). |
| C2.5 Reconstructable run | Supported bounded record/byte/configuration recovery; H/P/R. | Supplied native objects or explicit recipe replay remain necessary; recovery is not re-execution (#4). |
| C3.1 Backend-independent box | Supported: [BoxRegion](../dockingmt/core/search_domain.py), explicit/derived domains and physical units; D/S. | Rich domains and guidance remain future scope. |
| C3.2 Common result model | Supported: local docking/redocking share DockingResult; S/H/R. | Original scientific arms retain separate labels and denominators. |
| C3.3 Inspectable conversion | Supported: physical geometry, numerical backend projection and resolved calls; D/S/H. | Conversion records do not certify a richer domain's approximation. |
| C4.1 Deterministic derivation | Supported: source/selection/frame/padding recipe and detached geometry binding; D. | Earlier missing-provenance finding is resolved by #55. |
| C4.2 Visualizable domain | Python geometry/state and DOM controls supported; V. | Rendered visibility/framing remains deferred (#52/#60). |
| C4.3 Preserved domain provenance | Supported: recipe survives domain/problem/result serialization beside actual projection; D. | Explicit/legacy boxes honestly retain absent derivation. |
| C5.1 Source molecules/states | Supported through linked source/admission/result records; P/H/R. | Missing standalone source fingerprints remain absent (#4). |
| C5.2 Receptor state | Supported: original dry receptor, declared histidines/CYX/termini; P/H. | Water/cofactor/metal/environmental-state generality is outside the profile. |
| C5.3 Preparation history | Supported: named H/Q/type/projection/torsion reports and maps; P/C/H. | Complete fields do not validate a scoring model (#33). |
| C5.4 Search domain | Supported: physical/rounded domain, linked input evidence and derived recipe; D/H/P. | #55 is resolved; visual observation remains separate. |
| C5.5 Backend/options/seed | Supported: actual backend/version, resolved options, seed and producer; S/H. | Historical producers are not relabelled as the current receiver. |
| C5.6 Score producer | Supported: named method/version/unit/context and input hashes; [score contract](validation/score_semantics.md), S/H/V. | Scores are not affinity measurements; unknown descriptors remain unknown. |
| C6.1 Receptor/domain/pose | Python scene coordinates/identity and real widget state supported; V. | Browser rendering/controls are deferred; whole criterion is partial (#60/#52). |
| C6.2 Optional reference | Explicit reference and original-frame coordinate/identity checks supported; V. | Actual visual comparison remains deferred (#60/#52). |
| C6.3 No ad hoc conversion | Supported Python route: [dmt.view](../dockingmt/view.py), explicit inputs and provider-owned molecular composition; V. | End-to-end frontend observation remains required for C6 acceptance. |

## Decisions for the active queue

1. The #55 domain-provenance work and MolSysViewer #291 reception are delivered;
   do not schedule them as missing implementation again. #5 is closed for its
   original unsafe mechanisms, with scientific follow-up explicitly in #33.
2. The [installed saved-result notebook](validation/installed_result_inspection.md)
   is delivered under #4, with two exact eight-cell kernel profiles and 144
   existing audit/schema guards passing. The nine-cell preparation/admission
   walkthrough also passes both unit-policy profiles, with 64 existing installed
   contract/assessment guards. Its separately registered execution E now returns
   5+4 full poses from two attempts, with 144 existing audit/schema guards and
   saved-record reading passing. Next declare the public nine-heavy-atom
   evaluation route in the [workflow review](human_workflow_review.md), before
   RMSD. W/E add no whole-Core, recovery or visual acceptance claim.
3. MolSysMT #521 remains an undelivered extension. Retain its bounded existing
   profile/refusal boundary; do not replace it locally. MolSysMT #256 is explicitly
   post-1.0 H5MSM 0.6 MolecularMechanics persistence, not a prerequisite for the
   declared linked-bundle workflow or a reason to invent a DockingMT archive.
4. #52/#60 remain partial for visible C4/C6. Resume that observation on the
   maintainer's decision. Public API minima, candidate planning and actual
   archive/platform admission remain #30/#47 and do not follow from private tests.

## Existing Extended-MVP pieces

Public `score`, `DockingPose.with_scores`, `DockingResult.rank_by`, `dock_many`,
`evaluate_redocking` and `summarize_redocking` already exist. `dock_many` is serial,
incremental execution of prepared problems with explicit error handling, not a
campaign scheduler, preparation engine or map cache. Evaluation/summary retain
their explicit compatible-case criteria; they do not establish screening
enrichment, general cross-ligand ranking, clustering or interaction analysis.

These pieces should be reused when an accepted workflow needs them. They neither
justify duplicating an API nor automatically accept E1–E5. New receptor flexibility,
engines, pharmacophore guidance and large campaigns remain later work. Reusable
molecular operations belong to MolSysMT; pharmacophore/topography/flexibility
capabilities retain their respective providers.
