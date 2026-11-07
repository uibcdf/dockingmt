# Development and onboarding

Read [contributor instructions](../AGENTS.md), the [common guide](../MOLSYSSUITE_GUIDE.md)
and [local instructions](AGENTS.md) first. The [machine handoff](MACHINE_HANDOFF.md)
holds the dated checkpoint/custody; the [complete plan](PRE_STABILIZATION_PLAN.md)
holds product acceptance. These are setup procedures, not a newly qualified
dependency solve or platform.

## What we are building

DockingMT makes this scientific workflow inspectable and reproducible:

```text
explicit receptor/ligand sources and states
    -> provider-owned preparation with maps and reports
    -> declared search domain and protocol
    -> selected engine execution
    -> poses, named scores and actual input provenance
    -> explicit evaluation, comparison and interpretation
    -> saved records and docking-specific exploration
```

The starting profile is rigid-protein/small-ligand docking with Vina. It does not
infer experimental pH, missing chemistry, appropriate waters/cofactors or active
ligand torsions. Read the [preparation profile](validation/preparation_profile.md)
before changing preparation. Automatic preparation defaults to no active ligand
torsions; supplied prepared inputs keep their trees. An `unassessed` preparation
is not chemical validation. Scores are method-dependent model outputs, not
measured binding free energies.

| Concept | Meaning |
| --- | --- |
| `DockingProblem` | Inputs, selections, state/frame and search intent. |
| `SearchDomain` / `BoxRegion` | Physical region/derivation, separate from Vina's box approximation. |
| `VinaProtocol` | Resolved engine settings and preparation policy. |
| `PreparedLigand` / `PreparedReceptor` | Provider-backed preparation, correspondence and submitted representation. |
| `DockingPose` / `DockingResult` | Coordinates, named score definitions, identities and provenance; restored results may deliberately lack a molecular problem. |
| `DockingOutcome` | One serial input's result or recorded failure; its index is a position, not a ligand/run identity. |
| `PoseInteractions` / `bind_interactions` | Detached existing analyses associated with one explicitly selected pose and admitted carrier; see [contract and qualification](validation/pose_interaction_binding.md). |

Position, scientific rank, pose identity, molecular-state identity and scene frame
are different. Equal IDs/hashes do not prove chemical equivalence. Preserve
unknown information. See [score semantics](validation/score_semantics.md),
[reference evidence](validation/scoring_reference.md) and [result audit](validation/result_audit.md).

## Find the implementation

The [real source map](ARCHITECTURE.md) distinguishes implemented modules from
conceptual future packages. Public orchestration is in `dock.py`, `score.py`,
`batch.py`, `evaluation.py` and `aggregation.py`; `core/` owns scientific
records; `engines/` owns backend details; `preparation/` composes MolSysMT tools.
`molsysviewer_dockingmt/` owns the addon.

[Runtime tests](../tests/) differ from [administrative tests](../devtools/tests/).
[dmt_test_support](../dmt_test_support/) is unshipped scientific support, and
[devtools](../devtools/) contains source entry points/operators.
[Validation guides](validation/) and [data](validation/data/) preserve scientific
prescriptions and observations. Notebooks can execute expensive science.

## Set up a development machine

