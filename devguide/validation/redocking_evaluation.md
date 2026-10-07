# Public redocking evaluation

`dockingmt.evaluate_redocking(result, reference, *, rmsd_cutoff,
top_n=(1, 5), selection='all', reference_info=None)` evaluates one result
against one reference frame and returns a detached finite JSON report.
It reuses public `DockingResult.get_rmsds` and MolSysMT geometry. It does not
execute a docking engine or require the viewer.

```python
report = dockingmt.evaluate_redocking(
    result, reference,
    rmsd_cutoff=pyunitwizard.quantity(2.5, 'angstrom'),
    top_n=(1, 3, 5),
    reference_info={'uri': 'caller:reference', 'case': 'declared control'},
)
```

## Scientific interpretation

The caller must put pose and reference in the same receptor coordinate frame.
No rotation/translation, ligand superposition, symmetry correction or inferred
chemical equivalence is performed. The report records those choices explicitly.
`rmsd_cutoff` is mandatory: a finite non-negative scalar length with explicit
units. Recovery means the literal `rmsd <= cutoff`, without a hidden tolerance.
The example's 2.5 Å criterion is a caller declaration, not a universal validation
threshold. Scores are observations with their existing descriptors, not physical
affinities or proof of preparation accuracy.

Top-N means the first N **positions in current result order**, which is recorded
as `top_n_basis='result_order'`. Stored ranks are preserved separately, and are
not used to reorder poses. The first pose and the closest geometric pose are
reported separately. RMSD ties select the first current position. Requesting
N greater than the returned pose count considers only available poses and
records both counts. Empty results have no first/closest pose and no recovery;
this is not an inferred failure rate for a dataset.

Molecular and `DockingPose` references require existing verified source atom
keys. All poses must use the same mapped atom population; known ligand/receptor
state declarations cannot conflict. Unknown states remain unknown. Molecular
references may reorder atoms through their identities and retain additional
omitted H. The existing `selection` contract selects reference atoms, not pose
atoms; it cannot turn a pose retaining polar H into a heavy-atom-only metric.

An explicit coordinate quantity chooses **caller-declared positional matching**.
It must contain exactly one finite structure with the same number of atoms as
each pose. No reference molecular map is inferred or authenticated. Known
pose maps, when present, must have the same ordering for this route. Coordinate
and pose references require `selection='all'`.

## Report and ownership

The report has evaluation schema `1.0`, separate from pose/result records:

- `criterion`: metric, fixed angstrom unit, cutoff/comparison, frame declaration,
  atom scope/correspondence, alignment, symmetry and top-N interpretation.
- `reference`: actual single-frame coordinates in angstrom, available atom keys,
  resolved selected atom indices, caller declarations and snapshot SHA-256.
- `poses`: position, declared rank/IDs, atom count/map, actual geometry SHA-256,
  existing scores/descriptors, RMSD and the recovery observation.
- `first_pose`, `closest_pose`, `top_n`, `n_poses`: independent summaries.
- `context`: detached problem declarations (excluding receptor/partner payloads),
  protocol, known backend/version, preparation assessments, ranking history and
  available artifact hashes/format/size. Captured PDBQT bytes are not duplicated.
- `evaluator`: actual DockingMT/MolSysMT versions and public RMSD function.

`reference_info` must be finite JSON; it records caller declarations, without
claiming to authenticate a URI, checksum or common-frame assertion. The actual
reference snapshot and pose geometry hashes cover the fixed-unit numerical
records used here, not scientific validity. Preserve the original saved docking
result and input artifacts separately for replay.

Numbers cross this report's fixed-unit protocol using
`puw.get_value(..., to_unit='angstrom')`. The reader must interpret both cutoff
and RMSD in the recorded angstrom unit; application standard units do not
change that protocol. This is not a general quantity codec. A pm/fs policy
regression protects the boundary. Invalid measurements, complex/nonfinite
coordinates, conflicting states/populations and unmapped molecular comparisons
raise; provider exceptions retain their original identity. Evaluation never
mutates or reranks its inputs. Report edits do not mutate inputs or other
summary sections. Ordinary JSON can be read without an engine or viewer.

## Real controls and qualification limits

The [executed notebook](redocking_evaluation.ipynb),
[raw reports](data/redocking_evaluation/cases.json) and
[`qualify()` helper](../../devtools/qualify_redocking_evaluation.py) retain three
seeded native Vina 1.2.7 executions (seed 42, one CPU, exhaustiveness 1).

