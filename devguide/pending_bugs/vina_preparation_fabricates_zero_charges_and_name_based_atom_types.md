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

Current preparation writes zero partial charges, guesses AutoDock types from names, and drops hydrogens by name, including polar receptor hydrogens.

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
