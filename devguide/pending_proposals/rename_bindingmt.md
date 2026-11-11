---
summary: Adopt BindingMT as the canonical component identity and expand its molecular binding domain.
issue: uibcdf/bindingmt#108
status: active
opened: 2026-11-11
closed:
verification: measured
area: [architecture, public-api, interoperability]
guard: tests/test_bindingmt_identity.py
normative:
blocked_by: []
supersedes: []
---

# BindingMT identity and scientific scope

The maintainer accepts BindingMT and its expanded domain on 2026-11-11, then
explicitly chooses a complete early-development rename with one canonical
identity and no compatibility layer. No external consumers require deprecated
imports. The earlier local compatibility draft is superseded by that direction.

The maintainer has renamed GitHub to `uibcdf/bindingmt`; numeric repository
identity 1380446251, issues and Git history are retained. Local origin follows
that repository. The current workspace directory remains open at its existing
filesystem location; it does not define package/repository identity.

## Delivered identity and accepted domain

Canonical distribution/import is `bindingmt`; the viewer package, addon/workspace
and state identity use `molsysviewer_bindingmt` / `bindingmt`. Public component
exception names, diagnostic IDs, producer fields, development-helper namespace
`bmt_test_support`, active configuration, tests and documentation follow the same
identity. Docking-specific problem/protocol/result names remain meaningful within
this broader domain; they do not become universal binding classes.

Accepted scientific operations are molecular docking, fixed-identity complex
prediction, complex refinement, binding free-energy calculation and prediction,
and binding-interface characterization. Vision/scope/model/architecture explicitly
separate their scientific promises, states, conditions, molecular correspondence,
uncertainty and current implementation/qualification. Future scope does not add
empty runtime classes, implement providers or establish new automatic release
gates. #109/#110 remain separate provider proposals.

MolSysMT retains general molecular identity/preparation/conversion/maps/analysis;
TopoMT and specialized numerical/visual owners retain their kernels. BindingMT
owns binding-specific operations, association, adaptation and interpretation.
PeptideMT, Praxis and the other MolI owners retain their established boundaries.

## Qualification and handoff

The initial compatibility draft passed 4 identity and 60 source/admin controls;
those are superseded evidence, not qualification of the final clean rename.
Final qualification must cover canonical import/record/optional independence,
addon state, current metadata, helper/input hashes, applicable ordinary tests,
packaged resources and a fresh committed export. No molecular campaign, new
engine/model acquisition or native build is needed. Local cells remain serial,
CPU 0/nice 10/native workers 1, with a monitored 13 GiB reserve and bounded owned
memory. Preserve failed attempts and state missing remote/platform evidence.

After component delivery, close #108 and publish the maintainer-requested MolI
and MolSysSuite issues with the domain decision and central registry, policy,
guides, environment, dependency and consumer receiving actions. These are
separate owner handoffs; component delivery does not claim completed central
adoption or a public package/release.

Current status: canonical clean identity and domain are implemented. The renamed
private wheel has exactly 67 runtime paths. Shared editable replacement passes
pip check; 74 installed core controls and 48 real-Vina/dependency/viewer controls
pass, and 23 Node26 DOM cases pass. A wider 29-module attempt is incomplete after
signal 9 near its 120 s CPU budget, with no available-memory reserve interruption.
It retains one stale derived-presentation failure, now corrected by regenerating
its summaries without molecular operations. Raw scientific observations and
producer identities remain unchanged; current administrative presentation owner,
schema and producer hashes follow BindingMT. Complete the full ordinary test
selection as smaller serial groups, then deliver the two coordination issues.

A subsequent ten-module attempt is also incomplete after native SIGABRT at the
top-level API control, with no observed reserve/RSS interruption. Inspection
found several pre-existing native tests left Vina's `cpu=0` automatic thread
selection active despite process affinity. Those tests now explicitly request
`cpu=1`; the API default remains documented and its wider scheduling risk is
owned by #28. Do not infer a new runtime CPU policy or a passing interrupted
selection from this correction.

The corrected ten-module group passes all 260 cases on source `a6f0ff95`, with
zero skips/failures and 5 provider warnings. The next scientific group exceeds
its task-local 1 GiB RSS budget (sampled 1,200,123,904 bytes) and is stopped by
the supervisor, preserving over 53 GiB available memory. Its incomplete stream
does not qualify any complete selection. Do not automatically restart that
scientific group; the full ordinary/scientific gate remains missing under #28.
Continue the applicable bounded identity/API/records/addon and administrative
controls as a separate targeted selection, with explicit exclusions.

Final presentation cleanup also corrects BMT decision anchors and the component
label in the synthetic methanol fixture's title header. Coordinates, topology,
chemical annotations and original numerical observations are unchanged. Its
declared support hash follows the changed title bytes.

Later targeted controls expose a missing `unyt` test backend in the new private
receiver and an over-renamed schema expectation for the authenticated historical
P59 input. Complete previously reviewed unyt/SymPy/mpmath wheels are received
only in that private prefix. The original prior projection is frozen at its
unchanged SHA-256; its full schema/producer identity remains authenticated rather
than relabelled. Canonical current text/figure presentations are regenerated with
zero molecular imports/operations and identical saved numerical observations.
The support declaration now has 626 inputs, including that frozen original.

The saved human-case receiver also retains its original producer/schema
vocabulary as a hash-checked evidence descriptor, independently of the canonical
current runtime and output identity. Its guard compares the complete original
version record instead of assigning the new component name to an old producer.
That descriptor brings declared support to 627 inputs. CLI controls invoke the
actual staged, unshipped helper file; the source-only reporting CLI child opts
out of the installed worker's safe-path environment while runtime import-origin
checks stay isolated. These are qualification/support corrections, not public
compatibility packages or renamed historical measurements.
