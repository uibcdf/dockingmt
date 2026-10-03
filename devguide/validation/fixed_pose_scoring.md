# Public fixed-pose scoring

`dockingmt.score(problem, protocol=None, backend=None, pose=None,
score_name='score')` evaluates one already prepared ligand conformation against
a rigid receptor and returns a `DockingPose`. Vina/Vinardo call native
`Vina.score()`: no search, randomization or local optimization occurs.
The [executed notebook](fixed_pose_scoring.ipynb) demonstrates a prepared
software control, additive rescoring and an independent JSON roundtrip.

## Prepared-input contract

Supply matching `PreparedReceptor`/`PreparedLigand` objects, PDBQT files, raw
PDBQT text or MolSysMT's explicit `pdbqt_text:` form. The `DockingProblem`
normalization contract still applies. Scoring rejects inputs that need automatic
preparation. General molecular reads and conversions stay in public MolSysMT.
Known provisional preparations require explicit
`VinaProtocol(allow_provisional_preparation=True)`; external PDBQT remains
unassessed. Successful execution never upgrades that assessment.

The box is the affinity-map domain. Scoring, CPU, seed initialization, provisional
policy, input capture and timing settings are recorded. `exhaustiveness`,
`n_poses` and `energy_range` do not affect fixed-pose scoring and are explicitly
listed as unused search parameters. Active protocol torsions are rejected:
prepare the desired tree beforehand. AD4, flexible receptors, constraints and
search guidance remain unsupported. Existing docking-only backend subclasses
remain valid; their optional `score` method reports `pose_scoring` unsupported.

## Coordinates and identity

Without `pose`, returned coordinates follow PDBQT atom-record order. Prepared
objects preserve their original coordinates in that order and carry verified
source atom keys. Raw input establishes positional order only. MolSysMT converts
a geometry-only projection with `discard_torsion_tree=True`; the untouched
original bytes, types and torsion tree go to Vina and are fingerprinted.

With `pose`, the prepared ligand must already represent that pose. Atom count
and coordinates must match in PDBQT record order, with absolute per-coordinate
tolerance **0.000500001 Å** and zero relative tolerance. This admits three-decimal
PDBQT rendering plus numerical conversion noise; it does not perform molecular
alignment or establish chemical identity. Verified source keys additionally
check atom names (when present) and elements. Known input/pose state identifiers
must agree. Unknown identifiers stay unknown in the evaluation's evidence.
The operation does not rebuild prepared inputs from pose coordinates.

Returned coordinates, state/pose identity, rank, prior scores and nested metadata
are detached from the supplied pose. Rank is preserved without reranking; a
new pose has no rank. Geometry or state mismatch is rejected before native setup.
Use a different `score_name` to retain successive evaluations.

## Eight native components

The total uses `score_name`. Other names prefix the component with
`score_name + '.'`. Their order follows the upstream
[Vina 1.2.7 score implementation](https://github.com/ccsb-scripps/AutoDock-Vina/blob/v1.2.7/build/python/vina/vina.py):

| Column | Component | Meaning in the upstream score contract |
| --- | --- | --- |
| 0 | `total` | Total empirical score |
| 1 | `lig_inter` | Ligand intermolecular term |
| 2 | `flex_inter` | Flexible-receptor intermolecular term |
| 3 | `other_inter` | Other intermolecular term |
| 4 | `flex_intra` | Flexible-receptor intramolecular term |
| 5 | `lig_intra` | Ligand intramolecular term |
| 6 | `torsions` | Torsional term |
| 7 | `lig_intra_best_pose` | Ligand intramolecular best-pose reference term |

Retain even zero flexible-receptor components. These columns differ from
`Vina.energies()` used after docking. Each descriptor declares an empirical
score conventionally expressed in kcal/mol, method/version, component and
scoring stage. Only the total declares a preferred lower direction; no implicit
ranking occurs. Context includes submitted receptor/ligand hashes, map box,
grid spacing, weights and preparation assessment. Exact ligand-input hashes
deliberately make comparison admission conservative: equal units or names do
not establish comparability across poses or states.

## Independent attachment and provenance

`pose.with_scores(scores, score_definitions=None)` is a public engine-independent
operation for retaining other evaluations. It validates finite named real values
and optional descriptors, rejects any existing-name collision, and returns a
detached pose. Descriptors apply only to additions. Missing descriptors remain
unknown; caller-supplied descriptors remain caller declarations. No implicit
unit conversion, molecular operation or score computation occurs.

Native scoring appends a detached `metadata['scoring_history']` evaluation with
schema 1.0, operation, software versions, resolved protocol, applied/unused
settings, geometry/state checks, public preparation assessments, exact input
hashes and the new scores/descriptors. Optional input capture stores submitted
bytes in base64; optional timings name consecutive phases in seconds. The
usual pose reader/writer preserves these records without a live engine.
`audit_result` currently audits docking-result provenance; this new pose record
does not imply support for auditing a result assembled from several stages.

## Reproduction and limits

Run `python -m pytest tests/test_scoring.py --receptor=llm` in
`molsyssuite@uibcdf_3.14`, with DockingMT installed editable. Select the explicit
Python 3.14 Conda kernel for notebook execution. Notebook/test source qualification
uses the existing unchanged CI pins: MolSysMT
`c19a47ada0c2279029abfa296cf915560610ad9a` and MolSysViewer
`ec4c71e574d798b7c8675b7e7e983da878ce9889`. Neither sibling is changed.
The new operation does not import Meeko or MolSysViewer.

The minimal control deliberately overlaps receptor and ligand and has a positive
score. Its purpose is fixed-coordinate and component/provenance validation,
not binding prediction. The retained 1IEP flexible-input guard proves exact
submission and record-order handling, not pose recovery or parameterization
quality. No physical-energy, benchmark speed, scientific accuracy or preparation
qualification claim follows from these tests. Provider improvements remain
tracked with MolSysMT's owners.

## 2026-10-03 qualification result

All **595 tests pass without skips in 123.85 s**, including 31 new scoring and
attachment cases, on Python 3.14.7 and Vina 1.2.7. The unchanged 27 provider
warnings are retained without local suppression. Ruff lint/format, report-index
and diff checks pass. The notebook's four code cells execute successfully using
the requested Conda interpreter. Both scoring functions preserve the original
control geometry, and the additive example keeps 16 native score components,
two evaluation records and a separate undeclared manual score through JSON.
This is source-qualified behavior evidence within the bounds above.
