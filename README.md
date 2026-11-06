# DockingMT

*The molecular docking layer of MolSysSuite*

[![MolSysSuite: Scientific Component](https://img.shields.io/badge/MolSysSuite-scientific%20component-0b7285?labelColor=24292f)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_badges.md#scientific-component)
[![MolSysSuite policy](https://github.com/uibcdf/dockingmt/actions/workflows/molsyssuite-policy.yml/badge.svg?branch=main)](https://github.com/uibcdf/dockingmt/actions/workflows/molsyssuite-policy.yml)
[![Python 3.11 | 3.12 | 3.13](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md)
[![License](https://img.shields.io/github/license/uibcdf/dockingmt)](https://github.com/uibcdf/dockingmt/blob/main/LICENSE)
[![Codecov](https://codecov.io/gh/uibcdf/dockingmt/branch/main/graph/badge.svg)](https://app.codecov.io/gh/uibcdf/dockingmt)

DockingMT is a native scientific component of **MolSysSuite**, designed to provide a
reproducible, inspectable, and backend-independent framework for molecular docking.

Its long-term direction evolves *from box-based docking to molecular-landscape-aware docking*,
integrating conformational, topographic, flexibility, and pharmacophoric landscapes
provided by MolSysMT, TopoMT, ElastNetMT, and PharmacophoreMT.

AutoDock Vina is the initial reference engine for canonical protein–small-molecule docking
and redocking validation.

Our current public package route is the `uibcdf` Conda channel. Development
uses the local source checkouts; the qualified installation scope is described below.

## Start here

The current supported starting profile is one explicitly declared small-molecule
state and a rigid protein, with a physical search box and Vina. Molecular
preparation and characterization use MolSysMT. The installed walkthroughs below
have been qualified with a specific **private dependency composition**; a complete
compatible public installation is still tracked in
[the distribution review](devguide/validation/public_candidate_readiness.md).
These examples do not establish general predictive accuracy or binding affinity.

| Task | Current guide | What the example does |
| --- | --- | --- |
| Inspect a saved result | [Result inspection](devguide/validation/installed_result_inspection.md) | Reads caller-supplied records and checks available evidence; no new docking. |
| Inspect saved scoring evaluations | [Saved-scoring inspection](devguide/validation/installed_scoring_inspection.md) | Reads poses or explicit result collections, retaining scores, evaluation producers and missing evidence. |
| Prepare the declared 3PTB case | [Preparation and admission](devguide/validation/installed_3ptb_preparation.md) | Applies the explicit molecular recipe and checks inputs; no search. |
| Execute that case | [Two-search workflow](devguide/validation/installed_3ptb_execution.md) | Performs two new Vina searches and saves their results. |
| Evaluate saved poses | [Nine-heavy-atom evaluation](devguide/validation/installed_3ptb_evaluation.md) | Measures the declared positional RMSD without new searches. |

Each guide specifies its inputs, qualified composition and limitations. The
preparation walkthrough declares a dry protein, one ligand state and zero active
ligand torsions; these are case-specific choices. For another system, explicitly
choose states, waters/cofactors and active ligand bonds before execution.

During **automatic molecular preparation**, an empty `active_torsion_bonds` list
keeps the ligand rigid. Supplied prepared ligands and PDBQT retain their own
torsion trees. `assess_preparation(...)` returns a declaration assessment, not a
chemical-validity certificate: `unassessed` and an empty provisional-reason list
do not mean scientifically validated. Scores carry their method and conventional
units; they are not experimental binding free energies.

The detailed contracts below explain individual operations. Historical developer
benchmarks retain their original software requirements and are not the current
preparation walkthrough.

## Scientific evidence

The [scientific evidence overview](devguide/validation/scientific_evidence_overview_2026-11-04.md)
compares retained recovery/ranking observations, adverse controls and their limits.
Its table is reproducible from frozen records; repeated poses/seeds are not
independent complexes, and no pooled accuracy or affinity claim is made.
Original protocols, producers and failures remain linked. The
[evidence publication policy](devguide/validation/evidence_publication_policy.md)
explains the current repository presentation and when to reconsider it.

## Software qualification

Coverage reports measure the Python packages `dockingmt` and
`molsysviewer_dockingmt` through the existing unfiltered Linux/Python 3.14 CI suite,
including branches. The separate publisher runs automatically after ordinary
trusted-main CI and can retain/publish the measured XML when tests fail; PRs do
not request publication credentials. The badge reflects the last report accepted
by Codecov and may lag later direct or skipped commits. Scientific sibling packages,
native internals, browser/JavaScript runtime and separate validation campaigns are
outside this percentage; it is not a claim of scientific correctness or another
platform's qualification. The separate full-matrix workflow does not publish this
report. Original source/artifact/CI/service evidence is recorded under
[uibcdf/dockingmt#22](https://github.com/uibcdf/dockingmt/issues/22).

## Molecular input

Prepared ligands without their original native source reconstruct the available
PDBQT representation through MolSysMT. Flexible reconstruction delegates the known
atom-order permutation and restores prepared coordinate/charge precision through
public setters. It preserves available names and AutoDock labels; it does not
recover chemistry absent from PDBQT. The qualified source context is recorded in
[the reconstruction checkpoint](devguide/validation/flexible_reconstruction.md).

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

This example selects molecular inputs and a search domain. Before `dock(problem)`,
provide explicitly prepared/named inputs as described below; raw PDB conversion
alone does not supply a named AutoDock assignment.

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
objects for reconstruction while [MolSysMT mechanics persistence](https://github.com/uibcdf/molsysmt/issues/256)
is unresolved.

For `DockingProblem(...)`, inputs with multiple structures require
`receptor_structure_index` and `partner_structure_index` as applicable. The Vina
adapter prepares selected MolSys inputs when `dock(problem)` is called.
Preparation requires a valid named MolSysMT AutoDock4 assignment. Assign types
explicitly with `msm.build.assign_autodock_atom_types(...)` before automatic
preparation, or pass `typing_options` to `prepare_ligand`/`prepare_receptor`.
DockingMT selects no typing model and infers no types from names or residues.
The requested provider method requires its declared chemistry and indexed H;
an incomplete PDB or bare `atom_ff_type` column does not satisfy that contract.
Preparation also requires complete finite partial charges. Supply them before
automatic preparation or request a named MolSysMT method with `charge_options`
in either preparator. Absent charges raise an error; supplied zeros remain valid.
`VinaProtocol(allow_provisional_preparation=True)` cannot bypass absent charges or
missing named types. It retains inspection/opt-in for historical prepared objects
that already declare provisional provenance.
Ligand and receptor H reduction and charge transfer use public MolSysMT projection.
Merged parents need a declared virtual-H inventory and zero implicit H; inspect it with
`msm.physchem.get_hydrogen_inventory(...)`. Unknown counts are not assumed zero,
and fixed-state H addition also needs a declared inventory. Prepare or declare
the source through MolSysMT; provisional opt-in cannot bypass this requirement.
Both retained native systems carry aggregate prepared charges and derived
attribution. See the [ligand](devguide/validation/ligand_projection.md) and
[receptor](devguide/validation/receptor_projection.md) projection contracts.
Requested preparation stages compose their atom correspondence through public
MolSysMT maps, keeping generated atoms explicitly absent from the original input.
See the [map contract](devguide/validation/preparation_atom_maps.md) for native
direct/representative maps and compatible legacy output ordering.
The choice and assessment are recorded in result provenance. Externally
provided PDBQT inputs are accepted with an `unassessed` chemistry assessment.
Inspect a preparation before choosing an execution policy:

```python
from dockingmt import assess_preparation, prepare_ligand

prepared = prepare_ligand(
    ligand_with_declared_chemistry_indexed_hydrogens_and_charges,
    selection='all',
    typing_options={'typing_scheme': 'autodock4', 'method': 'chemical_environment'},
)
assessment = assess_preparation(prepared)
print(assessment['assessment'], assessment['provisional_reason_codes'])
```

`assess_preparation(...)` examines declared charge/type sources without molecular
conversion, file access or engine execution. Missing markers and external PDBQT
representations remain `unassessed`; this does not certify chemical validity.
Vina consumes the same public tool and retains its detached `assessment_report`
for each input in result provenance. See the
[API contract and executed notebook](devguide/validation/preparation_assessment.md).

Named charges are assigned explicitly with MolSysMT before preparation, for
example `msm.build.assign_partial_charges(ligand, method='gasteiger_marsili')`.
Preparation retains the original model and software provenance. Public
`dockingmt.audit_preparation_charges(prepared)` reports full-precision conservation,
hydrogen charge transfers and PDBQT rounding in elementary charge. See the
[charge contract and executed notebook](devguide/validation/named_partial_charges.md).
These numeric checks do not validate the charge model or chemical typing.
See the [required-charge contract](devguide/validation/required_partial_charges.md)
for explicit assignment, supplied zeros and failure behavior.

Complete charges are a DockingMT molecular-preparation representation requirement.
The Vina scoring function ignores supplied partial-charge values; its documentation
also states that charge assignment is not needed for Vina/Vinardo. See the
[official FAQ](https://autodock-vina.readthedocs.io/en/stable/faq.html) and
[Vina documentation](https://autodock-vina.readthedocs.io/en/latest/).
Charge conservation therefore checks representation integrity, not improved Vina
accuracy. Protonation and donor/acceptor typing remain relevant. Do not replace
missing charge data with invented zeros or infer that AD4 atom labels select AD4
scoring; the current preparation requirements still apply.

`prepare_ligand` also accepts explicit `hydrogen_options`, `charge_options` and
`typing_options` to call MolSysMT's fixed-state H, named-charge and named-type
builders in that order. Require
`mode='fixed_chemical_state'`, `pH=None` and an explicit engine for H addition;
attribute preservation defaults to strict. Original reports and generated-atom
maps are retained in preparation/result metadata. See the
[stage contract and notebook](devguide/validation/ligand_preparation_stages.md).
`prepare_receptor` accepts explicit `charge_options` before requested typing,
using the same provider operation without a receptor repair or H-addition stage.
The [declared 181L workflow](devguide/validation/181l_receptor_workflow.md)
provides bounded software evidence; its molecular-state hypotheses remain unassessed.

A controlled removal of nonpolar hydrogens
retains an explicit source atom map, and Vina's PDBQT output order is checked
before poses are returned. Molecular pose reconstruction and RMSD verify source
atom identities even when a flexible PDBQT tree changes their record order;
omitted hydrogens remain absent from reconstructed poses.
Raw PDBQT inputs without a molecular source map can still produce scores and
coordinates, but cannot be reconstructed as molecular poses or compared by
molecular RMSD. Explicit coordinate-array RMSD is positional. Other atom losses
require a verified map. Scientific preparation/model qualification remains scoped
under [issue #33](https://github.com/uibcdf/dockingmt/issues/33); #5's original
unsafe mechanisms are resolved.
Automatically prepared ligands remain rigid by default (`TORSDOF 0`). Supplied
prepared ligands or PDBQT retain their declared torsions. For a molecular ligand with an
explicit graph and bond orders, select active torsions by pairs of atom indices
in the selected ligand before nonpolar hydrogen removal:

```python
from dockingmt import VinaProtocol

protocol = VinaProtocol(
    active_torsion_bonds=[(1, 2)],
)
```

The pair above illustrates selected-ligand indices, not a bond recommendation for
every ligand. Explicit flexibility does not require provisional-preparation opt-in;
normal chemistry, charge and named-type requirements still apply. Nonempty
protocol cuts are for automatic preparation, not for rewriting supplied PDBQT.

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
unavailable graph information fails clearly. MolSysMT supplies the public
rotatable-bond classification and rigid-fragment partition; DockingMT records
the caller's explicit docking cuts. Explicit torsions do not validate charge
models or atom types.
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

The [recorded profiling study](devguide/validation/workflow_profiling.md) separates
import, problem construction, docking and export costs. Its developer runner's
default raw-PDB 181L preparation is historical and now refuses absent named
assignments. The separate `--manifest` route consumes verified captured PDBQT;
it executes new searches and does not reconstruct the original molecular source
or validate its chemistry. Consult the study's exact input/software requirements
before collecting new measurements.
The [profiling notebook](devguide/validation/workflow_profiling.ipynb) includes
tables and plots from the versioned raw reports and an optional section to collect
new measurements. Its default execution analyzes the saved baseline without docking.
The [result export benchmark](devguide/validation/result_export.md) and its
[comparison notebook](devguide/validation/result_export.ipynb) record the measured
reduction in time and Python allocations from removing redundant snapshot copies.

The [181L regression baseline](devguide/validation/181l_redocking_exploratory.md)
preserves the original file-backed record/replay commands, producer and exploratory
results. Those commands require their historical source/environment: current
raw-PDB preparation cannot recreate absent named assignments, and provisional
opt-in does not bypass that refusal. Use the current installed walkthrough above
for explicit preparation and saved-result inspection. The original unsafe
placeholder mechanisms in [#5](https://github.com/uibcdf/dockingmt/issues/5) are
resolved; scientific preparation/model qualification remains
[#33](https://github.com/uibcdf/dockingmt/issues/33).

An additional [1IEP external PDBQT check](devguide/validation/1iep_external_pdbqt.md)
uses the official AutoDock Vina prepared receptor and flexible ligand to audit
the Vina adapter. It retains the submitted PDBQT bytes, verifies pose atom
identity, and records the exact search box sent to Vina. Its external preparation
does not validate DockingMT's molecular profile, tracked in
[issue #33](https://github.com/uibcdf/dockingmt/issues/33).
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

Pose coordinates require finite real length data of shape `(N, 3)`. Complex or
nonfinite values are rejected before lossy conversion, including malformed saved
values and invalid mutable snapshots. See the
[coordinate-record contract](devguide/validation/pose_coordinate_contract.md).

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

For an installed-package walkthrough, use the
[saved-result inspection guide](devguide/validation/installed_result_inspection.md)
and [notebook](devguide/validation/installed_result_inspection.ipynb). They read
caller-supplied JSON with an externally expected identity, preserve the original
producer and score/unit meaning, and demonstrate damaged-evidence refusal.
Reading leaves the result detached; it does not reconstruct a molecular system
or perform new calculations. The two kernel profiles and actual private-archive
qualification retain their separate evidence and public-delivery limits.

For explicit preparation, the [3PTB guide](devguide/validation/installed_3ptb_preparation.md)
and [notebook](devguide/validation/installed_3ptb_preparation.ipynb) use public
MolSysMT/DockingMT APIs with caller-supplied source/declaration identities and
scientific choices. Run All prepares one receptor and rigid ligand and admits
two planned problems; it performs no engine, RMSD or viewer action. Both unit-policy
kernel profiles pass. The proposed execution follow-up requires a separate
registration; general molecular persistence and public delivery retain their owners.

The [execution follow-up](devguide/validation/installed_3ptb_execution.md) and
[notebook](devguide/validation/installed_3ptb_execution.ipynb) now deliver that
separately registered demonstration. Run All executes two new searches and
inspects the saved records through the public reader: native/displaced return
5/4 full poses in the qualified profile. No retry, RMSD, fixed-pose rescoring or
viewer action is included; recovery/affinity and public delivery remain separate.

The [saved-pose evaluation](devguide/validation/installed_3ptb_evaluation.md) and
[notebook](devguide/validation/installed_3ptb_evaluation.ipynb) complete the explicit
nine-observed-heavy-atom follow-up through public MolSysMT selection/geometry
and DockingMT reports. Both unit-policy profiles pass while preserving the full
thirteen-atom original records. Its retrospective <=2 Å positional observation
does not establish general model quality, affinity or public/visual acceptance.

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

## Installation status

DockingMT is currently developed and tested from source with its reviewed
scientific dependency versions. The first guarded Conda route is being prepared
under [#47](https://github.com/uibcdf/dockingmt/issues/47); its configuration does
not establish a published package or clean public installation. See
[development controls](devtools/README.md) for the managed source route.

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

Use `dockingmt.summarize_redocking(evaluations, failures=failures)` to summarize
compatible saved evaluations by caller case ID. It checks recorded policies,
retains separate failures and reports recovery with explicit evaluated/submitted
denominators. Its `any_returned` aggregate considers the complete returned set,
independently of requested top-N; with no evaluated reports it is `None`.
See the [collection contract](devguide/validation/redocking_summary.md)
and [offline notebook](devguide/validation/redocking_summary.ipynb).

The [5X72 positional-sensitivity control](devguide/validation/5x72_displacement_workflow.md)
provides a bounded scientific workflow with fixed inputs, public MolSysMT operations,
all 112 retained evaluations and a saved-result notebook. Constructed-point score
changes and negative outcomes remain separate from docking recovery and affinity.

The [prospective 3PTB protocol](devguide/validation/3ptb_prospective_protocol.md)
freezes an independent trypsin–benzamidinium case, explicit preparation decisions
and a 24-search population before execution. Source acquisition is complete;
molecular admission and docking results remain pending.
