# Executed registered 3PTB search population

Executed on 2026-10-10 under DockingMT [#5](https://github.com/uibcdf/dockingmt/issues/5),
[#6](https://github.com/uibcdf/dockingmt/issues/6),
[#4](https://github.com/uibcdf/dockingmt/issues/4) and
[#49](https://github.com/uibcdf/dockingmt/issues/49), all partial/open.
The unchanged [prospective protocol](3ptb_prospective_protocol.md) and
[molecular admission](3ptb_admission.md) supply the scientific population.

All **24 planned searches were attempted once and returned 167 poses**, with
zero search exceptions and no new fixed-pose scoring. Separate saved-pose
evaluation applies the registered positional nine-heavy-atom RMSD, no alignment
or symmetry matching, near-reference **at most 2.0 angstrom**.

| Arm | Box | Planned / attempted / returned / received evaluations | Poses | Rank-1 near | Any returned near |
| --- | --- | --- | ---: | ---: | ---: |
| Rigid | Native | 6 / 6 / 6 / 6 | 41 | 6 | 6 |
| Rigid | Displaced | 6 / 6 / 6 / 6 | 39 | 0 | 0 |
| C1–C flexible | Native | 6 / 6 / 6 / 6 | 41 | 6 | 6 |
| C1–C flexible | Displaced | 6 / 6 / 6 / 6 | 46 | 0 | 0 |

This finite result supports generation and first-rank recovery for this declared
case/hypothesis under the specified cutoff. It does not estimate probabilities,
experimental affinity, model/state suitability or multi-complex generalization.
Rigid first-pose RMSDs are approximately 1.930–1.945 angstrom; flexible ones
1.134–1.916 angstrom. Several lie close to the registered threshold. Best returned
RMSD can be smaller than first-pose RMSD; no ranking change is made. The nearest
displaced-box returned pose is approximately 52.901 angstrom from the reference.

## Immutable production and receiving evidence

The [original search archive](data/3ptb_search/audit_2026-10-10.json.gz) has SHA-256
`97104903c93b3f7a729a5a6ac196cdb7b59d686e318efdcf324f70131abba1f2`.
It retains all 24 original rows, attempts, exact captured input bytes and boxes,
complete thirteen-atom poses, five-column native energies, score descriptors,
native defaults, source/runtime/native artifact identity and all tracebacks.
Its [original producer](data/3ptb_search/producer_2026-10-10.py.txt) is preserved.
Consumer base is `105dfc15d47cde7005137f3e7405e2b515107c4f` plus the recorded
working-tree source hashes. Advertised package versions are recorded separately
from source commits and compiled artifact hashes.

**The original producer has 24 reporting failures and zero successful RMSD
evaluations.** Its selector indexed optional `source_atom_indices=None`. This
did not alter any search or pose. The corrected case-specific receiver selects
optional arrays only when present. It also supplies score descriptors once:
its initial constructor startup rejected duplicate descriptors before RMSD.
Both bounded corrections preserve identities, scores, ranks and the registered
comparison. They concern DockingMT orchestration, not missing molecular tools.

The [separate receiving archive](data/3ptb_search/evaluation_2026-10-10.json.gz),
SHA-256 `8351d4db25b2ad25de413158a8d3dc0a5e4fee31678ea06649994a1832fa53af`,
contains 24 successful evaluations and all 167 pose measurements. Every row keeps
its original failure/error. It binds the immutable original search SHA and records
a separate receiving source/runtime identity. There is no new preparation,
H generation, map calculation, scoring, optimization or docking in this receiver.
The [receiving producer](data/3ptb_search/receiving_producer_2026-10-10.py.txt),
[corrected helper](data/3ptb_search/receiving_search_helper_2026-10-10.py.txt) and
[qualification receipt](data/3ptb_search/checkpoint_2026-10-10.json) preserve these
distinctions. Generated consumer version metadata may differ at reception; its
original bytes/version remain recorded, and scientific product sources are checked.

## Pre-search interface clarification

The [registered execution handoff](3ptb_execution_handoff_2026-10-10.md),
[initial registration](data/3ptb_search/registration_initial_2026-10-10.json) and
[dated normalization registration](data/3ptb_search/registration_2026-10-10.json)
make the prepared-partner projection explicit before any attempt. The original
rows declare cuts `[]` or `[[0,6]]`. The executable protocol requests no automatic
preparation (`None` at construction, normalized to `[]` in its record); the exact
admitted prepared flexible PDBQT still carries its C1–C branch. All other protocol
parameters remain unchanged. Native `dock` uses actual wrapper defaults
`min_rmsd=1.0` angstrom and `max_evals=0`; map spacing is 0.375 angstrom and
`force_even_voxels=False`. These are recorded defaults, not new tuned controls.

An initial checksum assertion used compact JSON separators instead of the
original receipt's default separators and stopped before molecular work.
A subsequent protocol equality assertion expected literal null instead of the
public constructor's resolved empty list and stopped before the first attempt.
The [pre-search archive](data/3ptb_search/presearch_stop_2026-10-10.json.gz) and
[its producer](data/3ptb_search/presearch_producer_2026-10-10.py.txt) retain all
24 `not_attempted` rows. Neither stop constitutes a repeated scientific search.
The issue registrations retain these mistakes and their corrections.

## Molecular correspondence, domains and interpretation

Admission is replayed once; every literal PDBQT byte, full precision preparation
coordinate, box and population must match the prior archive before searching.
All rows reuse those live preparations. Successful returned calls independently
verify actual captured input hashes and actual submitted box coordinates.
The ordered population remains rigid/flexible, native/displaced, seeds
7/42/2026 and efforts 1/8. Twelve effort-8 rows return nine poses each; effort-1
rows return fewer. Retrieval counts and seed/effort strata remain explicit.

The saved written-to-full-source map selects exactly the original nine observed
atoms. IDs, names, elements and residue identities are checked against public
MolSysMT getters before any geometry calculation. Heavy-only public pose results
are passed to `dockingmt.evaluate_redocking`; positional RMSD comes from
`molsysmt.structure.get_rmsd`. No downstream matcher, fitting implementation,
symmetry algorithm or molecular repair is introduced. The complete native energy
matrix and resolved backend calls are now reusable adapter evidence documented
in [score semantics](score_semantics.md); four existing named scores/ranking are
unchanged.

Seven of 167 returned poses include at least one retained atom outside the
literal box; three include heavy atoms. They remain in all results and
denominators. The specific zero-based run / returned rank pairs are
`0/5`, `11/7`, `15/5`, `17/8`, `19/5`, `20/3`, `21/4`.
Heavy atoms are outside for `0/5`, `15/5`, `17/8`.
Every native-box first pose is fully inside. Neither a requested Vina box nor
the observed control is promoted to a guarantee that every returned atom lies
inside that literal region. All displaced returns remain over-threshold, so no
apparent near-reference negative-box return requires remapping.

Rigid/flexible ROOT orientation differs as recorded in admission. The comparison
cannot isolate torsional flexibility from that representation difference, and
score differences between arms are not affinity evidence. Source-identity RMSD
retains phenyl symmetry/amidinium resonance ambiguity. A future symmetry-aware
question needs a separate protocol and public provider support under
[MolSysMT #310](https://github.com/uibcdf/molsysmt/issues/310); no post-outcome
normalization is applied. The dry receptor omits calcium and waters; fixed H,
states and named models remain unassessed scientifically. Existing provider
#223/#226/#323/#348/#381 and compressed-input #385 are not closed by this result.
No PharmacophoreMT operation is required by the present workflow.

## Human workflow and qualification

The [executed notebook](3ptb_search_2026-10-10.ipynb) authenticates immutable
archives, replays public admission without searches, verifies all 167 saved poses
under pm/fs/degree standards with explicit elementary charge, and displays all
24 rows, full energy vectors and containment. It composes public Python APIs
and uses only public case data, following the pilots' general human-workflow
principle. Kernel and caller source directories are managed and cleaned.

The [search command](../../devtools/qualify_3ptb_search.py) requires a new output
path and records progress before/after attempts. It attempts each row once and
does not retry or discard failures. The [receiving command](../../devtools/evaluate_3ptb_saved.py)
authenticates original search bytes before saved geometric evaluation. A separate
replication must retain its own new producer and output; it must not replace the
original archive.

Scoped local tests cover native fifth-column preservation/defaults, prepared
protocol projection, pre-search drift rejection, immutable output protection,
all-attempt denominators, source-identity drift rejection, a known translated
heavy pose with deliberately distant H, saved replay under another unit policy,
and complete saved receiving evaluation while new native work is forbidden.
The receipt records applicable contract, reporting, format/index/link/guide and
notebook gates. Hosted evidence is synchronized on the owning issues after the
unskipped exact head completes.

## Exact-head CI comparison correction, 2026-10-10

The first published head `bb522d6` exposes two existing individual/batch equality
assertions that compare the newly retained native staging filename. A bounded
native reproduction finds only `engine_info.rigid_receptor` differs; after that
path and elapsed time are excluded, all fields are equal. The test correction
authenticates captured input bytes/hashes, checks that each recorded staging file
was cleaned, and excludes only that invocation-local path. Product code, native
options, all scientific archives/producers, score values, coordinates and
receiving measurements stay unchanged. Original failed CI evidence is retained
in the owning issue, with a new unskipped corrective head and its executed gates.

The broad routine environment's global `pip check` remains failed with already
reported third-party/AmberTools constraints. This actual workspace limitation is
recorded in [MolSysSuite #82](https://github.com/uibcdf/molsyssuite/issues/82).
No shared dependency is changed here and no clean whole-environment closure is
claimed. The pinned scientific source/native composition and bounded executed
DockingMT checks are separate evidence. Normal installed/public artifact
admission remains under DockingMT #30/#47.
