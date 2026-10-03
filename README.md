# DockingMT

*The molecular docking layer of MolSysSuite*

[![MolSysSuite: Scientific Component](https://img.shields.io/badge/MolSysSuite-scientific%20component-0b7285?labelColor=24292f)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_badges.md#scientific-component)
[![MolSysSuite policy](https://github.com/uibcdf/dockingmt/actions/workflows/molsyssuite-policy.yml/badge.svg?branch=main)](https://github.com/uibcdf/dockingmt/actions/workflows/molsyssuite-policy.yml)
[![Python 3.11 | 3.12 | 3.13](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md)
[![License](https://img.shields.io/github/license/uibcdf/dockingmt)](https://github.com/uibcdf/dockingmt/blob/main/LICENSE)

DockingMT is a native scientific component of **MolSysSuite**, designed to provide a
reproducible, inspectable, and backend-independent framework for molecular docking.

Its long-term direction evolves *from box-based docking to molecular-landscape-aware docking*,
integrating conformational, topographic, flexibility, and pharmacophoric landscapes
provided by MolSysMT, TopoMT, ElastNetMT, and PharmacophoreMT.

AutoDock Vina is the initial reference engine for canonical protein–small-molecule docking
and redocking validation.

## Molecular input

`DockingProblem` accepts molecular inputs that MolSysMT can convert to
`molsysmt.MolSys`. Select the receptor and partner independently, even when both
come from the same complex:

```python
import molsysmt as msm
import pyunitwizard as puw
from dockingmt import BoxRegion, DockingProblem

complex_path = msm.systems['T4 lysozyme L99A']['181l.pdb']
domain = BoxRegion.from_selection(
    complex_path,
    selection="group_name=='BNZ'",
    padding=puw.quantity(8.0, 'angstrom'),
)
problem = DockingProblem(
    receptor=complex_path,
    partner=complex_path,
    search_domain=domain,
    receptor_selection="molecule_type=='protein'",
    partner_selection="group_name=='BNZ'",
)

receptor = problem.receptor_molsys
ligand = problem.partner_molsys
source_ligand_indices = problem.partner_atom_indices
```

For an explicit `BoxRegion`, supply either `lengths` or its alias `size`.
The center and dimensions require finite length quantities, and dimensions must
be strictly positive. `BoxRegion.from_points(...)` also supports a single point,
a line, or a planar point set when positive scalar padding gives the box nonzero
extent along every axis. For example, use `padding=puw.quantity(2, 'angstrom')`
or `padding='2 angstrom'`.

For redocking from one experimental complex, `DockingProblem.for_redocking(...)`
uses the same ligand selection and structure to define the box and the docking
partner. It selects structure 0 when the complex has one structure; when the
complex has multiple structures, pass `structure_index` explicitly. The same
index is used for the receptor, ligand and box.
`problem.to_dict()['molecular_inputs']` includes the resolved chemical state and
MolSysMT conversion report for each molecular input.
File-backed inputs also carry a SHA-256 fingerprint; reconstruction refuses a
file whose contents have changed. In-memory inputs still require the original
objects for reconstruction while [MolSysMT H5MSM charge preservation](https://github.com/uibcdf/molsysmt/issues/234)
is unresolved.

For `DockingProblem(...)`, inputs with multiple structures require
`receptor_structure_index` and `partner_structure_index` as applicable. The Vina
adapter prepares selected MolSys inputs when `dock(problem)` is called.
Preparation preserves atomic partial charges and aromaticity when the source
provides them; otherwise it records placeholder charges. AutoDock atom types
currently use a heuristic in both cases. Vina rejects these provisional
preparations by default, including `PreparedLigand`
and `PreparedReceptor` objects produced by DockingMT. To run an exploratory
calculation while [issue #5](https://github.com/uibcdf/dockingmt/issues/5)
remains open, pass `VinaProtocol(allow_provisional_preparation=True)`. The choice
and the preparation assessment are recorded in result provenance. Externally
provided PDBQT inputs are accepted with an `unassessed` chemistry assessment.
Inspect a preparation before choosing an execution policy:

```python
from dockingmt import assess_preparation, prepare_ligand

prepared = prepare_ligand(ligand, selection='all')
assessment = assess_preparation(prepared)
print(assessment['assessment'], assessment['provisional_reason_codes'])
```

`assess_preparation(...)` examines declared charge/type sources without molecular
conversion, file access or engine execution. Missing markers and external PDBQT
representations remain `unassessed`; this does not certify chemical validity.
Vina consumes the same public tool and retains its detached `assessment_report`
for each input in result provenance. See the
[API contract and executed notebook](devguide/validation/preparation_assessment.md).

A controlled removal of nonpolar hydrogens
retains an explicit source atom map, and Vina's PDBQT output order is checked
before poses are returned. Molecular pose reconstruction and RMSD verify source
atom identities even when a flexible PDBQT tree changes their record order;
omitted hydrogens remain absent from reconstructed poses.
Raw PDBQT inputs without a molecular source map can still produce scores and
coordinates, but cannot be reconstructed as molecular poses or compared by
molecular RMSD. Explicit coordinate-array RMSD is positional. Other atom losses
require a verified map. Preparation chemistry remains provisional under
[issue #5](https://github.com/uibcdf/dockingmt/issues/5).
Ligands remain rigid by default (`TORSDOF 0`). For a molecular ligand with an
explicit graph and bond orders, select active torsions by pairs of atom indices
in the selected ligand before nonpolar hydrogen removal:

```python
from dockingmt import VinaProtocol

protocol = VinaProtocol(
    active_torsion_bonds=[(1, 2)],
    allow_provisional_preparation=True,
)
```

`VinaProtocol` requires integer search parameters and explicit units for a supplied
energy cutoff. Use `energy_range=puw.quantity(3.0, 'kcal/mol')` or
`energy_range='12.552 kJ/mol'`; bare numbers are rejected. Omitting the cutoff
resolves to 3 kcal/mol. Cutoffs must be finite, nonnegative scalars.
`dock`, `VinaBackend.dock`, the protocol constructor, and the preparation helpers
reject unknown argument names through ArgDigest. Molecular forms and selections
are interpreted by MolSysMT.

The current `VinaBackend` executes `vina` and `vinardo` scoring. A protocol can
record `scoring='ad4'`, but this adapter rejects its execution with a capability
error before preparation. It does not yet accept the external affinity maps
needed by AD4; [Vina's implementation](https://github.com/ccsb-scripps/AutoDock-Vina/blob/v1.2.7/src/lib/vina.cpp#L292-L299)
rejects computing Vina maps with that scoring function.

The current Vina adapter also requires empty `problem.constraints` and
`problem.search_guidance` lists or dictionaries, as supplied by default. A
nonempty request fails with a capability error before preparation or execution:
the adapter cannot apply those scientific requirements.

The same selection can be passed to `prepare_ligand(...)` when preparing a
ligand explicitly. DockingMT checks that selected bonds are single, outside
rings and amide C–N bonds, and have nonterminal heavy-atom sides; invalid or
unavailable graph information fails clearly. The temporary rigid-fragment
calculation is tracked by [MolSysMT #224](https://github.com/uibcdf/molsysmt/issues/224)
and will be removed when MolSysMT provides the verified operation. Explicit
torsions do not validate the still provisional charges and atom types.
Result provenance records the hydrogen and torsion policies, preparation
assessment, and SHA-256 digests of the PDBQT bytes submitted to Vina. Remaining
preparation-decision provenance is tracked in
[issue #4](https://github.com/uibcdf/dockingmt/issues/4).
Set `VinaProtocol(capture_backend_inputs=True)` to also retain the exact receptor
and ligand PDBQT bytes as base64 in the serialized result's `backend_artifacts`.
This increases manifest size and supports independent inspection of the backend
inputs; it does not validate their chemistry. File inputs are staged from the
captured bytes before Vina reads them, so the recorded digest identifies the
submitted content.

For performance diagnostics, use `VinaProtocol(collect_timings=True)` and inspect
`result.provenance['timings']`. The record contains consecutive adapter phases,
their total, an explicit `second` unit, and a monotonic `perf_counter` clock.
Profiling is disabled by default. The existing `elapsed_seconds` still measures
only native docking; constructing the problem and exporting the result happen
outside the adapter timings. Successful runs retain timings after temporary-file
cleanup; failures keep their normal exception behavior.

Measure the current 181L workflow in fresh processes with paired profiling modes:

```bash
python devtools/profile_workflow.py --repeats 3 --report /tmp/181l-profile.json
```

Pass `--manifest /tmp/181l-manifest.json` to profile verified captured PDBQT inputs
instead of automatic molecular preparation. The command checks matching inputs,
outputs, and execution context, and separates import, problem construction,
docking, dictionary export, JSON encoding, and file writing. See the
[phase definitions and measured limits](devguide/validation/workflow_profiling.md).
The [profiling notebook](devguide/validation/workflow_profiling.ipynb) includes
tables and plots from the versioned raw reports and an optional section to collect
new measurements. Its default execution analyzes the saved baseline without docking.
The [result export benchmark](devguide/validation/result_export.md) and its
[comparison notebook](devguide/validation/result_export.ipynb) record the measured
reduction in time and Python allocations from removing redundant snapshot copies.

For the file-backed 181L regression case, save a result manifest and replay it
in a separate command:

```bash
python devtools/redocking_181l.py record --manifest /tmp/181l-manifest.json
python devtools/redocking_181l.py replay --manifest /tmp/181l-manifest.json --report /tmp/181l-report.json
```

The report lists each pose's source-mapped RMSD and named scores, near-native
rank at the declared 2.5 Å cutoff, failure mode, source and PDBQT fingerprints,
code revision, and replay differences. The manifest retains both PDBQT inputs;
replay validates their digests and checks that the new run submits identical
bytes. Its assessment is **exploratory** while
the chemical preparation in [issue #5](https://github.com/uibcdf/dockingmt/issues/5)
remains provisional. Use the reported metrics for regression, not as a validated
docking-performance claim. The measured case is documented in the
[181L regression baseline](devguide/validation/181l_redocking_exploratory.md).

An additional [1IEP external PDBQT check](devguide/validation/1iep_external_pdbqt.md)
uses the official AutoDock Vina prepared receptor and flexible ligand to audit
the Vina adapter. It retains the submitted PDBQT bytes, verifies pose atom
identity, and records the exact search box sent to Vina. DockingMT's molecular
preparation remains under [issue #5](https://github.com/uibcdf/dockingmt/issues/5).
The [1IEP native preparation audit](devguide/validation/1iep_preparation_audit.md)
also verifies seven explicitly selected torsions and records the remaining
charge and atom-type differences.

## Inspecting results

`dockingmt.score(...)` evaluates one already prepared PDBQT conformation with
Vina/Vinardo and returns a `DockingPose`, without pose search or optimization:

```python
problem = dmt.DockingProblem('receptor.pdbqt', 'ligand_pose.pdbqt', box)
pose = dmt.score(problem, dmt.VinaProtocol(cpu=1, seed=123), score_name='vina_fixed')
rescored = dmt.score(
    problem, dmt.VinaProtocol(cpu=1, seed=123, scoring='vinardo'),
    pose=pose, score_name='vinardo_fixed',
)
```

It retains all eight native components, empirical units, exact input hashes and
independent evaluation history. A supplied pose must match the prepared ligand
geometry and known states. Existing names cannot be overwritten. The public
`pose.with_scores(...)` also adds external evaluations independently. See the
[fixed-pose contract](devguide/validation/fixed_pose_scoring.md) and
[executed notebook](devguide/validation/fixed_pose_scoring.ipynb) for preparation,
identity and comparison limits.

Pose scores require nonempty names and finite real values. DockingMT normalizes
them to Python floats without inferring units. `result.rank_by('vina')` returns
a new result with lower scores first; use `ascending=False` for higher scores
first. Ties preserve input order, and provenance records the selected score and
direction. Ranking rechecks scores after rescoring edits and rejects invalid
values before returning a ranked result.

Vina/Vinardo poses now expose `pose.score_definitions`: method/version, empirical
meaning, conventional unit, preferred direction and submitted-input/settings
context. Described rankings require matching definitions and state IDs; legacy
undescribed scores remain explicitly rankable. The direction stays explicit and
each decision is retained in `result.ranking_history`, including the initial
backend order. See the [score contract](devguide/validation/score_semantics.md)
and [executed offline example](devguide/validation/ranking_history.ipynb).

`DockingPose.to_dict()` and `DockingResult.to_dict()` produce independent
structured snapshots, including nested metadata and provenance. Editing an
exported record cannot change the original object. The corresponding
`from_dict()` methods reconstruct independently of the supplied record.
The serialized schema remains version `1.0`.
Readers accept explicit `schema_version='1.0'` and legacy records without the
field. An explicitly unsupported or malformed version is rejected before
interpreting the scientific payload. This applies to `BoxRegion`, `DockingPose`,
`DockingResult`, `DockingProblem`, and `VinaProtocol`, including their nested
pose and domain records.

## Governance and Design Authority

* [`MOLSYSSUITE_GUIDE.md`](MOLSYSSUITE_GUIDE.md) routes suite-wide policies and cross-component issues to `uibcdf/molsyssuite`.
* [`AGENTS.md`](AGENTS.md) specifies developer and AI agent instructions.
* [`devguide/`](devguide/) contains the frozen architectural and scientific seed (`devguide v0.1`).

For an iterable of prepared `DockingProblem` inputs, use
`dockingmt.dock_many(problems, protocol, on_error='record')`. It delivers one
`DockingOutcome` at a time, retaining either a normalized result or a failure
summary with the input position and declarations. The default error policy
propagates failures. See the [incremental execution contract](devguide/validation/incremental_docking.md)
and [executed notebook](devguide/validation/incremental_docking.ipynb).

## Development

Routine development uses `molsyssuite@uibcdf_3.14` (Python 3.14); the required source range is Python 3.11 to 3.14.
Qualification and public delivery remain tracked in [#30](https://github.com/uibcdf/dockingmt/issues/30);
the badge retains the previously verified range until admission.

```bash
# Run local gates before committing
ruff check .
ruff format --check .
pytest --receptor=llm
python devtools/devguide_index.py --check
```

Saved records can be checked with `dockingmt.audit_result(record)`, which reports
internal agreement, missing evidence and contradictions without running docking.
See the [offline audit contract](devguide/validation/result_audit.md) and
[executed notebook](devguide/validation/result_audit.ipynb).

For a standalone scoring or rescoring pose, use
`dockingmt.audit_pose(pose.to_dict())`. It checks current scores against the
retained evaluations, descriptors, execution settings and input evidence.
See the [pose audit contract](devguide/validation/pose_audit.md) and
[executed notebook](devguide/validation/pose_audit.ipynb) for its offline scope.

The experimental MolSysMT prepared-PDBQT input path and initial SDF acceptance
are documented in [native format consumption](devguide/validation/native_molsysmt_formats.md)
and its [executed 1IEP notebook](devguide/validation/native_molsysmt_formats.ipynb).

`dockingmt.view(result, reference=reference)` displays a static reference or one
reference frame per pose. Reusing a viewer replaces the displayed molecular
scene, and loading failures propagate. See the [frame correspondence contract](devguide/validation/viewer_reference.md)
and [executed notebook](devguide/validation/viewer_reference.ipynb).

Use `dockingmt.evaluate_redocking(result, reference, rmsd_cutoff=cutoff)` for
per-pose RMSD and first-N recovery with explicit units and retained comparison
evidence. See the [evaluation contract](devguide/validation/redocking_evaluation.md)
and [executed notebook](devguide/validation/redocking_evaluation.ipynb).
