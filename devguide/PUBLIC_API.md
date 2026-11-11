# Public API guide

Use `import dockingmt as dmt` for the supported entry points. For a first
workflow, start with the [saved-result inspection](validation/installed_result_inspection.md)
or the [preparation-to-execution walkthroughs](../README.md#start-here).
This page maps the current source API and its work/ownership boundaries; the
walkthroughs retain their own exact installed compositions and qualifications.

The map covers all 33 names in `dockingmt.__all__`, including the additive
`dockingmt.exceptions` namespace delivered under [#94](https://github.com/uibcdf/dockingmt/issues/94).
It was checked against source base `457eb090f0e36b6d2b34e1b7d90cbab4d43a4c00`
plus that increment. It is maintained guidance, not a stable-1.0 promise or a
claim that an earlier wheel contains later APIs. The separate
[current private wheel receiving](validation/record_wheel_editable_2026-11-09.md)
qualifies these offline APIs with the recorded editable sibling composition;
public installation and full scientific/platform gates retain their own scope. For the installed version, use
`help(dmt.DockingResult)` or `inspect.signature(dmt.dock)`.

## Choose an operation

| Need | Public route | Work performed |
| --- | --- | --- |
| Read saved observations | `DockingPose.from_dict`, `DockingResult.from_dict`, `DockingOutcome.from_dict` | Validate and restore records without reconstructing a molecular problem or running an engine. |
| Inspect available evidence | `audit_pose`, `audit_result`, `verify_captured_inputs` | Cross-check supplied mappings/captured bytes offline. An internally consistent record is not authenticated provenance or chemical validation. |
| Change a result's order | `DockingResult.rank_by` | Stable ordering of existing scores, with ranking history; no new score or search. |
| Describe a physical region | `BoxRegion` | Quantity-aware box construction. `from_selection` additionally reads a molecular system through MolSysMT. |
| Declare molecular inputs | `DockingProblem`, `DockingProblem.for_redocking` | Resolve supported inputs/selections/states through MolSysMT. This can read/convert molecular data. |
| Make explicit preparations | `prepare_receptor`, `prepare_ligand` | Molecular preparation and export using provider tools; choices remain explicit and case-dependent. |
| Inspect preparation declarations/charges | `assess_preparation`, `audit_preparation_charges` | Inspect a prepared object; neither certifies general chemical validity. |
| Declare engine parameters | `VinaProtocol` | Construct/validate parameters; construction itself does not run Vina. |
| Search or evaluate a prepared pose | `dock`, `score`, `VinaBackend` | Invoke the selected engine; may prepare supported inputs, allocate maps and perform native work. Scoring is a distinct operation from search. |
| Run a prepared collection | `dock_many` → `DockingOutcome` | Execute serially as the caller advances the iterator; no hidden preparation phase, global ranking or parallel executor. |
| Compare existing fixed-score observations | `compare_scores` | Validate actual matching preparations/identity through MolSysMT; no new scoring/search. The accepted profile is Vina/Vinardo 1.2.7 `lig_inter`. |
| Measure recovery against a reference | `evaluate_redocking` | Molecular correspondence/geometry through MolSysMT with explicit reference, cutoff and frame/symmetry policy; no new search. |
| Combine compatible evaluation reports | `summarize_redocking` | Offline cohort/denominator checks; incompatible populations are refused. |
| Associate saved interaction analysis | `bind_interactions` → `PoseInteractions` | Validate an existing analysed carrier against one selected pose. Does not run a detector or infer atom matching. |
| Explore interactively | `view` (`show` is the same function) | Construct/use MolSysViewer and its DockingMT addon; rendering/communication has separate live acceptance. |
| Implement an extension | `SearchDomain`, `DockingProtocol`, `DockingBackend` | Existing abstract contracts. Only add a concrete implementation for an accepted workflow. |
| Inspect version or units | `__version__`, `__print_version__`, `pyunitwizard` | Version value/printing and the provider module. PyUnitWizard retains ownership of its API. |
| Handle a diagnosed local failure | `exceptions` | Public aliases to the existing DockingMT catalog classes; see below. |

### Read and audit a caller-owned file

This example reads an existing JSON result. It writes no file and performs no
molecular reconstruction, preparation, engine operation or visualization.
Replace `saved-result.json` with your own input path.

```python
import json
from pathlib import Path

import dockingmt as dmt

record = json.loads(Path('saved-result.json').read_text(encoding='utf-8'))
try:
    result = dmt.DockingResult.from_dict(record)
except dmt.exceptions.ArgumentError as error:
    print(error.code, error.extra.get('arg_name'))
    raise

report = dmt.audit_result(result.to_dict())
print('Poses:', len(result))
print('Evidence:', report['status'])
if result.top_pose is not None:
    print('Selected pose:', result.top_pose.pose_id)
```

Audit status is `consistent`, `incomplete` or `inconsistent`; contradictions
take precedence over missing evidence. A restored record can be usable while
its evidence is incomplete. Native memory failures during quantity/protocol/
reference checks propagate to the caller rather than becoming an audit verdict;
see [the source correction](validation/audit_resource_errors_2026-11-09.md).
`verify_captured_inputs` takes the **artifacts
mapping**, such as `record['provenance']['backend_artifacts']`, rather than the
whole result. Missing captures remain missing evidence.

## Units, positions and ownership

Pass physical quantities with their units, for example
`dmt.pyunitwizard.quantity([1, 2, 3], 'nm')`. Pose coordinates are normalized to
nanometres internally; records carry explicit units. Backend conversion names
its target unit (`BoxRegion.to_backend_box(unit='angstrom')`). Reading a record
must not reinterpret its values using the application's current unit policy.

`result[i]`, `PoseInteractions.pose_index` and `DockingOutcome.index` use
zero-based positions. `view(..., pose_rank=1)` uses a **one-based collection
position**, despite its historical parameter name. Neither is a scientific
rank or a stable pose identity. `DockingResult.top_pose` selects the first pose
with `rank == 1`, otherwise the first current pose, otherwise `None`; it does
not sort scores. Use explicit `pose_id` and partner/receptor state IDs when
associating observations. Optional unknown IDs do not establish identity.

`result.poses` returns a fresh list containing the live pose objects. Indexing,
iteration, `top_pose` and pose coordinate access also expose live objects/data.
Public pose attributes include `scores`, `rank`, `pose_id`, `partner_state_id`,
`receptor_state_id` and `metadata`. Constructors do not promise a recursively
detached copy of every supplied Python object. Keep borrowed molecular inputs
stable while an operation uses them.

`to_dict`/`from_dict` provide detached observation snapshots for pose/result/
outcome records. Prepared ligand/receptor `to_dict` and problem `to_dict` also
detach their declaration lists and nested metadata. Problem `from_dict` detaches
consumed declarations and selections; explicit live receptor/partner arguments
remain borrowed, and unused/replaced record payloads are not copied. `ranking_history` and score-definition access also detach their
evidence. A Python snapshot may contain caller-supplied NumPy values, tuples,
sets or other metadata: `to_dict` is **not a universal JSON encoder**. Select
JSON-compatible metadata before using `json.dumps`; never erase units or
scientific evidence merely to serialize it.

Prepared declaration exports retain their existing schema and omit coordinates
and `source_molsys`; they are not full molecular checkpoints. Keep native
molecular systems through the provider's supported persistence route. Copying a
Python declaration needs memory proportional to that declaration, while leaving
the live molecular source outside the copied payload.

When a source is identified as an existing file, an open/read failure propagates
its original filesystem exception. It is not recorded as literal text or
reclassified as changed scientific content. Successful hashes and explicit
literal/nonfile inputs retain their existing interpretation.

`rank_by(score_name, ascending=True)` returns a new ordered result with new pose
objects, stable ties and recorded ranking evidence. It validates score
descriptors and states; it does not prove chemical comparability. The explicit
direction controls ordering. Its attached problem remains borrowed/reused.

`compare_scores` additionally validates supplied preparations and correspondence
through MolSysMT. Its [54-case installed software controls](validation/installed_score_comparison_2026-11-10.md)
exercise method/reference compatibility, units, direction, grouping, ties and
refusals with explicitly synthetic molecular seams. Passing those controls is
separate from validating a real molecular comparison or its scientific meaning.

`result.reconstruct_problem(...)` is an explicit molecular operation; it can
read/convert supplied or retained source inputs and attaches the problem only
after validation. `DockingProblem.from_dict` also resolves molecular inputs.
Prepared objects export dictionaries but have no public `from_dict` codec;
their exported preparation record is not a lossless native molecular archive.
See [molecular inputs](archive/use_molsysmt_as_canonical_molecular_input_for_the_core_mvp.md) and
[record contracts](validation/result_export.md) for the detailed boundaries.

## Declare resources and scientific choices

Choose engine CPU use explicitly, especially on a shared machine:

```python
import dockingmt as dmt

protocol = dmt.VinaProtocol(cpu=1, seed=17, capture_backend_inputs=True)
```

The current API default is `cpu=0`, passed to Vina's automatic CPU selection;
it does not impose a one-worker limit. This example constructs parameters only.
The declaration does not reserve memory or CPUs. Apply the execution host's
resource policy before running an engine.

Other defaults include `exhaustiveness=8`, `n_poses=9`, energy range 3 kcal/mol,
`seed=None`, `scoring='vina'`, `allow_provisional_preparation=False`,
`capture_backend_inputs=False` and `collect_timings=False`. Native capabilities
and supported adapter routes still govern which scoring method can run.
Construction accepting a method name alone is not backend qualification.

During automatic preparation, an empty `active_torsion_bonds` list keeps the
ligand rigid; supplied prepared/PDBQT inputs retain their own torsion trees.
Select molecular states, hydrogens, charges, waters/cofactors and active bonds
deliberately. `assess_preparation(...)` declarations, charge audits and
provisional admission have separate meanings, explained in the
[preparation walkthrough](validation/installed_3ptb_preparation.md).
An engine score is not experimental binding affinity.
MemoryError and OS ENOMEM from prepared-geometry conversion and reads propagate
unchanged; ordinary malformed geometry keeps its structured argument error and
provider cause. See [the source correction](validation/scoring_geometry_resource_errors_2026-11-10.md)
and [genuine installed receiving](validation/installed_allocation_fixes_2026-11-10.md).

`dock_many` admits options/resolves the backend at the call, then consumes and
executes one input at a time during iteration. It borrows the protocol/backend
and source iterator. Prepared inputs or PDBQT are required. With
`on_error='record'`, item failures become detached summaries in outcomes;
source-iterator failures, memory-allocation failures (`MemoryError` or
`OSError` with `errno.ENOMEM`) and process-control interruptions still propagate.
Ordinary file errors such as missing files or full disks remain recordable. Retain/write each outcome if needed: the iterator does not
retain completed results. See [the collection workflow](validation/e2_native_collection_2026-11-07.md#short-reviewed-public-route).

The [earlier installed batch/refusal controls](validation/installed_execution_boundaries_2026-11-10.md)
receive the full batch module under both caller unit policies: individual and
serial-batch runs agree for the same explicit seed, and an intervening file
failure leaves later results intact. Capability and staging-cleanup controls
pass separately without native construction. This synthetic software evidence
retains its exact inputs/providers and does not extend scientific/public scope.
The later [OS allocation correction](validation/batch_os_allocation_fix_2026-11-10.md)
is qualified in source; that earlier cached wheel has not received the fix.
The new genuine `0.0.0+359.g37a61e6` private wheel
[receives both #106 and #107](validation/installed_allocation_fixes_2026-11-10.md):
all 305 resource/backend/staging/audit/batch cases pass under each unit policy,
including the original tiny native score and search controls. This is bounded
private installed evidence; public distribution, full scientific coverage and
platform acceptance retain their separate gates.

The same actual wheel also passes the
[complete 26-module offline union](validation/installed_offline_union_2026-11-10.md):
1,287 cases per unit policy, retaining four explicitly excluded native cases.
Original case identities and selected ASTs remain intact, both installed roots
are actually imported/validated and all 606 support inputs retire. This software
gate performs no actual molecular, engine or Viewer operation; earlier live
controls retain their separate evidence and original producer identities.

`evaluate_redocking` requires `rmsd_cutoff` and an explicit reference population;
its `top_n` windows follow current collection order, independently of recorded
rank. Selection/frame/symmetry choices affect the question being measured.
`summarize_redocking` retains compatible report denominators and explicit
failures; it does not turn repeated poses/seeds into independent complexes.
See [evaluation](validation/installed_3ptb_evaluation.md) and
[aggregation](../dockingmt/aggregation.py).

`bind_interactions` requires explicit `pose_index`, atom correspondence and both
state IDs, an existing analysed one-frame carrier, and the deliberate
`assume_aligned=True` declaration. The default `False` refuses an unasserted
frame. The binding retains its result/pose and provides detached carrier/
analysis access; it has no public persistence codec. See
[the binding contract](validation/pose_interaction_binding.md) and
[the explicit view route](validation/pose_interaction_view.md).

## Catch local diagnostics

Use `dmt.exceptions.ArgumentError` for a DockingMT-owned diagnosed argument
failure, or `dmt.exceptions.DockingMTException` for its local catalog family.
`ArgumentError` is not a subclass of native `ValueError`. The public namespace
exports the **same existing classes**, preserving identity, implementation
module paths, native multiple inheritance, catalog codes, `extra` and causes.
The `Viewer*` classes retain their existing ValueError/RuntimeError families.

For a caught local error, inspect `error.code`, field context in `error.extra`
and `error.__cause__` when present. For example, a normalized field failure
keeps its original provider cause rather than discarding it. Errors raised
directly by ArgDigest or another provider keep that provider's ownership and
are not all subclasses of the local family. File/JSON errors also retain their
own types. Memory/resource failures and `KeyboardInterrupt`/`SystemExit` must
not be treated as ordinary bad input or swallowed by a broad retry loop.

The source map below lists all 13 public exception aliases. No provider error
or warning category is re-exported as a local exception.

## Source map

The following signatures are source declarations; decorators may expose further
argument diagnostics. Properties are accessed without parentheses. The map
includes source-defined public class members and their useful collection
dunder methods. Inherited extension contracts retain the owning base class.
Private implementation names and arbitrary provider attributes are outside it.

<!-- SOURCE_MAP:START -->

### Root functions and values

| Name | Declaration / owner |
| --- | --- |
| [bind_interactions](../dockingmt/interactions.py) | `bind_interactions(result: DockingResult, molecular_system: Any, *, pose_index: int, pose_atom_indices: Any, partner_state_id: str, receptor_state_id: str, assume_aligned: bool=False, coordinate_tolerance: Any=None) -> PoseInteractions` |
| [compare_scores](../dockingmt/comparison.py) | `compare_scores(result, score_name, *, problems, ascending)` |
| [summarize_redocking](../dockingmt/aggregation.py) | `summarize_redocking(evaluations: Mapping, *, failures: Mapping \| None=None) -> dict` |
| [evaluate_redocking](../dockingmt/evaluation.py) | `evaluate_redocking(result: DockingResult, reference: Any, *, rmsd_cutoff: Any, top_n: tuple[int, ...]=(1, 5), selection: Any='all', reference_info: Mapping \| None=None, symmetry_options: Mapping \| None=None) -> dict[str, Any]` |
| [dock_many](../dockingmt/batch.py) | `dock_many(problems, protocol=None, backend=None, on_error='raise')` |
| [audit_pose](../dockingmt/core/pose_audit.py) | `audit_pose(record)` |
| [assess_preparation](../dockingmt/preparation/assessment.py) | `assess_preparation(prepared)` |
| [audit_preparation_charges](../dockingmt/preparation/charges.py) | `audit_preparation_charges(prepared)` |
| [audit_result](../dockingmt/core/audit.py) | `audit_result(record)` |
| [verify_captured_inputs](../dockingmt/core/audit.py) | `verify_captured_inputs(artifacts)` |
| `__version__` | Generated version value; created by the build/version machinery. |
| [__print_version__](../dockingmt/__init__.py) | `__print_version__()` |
| [pyunitwizard](../dockingmt/_pyunitwizard.py) | Provider module; follow PyUnitWizard documentation. |
| [prepare_receptor](../dockingmt/preparation/receptor.py) | `prepare_receptor(molecular_system: Any, selection: str="molecule_type=='protein'", state_id: str \| None=None, *, charge_options: dict[str, Any] \| None=None, typing_options: dict[str, Any] \| None=None) -> PreparedReceptor` |
| [prepare_ligand](../dockingmt/preparation/ligand.py) | `prepare_ligand(molecular_system: Any, selection: str="molecule_type=='small molecule'", state_id: str \| None=None, torsion_dof: int \| None=None, active_torsion_bonds: list[tuple[int, int]] \| None=None, *, hydrogen_options: dict[str, Any] \| None=None, charge_options: dict[str, Any] \| None=None, typing_options: dict[str, Any] \| None=None) -> PreparedLigand` |
| [dock](../dockingmt/dock.py) | `dock(problem: DockingProblem, protocol: DockingProtocol \| None=None, backend: DockingBackend \| str \| None=None) -> DockingResult` |
| [score](../dockingmt/score.py) | `score(problem: DockingProblem, protocol: DockingProtocol \| None=None, backend: DockingBackend \| str \| None=None, pose: DockingPose \| None=None, score_name: str='score') -> DockingPose` |
| [show](../dockingmt/view.py) | Exact alias of `view`. |
| [view](../dockingmt/view.py) | `view(item: Any=None, *, result: DockingResult \| None=None, problem: DockingProblem \| None=None, search_domain: SearchDomain \| None=None, reference: Any=None, receptor: Any=None, partner: Any=None, pose_rank: int=1, view: Any=None, **kwargs: Any) -> Any` |

### Model and extension classes

#### PoseInteractions

Source: [dockingmt/interactions.py](../dockingmt/interactions.py).

| Member | Declaration |
| --- | --- |
| `__init__` | `__init__(result: DockingResult, molecular_system: Any, *, pose_index: int, pose_atom_indices: Any, partner_state_id: str, receptor_state_id: str, assume_aligned: bool=False, coordinate_tolerance: Any=None)` |
| `pose_index` | Property `int` |
| `result` | Property `DockingResult` |
| `pose` | Property `DockingPose` |
| `association` | Property `dict[str, Any]` |
| `analysis_names` | Property `tuple[str, ...]` |
| `get_analysis` | `get_analysis(name: str) -> Any` |
| `to_molecular_system` | `to_molecular_system() -> Any` |

#### DockingOutcome

Source: [dockingmt/core/outcome.py](../dockingmt/core/outcome.py).

| Member | Declaration |
| --- | --- |
| `__init__` | `__init__(index, *, backend=None, problem_info=None, protocol_info=None, result=None, error=None)` |
| `index` | Property |
| `status` | Property |
| `backend` | Property |
| `result` | Property |
| `error` | Property |
| `problem_info` | Property |
| `protocol_info` | Property |
| `to_dict` | `to_dict()` |
| `from_dict` | `from_dict(record)` |

#### SearchDomain

Source: [dockingmt/core/search_domain.py](../dockingmt/core/search_domain.py). Bases: `ABC`.

| Member | Declaration |
| --- | --- |
| `center` | Property `Any` |
| `volume` | Property `Any` |
| `as_box_approximation` | `as_box_approximation() -> BoxRegion` |

#### BoxRegion

Source: [dockingmt/core/search_domain.py](../dockingmt/core/search_domain.py). Bases: `SearchDomain`.

| Member | Declaration |
| --- | --- |
| `__init__` | `__init__(center: Any, lengths: Any \| None=None, size: Any \| None=None, name: str \| None=None)` |
| `derivation` | Property `dict[str, Any] \| None` |
| `center` | Property `Any` |
| `lengths` | Property `Any` |
| `size` | Property `Any` |
| `bounds` | Property `tuple[Any, Any]` |
| `volume` | Property `Any` |
| `as_box_approximation` | `as_box_approximation() -> BoxRegion` |
| `to_backend_box` | `to_backend_box(unit: Any='angstrom') -> dict[str, Any]` |
| `contains` | `contains(point: Any) -> bool` |
| `from_bounds` | `from_bounds(min_coords: Any, max_coords: Any, padding: Any \| None=None, name: str \| None=None) -> BoxRegion` |
| `from_points` | `from_points(points: Any, padding: Any \| None=None, name: str \| None=None) -> BoxRegion` |
| `from_selection` | `from_selection(molecular_system: Any, selection: str='all', structure_indices: int \| list[int]=0, padding: Any \| None=None, name: str \| None=None, chemical_state: Any='reference') -> BoxRegion` |
| `to_dict` | `to_dict() -> dict[str, Any]` |
| `from_dict` | `from_dict(data: dict[str, Any]) -> BoxRegion` |

#### DockingPose

Source: [dockingmt/core/results.py](../dockingmt/core/results.py).

| Member | Declaration |
| --- | --- |
| `__init__` | `__init__(coordinates: Any, scores: dict[str, float] \| None=None, rank: int \| None=None, pose_id: str \| None=None, partner_state_id: str \| None=None, receptor_state_id: str \| None=None, metadata: dict[str, Any] \| None=None, score_definitions: dict[str, dict[str, Any]] \| None=None)` |
| `score_definitions` | Property `dict[str, dict[str, Any]]` |
| `coordinates` | Property `Any` |
| `n_atoms` | Property `int` |
| `with_scores` | `with_scores(scores: dict[str, float], score_definitions: dict[str, dict[str, Any]] \| None=None) -> DockingPose` |
| `to_dict` | `to_dict() -> dict[str, Any]` |
| `from_dict` | `from_dict(data: dict[str, Any]) -> DockingPose` |
| `get_rmsd` | `get_rmsd(reference: Any, selection: str='all') -> Any` |
| `to_molecular_system` | `to_molecular_system(partner: Any) -> Any` |

#### DockingResult

Source: [dockingmt/core/results.py](../dockingmt/core/results.py).

| Member | Declaration |
| --- | --- |
| `__init__` | `__init__(poses: list[DockingPose], problem_info: dict[str, Any] \| None=None, protocol_info: dict[str, Any] \| None=None, provenance: dict[str, Any] \| None=None, problem: Any=None)` |
| `ranking_history` | Property `list[dict[str, Any]]` |
| `__len__` | `__len__() -> int` |
| `__getitem__` | `__getitem__(index: int) -> DockingPose` |
| `__iter__` | `__iter__() -> Iterator[DockingPose]` |
| `poses` | Property `list[DockingPose]` |
| `top_pose` | Property `DockingPose \| None` |
| `rank_by` | `rank_by(score_name: str, ascending: bool=True) -> DockingResult` |
| `to_dict` | `to_dict() -> dict[str, Any]` |
| `from_dict` | `from_dict(data: dict[str, Any]) -> DockingResult` |
| `reconstruct_problem` | `reconstruct_problem(receptor: Any=None, partner: Any=None) -> DockingProblem` |
| `get_rmsds` | `get_rmsds(reference: Any, selection: str='all') -> list[Any]` |

#### DockingProblem

Source: [dockingmt/core/problem.py](../dockingmt/core/problem.py).

| Member | Declaration |
| --- | --- |
| `__init__` | `__init__(receptor: Any, partner: Any, search_domain: SearchDomain, constraints: list[Any] \| dict[str, Any] \| None=None, search_guidance: list[Any] \| dict[str, Any] \| None=None, metadata: dict[str, Any] \| None=None, receptor_selection: Any='all', partner_selection: Any='all', receptor_structure_index: int \| None=None, partner_structure_index: int \| None=None)` |
| `for_redocking` | `for_redocking(complex_system: Any, receptor_selection: Any, partner_selection: Any, padding: Any, structure_index: int \| None=None, metadata: dict[str, Any] \| None=None) -> DockingProblem` |
| `receptor` | Property `Any` |
| `partner` | Property `Any` |
| `receptor_molsys` | Property `Any \| None` |
| `partner_molsys` | Property `Any \| None` |
| `receptor_atom_indices` | Property `list[int] \| None` |
| `partner_atom_indices` | Property `list[int] \| None` |
| `receptor_structure_index` | Property `int \| None` |
| `partner_structure_index` | Property `int \| None` |
| `receptor_chemical_state_index` | Property `int \| None` |
| `partner_chemical_state_index` | Property `int \| None` |
| `receptor_selection` | Property `Any` |
| `partner_selection` | Property `Any` |
| `search_domain` | Property `SearchDomain` |
| `constraints` | Property `list[Any] \| dict[str, Any]` |
| `search_guidance` | Property `list[Any] \| dict[str, Any]` |
| `metadata` | Property `dict[str, Any]` |
| `to_dict` | `to_dict() -> dict[str, Any]` |
| `from_dict` | `from_dict(data: dict[str, Any], receptor: Any \| None=None, partner: Any \| None=None) -> DockingProblem` |

#### DockingProtocol

Source: [dockingmt/core/protocol.py](../dockingmt/core/protocol.py). Bases: `ABC`.

| Member | Declaration |
| --- | --- |
| `name` | Property `str` |
| `required_capabilities` | Property `set[str]` |
| `parameters` | Property `dict[str, Any]` |
| `validate_problem` | `validate_problem(problem: DockingProblem) -> None` |
| `to_dict` | `to_dict() -> dict[str, Any]` |

#### VinaProtocol

Source: [dockingmt/core/protocol.py](../dockingmt/core/protocol.py). Bases: `DockingProtocol`.

| Member | Declaration |
| --- | --- |
| `__init__` | `__init__(exhaustiveness: int=8, n_poses: int=9, energy_range: Any=None, seed: int \| None=None, scoring: str='vina', cpu: int=0, allow_provisional_preparation: bool=False, capture_backend_inputs: bool=False, active_torsion_bonds: list[tuple[int, int]] \| None=None, collect_timings: bool=False)` |
| `name` | Property `str` |
| `exhaustiveness` | Property `int` |
| `n_poses` | Property `int` |
| `energy_range` | Property `Any` |
| `seed` | Property `int \| None` |
| `scoring` | Property `str` |
| `cpu` | Property `int` |
| `allow_provisional_preparation` | Property `bool` |
| `capture_backend_inputs` | Property `bool` |
| `active_torsion_bonds` | Property `list[tuple[int, int]]` |
| `collect_timings` | Property `bool` |
| `required_capabilities` | Property `set[str]` |
| `parameters` | Property `dict[str, Any]` |
| `validate_problem` | `validate_problem(problem: DockingProblem) -> None` |
| `to_dict` | `to_dict() -> dict[str, Any]` |
| `from_dict` | `from_dict(data: dict[str, Any]) -> VinaProtocol` |

#### DockingBackend

Source: [dockingmt/engines/base.py](../dockingmt/engines/base.py). Bases: `ABC`.

| Member | Declaration |
| --- | --- |
| `name` | Property `str` |
| `capabilities` | Property `set[str]` |
| `is_available` | Property `bool` |
| `validate_capabilities` | `validate_capabilities(protocol: DockingProtocol) -> None` |
| `dock` | `dock(problem: DockingProblem, protocol: DockingProtocol \| None=None) -> DockingResult` |
| `score` | `score(problem: DockingProblem, protocol: DockingProtocol \| None=None, pose: DockingPose \| None=None, score_name: str='score') -> DockingPose` |

#### VinaBackend

Source: [dockingmt/engines/vina.py](../dockingmt/engines/vina.py). Bases: `DockingBackend`.

| Member | Declaration |
| --- | --- |
| `__init__` | `__init__() -> None` |
| `name` | Property `str` |
| `capabilities` | Property `set[str]` |
| `is_available` | Property `bool` |
| `dock` | `dock(problem: DockingProblem, protocol: DockingProtocol \| None=None) -> DockingResult` |
| `score` | `score(problem: DockingProblem, protocol: DockingProtocol \| None=None, pose: DockingPose \| None=None, score_name: str='score') -> DockingPose` |

For a native molecular source, rendering an unchanged prepared view preserves
the source without copying unrelated caller resources, including when caller
length units differ from preparation units. Explicit coordinate, charge or type
edits require an independent provider copy; provider failures retain their
original exception. Rendering preserves the caller's unit policy.

`to_molecular_system()` returns an independent provider copy when a native
source is available. It preserves unchanged canonical geometry exactly and
applies actual coordinate edits through the public provider setter. Available
native chemistry and mechanics remain with that source. Source-free conversion
retains its partial-chemistry and declared-axis contracts.

#### PreparedReceptor

Source: [dockingmt/preparation/receptor.py](../dockingmt/preparation/receptor.py).

| Member | Declaration |
| --- | --- |
| `__init__` | `__init__(state_id: str, atom_names: list[str], group_names: list[str], group_ids: list[int], coordinates: Any, atom_types: list[str], charges: list[float], metadata: dict[str, Any] \| None=None, source_molsys: Any=None)` |
| `n_atoms` | Property `int` |
| `to_pdbqt` | `to_pdbqt() -> str` |
| `to_dict` | `to_dict() -> dict[str, Any]` |
| `to_molecular_system` | `to_molecular_system() -> Any` |

#### PreparedLigand

Source: [dockingmt/preparation/ligand.py](../dockingmt/preparation/ligand.py).

| Member | Declaration |
| --- | --- |
| `__init__` | `__init__(state_id: str, atom_names: list[str], group_name: str, coordinates: Any, atom_types: list[str], charges: list[float], torsion_dof: int=0, group_names: list[str] \| None=None, group_ids: list[int] \| None=None, metadata: dict[str, Any] \| None=None, source_molsys: Any=None, _torsion_tree: TorsionTree \| None=None)` |
| `n_atoms` | Property `int` |
| `pdbqt_atom_indices` | Property `list[int]` |
| `to_pdbqt` | `to_pdbqt() -> str` |
| `to_dict` | `to_dict() -> dict[str, Any]` |
| `to_molecular_system` | `to_molecular_system() -> Any` |

### exceptions

Source: [dockingmt/exceptions.py](../dockingmt/exceptions.py). Each name aliases its existing implementation class.

| Public alias | Existing bases |
| --- | --- |
| `DockingMTException` | `CatalogException` |
| `LibraryNotFoundError` | `DockingMTException` |
| `ArgumentError` | `DockingMTException` |
| `CapabilityMismatchError` | `DockingMTException` |
| `DockingMTViewerError` | `DockingMTException` |
| `ViewerPoseCountError` | `DockingMTViewerError`, `ValueError` |
| `ViewerStructureCountError` | `DockingMTViewerError`, `ValueError` |
| `ViewerInputMissingError` | `DockingMTViewerError`, `ValueError` |
| `ViewerPosePositionError` | `DockingMTViewerError`, `ValueError` |
| `ViewerShapeOwnershipError` | `DockingMTViewerError`, `ValueError` |
| `ViewerStateError` | `DockingMTViewerError`, `RuntimeError` |
| `ViewerCapabilityError` | `DockingMTViewerError`, `RuntimeError` |
| `ViewerActionError` | `DockingMTViewerError`, `ValueError` |

<!-- SOURCE_MAP:END -->
