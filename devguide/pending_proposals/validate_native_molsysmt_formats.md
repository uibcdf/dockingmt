---
summary: Validate native MolSysMT SDF/PDBQT inputs and define the supported preparation profile
issue: uibcdf/dockingmt#33
status: partial
opened: 2026-10-03
closed:
verification: measured
area: [preparation, inputs, molsysmt, vina]
guard: tests/test_native_molsysmt_formats.py::test_prepared_pdbqt_public_roundtrip_and_vina_admission
normative: devguide/validation/native_molsysmt_formats.md
blocked_by: []
supersedes: []
---

# Native MolSysMT SDF/PDBQT consumer acceptance

## What

Consume and qualify the experimental forms delivered by MolSysMT at
`eb0549b50689b2af5d8fbedb2687fb5746d43de6`. The inspected provider checkout is
`bbeeb72cf4da1c7e287abf0452b420922fcbc537` (later documentation). This is a
prepared-input format profile, not chemical preparation qualification.

## How

Start with the pinned Vina 1IEP, 1S63 and 5X72 ligands and 1IEP receptor. Exercise
public file/string/native conversions, exact retained atom identities, explicit
charges and labels, separate declared torsion trees, fragments, serialization
units, source immutability and Vina parser admission. Admit MolSysMT's explicit
`pdbqt_text:` strings into the existing unassessed Vina path, removing the format
prefix at the external-engine boundary.

## Why

Molecular format operations belong to MolSysMT. Consumer evidence determines when
DockingMT can retire temporary operations without changing scientific assumptions.

## What was refuted

Format parity does not qualify chemical assignments. PDBQT contains partial graph
evidence; its BRANCH records cannot replace a complete SDF chemical graph. Equal
atom counts do not provide a map, and TORSDOF need not equal active branch count.

## Scope and exclusions

No provider or viewer edits. Preserve all sibling dirty/ahead/behind work reported
by the refreshed suite inventory. Provider source code is clean at inspection;
its dirty guides/reports and test fixtures are preserved. The reported installed
MolSysMT version (`0.22.4+118.g03b318549.dirty`) is stale relative to inspected source;
retain the exact source commit as well as the runtime version in evidence.

This slice preserves original prepared atoms, charges and labels. It does not
assign charge/type parameters, merge hydrogens, select protonation or chemically
classify torsions. #5, #6 and #17 retain their separate acceptance. Temporary
writers and raw parsers remain until broader supported-profile tests justify
replacement; no new local molecular reader is introduced.

## Acceptance criteria

- Qualified public paths for real prepared inputs, malformed/unsupported controls,
  non-default units, source immutability and Vina parser acceptance.
- Atom identity and declared branch/fragment correspondence, with explicit evidence
  for any reordering, omission or addition.
- Provider-owned reports for unsupported real inputs and staged removal decisions.
- Separately reviewed minimum chemical preparation profile; no premature #5 closure.

## Initial inspected gaps

The direct native SDF route rejects original 1IEP (explicit valence field on atom
32) and 1S63 (unversioned counts line). Both original 5X72 SDF files convert with
explicit `stereo_engine='rdkit'` and `discard_properties=True`. The four prepared
ligand PDBQT files convert and serialize with preserved declared trees. Retain
these inputs unchanged and report the SDF profile gaps to molsysmt#215.

## Initial qualified slice (2026-10-03)

Sixteen targeted tests pass in 20.04 s. The executed notebook's three code cells
exercise the four native ligand round trips and a real 1IEP Vina run through
MolSysMT file-to-explicit-string conversion. Recorded byte hashes match the
original pinned inputs; the saved-result audit reports complete internal
agreement while preparation remains unassessed. This is an integration check,
not chemical or predictive validation.

