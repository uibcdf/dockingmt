---
summary: Qualify same-state multi-pose rescoring with explicit reference and comparison evidence.
issue: uibcdf/dockingmt#78
status: active
opened: 2026-11-06
closed:
verification: inspected
area: [scoring, provenance, scientific-validation]
guard: tests/test_scoring_reference.py
normative:
blocked_by: [uibcdf/molsysmt#599, uibcdf/molsysmt#447]
supersedes: []
---

# Same-state multi-pose rescoring

## What

Complete a representative E1 workflow for several existing poses of one
declared ligand state against one rigid receptor, retaining original docking
and named Vina/Vinardo evaluations with explicit comparison/ranking admission.
The [pre-stabilization objective](../PRE_STABILIZATION_PLAN.md) remains broader.

## How

First record native fixed-score reference semantics and inspect supported
molecular tools. Request/receive missing molecular projection and identity
evidence from MolSysMT; then define and execute a bounded registered workflow.
Keep receptor/method/version/state/preparation/grid/weights/reference conditions
explicit and every actual submitted-input hash. Retain missing/refused cases.

## Why

At `530a4cf`, fixed scoring requires a prepared input already matching the pose,
and ranking requires identical declared contexts/state IDs. Distinct input-byte
hashes do not establish chemical equivalence. Vina's current-conformation
reference also differs from docking's shared best-pose convention; merely
comparing equally named numeric columns would conceal that distinction.

## What was refuted

No downstream PDBQT coordinate rewriter, graph fingerprint, molecular matcher
or repair is acceptable. State strings alone do not prove molecular identity.
Removing hashes/editing descriptors cannot establish comparability. No new
generic stage/campaign framework is needed for this bounded workflow.

## Scope and exclusions

Core/Extended functionality targets prospective 0.5.0; 1.0.0 remains after
stabilization. #78 does not accept all E1–E5, scientific accuracy or public/visual
delivery. Preserve fixed candidate `905abc9`, existing receipts and original
scientific producers. Native experiments require a separate declared population
and budget; local qualification remains light, serial and resource-guarded.

## Acceptance criteria

- New reference evidence matches the executed native policy and reported native
  component; legacy records retain their original observations and unknowns.
- Provider-supported projection and identity evidence preserve chemistry,
  source/input/output maps, actual bytes, units and unsupported/partial scope.
- Comparison/ranking admission is justified, explicit, conservative for unknown
  evidence and tested with changed method/state/inputs/reference conditions.
- A registered representative native/installed workflow retains original scores,
  all new named evaluations, failures/denominators, ranking history and detached
  JSON audits, with exact software/artifact/input provenance.
- Appropriate source/installed/scientific gates are executed for their actual
  claims. A planning or metadata slice alone cannot close this report.

## Provider receiving — 2026-11-06

Static inspection uses fetched main `ed09f64539a5af6c1dbe9bd352c7ef65dcd4a7a6`,
separate from qualified runtime pin `00abb958f`. Local sibling worktrees are
preserved behind their remotes; their unrefreshed files are not treated as main.
Public basic tools, `chemical_states.get_atom_correspondences`, PDBQT reading/
writing/maps and existing issues were inspected.

[MolSysMT #599](https://github.com/uibcdf/molsysmt/issues/599) requests a supported
prepared-conformation projection/composition, including partial representations,
map completeness, chemical field/tree preservation and precision/metadata losses.
Existing [#447](https://github.com/uibcdf/molsysmt/issues/447) receives the same-state
identity/equivalence use case; #521 remains the partial/reference reading owner.
These are provider requests, not new-source/runtime acceptance.
