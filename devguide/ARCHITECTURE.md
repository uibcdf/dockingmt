# Architecture

## Architectural objective

Create a backend-independent scientific core surrounded by adapters.

```text
                    DockingProblem
                         |
        +----------------+----------------+
        |                |                |
  Molecular states   Search domain   Constraints /
                                    Search guidance
        |                |                |
        +----------------+----------------+
                         |
                  DockingProtocol
                         |
       +---------+-------+-------+---------+
       |         |       |       |         |
 Preparation  Sampling Scoring Refinement Ranking
       |         |       |       |         |
       +---------+-------+-------+---------+
                         |
                    Backend(s)
                         |
                    DockingRun
                         |
                   DockingResult
                         |
                       Poses
```

Above individual runs:

```text
DockingCampaign
      |
      +-- Run/Result
      +-- Run/Result
      +-- Run/Result
      |
      +-- aggregate analysis
```

## Proposed package boundaries

The exact Python layout is not frozen:

```text
dockingmt/
├── core/          # scientific concepts and stable data model
├── protocols/     # canonical/composed workflows
├── preparation/   # scientific preparation contracts/implementations
├── regions/       # search-domain representations/conversions
├── guidance/      # future search-guidance abstractions
├── constraints/   # future constraint abstractions
├── scoring/       # scoring/rescoring abstractions
├── engines/       # docking-engine/backend adapters
├── analysis/      # pose comparison, clustering, interactions
├── campaigns/     # higher-level execution/aggregation when needed
├── integrations/  # optional MolSysSuite bridges
└── io/            # serialization/interchange
```

Do not create empty architecture for speculative completeness. Add modules when responsibilities become real.

## Protocol composition

A protocol must not require one monolithic engine. It may resolve stages to different providers:

```text
Preparation provider
      ↓
Sampling backend A
      ↓
Refinement backend B
      ↓
Scoring backend C
      ↓
Ranking policy
```

The MVP may use Vina for several stages, but the public model must not encode this as a permanent 1:1 relationship.

## Capability-driven backends

Backends should advertise supported capabilities, for example:

```text
small_molecule
macrocycle
peptide
rigid_receptor
flexible_sidechains
global_search
multiple_ligands
custom_scoring
rescoring
gpu
constraints
water_aware
metal_aware
covalent
```

Protocols should validate requested capabilities before execution.

## Adapters

```text
DockingMT scientific model
          ↓
backend-specific model/files/parameters
          ↓
execution
          ↓
backend output
          ↓
DockingMT result model
```

Lossy conversions must be explicit. Example:

```text
TopoMT-rich pocket
      ↓
BoxRegion approximation
      ↓
Vina search box
```

The original rich pocket information should remain attached to provenance/context rather than being discarded.

## Preparation boundary

Backend file generation is not equivalent to scientific preparation.

Keep separable:

```text
molecular preparation
        ↓
prepared molecular state
        ↓
backend conversion
        ↓
backend input
```

This permits future alternative preparation methods without redefining docking.

## Provenance

A `DockingRun` should eventually capture at least:

- DockingMT version;
- backend(s) and versions;
- protocol and resolved parameters;
- preparation methods and versions;
- molecular-state identities;
- random seed(s);
- receptor/partner identity;
- search-domain definition and conversions;
- constraints/guidance and approximations;
- unit conversions;
- execution metadata relevant to reproducibility.

## Identity preservation

Backend conversion must preserve a mapping between source atoms/entities and backend atoms/entities wherever possible. If an engine changes ordering, typing or representation, DockingMT should retain the mapping required to reconstruct scientifically meaningful results.

## Physical-quantity infrastructure

The core follows the current MolSysSuite PyUnitWizard contract. DockingMT does not own a
separate unit subsystem.

Adapters own conversion to/from backend-native numerical conventions.

Scores must carry semantic metadata sufficient to distinguish:

- physical quantities with units;
- empirical scores expressed conventionally in energy-like units;
- dimensionless model scores;
- ranks/probabilities/confidences.

## Shared MolSysSuite infrastructure

DockingMT should inherit the suite infrastructure contracts:

```text
physical quantities       -> PyUnitWizard
public argument boundary  -> ArgDigest
optional dependencies     -> DepDigest
structured diagnostics    -> SMonitor
molecular-system model    -> MolSysMT
visualization host        -> MolSysViewer
```

These are architectural responsibilities, not convenience libraries.

## Optional dependencies

The core should remain importable without every docking engine or optional chemistry
provider installed. Optional provider availability and lazy loading should use DepDigest
rather than ad hoc import guards.

Missing providers and capability failures should surface through actionable,
catalog-driven SMonitor diagnostics.

## Native high-performance code

No implementation language is prescribed. Rust, C++, CUDA or other approaches should be selected only when a concrete algorithmic or performance requirement exists.

A native engine must implement DockingMT contracts rather than redefine them.

## Scientific defaults

Defaults with scientific consequences belong to the resolved protocol/run, not hidden
implementation constants.

Examples include search padding, exhaustiveness, pose count, seed policy and preparation
choices. They must be inspectable and version-aware.


## Execution model

Backend and execution environment are orthogonal:

```text
DockingProtocol
      |
      v
Backend / Engine
      |
      v
Execution request
      |
      v
Executor
      |
      v
DockingRun
```

The backend answers **what scientific implementation performs the operation**.
The executor answers **where and how the resolved operation is executed**.

Possible future executors include local serial execution, local multiprocessing,
Slurm/HPC submission, GPU-node execution and distributed campaign execution.

The Core MVP does not need a generalized executor framework. A local execution path
may remain implicit until a second real execution environment creates a concrete need
for the abstraction.


## Serialization boundary

Serialization belongs to the scientific-object boundary, not to backend artifacts.
Backend files such as PDBQT may be retained for provenance/debugging, but they are not
the canonical persistent representation of a `DockingResult`.

Stable scientific objects should use versioned schemas so saved results can be read,
inspected and migrated independently of the backend process that produced them.
