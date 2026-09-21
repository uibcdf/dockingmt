# Engine Strategy

## Initial reference engine: AutoDock Vina

AutoDock Vina is the preferred first backend because it is established, familiar and appropriate for canonical protein–small-molecule docking workflows.

The first implementation should use the cleanest stable programmatic integration available and avoid coupling DockingMT's public scientific API to Vina-specific command-line concepts.

## What Vina is for

Vina should let us validate:

- the scientific data model;
- preparation boundaries;
- search-domain handling;
- backend adapters;
- docking execution;
- sampling/scoring separation;
- result normalization;
- provenance;
- visualization;
- redocking validation.

## What Vina is not

Vina is not:

- the definition of a search domain;
- the definition of a ligand/docking partner;
- the universal scoring model;
- the permanent limit on receptor flexibility;
- the architecture of DockingMT.

## One protocol, multiple backends

Future protocols may compose:

```text
Vina sampling
    ↓
OpenMM-like physical refinement
    ↓
GNINA-like rescoring
    ↓
DockingMT ranking/analysis
```

Therefore the architecture must not require exactly one engine per protocol.

## Future engines — DESIGNED FOR

Candidates worth keeping architecturally possible include:

- GNINA or related CNN-scoring engines;
- ML pose-generation engines such as diffusion-based approaches;
- specialized macrocycle/peptide docking backends;
- other classical docking engines where licensing/distribution permits;
- a future native DockingMT engine.

No future backend is committed by this document.

## Rust question

Do not rewrite Vina in Rust for the MVP.

A Rust component may make sense later if DockingMT develops a native algorithm or a clearly identified performance-critical kernel. Implementation language should follow scientific and performance requirements.

## Capability contract

A backend must declare what it can actually do. Unsupported requests should:

1. fail clearly; or
2. use an explicit documented approximation accepted by the protocol/user.

DockingMT should never silently imply scientific equivalence across engines.


## Licensing and distribution

Supporting a backend does not imply redistributing it.

For every backend/provider integration, distinguish:

- supported by DockingMT;
- detected/used when separately installed;
- installed as an optional dependency;
- bundled or redistributed by DockingMT.

Licensing, packaging and redistribution constraints must be reviewed per provider.
Architecture must not assume that every supported engine can legally or practically
be bundled with DockingMT.