| Control | Comparison | Observed RMSD (Å) | Preparation |
| --- | --- | --- | --- |
| 181L BNZ | Verified six retained atoms against molecular reference | 2.292, one returned pose | Explicitly provisional |
| 1IEP published prepared ligand | All 40 input PDBQT atoms in verified output order | 0.876, one returned pose | External, unassessed |
| 1IEP domain shifted 30 Å in x | Same 40-atom reference | 25.247, 22.875, 22.244 | External, unassessed |

The displaced box excludes the native reference atoms; none of its returned
poses meets the declared 2.5 Å criterion. This is a methodological search-domain
control, not a biologically inactive ligand or affinity/selectivity comparison.
The positive cases are software observations, not chemical qualification or
general redocking success rates.

The 1IEP inputs are the unmodified licensed fixtures in
[`tests/data/vina_torsions`](../../tests/data/vina_torsions/README.md).
Their receptor/ligand SHA-256s are checked against the pinned upstream inventory
and against bytes actually submitted to Vina. MolSysMT converts the ligand
PDBQT with explicit `discard_torsion_tree=True` only to obtain reference
coordinates. The original input and torsion tree still go unchanged to Vina.
This positional reference is the prepared input conformation including three
polar H, **not** the historical 37-heavy-atom SDF metric in
[`1iep_external_pdbqt.md`](1iep_external_pdbqt.md). Its different RMSD must not
be described as an improved reproduction of that older metric.

Qualification uses editable `molsyssuite@uibcdf_3.14`, Python 3.14.7, the unchanged
MolSysMT source pin `c19a47ada0c2279029abfa296cf915560610ad9a` and CI viewer pin
`ec4c71e574d798b7c8675b7e7e983da878ce9889`. Source-pin integration is distinct
from published dependency compatibility. The active provider worktree is
preserved and not used to certify these exact-source observations.

The final local gate passes **750 tests without skips in 183.19 s**; 44 new
evaluation cases include the native controls. The 96 existing/provider warning
occurrences remain visible. Ruff lint/format, report indexes, reporting guard
and diff checks pass. All three code cells of the notebook execute.

Correction, 2026-10-03: the reported Sabueso/Ackredit version mismatch came from
stale editable-install metadata, as clarified by the maintainer. The
dependency-incompatibility interpretation and requested provider follow-up are
[withdrawn](https://github.com/uibcdf/molsyssuite/issues/82#issuecomment-5974182219).
After the reinstall, editable Ackredit is `0.9.0+7.g3c6e77c.dirty` and the same
Python 3.14.7 interpreter's `pip check` exits 0, `No broken requirements found.`
The historical check did not demonstrate an API incompatibility; the stale
metadata mismatch is resolved.

The full local regression after that refresh also passes: **750 tests, no skips,
198.37 s**, with the same 96 warnings and unchanged provider pins. Ruff
lint/format, generated report indexes and diff checks pass. The implementation
commit `a5fb97b763012eb0df7fd3eb9206ce10c784fb1c` has successful
[CI](https://github.com/uibcdf/dockingmt/actions/runs/37159093062) and
[suite policy](https://github.com/uibcdf/dockingmt/actions/runs/37159093232)
runs. Existing notebook measurements retain their original execution evidence.

### Portable live-search guard correction — 2026-10-07

[DockingMT #46](https://github.com/uibcdf/dockingmt/issues/46) records a macOS
arm64 failure of the live first-pose recovery expectation at exhaustiveness 1.
The earlier table and executed notebook retain their measured Linux outcomes;
a seed does not make those outcomes a recovery guarantee on another platform.
The live integration guard now independently compares each returned pose's
positional RMSD with its recorded reference and checks recovery at the unchanged
2.5 angstrom cutoff. It retains input-byte/identity checks and the displaced-box
negative control. A separate retained-data guard preserves the original positive
and negative observations. Search parameters and production evaluation are unchanged.

## Provider follow-up

[DockingMT #38](https://github.com/uibcdf/dockingmt/issues/38) owns this report.
Future chemically constrained symmetry correspondence is handed off to
[MolSysMT #310](https://github.com/uibcdf/molsysmt/issues/310). Positional RMSD is
not a defect: symmetry-aware recovery needs its own supported molecular policy
and evidence. Missing/ambiguous chemical declarations must not be silently
declared equivalent. No local symmetry, graph matching, RMSD kernel or general
atom-mapping implementation is added to DockingMT.
