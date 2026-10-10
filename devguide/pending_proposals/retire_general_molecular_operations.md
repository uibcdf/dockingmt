---
summary: Retire remaining consumer implementations of general molecular operations
issue: uibcdf/dockingmt#49
status: partial
opened: 2026-10-10
closed:
verification: measured
area: [molsysmt, preparation, viewer, architecture]
guard: tests/test_molecular_delegation.py
normative:
blocked_by: []
supersedes: []
---

# General molecular operations belong to their provider

## What

The [owning review](https://github.com/uibcdf/dockingmt/issues/49) distinguishes
actual MolSysMT delegation from remaining consumer duplicates. The maintainer
requires general molecular operations to be proposed and implemented in MolSysMT;
pharmacophoric operations belong to PharmacophoreMT. DockingMT selects and
interprets docking workflows and consumes these tools.

## How

The first migration removes manual coordinate concatenation from
`build_docking_complex_system`. Every pose frame is composed with public
`msm.merge([receptor, ligand_frame])`; public `msm.append_structures` collects the
frames. Static-receptor pairing, pose order and the requirement for a verified
source ligand remain DockingMT decisions. No local molecular merger or new
dependency is introduced.

The three new guards exercise distinct ligand placements with the static receptor,
input immutability, default and pm/fs unit policies, actual public delegation for
every frame, and propagation of a later provider composition failure. Existing
viewer/result contracts exercise real pose reconstruction and viewer navigation.
These are molecular consumer contracts, not docking-quality measurements.

The first slice executed provider
`5bd893c85fe8d211663b2b1f865f5f1d2c382a90`, with the existing qualified ArgDigest
and Viewer sources. No provider upgrade, environment change,
native rebuild or sibling worktree edit was part of that slice.

Local selected validation: 40 viewer, molecular-delegation and result tests pass
in 26.04 s, with 37 existing provider warnings. The reporting check passes
separately (four cases including three repeated new guards, 6.23 s): **41 distinct
selected tests**, no skips. Ruff lint/format, generated indexes, all seven
registered guide copies, contributor routing and document links pass. Its
four-minor hosted CI passed on `74f67fe91dbf4a37924f7e6f9ac11bdaab69bc05`:
1,048 tests per minor, no skips, with quality, distribution governance and coverage
publication passing. This is source-suite evidence after ordinary installation
and isolated installed checks.

## Second slice: native source-free rigid conversion

Prepared receptors and rigid ligands without a source now call public PDBQT
conversion rather than rebuilding temporary PDB files, renaming duplicate atoms
and locally deriving element fields. Public `msm.set` restores the original
coordinate and partial-charge precision after PDBQT's fixed-width numerical
rounding. Parsed AutoDock labels are retained. This partial representation does
not claim missing bonds, complete chemical state or a new charge/type calculation.
The existing docking writer and submitted engine bytes are unchanged.

Adopt provider `739395d7ea31bec5c3f77cdcb1135ecf7e7c9bac`, the first commit
containing the prepared-mechanics merge correction in
[molsysmt#352](https://github.com/uibcdf/molsysmt/issues/352), in both CI source
routes and the dependency inventory. Keep the existing ArgDigest and lane-specific
Viewer pins. Do not cherry-pick or modify provider implementation downstream.
The newer provider head is outside this adoption's executed scope.

Local evidence: eight provider merge guards pass; the original 1,483-atom public
reproduction succeeds. The isolated consumer slice passes 67 selected preparation,
flexibility, viewer, result and delegation cases (38.98 s, 37 warnings), including
eight new cases covering duplicate identities, full precision, default/pm-fs
policies, provider failure propagation and mechanics retained across complex
frames. A complete pre-change local run was interrupted after reporting progress
at 210/1,048 cases; its retained log is incomplete and is not a full-suite pass.
Twenty-nine governance, reporting, distribution and coverage controls pass
separately (3.06 s): 96 distinct consumer cases across these two selections.
After strengthening identity/detachment assertions and retaining quantity-form
normalization, the 21 preparation/delegation cases pass again (10.89 s); these
repeat cases within the 96, not an additional distinct selection.
Required full qualification is the four-minor hosted run of the final commit.

These local controls use a detached provider source checkout with the authenticated
unchanged native binary (SHA-256
`c535c7d2f0e2a92b6ebf8298a60b19e4b5555467b4aa087e9563c6760619827e`).
Provider native sources are unchanged between these two commits. Build-backend
metadata was generated for the isolated probe; initial pre-change imports reported
the older installed distribution version despite verified candidate source origins.
Neither that source probe nor copied native bytes constitute an ordinary installed
candidate. CI must execute normal installation, source/metadata route checks and
isolated installed import checks, in addition to the complete source suite.

Source-backed conversion continues to copy the verified molecular source and
replace coordinates publicly. Source-free flexible reconstruction still requires
application of a known atom permutation; it retains the previous bounded bridge
pending [molsysmt#369](https://github.com/uibcdf/molsysmt/issues/369), #223 and #226.
There is no new downstream permutation algorithm or general molecular helper.

## Why

The previous path merged the first frame publicly but assembled later frames with
NumPy concatenation, a copied topology and coordinate replacement. Calling the
provider for every frame makes it responsible for molecular composition and
attribute handling; its failures propagate instead of being bypassed.

## Remaining work and bounded migration

- **Charge absence policy adopted:** the
  [required-charge contract](../validation/required_partial_charges.md) removes
  zero fabrication in both roles and delegates every explicit calculation to
  MolSysMT. Supplied zeros retain their own provenance. No new molecular
  transform is introduced. Scientific model acceptance remains #5; the native
  unit-policy limitation is reported in MolSysMT #381.

- **Typing adopted:** the [2026-10-10 compatibility change](../validation/required_named_typing.md)
  removes both consumer classifiers. A valid named provider assignment or explicit
  typing options are required; DockingMT chooses no model. Scientific acceptance
  remains open under [#5](https://github.com/uibcdf/dockingmt/issues/5).
- **Projection:** retained/omitted H, charge aggregation and derived atom maps
  belong to [molsysmt#223](https://github.com/uibcdf/molsysmt/issues/223). Its public
  operation must perform the transform, not merely describe a consumer transform.
- **Serialization:** public native PDBQT output is available under
  [molsysmt#214](https://github.com/uibcdf/molsysmt/issues/214). Its formatting differs
  from the legacy consumer output. Qualify the complete charge/type/tree/map
  profile, explicitly retain old producer bytes and decide representation
  compatibility before replacing writers. Do not rewrite historical archives.
- **Poses and flexible source-free reconstruction:** provider MODEL-aware reading
  and export/source maps belong to
  [molsysmt#226](https://github.com/uibcdf/molsysmt/issues/226) and #223. Keep the
  prepared atom axis explicit; provider extraction does not supply an arbitrary
  atom reorder. Do not add a consumer reordering or molecular parsing algorithm.
- **Connectivity:** the existing retained-graph traversal remains the bounded
  exception under [molsysmt#348](https://github.com/uibcdf/molsysmt/issues/348), with
  its existing review date 2027-01-06.
- **Source-free conversion:** replacing PDB reconstruction with native PDBQT
  conversion can retain molecular types/charges and restore full coordinate and
  charge precision through public setters. That adds mechanics to the native
  representation, exposing the old pinned provider's merge defect in
  [molsysmt#352](https://github.com/uibcdf/molsysmt/issues/352). The provider fix is
  delivered and its first containing commit is adopted in the second slice,
  subject to the final exact-commit CI checkpoint above. Source-free flexible
  permutation remains provider-owned. Do not silently discard mechanics or
  implement a downstream merger or atom reordering to bypass these requirements.

The remaining historical conversion/writer/projection routes are tracked here and
in [#33](https://github.com/uibcdf/dockingmt/issues/33); they are not architectural
acceptance. Responsible role: DockingMT contributors. Review by 2027-01-06.
Removal requires a qualified supported provider operation covering the existing
units, inventories, correspondence, source immutability and explicit preparation
attribution. They must not be generalized while adoption is pending.

## What was refuted

Successful current tests do not prove that all molecular operations are delegated.
Source inspection of a newer provider does not qualify its runtime, installed
artifacts or scientific compatibility. MOLI's platform architecture does not
transfer provider implementation ownership to DockingMT. Independent finite
checks of provider geometry in developer controls are not a replacement geometry
API. No current missing pharmacophoric capability was established, so no
speculative PharmacophoreMT implementation or issue is introduced.

## Scope and exclusions

Keep #49 partial. This slice does not close #5/#33 or the provider proposals.
No new scores, searches, optimizations, public release or artifact admission.
The previously completed, unintegrated seven-point scientific producer and raw
archive remain unchanged and separate from this migration's validation.

## Acceptance criteria

Delegate each reviewed general operation through a supported provider contract,
or retain a current bounded owner-linked exception and removal condition. Verify
actual calls and user-visible identity, units, failure and provenance behavior.
Preserve docking decisions, original scientific inputs/producer bytes, and human
work in sibling checkouts. Provider maintainers own their delivery decisions.

## Typing compatibility evidence, 2026-10-10

The [paired legacy/named comparison](../validation/legacy_named_typing_comparison.md)
executes 23 comparisons, four declared incomplete-input controls and the already
tracked native 1IEP reader limit. Fourteen pairs differ; native 5X72 has 18 C → A
changes per ligand despite unchanged positions, retained counts and total charge.
The existing public named operation covers this classification; no new consumer
algorithm is needed. Retain original producer/raw evidence and existing defaults
for this slice. The next bounded compatibility change removes heuristic typing,
requires valid named assignments or explicit provider options, and explains
missing prerequisites. Writer/projection/permutation adoption remains separate.
The comparison is source-composition evidence, not chemical validation or a new
installed candidate. Existing typing/charge/reporting contracts pass 89 cases.


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

## Native prepared-export boundary — 2026-10-10

The [executed writer checkpoint](../validation/native_prepared_export.md) adds
five consumer controls for both methanol roles under angstrom/pm input, real
Vina admission and a declared six-carbon flexible axis. The serializer works
with explicit prepared values and tree. The retained native source still holds
pre-aggregation charges; directly serializing it would lose the omitted H
contribution, while serializing the full source retains all H. Public replacement
of charge values correctly removes calculation provenance. Native blank groups
also differ from prepared LIG/1 presentation. These are distinct transform and
compatibility requirements, not a claim that #214 has no functioning writer.

Keep the production routes unchanged pending the provider-owned native projection
and maps in #223. This checkpoint adds no molecular algorithm, snapshot builder,
serializer or implicit fallback. Evidence is handed to #223/#214 and #49/#5;
the current provider source and the original scientific archives remain fixed.
The final five controls pass without skips in 8.20 s; the surrounding selection
passes 119 without skips in 93.77 s, with 47 retained warnings. All 119 distinct
contracts and applicable administrative checks are covered. Exact published-head
hosted checks are recorded on the owning issues after execution.


## 2026-10-10 executed 3PTB admission

The 3PTB workflow composes public molecular tools and adds no general molecular implementation. Direct compressed-PDB recognition fails before reading; reusable support is proposed in [MolSysMT #385](https://github.com/uibcdf/molsysmt/issues/385). A separately registered caller archive handoff restores exact original plain bytes, authenticated before public conversion. The 2026-11-10 review and provider-qualified removal condition are retained. This does not retire #223/#348 or qualify compressed consumption.

The [executed admission](../validation/3ptb_admission.md), [notebook](../validation/3ptb_admission_2026-10-10.ipynb) and separate receipt retain measured scope. Owning issues remain partial/open.
