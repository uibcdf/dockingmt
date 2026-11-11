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

Current status: the canonical clean rename and conceptual design are implemented;
finish qualifying the final payload and deliver the two coordination issues.
