# Nonvisual Core MVP acceptance audit — 2026-10-28

Coordination: [#28](https://github.com/uibcdf/dockingmt/issues/28), with
[#4](https://github.com/uibcdf/dockingmt/issues/4),
[#5](https://github.com/uibcdf/dockingmt/issues/5) and
[#33](https://github.com/uibcdf/dockingmt/issues/33).
The criteria in [MVP](../MVP.md) are unchanged. This audit maps all **32 C0–C5
criteria** to existing implementation, immutable evidence and remaining work.
It changes no runtime, dependency, chemical hypothesis, search population or
scientific producer. It does not accept C6 or the whole Core MVP.

## Verdict and evidence boundaries

| Gate | Audit finding | Remaining acceptance / owner |
| --- | --- | --- |
| C0 — Foundations | Core implementations and representative boundary guards are supported. | Complete public-boundary/adoption review stays #19; conditional molecular-profile coverage stays #49. No claim that every public surface was exhaustively admitted. |
| C1 — Preparation | The explicitly declared 3PTB protein/ligand recipe has executed preparation and traceability evidence. Placeholder mechanisms are removed from current code. | Decide the bounded scientific preparation/scoring profile under #5/#33; do not call field coverage experimental state or model validation. |
| C2 — Redocking | Preserved positive/negative 3PTB searches and separate receiving evaluation support one declared case. | The original human run and current writer/reader composition have different producers. This audit does not execute a new current-composition human experiment or establish multi-complex accuracy. #33/#4 retain that distinction. |
| C3 — Explicit local docking | Explicit boxes, normalized results and backend projections are supported for the box profile. | Richer domains are outside this audit. Construction provenance for a derived box is a C4 issue, not evidence of wrong box coordinates. |
| C4 — Selection-derived domain | Geometry and unit/serialization behavior are supported. **The complete gate is partial.** | New #55 owns absent derivation provenance; visible observation remains deferred under #52. |
| C5 — Result/provenance | The preserved case bundle answers source/state/preparation/domain/backend/score questions. | A standalone prepared-result JSON lacks original-file fingerprints; the bundle supplies the source binding. General prepared-input provenance remains #4. |

“Supported” means evidence exists for the stated profile, not unconditional gate
acceptance or a maturity score. C1/C2 scientific limits and C4's missing record/
observation prevent declaring the whole Core complete. C6 remains explicitly
**deferred**, not failed and not silently accepted.

### Evidence identities

- **E1 — Current implementation qualification:** runtime source
  `c9c819688a8ff9a9d662af842ef2c82627ceb8b3`, qualified MolSysMT
  `e395e52646dab2ecb480d3d67aa7254be99b8524`.
  [Terminal #49 receipt](https://github.com/uibcdf/dockingmt/issues/49#issuecomment-6480128177):
  1,279 source tests per Python 3.11–3.14, all seven CI jobs, actual coverage
  upload, and 209 ordinary-installed cases. These are prior executed gates,
  reused because this audit changes documentation/evidence only.
- **E2 — Original molecular admission:** [3PTB admission](3ptb_admission.md)
  and [frozen protocol](3ptb_prospective_protocol.md). Explicit dry receptor,
  histidine/CYX/terminus choices and benzamidinium +1, not inferred protonation.
- **E3 — Original search and separate receiving:** [24 searches / 167 poses](3ptb_search.md).
  Original archive SHA-256 `97104903c93b3f7a729a5a6ac196cdb7b59d686e318efdcf324f70131abba1f2`;
  separate evaluation `8351d4db25b2ad25de413158a8d3dc0a5e4fee31678ea06649994a1832fa53af`.
  Original reporting failures remain original failures.
- **E4 — Human workflow:** [executed notebook](human_3ptb_workflow_2026-10-20.ipynb)
  and [qualification](data/human_3ptb/qualification_2026-10-20.json).
  Wheel producer `1decee504b112cfd92026c52dcbe22449de30f4f`, MolSysMT
  `c35252d89a28a8faff11e0014bda91312167f549`: one registered fresh search,
  five poses, then recovery of that same result after an informative stereo
  admission refusal. Neither producer nor provider is relabelled as E1.
- **E5 — This record audit:** [retained evidence](data/core_mvp_audit_2026-10-28/manifest.json).
  Six existing ordinary-installed controls pass; 36 other collected tests are
  explicitly deselected, zero skips. One guard receives all 24/167 saved cases
  while forbidding preparation, scoring, maps and searches. Standard-library
  record inspection authenticates 16 human-manifest members and submitted-byte
  hashes, checks score contexts/states and preserves a before/after file ledger.
- **E6 — Executed domain probe:** [record](data/core_mvp_audit_2026-10-28/domain-probe.json)
  confirms geometry roundtrip but absent source/selection/frame/padding fields;
  [#55](https://github.com/uibcdf/dockingmt/issues/55) owns the missing descriptor.
- **E7 — Scene construction only:** [scene record](3ptb_scene.md) and saved
  scene notebook. Python construction/export is not a browser observation.

## Criterion-by-criterion review

The criterion numbers below follow each gate's existing bullet order.

| Criterion | Concrete evidence | Limit / owner |
| --- | --- | --- |
| C0.1 Implementable core concepts | `DockingProblem`, `VinaProtocol`, `DockingPose`, `DockingResult`, `BoxRegion`; E1/E4. | Present box/rigid-receptor workflow, not all design horizons; #28. |
| C0.2 Isolated Vina adapter | [adapter](../../dockingmt/engines/vina.py), backend abstraction and capability guards; E1. | No second engine claimed. |
| C0.3 Backend files are not the scientific model | Problems/domains/results serialize independently of staged PDBQT; E4/E5. | External PDBQT remains an explicitly limited input profile; #49. |
| C0.4 Molecular identity survives conversion | Prepared source keys, completed native maps and known-source reading; E1. | External/partial/multiple-state verifier retirement stays #49 and MolSysMT #521. |
| C0.5 Run provenance | E4 result plus admission/qualification bundle; E5 verifies hashes and state links. | Standalone source-file provenance is conditional; #4. |
| C0.6 Capability validation | [backend checks](../../dockingmt/engines/base.py), `test_capability_validation`; E1. | Supported capabilities only. |
| C0.7 Physical quantities | Explicit length/energy boundaries and nondefault-unit guards; E1/E5. | No new global policy or unit convention. |
| C0.8 ArgDigest boundary | `dock`, protocol, preparation and geometric entry points; [argument guards](../../tests/test_argument_contracts.py). | Representative paths inspected; complete public-surface/adoption review remains #19. |
| C0.9 Optional providers / DepDigest | Lazy Vina/viewer imports and [missing-dependency guards](../../tests/test_support_contracts.py); E1. | Availability is not scientific suitability. |
| C0.10 SMonitor diagnostics | Catalog, structured errors, reconstruction and warnings in the same support guards; E1. | No exhaustive diagnostics review or new guide/tool adoption. |
| C0.11 Inspectable defaults | Serialized protocol and actual resolved native calls/engine info in E4/E5. | Wrapper defaults retain their original engine/version; not universal scientific recommendations. |
| C1.1 Inspectable inputs/transforms | E2/E4 record source bytes, template/H/model reports, charge/type and projection choices. | Recipe is an explicit hypothesis. |
| C1.2 Identifiable prepared states | E4 receptor and partner state IDs agree across problem, preparation and all five poses; E5. | Native state labels can be absent; do not infer experimental validity. |
| C1.3 Traceable backend representation | Captured role payloads and hashes, prepared/source axes and E2 admission; E5. | Source-file binding uses the full case bundle; #4. |
| C1.4 Clear preparation errors | Missing Q/named types, provider refusal, stale evidence and unknown H inventory guards; E1. | Remaining scientific acceptance is not an error-repair implementation; #5/#33. |
| C2.1 Normalized multiple poses | E3 has 167 poses, E4 five; existing saved-result receiving/roundtrip in E5. | Original producer failures remain in E3. |
| C2.2 Scores/ranks preserved | E5 matches all four stored score columns to the original five-column backend rows and score contexts. | No rescoring or reranking. |
| C2.3 Native-reference RMSD | E3/E4 preserve the registered nine-heavy-atom positional criterion and separate optional symmetry. | No fitting, outcome-selected cutoff or symmetry replacement. |
| C2.4 State identity retained | E2/E4 declared receptor/ligand state IDs; explicit multi-structure rejection guard in E5. | pH/state suitability remains a hypothesis, not an automatically solved problem. |
| C2.5 Reconstructable configuration | E4 saved-result recovery plus E5 current receiver; actual protocol/bytes/defaults are stored. | Recovery is not a new native experiment on E1's composition. Broader replay/source persistence stays #4/#33. |
| C3.1 Backend-independent box | `BoxRegion`, quantity/geometry contracts and explicit E3 native/displaced domains. | No richer-domain delivery inferred. |
| C3.2 Common result model | E3/E4 both use `DockingResult`; E5 verifies ordinary installed roundtrip. | Scientific arms remain separately labelled. |
| C3.3 Inspectable engine conversion | Physical domain, rounded backend box, units and resolved calls stored in E3/E4. | Geometry records do not contain a complete construction recipe; #55. |
| C4.1 Deterministic/inspectable construction | Public MolSysMT coordinate access, geometry guards and E6. | Resulting geometry is inspectable; construction provenance is incomplete; #55. |
| C4.2 Visualizable domain | E7 constructs/exports the scene through the existing add-on. | Rendered visibility/framing/controls remain unobserved and deferred; #52. |
| C4.3 Conversion without lost source/provenance | Physical/backend geometry persists in E3/E4; E6 identifies missing derivation. | **Partial:** selection, frame and padding do not survive in a standalone domain descriptor; #55. |
| C5.1 Source molecules/states | E4 state labels, source keys and E2/E4 qualification/source hashes form a traceable bundle. | Prepared-result `source_fingerprint` fields are `None`; not a self-contained original-file record; #4. |
| C5.2 Receptor state | Explicit dry/HID57/HIE40/HIE91/CYX/terminus state ID and recipe in E2/E4. | Declared choices, not experimental pH inference. |
| C5.3 Preparation history | Named Q/type/H/projection/torsion policies and original versus derived reports; E1/E4/E5. | Stored completeness does not certify the chemical model; #5/#33. |
| C5.4 Searched domain | E4 physical box and actual rounded Vina projection, linked to submitted inputs. | Generic derived-domain recipe is the confirmed #55 gap. |
| C5.5 Backend/parameters/seed | Vina 1.2.7, original component/provider versions, protocol, seed and resolved calls; E4/E5. | Current E1 qualification is a different context, not a replacement original identity. |
| C5.6 Score producer | Per-pose named descriptors include method/version, component, units and matching input hashes; E5. | Docking scores are not affinity measurements; no universal model suitability claimed. |

## What is actually resolved and what stays open

The original #5 mechanisms are absent from current supported preparation: no
implicit zero substitution, no name-derived typing, no local H-parent charge
aggregation, and no consumer molecular serializer. Explicit supplied zeros remain
valid data; requested provider operations fail transparently. These corrected
mechanisms are not a reason to repeat molecular implementations in DockingMT.
#5 stays partial for bounded preparation/scoring-profile acceptance, not because
those old mechanisms still run. Complete-source pose reading is adopted; remaining
partial/reference reading is proposed in MolSysMT #521.

#4 has structured selections, frames, declared states, named preparation,
submitted bytes and score history. What remains is explicit handling/acceptance of
source/decision provenance across arbitrary prepared inputs and replay contexts.
The full 3PTB bundle supplies original-source context absent from the standalone
prepared result. This audit neither invents a native molecular fingerprint nor
claims a general molecular snapshot format.

#33 has delivered/received provider formats and broad consumer migrations.
Its remaining scope is an explicit supported chemical/representation profile,
remaining input dialects, the #521 boundary and scientific limits. Earlier
“projection/maps/writers not implemented” statements are historical, not current
blockers. The complete-disconnected single-ROOT restriction remains MolSysMT #214.

## Ordered next actions

1. **Settle and implement the bounded #55 domain-provenance contract.** Preserve
   explicit-box/legacy readability and delegate molecular access to MolSysMT.
   This is an actionable nonvisual DockingMT step independent of #521.
2. **Reconcile the declared supported profile under #5/#33 and prepared-source
   provenance under #4.** Use the positive/negative controls and stated uncertainties;
   the first path need not solve all chemistry. If a current-composition admission
   or new scientific control is needed, register it separately before execution;
   do not relabel E3/E4 as new experiments or tune the old population.
3. Receive public partial/reference tools from MolSysMT #521 when delivered;
   qualify actual calls before retiring the remaining verifier. Multiple native
   states retain their own explicit admission question under #49/#33.
4. Resume the saved scene observation only on the maintainer's decision. C6 and
   the visible part of C4 remain #52. Public artifact/release work retains its own
   #30/#47 gates; this audit neither publishes nor creates an extra publication rule.

The human-first, public-API workflow is consistent with the previously inspected
vertical-pilot direction. No private pilot text/data is copied, no pilot execution
is claimed, and no new backend, flexible-receptor, screening or pharmacophore
feature is authorized merely by this audit.