The reference routine workspace is **Linux x86_64 / Python 3.14**. Required source
support spans **3.11–3.14**; actual platform/public admission remains
[#30](https://github.com/uibcdf/dockingmt/issues/30). Another OS requires its own
qualification; a Linux environment/wheel does not prove macOS compatibility.

Clone into a workspace of your choice:

```bash
git clone https://github.com/uibcdf/dockingmt.git
git clone https://github.com/uibcdf/molsyssuite.git
```

Inspect branch/commit/status before updating existing clones; preserve human work.
Use the central [workspace instructions](https://github.com/uibcdf/molsyssuite/blob/main/devguide/development_workspace.md)
and actual versioned recipe. Before solves/builds/scientific cells, admit resources:
one allowed logical CPU, low priority, one native/build worker, a task-local RAM
reserve and monitoring. Apply limits to descendants; stop only owned work.
Do not automatically restart after a headroom interruption.

```bash
cd molsyssuite
conda env create --file devtools/conda-envs/molsyssuite-dev-py314.yaml
conda activate 'molsyssuite@uibcdf_3.14'
python -c 'import sys; assert sys.version_info[:2] == (3, 14); print(sys.executable)'
```

Activate before native builds. Follow the central `development_environment.py
toolchain` check; it compiles C/Rust smoke programs and needs the same resource
admission. The central batch installer expects the **complete eligible cohort**,
not just these two clones. Inspect its `profile`/`sources` operations first.

For a smaller DockingMT workspace, the central environment alone is not a full
scientific installation: MolSysMT and the compatible ArgDigest source generation
are also needed. The handoff records the controlled sources below. Return to
the parent workspace directory first (`cd ..` from the `molsyssuite` clone above).
Create new, owned directories; inspect existing clones instead of resetting them:

```bash
git clone --no-checkout https://github.com/uibcdf/argdigest.git argdigest &&
  git -C argdigest checkout --detach 3d1ec53c374098016452abab74706e9d80df5462
git clone --no-checkout https://github.com/uibcdf/molsysmt.git molsysmt &&
  git -C molsysmt checkout --detach 00abb958fb93649131d5ce5fe5e12e90cf4900e9
```

After the toolchain, dependency and resource checks, connect these sources to
the active interpreter from that same parent workspace directory:

```bash
python -m pip install --no-deps --no-build-isolation --editable argdigest --editable molsysmt
```

The addon additionally needs MolSysViewer: acquire its reviewed
`78ede79e2e345593db5bfe80d246d3f6c70bd005` source in an owned clone and apply the
same installation policy. Select Vina and other optional dependencies from the
accepted workflow/test recipe. Third-party resolution on the destination still
needs qualification; these source pins are not an environment lock.

Then, from the DockingMT checkout, connect the routine interpreter:

```bash
python -m pip install --no-deps --editable .
python -m pip check
```

Use `--no-build-isolation` for native components needing declared in-environment
tools. Conda supplies dependencies; editable installation connects the clone.
Our public route is Conda `uibcdf`, not PyPI. Pytest Receptor has its separately
documented additional PyPI route. Review optional test/build tools and exact
published receptor versions in [developer controls](../devtools/README.md),
[the test environment](../devtools/conda-envs/test_env.yaml) and [CI](../.github/workflows/ci.yml);
the shared workspace and member recipes are not interchangeable locks.

After admitting resources for provider imports, verify isolated origins:

```bash
python -I -c 'import sys, dockingmt; print(sys.executable); print(dockingmt.__file__)'
```

Record actual commits/origins and `pip check` outcomes. Do not hide unrelated
closure failures. Imports/editables do not qualify public artifacts or science.

## Development versus exact receiving

| Context | Install policy | Evidence |
| --- | --- | --- |
| Routine development | Local clones editable in the admitted 3.14 workspace. | Behavior at those actual revisions. |
| Controlled source CI/private receiving | Normal directory installs from immutable provider commits; exact context/SDK checks. | That particular composition and executed scope. |
| Staged/public Conda | Exact artifact hashes and public closure; no source fallback. | Its executed artifact/platform/minor/profile gates. |

[dependency_routes.toml](../devtools/dependency_routes.toml) owns controlled sources,
not permission to overwrite colleagues' clones or invent public minima.
The route checker intentionally rejects editables in normal-source receiving.
Use `--declared-only` for declaration review. The [SDK setup](../devtools/README.md#dependency-routes-and-immutable-scientific-clones)
explains acquiring the ignored clean immutable SDK in a fresh clone.

## Choose checks by the change

For documentation/reports, after provisioning administrative tools and the SDK:

```bash
python devtools/devguide_index.py --check
python devtools/check_dependency_routes.py --declared-only
python -m pytest --receptor=llm -o addopts= devtools/tests/test_distribution_contract.py tests/test_reporting_protocol.py
ruff check .
ruff format --check .
```

These administrative checks avoid scientific-provider imports. Use a **published**
Pytest Receptor; a development suffix is not that release. Follow [its guide](../PYTEST_RECEPTOR_GUIDE.md)
for isolated tooling if the common workspace uses development source.

Runtime changes need relevant contract assertions. Scientific changes need
registered inputs/populations/hypotheses, resources/call budgets, controls and
failure policy. Do not run the full scientific suite as an onboarding smoke test.
Helpers/fixtures have an exact [resource declaration](../devtools/conda-build/resources.toml);
update changed inputs' hashes while preserving frozen historical snapshots.

Inspect Actions first with a published GH Run Receptor, then authoritative
job/step facts. A live handle is pending, not passing/stopped. Do not start a
replacement because an observation window expired. See [its guide](../GH_RUN_RECEPTOR_GUIDE.md)
and [the recovery workflow](../.github/workflows/full-matrix.yml).

## Making a change

1. Choose an accepted workflow/owning issue. Inspect existing evidence before
   reopening delivered work.
2. Use public MolSysMT tools for molecular work; request uncovered reusable needs
   there. Specialized/shared components keep their domains. No downstream
   substitutes or unreviewed pin changes.
3. Use ArgDigest for nontrivial public constraints, DepDigest for selected optional
   providers, SMonitor for structured diagnostics and PyUnitWizard for quantities;
   read their applicable guides.
4. Complete the accepted workflow with relevant checks. Keep science outside
   transient UI state.
5. Update reports/decisions/guidance, regenerate `devtools/devguide_index.py`,
   and archive resolved work under the [reporting protocol](reporting_protocol.md).
6. Verify final declaration/publication/resources, including a fresh committed
   export where required. Inspect exact-head CI; record missing evidence and
   recovery ownership. Releases keep separate gates.

Preserve producers, failures and attempted/completed/evaluated denominators.
Software tests, poses, seeds, complexes and visible canvas observations differ.
See the [publication policy](validation/evidence_publication_policy.md) and
[non-Git custody checklist](MACHINE_HANDOFF.md#evidence-that-does-not-arrive-with-git).
Moving machines does not automatically lift the previous local E4 hold or resume
the cleared implementation goal. The [implementation strategy](IMPLEMENTATION_STRATEGY.md)
and [release ladder](RELEASE_MILESTONES.md) retain accepted product direction.
