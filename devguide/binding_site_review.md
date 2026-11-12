# Binding-site revision 2: contribution audit and worked handoffs

Owner: [BindingMT #111](https://github.com/uibcdf/bindingmt/issues/111), 2026-11-11.
Status: **design review, before implementation**. The
[main proposal](binding_site_design.md) owns the scientific contract. This
companion traces the requested changes and gives concrete review material.
“Documented” below means a proposed contract/example, not an executed receiving
test, a frozen wire schema or another component's acceptance.

The initial second draft at
[`54cfab9`](https://github.com/uibcdf/bindingmt/blob/54cfab985fd79c9e10922d412b068048412f1d0a/devguide/binding_site_design.md)
had the right architecture but left examples, definition/evidence identity and
consumer reference behavior underspecified. This audited edition corrects those
gaps while preserving the useful small core and the maintainer's ensemble scope.

The subsequent TopoMT, PeptideMT and PharmacophoreMT responses each consider
their original requests addressed at design level and recommend bounded B/C
increments. The [implementation/work plan](binding_site_implementation_plan.md)
records their remaining agreements and offered inputs. Its reviewed sequence
assigns the local core, selection/foreign adapters, actual application checks
and first consumer cases explicit work and milestones. No receiving pass is
inferred from those positive reviews or this planning refinement.

## 1. Request-by-request disposition

| Contribution/request | Revision-2 coverage and correction | Remaining acceptance |
| --- | --- | --- |
| PeptideMT 1: ordinary definition/evidence API | Main section 7 supplies a criterion, attributed observation, inspection, save/read and immutable revision. The audit explicitly preserves the observation's original claim association; reuse is a new interpretation. | Implement the public route and show that adding geometry gives no stronger support. |
| PeptideMT 2: molecular handshake and requested/resolved/used membership | Main sections 4/7 specify scoped checks and missing/contradictory behavior. Worked case R below covers insertion codes/gaps, extraction, permutation, explicit expansion and generated atoms. Caller maps and trust preconditions are distinguished from verified origin. | MolSysMT agreement on admitted descriptors/checks; implementation must demonstrate match, missing proof and contradiction on real native inputs. |
| PeptideMT 3: effective information consumed | Main section 8 and case P inspect effective payloads with admitted and evaluation-only information present. Projection/export consumption is separated from evidence about execution/enforcement. | A consumer-owned supplied/absent receiving control; no general leakage certification is claimed. |
| PeptideMT 4: non-box meaning and placement | Direct region projection remains independent of boxes. Later profiles distinguish candidate populations, alternatives, every-entry requirements and pair restraints, plus placement/sampling policy. | Provider-specific receiving under #109/#110; it does not block the data-only core. |
| PharmacophoreMT 1: concrete direct handoff/public construction | Case H follows selected view → resolved region → recognition context → native inventory → selected hypotheses, then owner save/read and a saved site association. No box is required. | Implement the BindingMT projection and qualify it against pinned native operations. |
| PharmacophoreMT 2: chemical selection/state guarantees | Regional membership, recognition participants and retained features stay separate. Original→target structure/state maps are explicit. State-dependent membership cannot be silently reinterpreted by overriding a selector. Geometry-only membership policies need their own qualified profile. | Boundary-feature, mixed-state, missing-association and contradiction controls; native admission stays mandatory. |
| PharmacophoreMT 3: meaning in both directions | Main sections 11.2/11.3 and case H preserve native hypothesis references, essential/optional status, weights, exclusions, alternatives and application intent. Unknown native meaning is reference-only. | Native-reader controls including zero-weight essential sites and exclusion veto; no competing BindingMT matcher. |
| PharmacophoreMT 4: saved association/lifecycle | S0 → H → S1 keeps exact artifact references without circular hashes or a reverse dependency. Existing H remains tied to S0 when unrelated S2 is added. | Qualified save/read and changed-source/state/map cases without recognition replay. |
| PharmacophoreMT capture limitation/early B/C case | The 256-total-source-atom, 64-feature, 2-MiB profile stays explicit and narrower than general extraction. Case H uses an admitted source; selection cannot bypass the cap. | Early bounded receiving; larger-source and dynamic profiles remain owner-led extensions. |
| TopoMT 1: versioned receiving/minimum records | Main section 11.1 now uses a BindingMT-owned profile name and explicit admission/refusal rules. Case T supplies a center-only specimen and a normal saved-record bridge route. | An actual source-pinned ProviderRecord round trip after implementation. Native DFND receiving stays coordinated with TopoMT #60. |
| TopoMT 2: view relations/composites/quantity meaning/paths | Main section 3.1 closes relation direction/domain and separates membership coverage from spatial support. Grouping, union and alternatives differ. Provider/DFND/box volumes and ordered paths retain owner meanings. | Qualified relation/geometry operations; heterogeneous owner records review the schema without requiring all adapters first. |
| TopoMT 3: context/dependency coverage | Main section 4 separates saved geometry, molecular correspondence and finding applicability. An input atom outside lining remains a required adversarial case. Count/label/map-range checks cannot authenticate the source. | Owner-defined input/query coverage for claims about a current finding; missing proof refuses that claim. |
| TopoMT 4: intent/information/attribution | Main section 8 records effective choices, loss, roles and actual enforcement evidence. Original citations/versions remain; reading earns no new engine credit. | Ordinary problem/result propagation and supplied/absent controls. |
| TopoMT 5: heterogeneous receiving cases | Center-only and molecular-map specimens are concrete; main section 12.1 retains incomplete support, DFND, supplied-assembly interfaces and ordered channels as separate cases. | First useful bridge is one admitted case; the remaining bridges are later receiving, not hidden core prerequisites. |
| TopoMT 6: focus, future evidence and ownership | Data-only declaration/replay and explicit BoxRegion projection remain first. Supporting/challenging evidence keeps participant/condition scope as a later extension. | Central agreement and each owner's adoption remain separate; favorable comments do not close them. |

References: [PeptideMT contribution](https://github.com/uibcdf/bindingmt/issues/111#issuecomment-6811981030),
[PharmacophoreMT contribution](https://github.com/uibcdf/bindingmt/issues/111#issuecomment-6812006751),
[TopoMT contribution](https://github.com/uibcdf/bindingmt/issues/111#issuecomment-6812012062).

## 2. Review specimens and their evidence level

The [manifest](examples/binding_site_review/manifest.json) identifies three small
JSON specimens and their exact bytes. They are **authored candidate records**,
not outputs of an implemented BindingMT reader/adapter:

| Specimen | What it makes concrete |
| --- | --- |
| [annotation.json](examples/binding_site_review/annotation.json) | A complete proposed small declaration envelope with original addresses, independent structural scope, unknown support and unresolved mapping; no coordinate copy. |
| [provider_center.json](examples/binding_site_review/provider_center.json) | One explicit-unit center point plus unavailable molecular membership. It models the P2Rank-style distinction with a clearly synthetic owner finding, no provider execution, extent or volume. |
| [resolved_region.json](examples/binding_site_review/resolved_region.json) | Original/current axes, source addresses, a nonidentity atom map, a generated target atom, partial membership, target-local structure/state selectors, expected scoped checks and losses. |

The wrapper's `review_status` distinguishes examples from wire payloads; the
proposed record is under `record`. The manifest and example wrapper are review
packaging, not new public interchange families. Only the center's sealed
PyUnitWizard QuantityRecord is generated through its current public codec and
checked in explicit nm/pm units. The BindingMT envelope/adapter and authored
check outcomes have not been runtime-qualified. These examples deliberately
retain synthetic identities rather than counterfeit provider-run evidence.

File/record digests establish content consistency, not authentic chemistry or
scientific provenance. Relative content references in the examples are explicit
inspection/replay inputs, never permission for automatic file/network lookup.

## 3. Case R: one compact molecular-map example

Source MolSys has six atoms and three source groups, with the following original
author addresses. Native group indices and source residue IDs are different axes:

| Original source address | Source group index | Source atoms | Target group index | Target atoms |
| --- | --- | --- | --- | --- |
| Chain A, ID `12`, empty insertion code | 0 | 0, 1 | 0 | 2, 3 |
| Chain A, ID `12`, insertion code `A` | 1 | 2, 3 | 1 | 0, 1, 4 |
| Chain A, ID `15`, empty insertion code | 2 | 4, 5 | Unmapped: removed by extraction | Unavailable |

The declared source→target extraction/permutation keeps source atoms in target
order `[2, 3, 0, 1]`; target atom 4 was explicitly generated afterward. It has
no source atom and inherits no evidence/confidence. An explicit all-atom
expansion on the current target groups can include it as a new application
member; that is different from inheriting source-annotation atom membership.
An unknown insertion code would remain unknown, rather than matching the
explicitly empty code above.

The requested population contains all three addresses. A complete projection
refuses because ID `15` is unavailable. An explicit partial projection resolves
the two mapped groups and records its narrower meaning. Target atom order is
`[0, 1, 2, 3, 4]`; entry→atom maps retain original request order. Source structure
2 is captured target structure 0, so downstream native calls use local index 0.
The example's state association is declared, not authenticated by authored JSON.
Its assurance scope is `declared_membership_projection` under the supplied-map/
unchanged-input precondition. It would not satisfy a request for verified source
correspondence or current-finding applicability. Actual receiving must obtain
the required native facts; writing an expected `match` in a specimen supplies
no proof. The wrapper explicitly labels those outcomes as authored expectations.

Receiving must distinguish:

- **Match within an admitted scope:** owner-supported source/map/attribute facts
  support the chosen application, under recorded unchanged-input assumptions.
  The example's map-range check is only one such fact, not complete identity.
- **Missing proof:** no insertion-code/source correspondence or required state
  association. Keep the declaration readable and refuse the dependent request.
- **Contradiction:** an available owner map, effective state or required frame
  disagrees. A matching count/name or `declared_frame` cannot override it.
- **Changed source outside exported members:** the map and lining geometry can
  remain unchanged while the original detector input changed. Do not certify a
  current pocket from that limited evidence.

The source facts come from public MolSysMT `get`/`select`, qualified extraction/
permutation maps and structure/state operations, not a BindingMT source parser.
Source numbering/insertion information unavailable in native fields remains an
original annotation plus explicit correspondence; it is not reconstructed by
guessing. Current [native query semantics](https://github.com/uibcdf/molsysmt/blob/aee7aa65da56e896d1cb2d655bf73736f6453a43/devguide/native_queries.md)
and [public state/structure queries](https://github.com/uibcdf/molsysmt/blob/aee7aa65da56e896d1cb2d655bf73736f6453a43/molsysmt/basic/get.py)
are the inspected baseline. A reusable authenticated descriptor remains owner
review, not a new guarantee invented by this example.

## 4. Case T: TopoMT import, replay and ordinary application

The source-pinned receiving plan uses current
[`ProviderRecord`](https://github.com/uibcdf/topomt/blob/3a8ee979db8de6f6345de74558a878bb96ba3234/topomt/third_party/output.py)
and [`ProviderRun`](https://github.com/uibcdf/topomt/blob/3a8ee979db8de6f6345de74558a878bb96ba3234/topomt/provider_output.py).
Its saved-output fixtures and the
[P2Rank quantity/geometry assertions](https://github.com/uibcdf/topomt/blob/3a8ee979db8de6f6345de74558a878bb96ba3234/tests/test_new_provider_evidence.py)
are reusable evidence inputs. No rerun of the original engine is needed.

For the first successful domain bridge, choose an existing saved record whose
mapping/support actually permits it. The following is a **BindingMT API sketch**;
`provider_record`, its matching `system` and the explicit padding are caller
inputs. The adapter parameters also remain proposed:

```python
site = bmt.BindingSite.from_topomt(
    provider_record, molecular_system=system, structure_index=2,
)
print(site.describe())
site.save("received-site.json")
restored = bmt.BindingSite.load("received-site.json")
domain = restored.to_search_domain(
    system, view="provider_membership", method="enclosing_box",
    structure_index=2, padding=declared_padding,
)
problem = bmt.DockingProblem(
    system, partner, search_domain=domain, receptor_structure_index=2,
)
problem_record = problem.to_dict()
restored_problem = bmt.DockingProblem.from_dict(
    problem_record, receptor=system, partner=partner,
)
```

The adapter documents its view key; callers inspect/select it rather than rely
on provider feature ranking. Problem read and a normal result round trip must
preserve the site recipe, original identities/citations and new projection's
own attribution. This is a future receiving assertion, not an executed result
claim. An absent mapping with only a center takes a different path: preserve
the point and explain why exact support/extent is unavailable. A caller-chosen
box around that point is a new explicit approximation/prior, never the original
provider's pocket volume. Saved replay keeps unavailable references intact.

Native DFND, interface and ordered-channel examples remain the separate scoped
cases in main section 12.1. They review the catalogue's breadth without making
every numerical geometry operation a prerequisite for this one bridge.

## 5. Case H: direct native pharmacophore handoff and saved association

Use an admitted prepared MolSys and an explicit site view, with no box step.
Regional membership is retained unchanged. The PharmacophoreMT consumer declares
its recognition-context policy and retained native feature indices. For example,
a regional atom list intersecting only part of a ring needs either an explicitly
expanded complete recognition context or a reported unsupported/omitted feature.
Expanded recognition context does not expand the binding hypothesis or make
every recognized feature essential. Hydrogens are handled by the declared owner
policy, not added silently.

The following combines proposed BindingMT calls with existing public
PharmacophoreMT calls. `recognition_atom_indices`, `requested_families`,
`retained_projection_specs` and `declared_matching_tolerance` are explicit
consumer inputs. Their scientific selection is not supplied by this draft.
Native projection specifications name retained feature indices and required
direction/distance/orientation choices; unlisted features do not become sites.
The later association also receives `recognition_policy_ref` and the original
owner-supplied `original_attribution`; producer identity is not a bibliography.

```python
site.save("site-S0.json")
region = site.resolve_region(
    prepared_system, view="membership", structure_index=0,
    chemical_state="structure", expansion="all_atoms",
)
capture = phmt.modeler.capture_features(
    prepared_system,
    selection=recognition_atom_indices,
    structure_index=region["context"]["target_structure_index"],
    chemical_state=region["context"]["effective_target_chemical_state"],
    features=requested_families,
)
hypothesis = phmt.modeler.from_receptor_projections(
    capture["inventory"], projection_specs=retained_projection_specs,
    radius=declared_matching_tolerance,
)
phmt.io.to_json(hypothesis, "hypothesis-H.json")
restored_hypothesis = phmt.io.load_json("hypothesis-H.json")
```

These native operations are inspected at
[`ecd1694`](https://github.com/uibcdf/pharmacophoremt/tree/ecd16946d64dd5cdc64132b026aaf12be2c0ef3a):
[capture](https://github.com/uibcdf/pharmacophoremt/blob/ecd16946d64dd5cdc64132b026aaf12be2c0ef3a/pharmacophoremt/modeler/feature_capture.py),
[explicit feature projection](https://github.com/uibcdf/pharmacophoremt/blob/ecd16946d64dd5cdc64132b026aaf12be2c0ef3a/pharmacophoremt/modeler/receptor_projections.py)
and [native IO](https://github.com/uibcdf/pharmacophoremt/blob/ecd16946d64dd5cdc64132b026aaf12be2c0ef3a/pharmacophoremt/io/phmt/__init__.py).
Use new owned output paths: the native writer retains its existing file policy.
Native H persistence is not a promise of full feature-inventory persistence;
preserve capture/evaluation/producer evidence through the owner's admitted
record route or an explicit reference, and report unsupported routes honestly.
Do not invent another feature codec or bypass native reader checks.

The initial capture profile's limit applies to the **whole prepared source**:
256 atoms, 64 features and 2 MiB of sealed observation. A small recognition
selection cannot bypass it. A newly extracted system requires its own explicit
maps, chemistry completeness and receiving qualification; it is not a hidden
large-receptor workaround.

Associate already saved S0 and H without changing H or requiring reverse imports:

```python
import hashlib
import json
from pathlib import Path

with Path("region-R.json").open("x") as stream:
    json.dump(dict(region), stream, allow_nan=False)
region_ref = {
    "uri": "region-R.json",
    "sha256": hashlib.sha256(Path("region-R.json").read_bytes()).hexdigest(),
}
source_site_ref = {
    "uri": "site-S0.json",
    "sha256": hashlib.sha256(Path("site-S0.json").read_bytes()).hexdigest(),
    "definition_key": "definition", "view_key": "membership",
}
hypothesis_ref = {
    "owner": "pharmacophoremt", "uri": "hypothesis-H.json",
    "sha256": hashlib.sha256(Path("hypothesis-H.json").read_bytes()).hexdigest(),
}
associated = site.with_evidence(
    key="native-hypothesis-H", claim_ref="definition",
    kind="owner_hypothesis_reference", source=hypothesis_ref,
    participants=("host",), views=("membership",),
    observation={
        "source_site": source_site_ref, "use": "annotation",
        "region_projection_ref": region_ref,
        "binding_support": "unknown",
        "structure_index": region["context"]["target_structure_index"],
        "chemical_state": region["context"]["effective_target_chemical_state"],
        "recognition_policy_ref": recognition_policy_ref,
        "recognition_atom_indices": capture["evaluation"]["selected_atom_indices"],
        "retained_feature_indices": [
            spec["feature_index"] for spec in retained_projection_specs
        ],
        "native_projection_evidence_ref": hypothesis_ref,
        "requested_families": requested_families,
        "capture_evaluation": capture["evaluation"],
        "capture_ref": capture["capture_sha256"],
        "producer": capture["producer"],
    },
    attribution=original_attribution,
)
associated.save("site-S1-associated.json")
replayed = bmt.BindingSite.load("site-S1-associated.json")
print(replayed.inspect())
```

Here `host` is the declared participant key. Native quantity-bearing projection
choices remain in the owner-native hypothesis/recipe referenced by H, rather
than being copied as bare numerical distances into BindingMT. Extra physical
evidence fields require their own shared quantity records/handshakes. The capture
digest alone is not a recoverable inventory or verified prepared source. S1
references S0 and H; H need not contain S1's future digest. Reading S1 invokes no
recognition. H is interpreted only by the native reader under its own profile;
if missing or unknown, the association remains reference-only. Native zero-weight
essential status and exclusion veto require actual owner-reader receiving tests.
They are not inferred from an attribute name or recomputed by BindingMT.

## 6. Case P: effective supplied-site and absent-site requests

The consumer holds an admitted site and a separate evaluation artifact E. Its
provenance can retain both without admitting E to generation. The receiving
control observes these concrete boundaries:

| Field/boundary | Supplied-site request | Independently built absent-site request |
| --- | --- | --- |
| Molecular input | Declared admitted source/structures and maps | Independently declared admitted source/structures and maps |
| Site application | Exact selected site/view/projection and admitted entries | None |
| Effective localization input | Only the explicitly allowed region/domain/contact semantics and chosen parameters | No inherited site-derived field; any required global domain has its own independent policy/provenance |
| Evaluation artifact E | Recoverable provenance/evaluation reference | Recoverable provenance/evaluation reference |
| Exported generation payload | E's coordinates, annotations and localization cues are absent | Both E-derived and previous-request/viewer/site-derived cues are absent |
| Execution/enforcement evidence | Declared by the selected provider profile; record unknowns | Same rule; an absent-site flag alone proves no payload property |

Inspect the final native export/service/library arguments, including selected
molecular structures and auxiliary fields, not only an initial request flag.
Record submitted inputs separately from actual execution/enforcement receipts.
The control does not infer scientific influence inside a black-box program or
certify every possible information leak. No real engine is needed for the
initial data-only export control; live execution has its separate owner gate.

## 7. Remaining decisions for the next owner review

The contributions are represented in the audited design, but these outcomes
remain explicitly open:

1. **MolSysMT:** agree the admitted descriptors and scoped checks for actual
   source/structure/state/map reuse. No universal source receipt or site observer
   has been delivered by this design.
2. **TopoMT:** review the BindingMT-owned receiving profile, relation domains and
   original finding dependency coverage; select one existing saved record for
   the first executed bridge. DFND and other geometry profiles advance separately.
3. **PharmacophoreMT:** review target-local state forwarding, recognition selection,
   exact saved associations and the bounded early native receiving case.
   Ensemble/dynamic hypothesis correspondence remains prospective owner work.
4. **PeptideMT:** agree the effective-input observation boundary and the
   independently supplied/absent cases, with its own permitted-information policy.
5. **MolSysSuite:** record shared acceptance and later component-specific adoption
   for the meanings actually exercised, without waiting for every future consumer.

The next code increment should implement the accepted small profile and produce
the source-pinned receiving outputs above. Documentation coverage, a valid
QuantityRecord, owner review and runtime qualification remain separate facts.
