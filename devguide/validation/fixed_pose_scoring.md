# Public fixed-pose scoring

`dockingmt.score(problem, protocol=None, backend=None, pose=None,
score_name='score')` evaluates one already prepared ligand conformation against
a rigid receptor and returns a `DockingPose`. Vina/Vinardo call native
`Vina.score()`: no search, randomization or local optimization occurs.
The [portable notebook](fixed_pose_scoring.ipynb) demonstrates a prepared
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

New evaluations explicitly retain the
[native reference convention and quantity](scoring_reference.md), independently
of the current reader or original docking producer. The no-argument native call
and its eight values remain unchanged. This adds no cross-pose ranking permission
and infers no new policy for legacy saved observations.

## Independent attachment and provenance

`pose.with_scores(scores, score_definitions=None)` is a public engine-independent
operation for retaining other evaluations. It validates finite named real values
and optional descriptors, rejects any existing-name collision, and returns a
detached pose. Descriptors apply only to additions. Missing descriptors remain
unknown; caller-supplied descriptors remain caller declarations. No implicit
unit conversion, molecular operation or score computation occurs.

Native scoring appends a detached `metadata['scoring_history']` evaluation with
schema 1.0, operation, evaluation name, backend box, software versions, resolved protocol, applied/unused
settings, geometry/state checks, public preparation assessments, exact input
hashes and the new scores/descriptors. Optional input capture stores submitted
bytes in base64; optional timings name consecutive phases in seconds. The
usual pose reader/writer preserves these records without a live engine.
Use [`audit_pose(record)`](pose_audit.md) to check standalone saved evaluations
against current pose scores and declarations. Missing independent name/box
evidence in older scoring records stays incomplete; their reader remains compatible.
`audit_result` also checks these per-pose evaluation histories when a collection
stores them, keeping original result-level docking provenance separate. Missing
collection evidence stays incomplete; an evaluation is not promoted to that
provenance. This is not a general stage-composition or score-comparison policy.

## Run the notebook with explicit inputs

Choose a Python environment containing DockingMT and a compatible Vina engine,
and select that environment's notebook kernel. No checkout location, Conda
environment name or Python minor is hardcoded in the cells. Before opening the
notebook, supply the saved input record and its independently expected file digest:

```bash
export DOCKINGMT_RESULT_PATH="prepared_input_record.json"
export DOCKINGMT_RESULT_SHA256="DIGEST_FROM_YOUR_TRUSTED_SOURCE"
jupyter lab
```

Alternatively, replace those two environment lookups in the first cell with your
explicit path and trusted digest. JSON and gzip-compressed JSON are supported.
For the retained synthetic example, download
[the original input record](data/audit/minimal_vina_result.json), keep its bytes
unchanged and use the externally recorded SHA256:

```text
4d66f4e3d00f5e5e6014ce00bd0ec11370890997f570f6272dc1f5205f1c0a88
```

The first cell verifies file identity, admits the record with public audit/schema
APIs and requires both captured prepared PDBQT byte strings plus the declared
box. A wrong digest, unsupported/inconsistent record or unavailable capture stops
before native setup. Capture verification authenticates the recorded byte hashes;
it does not reconstruct absent chemical state, source topology or historical
software. Original producer information remains visible separately from the
current reader. This example does not recover a full molecular problem.

The conformation scored is the original **captured submitted partner**, not an
automatically selected historical output pose. To evaluate another conformation,
supply matching already prepared inputs through the public scoring contract above.
The next cells perform the existing Vina/Vinardo evaluations with CPU1, retain
16 native components/two histories and demonstrate an independent roundtrip with
one explicitly undeclared manual score. Public structured errors handle the
expected duplicate-score refusal; unrelated exceptions propagate. The notebook
contains clean outputs, a generic Python kernel declaration and no checkout-specific or helper
imports. Choose current installation routes from the maintained package guidance;
this private receiving does not establish a new public engine/platform matrix.

## Original developer reproduction and limits

Original 2026-10-03 developer profile: run `python -m pytest tests/test_scoring.py --receptor=llm` in
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


## Current installed scoring and portable source cells — 2026-11-10

[Current receiving](installed_fixed_score_2026-11-10.md) uses the same genuine
installed aeae47d wheel and retained native engine with the fixed six-provider
cohort. It keeps the original developer notebook/source outputs and historical
producer/data identities separate from the revised portable example (#105).
The 31 small-input scoring cases and 89 record semantics/reference/audit controls
pass under both caller policies; the single larger receptor guard remains an
explicit unexecuted selection boundary. Actual direct/API component equality,
negative native setup, preparation policy, file cleanup and independent histories
retain their original assertions. No runtime API or force field is changed.

The revised four exact formatted notebook cells are received separately from
outside-source directories with explicit caller inputs and ordinary installed
origins. Wrong identity/missing-capture controls both stop in the first cell with zero
native calls. These are headless Python executions, not new Jupyter/browser/public-platform
receiving. The original developer qualification above is not relabelled with
current software. Exact source/input/output/native identities and remaining scope
are retained in the owning receiving record.
