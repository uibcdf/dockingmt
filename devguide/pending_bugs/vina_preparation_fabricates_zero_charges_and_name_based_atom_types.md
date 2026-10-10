---
summary: Vina preparation fabricates zero charges and name-based atom types
issue: uibcdf/dockingmt#5
status: partial
opened: 2026-09-22
closed:
severity: high
verification: measured
area: [preparation, vina]
guard: tests/test_engines.py::test_vina_rejects_provisional_chemistry_from_automatic_and_prepared_inputs
normative:
blocked_by: []
supersedes: []
---

# Vina preparation fabricates zero charges and name-based atom types

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Partial; DockingMT Core MVP work.

## What

The original preparation wrote zero partial charges, guessed AutoDock types from
names and dropped hydrogens by name. The dated slices below describe adopted
provider capabilities. Current preparation requires named MolSysMT types;
missing-charge placeholders and broader scientific qualification keep this issue partial.

## How

Replace these assumptions with validated MolSysMT parameters and a documented PDBQT projection. Check that charge and typing schemes are declared and compatible with the selected Vina scoring mode; until available, reject incomplete inputs with actionable diagnostics.

## Why

The generated PDBQT can be syntactically accepted while misrepresenting the prepared receptor or ligand chemistry.

## What is measured and what is assumed

**Inspected:** Source inspected at dockingmt/preparation/ligand.py and receptor.py; scientifically validated impact and numerical score differences have not been measured.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

A passing docking run was rejected as proof of chemical correctness because Vina can process a chemically misparameterized PDBQT.

## Scope and exclusions

Vina input chemical parameterization; general charge models, AutoDock typing, and atom mapping are owned by MolSysMT.

## Acceptance criteria

- No supported Vina preparation path silently substitutes zero charges or name-derived chemistry when required input is absent.
- Focused ligand and conventional protein-receptor tests cover nonzero charges, polar hydrogen retention, chemically distinct atom types, and the selected scoring mode; unsupported inputs fail clearly.

## Dependencies and risks

Related tracked work: uibcdf/dockingmt#3
Cross-component implementation links: uibcdf/molsysmt#214, uibcdf/molsysmt#221, uibcdf/molsysmt#222, uibcdf/molsysmt#223.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.

## 2026-09-22 progress

The MolSysMT input implementation now derives element identity from the source,
retains polar hydrogen atoms, preserves source partial charges when present, and
records when zero placeholders or heuristic AutoDock types were used. The
remaining heuristic is based on element, group, and available aromaticity, not
atom names. Neither this heuristic nor the zero-charge fallback is a validated
parameterization.

Vina now rejects DockingMT-generated provisional preparations by default, for
both automatic MolSysMT input and previously created prepared objects. The
caller can explicitly opt into exploratory docking with
`VinaProtocol(allow_provisional_preparation=True)`; the policy and assessment
are serialized in result provenance. Existing external PDBQT inputs remain
accepted with an `unassessed` chemistry assessment. This addresses silent use
of DockingMT's known placeholders, but does not satisfy the full acceptance
criteria: validated receptor and ligand parameterization, scoring compatibility,
and scientific preparation tests are still needed. The provider requirements
remain tracked by molsysmt#221 and molsysmt#222.

## 2026-09-26 pinned 1IEP preparation audit

The [reproducible audit](../validation/1iep_preparation_audit.md) compares native
MolSysMT-based preparation against the official example's aligned PDBQT files. All
40 ligand and 2,702 receptor PDBQT atoms match by coordinate. Native charges are
zero for all retained atoms, whereas the published files have nonzero charges on
40 ligand and 2,669 receptor atoms. Four ligand and 24 receptor atom types differ.
The native ligand has zero branches and torsional degrees of freedom; the published
ligand has seven of each. This measures disagreement with a published input, not
the scientific accuracy of either parameterization or a docking score effect.