The [maintained profile](../validation/native_molsysmt_formats.md) records the
paths, mappings, units, tolerances and staged removal conditions. The actual SDF
limitations are reported in [molsysmt#215](https://github.com/uibcdf/molsysmt/issues/215#issuecomment-5967782707).
The complete chemical profile, original unsupported SDF cases, broader fragment
projection and provider pose-ensemble acceptance remain open. No temporary
chemical operation is retired based solely on serialization support.

## Complete local gate

The first full run exposed one test-collection leak from the new test module's
top-level Vina import (493 passed, one bootstrap guard failed). The import now
occurs only inside the parser test. The repeated full run passes all 494 tests
without skips in 74.85 s, with the same twelve provider warnings. Ruff lint and
formatting (85 Python files), generated report indexes and diff checks pass.
Hosted qualification against the newly pinned provider commit remains separate.

## 2026-10-03 hosted receipt and fragment migration

The preceding prepared-input implementation at `be39d74` passed all four required
Python jobs in [run 37114604512](https://github.com/uibcdf/dockingmt/actions/runs/37114604512).
This establishes that software slice's hosted qualification, not chemical validity.

The [next migration](../validation/rigid_fragment_consumption.md) consumes public
MolSysMT partitioning across all four source ligands, preserving exact old PDBQT
bytes and atom permutations. It retires only the final local partition loop.
Thirteen new tests pass in `molsyssuite@uibcdf_3.14` (Python 3.14.7). After the
maintainer installed Vina 1.2.7, all 43 fragment/flexible/native-format tests pass
without skips in 30.37 s, including real Vina execution. Chemistry checks, original SDF
limitations, writers and pose-ensemble parsing remain separately open. Provider
source inspected is `bd65456e0`, with in-progress sibling work preserved.

The complete repeated gate passes all 507 tests without skips in 72.62 s on
Python 3.14.7 with Vina 1.2.7 and the twelve existing provider warnings. Ruff,
formatting (86 Python files), report indexes and diff checks pass. The new
four-code-cell notebook executes on the same interpreter and retains all four
PDBQT byte comparisons, permutations, fragment memberships and Vina admissions.

## 2026-10-03 chemical coverage assessment

The next consumer slice adds the [read-only chemical coverage summary](../validation/chemical_readiness_consumption.md)
to ligand/receptor preparation metadata and saved-result provenance. Public
MolSysMT #217 reports available fields and origins while leaving docking readiness,
charge models and other scientific checks unassessed. Both workflows pin source
`3edbf8ad0a13b9a56a009c0bd3f707e54b807351`; qualification uses an isolated snapshot
because sibling development continues. No provider/viewer worktree is changed.

Seven new cases and the extended real-engine safeguard pass in the 37-case focused
run. The notebook inspects caffeine and all four original prepared ligand PDBQT
inputs. Compact metadata stores counts, not copies of molecular value arrays;
paired preparation samples and JSON footprint are retained. #5 safeguards remain,
and #33 stays partial pending actual chemical preparation and format-profile gaps.

Complete local qualification: **514 passed, no skips, 69.45 s**, with twelve known
provider warnings, using Python 3.14.7, Vina 1.2.7 and the exact MolSysMT snapshot.
The stale CI-pin assertion exposed by the first full run is synchronized. Ruff,
formatting (88 Python files), report indexes and diff checks pass. All four new
notebook code cells execute against the recorded implementation digest.

Remote policy adoption `fda469f` was integrated before publication, preserving
the synchronized guide and policy 1.5.4/Python 3.14 baseline. The aligned policy
guard and repeated full gate pass **514 tests, no skips, 69.60 s**, with the same
twelve warnings; lint, formatting and index/diff checks remain green.

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

## 2026-10-06 bounded real receptor/BNZ workflow

The [181L audit](../validation/181l_receptor_workflow.md) consumes the existing
public peptide-template and native terminal-repair APIs alongside qualified H,
charges and typing. It preserves 1,289 observed heavy coordinates/IDs, names one
explicit receptor state and saves all generated-atom/source/projection maps.
Six real default Vina results retain captured PDBQT and recoverable evaluation
provenance. The writer width defect is separately tracked in #44.

This is source-profile composition on Python 3.14, using provider 5bd893c85 and
its preserved native artifact; the advanced live provider is not altered or
claimed qualified. PDB reader policy #304, export/name projection #223,
environmental H refinement #323 and symmetry correspondence #310 retain their
provider owners. General scientific preparation, installed artifacts and hosted
qualification remain open, so this issue remains partial.

## Original 5X72 crystal-reference dialect — 2026-10-09

The [independent-complex challenge](../validation/5x72_root_order_workflow.md)
distinguishes the existing supported hydrogenated prepared SDFs from the original
24-heavy-atom experimental SDFs. The latter have unversioned counts lines and
hit the existing native-reader boundary. Exact unchanged bytes, SHA-256 digests,
native refusal and explicit RDKit reference consumption are reported in
[MolSysMT #215](https://github.com/uibcdf/molsysmt/issues/215#issuecomment-6080146217).
Graph/element/stereo correspondence and exact coordinate agreement with independent
PDB instances are guarded without modifying the files or inventing experimental H.
This adds evidence for the existing dialect decision; it does not expand the native
SDF admission/readiness claim. #33 remains partial/open, with the provider-owned
exit condition unchanged.

## Prepared rigid occupancy composition — 2026-10-09

The [fixed-P69 workflow](../validation/5x72_occupancy_workflow.md) consumes public
MolSysMT fixed-state H addition, prepared PDBQT projections, detached `add`,
explicit identity setters and native rigid/tree writers. The original protein
atom fields stay equal; a same-writer sham reproduces the 50 historical P59
pose coordinates and docking scores. All 78 new poses preserve geometry/tree
during frozen evaluation in both receptor contexts, with complete input capture.
This is prepared-representation evidence, not complete PDBQT chemistry or a
general reader/preparation-readiness expansion.

[MolSysMT #352](https://github.com/uibcdf/molsysmt/issues/352) records mechanics
merge failures. [#353](https://github.com/uibcdf/molsysmt/issues/353) records add
chain-ID loss; this finite fixture explicitly restores its checked two-chain A/A
map through public set until provider add retains it. The workflow records
ownership, rationale, impact, review point and removal condition. No generic
consumer merger/writer or sibling source change is introduced. #33 stays partial
for the wider format, chemistry, readiness and provider migration scope.

The [portable annotation correction](../validation/5x72_occupancy_workflow.md#portable-dataframe-annotation-correction--2026-10-09)
separates original-profile snapshot authentication from current Pandas dataframe
dtype annotations. Both references retain independently checked experimental
identity/coordinates. The saved producer and all input/scoring bytes stay
immutable; a new inferred-string regression tests this boundary without treating
scientific preparation or the broader format profile as qualified.