MolSysMT's public `build.get_missing_bonds` repaired the two absent receptor
hydrogen bonds required by the native writer. No local replacement was needed.
The general missing capabilities remain MolSysMT
[#221](https://github.com/uibcdf/molsysmt/issues/221) for charges,
[#222](https://github.com/uibcdf/molsysmt/issues/222) for named AutoDock typing, and
[#224](https://github.com/uibcdf/molsysmt/issues/224) for rotatable bonds and rigid
fragments. Until a scientifically supported path is available, the default Vina
rejection and this issue remain open.

The subsequent explicit-torsion implementation can reproduce seven 1IEP PDBQT
branches, but leaves the zero-charge and atom-type differences in this report
unchanged. Flexible-tree acceptance is therefore not a resolution of this issue.

## 2026-10-03 stored-field coverage consumption

Preparation now consumes MolSysMT's read-only `physchem.get_chemical_readiness`
from source `3edbf8ad0`, retaining compact field/origin counts, selected state/frame,
explicit H count, connectivity integrity counts and unassessed checks before
hydrogen projection. The [consumer record](../validation/chemical_readiness_consumption.md)
and executed notebook distinguish formal charges from partial-charge assignment
and stored presence from scientific validity. No universal ready flag, chemical
repair or implicit parameterization is added.

The default Vina safeguard and provisional opt-in remain unchanged; the real-engine
guard now verifies summary persistence in saved-result provenance. Seven new
consumer cases cover source/state/axis identity, incomplete/conflicting coverage,
JSON serialization, immutability and a non-default unit policy. All 37 focused
cases pass against an isolated snapshot of the pinned provider in 23.05 s.
Validated chemical preparation remains open; this issue stays partial.

The complete local gate passes 514 tests without skips in 69.45 s on Python
3.14.7 with Vina 1.2.7 and twelve known provider warnings. The notebook executes
against the exact provider snapshot; lint, formatting and index/diff checks pass.

## 2026-10-03 exact receptor residue coverage

Receptor preparation now consumes MolSysMT `build.get_residue_chemical_coverage`
from exact source `e8e4fff22`, reusing its embedded stored-field audit. The
[consumer record](../validation/receptor_coverage_consumption.md), executed
notebook and raw cases/profile retain original 181L/1IEP counts, exact MSE/SEP,
incomplete ALA, unknown PTR, water/zinc, source-state selection and read-only/unit
checks. Compact provenance retains counts and template digests before hydrogen
projection; unsupported chemistry is unassessed, not parent-substituted.

Original 1IEP has 274 assessed heavy-atom groups but unassessed H/protonation and
still fails preparation on absent hydrogen attachment bonds. No repair or charge/type
qualification is introduced. Real Vina guards retain default provisional rejection;
automatic and supplied receptor coverage survives saved-result serialization.
All 522 tests pass without skips on Python 3.14.7 with Vina 1.2.7 against the exact
provider archive. CI/full-matrix pins advance to that source. This is a bounded
consumer qualification; validated preparation and this issue remain partial.

## 2026-10-03 PDB inference-profile correction

The [reader-policy diagnosis](../validation/pdb_bond_inference.md) reproduces the
hosted/local discrepancy by blocking only OpenMM imports. The provider audit
correctly reports absent stored connectivity as incomplete; the hosted test
environment had omitted the engine used by the reference PDB profile. OpenMM is
now declared in the shared test environment, and two original-source controls
protect explicit-only behavior without repairing the graph. It is not a new
runtime dependency or validated parameterization.

MolSysMT #304 owns the requested selectable native alternative, retention of
OpenMM, direct-file flag propagation and explicit evidence/failure semantics.
The existing native candidate tool exactly matches the 181L protein reference
edge set but differs by 18 pairs on original 1IEP, with warnings retained. The
executed notebook/raw probe preserve source maps and those unresolved differences.
No provider implementation is assumed delivered; this issue remains partial.

## 2026-10-03 explicit chemical-template consumer qualification

The [consumer record](../validation/chemical_template_consumption.md), executed
notebook and raw indexed reports qualify public MolSysMT assessment/application
from exact source `c19a47ada0`. The existing `prepare_ligand` boundary consumes the
returned native system. Original 181L BNZ accepts a declared heavy-only template;
permuted 5X72 P59/P69 absent-field controls preserve both poses, IDs and chosen
state while receiving the expected R/S assignments. Original native SDF versus
adapter-template aromatic encodings remain unassessed; no normalization is added.

Fourteen focused consumer cases protect conflicts, absent edges, exhaustive H
mapping, matching explicit fields, unselected state preservation and non-default
units. A real Vina test retains default provisional rejection and saved-result
assessment after explicit exploratory opt-in. Reports remain separate workflow
records because MolSysMT #298 has no native report attachment. Charge/type
qualification and general preparation remain open; this issue stays partial.

The full source-qualified gate passes 538 tests without skips in 108.31 s on
Python 3.14.7, using an isolated MolSysMT archive and the existing CI viewer pin.
The executed notebook asserts the requested Conda interpreter. The initial live
viewer profile exposed an in-progress explicit frame-pairing requirement under
molsysviewer#151; its checkout is preserved and the separate consumer migration
is retained in the validation record. Ruff, indexes and diff checks pass.

## 2026-10-03 public preparation assessment

`dockingmt.assess_preparation` now exposes the existing provisional preparation
classification before engine execution. Vina consumes the public operation and
retains its bounded, detached `assessment_report` with stable reason codes and
declared charge/type sources, preserving the existing provenance fields and
default rejection policy. External PDBQT representations stay unassessed;
explicit zero charges alone do not imply placeholders. No molecular operations
or provider chemistry checks are duplicated.

The [contract](../validation/preparation_assessment.md) and executed notebook
document the public boundary. Thirty focused cases pass; the full source-qualified
gate passes 564 tests without skips in 100.53 s on Python 3.14.7 using unchanged
CI provider pins. Fresh-process absence of engine/viewer, malformed declarations,
detachment, real Vina persistence and template-transfer safeguards are covered.
This issue remains partial: public inspection does not deliver validated chemical
parameterization or scoring compatibility.

## 2026-10-03 native capability review from Meeko source

The [source review](../validation/meeko_native_capability_review.md) maps useful
Meeko methods to public native MolSysMT operations (#221–#224) and DockingMT
protocol decisions. The user explicitly excludes importing Meeko. Named chemical
typing is the recommended next slice; source inspection identifies N/NA and S/SA
context, ordered rule precedence, charge-preserving H projection and explicit
rotatable-bond policy as concrete requirements. Existing local projection and
fragment consumption are distinguished from pending provider tools.

Vina/Vinardo do not require computed partial charges; a future scoring-aware
policy must distinguish that fact from chemical validity and AutoDock4 needs.
No gate is relaxed here. Metal/selenium charge approximations, integer-charge
rectification and regenerated export hydrogens are not adopted implicitly.
This is inspected design evidence, not runtime equivalence or a new dependency.

## 2026-10-04 named-charge consumer qualification

The bounded [consumer slice](../validation/named_partial_charges.md), tracked
by dockingmt#40, preserves public MolSysMT #221 model/software attribution,
original coverage and source indices through selected projection and existing
nonpolar-H charge transfers. Public `audit_preparation_charges` observes current
numeric binding, conservation and actual three-decimal PDBQT rounding. The
executed notebook qualifies methanol, selected OH, flexible 5X72 and explicit-H
1VII AMBER14 (+2 e before export; +1.988 e after rounding).

Public MolSysMT indexed extraction owns stale molecular binding detection. No
charge calculation, graph validator, implicit model or renormalization is added
in DockingMT. CI pins advance to qualified source `7894435e748bc55254b6c3d2b63ae82c101e5774`;
dirty sibling work is preserved. Typing (#222), general preparation/scoring
compatibility and provider H/export projection (#223) remain separate. The
default provisional gate is preserved; this owning issue remains partial.

## 2026-10-04 explicit fixed-state H/charge stages

The [bounded consumer contract](../validation/ligand_preparation_stages.md),
tracked by dockingmt#41, adds opt-in provider option mappings to existing public
`prepare_ligand`. MolSysMT H addition precedes named charges, defaults to strict
attribute preservation and retains original reports/credit and composed input,
expanded, prepared and written correspondence. Generated H has no original input
index; no local chemistry or geometry algorithm is introduced.

The supported methanol control preserves original identity/coordinates, adds four
H, retains the polar H and conserves 0 e in the existing charge projection.
Idempotence, explicit attribute loss, non-default units, unchanged provider errors,
result persistence and the default provisional typing gate are guarded. The full
source-qualified suite passes 887 tests without skips on Python 3.14.7/Vina 1.2.7.
Original 181L BNZ remains a negative control pending MolSysMT #314 bond aromaticity;
the notebook retains the rejection and unchanged pose. #41 and this owning issue
remain partial. Published source pins are unchanged and sibling work is preserved.

## 2026-10-06 named-type consumer qualification

[DockingMT #43](https://github.com/uibcdf/dockingmt/issues/43) consumes valid
named MolSysMT AutoDock4 assignments, including projected parent labels, and
adds explicit optional typing after requested ligand H/charge stages. The
[contract and executed evidence](../validation/named_autodock_types.md) cover
independent N/S environments, F/P polar H, original BNZ (12 evaluated/six aromatic
C), flexible written order, pm/coulomb units and native stale/consumer mutation
rejection. Complete provider attribution and atom maps survive saved result JSON.

A real default Vina run with named/charged synthetic receptor and partner returns
one pose without provisional opt-in. Known heuristic-type reasons disappear for
this bounded route; scientific preparation assessment remains unassessed. The
full local source suite passes 952 tests without skips on Python 3.14.7/Vina 1.2.7.
Original BNZ's earlier H failure was resolved under #42, preserved in local commit
`6f193fb` and separately dated notebooks/receipts.

This owning issue stays partial: conventional protein-receptor/scoring scientific
qualification, broader chemistry coverage, provider atom/charge-preserving export
MolSysMT #223 and public/installed/hosted checkpoints are not established by this
consumer slice. Untyped workflows keep their existing default safeguard.

## 2026-10-06 real protein and ligand composition

The [explicit 181L receptor workflow](../validation/181l_receptor_workflow.md)
advances the conventional-protein boundary beyond the toy controls: 1,289
observed heavy atoms, public native OXT repair, one declared 162-residue peptide
state, 1,313 generated H, named Gasteiger charges and chemical_environment@1
AutoDock types. The 2,603-atom assignment projects to 1,615 receptor atoms,
conserving +8 e before three-decimal export (7.943 e after rounding). Native
source IDs/coordinates and all transformation decisions/maps are retained.

Generated names exposed malformed receptor PDBQT columns, tracked separately
in #44. The consumer writer rejects overwide names; this fixture explicitly
names generated H through the provider setter before mechanical assignments,
with original names/IDs/history retained. No implicit preparation rename is added.
Six real default Vina runs with original BNZ retain exact submitted bytes and
saved-result provenance; all return a pose within the declared positional RMSD
cutoff, while one first pose fails it.

Named models remove the known placeholder/heuristic reasons for this declared
case. Chemistry stays scientifically unassessed: protonation/waters, generated
geometry without environmental refinement (#323), broader chemical/scoring
coverage, provider export (#223), installed/public/hosted evidence remain open.
This issue remains partial. The earlier exploratory baseline is preserved.

## 2026-10-07 real matched flexible ligand

The [1IEP experiment](../validation/1iep_flexibility_workflow.md) uses the original 69-atom/73-edge SDF state with public named Gasteiger charges and chemical-environment AutoDock types. Both rigid and seven-axis preparations retain 37 heavy atoms and three polar H; 29 H-charge transfers conserve +1 e (0.999 e in three-decimal PDBQT). Twelve seed/exhaustiveness searches retain original producer reports, assessments and verified source maps without provisional opt-in. This adds a real matched flexible ligand to bounded consumer evidence, while the receptor remains an external unassessed reference. Chemical-state selection, environmental geometry, scoring validity, wider preparation and public dependency closure remain unqualified; #5 stays partial.

## 2026-10-10 legacy versus named typing compatibility

The [controlled comparison](../validation/legacy_named_typing_comparison.md)
retains 23 paired preparations and four incomplete-input controls on the adopted
MolSysMT `739395d7e` source. Fourteen pairs change types or retained H, including
18 C → A differences in each native 5X72 ligand, N → NA for amine/pyridine
controls, SA → S for sulfone, and retained provider polar H on F/P. Both routes
preserve source inputs/positions and total charge. Original 1IEP native SDF input
remains outside the provider subset (#215), explicitly excluded from these pairs.
The original producer/raw bytes are retained, with no new molecular algorithm,
preparation default, score or search. Eighty-nine existing named-type, charge and
reporting contracts pass. Retire unqualified consumer typing through a separate
public compatibility change requiring preassigned named reports or explicit
provider typing options; do not automatically choose an experimental model.
Scientific acceptance and missing-charge scope remain open.


## Required named typing implementation — 2026-10-10

The [compatibility contract](../validation/required_named_typing.md) retires both
consumer AutoDock classifiers. Molecular preparation requires a valid named
MolSysMT assignment or explicit `typing_options`, with no default model, implicit
H/charge calculation or fallback. Bare labels and charge-only/untyped inputs fail
clearly, including automatic Vina with provisional opt-in. Existing assignment
binding, projected parent context, H/HD policy, charge/source maps and historical
prepared-object provenance controls remain.

New guards cover both roles and ensure rejection before engine construction and
without input mutation or unrequested molecular work. Existing integration cases
use actual named provider assignments. The four original torsion references keep
their file digests, original-atom correspondence, cuts and fragments; neutral 1S63
and its extra-HD reference remain distinct inventories. Real 181L tests reuse the
already declared HIE/charged-termini provider workflow. Original scientific
receipts and the unintegrated 5X72 displacement producer/archive remain unchanged.

Charge-only 1VII AMBER14 (+2 e/596 atoms) lacks the declared complete chemical
graph required by the explicit typing method; current tests retain that provider
rejection instead of repairing it downstream. [MolSysMT #376](https://github.com/uibcdf/molsysmt/issues/376)
records the separately observed native MolSys mechanical-setter adapter gap;
negative fixtures use the supported public MolecularMechanics route. Neither
boundary justifies a consumer molecular helper.

Local qualification uses the unchanged CI provider source `739395d7e`, native
binary and qualified ArgDigest/Viewer composition on Python 3.14.7. The complete
affected contract selection and administrative gates are recorded below after
execution. Required exact-head evidence remains the normal unskipped four-minor
hosted CI with installation, isolated installed checks and full source suites.
Keep #5/#49 partial: missing-charge policy, provider projection/export/poses and
scientific chemical/scoring acceptance remain separate.


Local final contract selection: **232 passed without skips in 200.04 s**, with
113 retained provider warnings, including the 12 new required-typing cases.
Earlier diagnostic failures were corrected; only the final passing selection
qualifies this source. Ruff lint/format (152 files), current guide/contributor
routes, all seven unchanged canonical guide snapshots, generated indexes,
changed-document local links, archived evidence digests and diff checks pass.
The reporting contract is checked separately. These local results do not replace
the four required hosted interpreter/installed checkpoints; terminal evidence
will be linked on the owning issues for the published commit.


### Full-suite legacy-workflow correction

Initial hosted candidate `bbf539c` exposed two indirect legacy PDB workflows
outside the local selection; it is not a passing full-suite checkpoint. Original
evaluation and record/replay producers and scientific receipts remain unchanged.
The [compatibility correction](../validation/required_named_typing.md#full-suite-correction--2026-10-10)
retains independent live evaluation with named preparation and actual captured
replay with explicitly supplied original objects. File-backed reconstruction
still preserves identity but cannot recreate named assignments from a raw PDB.
Legacy producer rejection is now guarded. MolSysMT #256 owns mechanical snapshot
persistence; no consumer snapshot or implicit preparation recipe is added.


The corrected evaluation/replay selection passes **51 tests without skips in
117.17 s**, with 40 retained provider warnings. Together with the unchanged
232-case preparation selection this covers **283 distinct local contracts**;
reporting is checked separately. The initial hosted run
[38037422889](https://github.com/uibcdf/dockingmt/actions/runs/38037422889)
finished with the same two legacy-workflow failures in each of four minors
(1,066 passed/2 failed per lane); it is retained as diagnostic evidence only.
The corrected published head requires a new complete unskipped matrix.
