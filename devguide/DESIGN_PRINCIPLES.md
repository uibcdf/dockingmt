# Design Principles

These principles protect DockingMT from premature architectural constraints.

## Constitutional principles

### 1. DockingMT is not a Vina wrapper
AutoDock Vina is the initial reference engine, not the conceptual model.

### 2. Engine is not protocol
A `DockingProtocol` describes scientific intent and composition. A `DockingEngine` or backend provides computational capabilities.

### 3. A protocol may use more than one backend
Future workflows may combine pose generation, physical refinement and ML rescoring using different computational providers.

### 4. Sampling is not scoring
Pose generation, scoring, rescoring, refinement and ranking must remain separable concepts.

### 5. Preparation is science, not file conversion
Protonation, tautomerism, stereochemistry, charges, atom typing, receptor cleanup, waters, metals and related choices can change the scientific problem. Preparation decisions belong to the protocol and provenance.

### 6. SearchDomain is not a box
A rectangular box is one representation accepted by some engines. Future search domains may be selection-derived, pocket-derived, surface/topography-derived, global or otherwise constrained.

### 7. Search domain is not search guidance
“Where may the search occur?” and “what information should guide or bias the search?” are different questions.

### 8. Ligand does not mean small molecule
The MVP targets small molecules, but the scientific role of a docking partner must not be hard-coded to that chemical class.

### 9. Pose is not molecular state
A pose may depend on molecular state, internal conformation, spatial placement and receptor state. These concepts must not be collapsed unnecessarily.

### 10. DockingResult is not an output file
Results are scientific objects containing poses, scores, ranks, metadata and provenance. Files are serialization or backend-interchange formats.

### 11. A score is not a single scalar truth
A pose may carry multiple scores from different functions or stages. Ranking policy must be explicit.

### 12. Run is not campaign
A single computational execution and a collection of related runs across ligands, receptor states, engines or protocols require different conceptual levels.

### 13. MolSysSuite integration should use scientific contracts
TopoMT, PharmacophoreMT and ElastNetMT are evolving. DockingMT should integrate through stable concepts/adapters rather than unnecessary hard dependencies on internal implementations.

### 14. MVP scope is not architectural scope
Implement only what is needed now, while avoiding representations that prohibit anticipated extensions.

### 15. Provenance is part of the scientific result
Engine, version, parameters, random seed, preparation choices, molecular-state identity, inputs and transformations must be recoverable.

### 16. Molecular identity must survive transformations
A ligand, molecular state, receptor state, run and pose must remain traceable across preparation, backend conversion, execution and result normalization.

### 17. Units must be explicit and normalized
Backend conventions must not silently leak into the scientific model. Length, energy and angular units require a documented policy.

### 18. Reproducibility and inspectability beat hidden convenience
High-level convenience functions are welcome, but they must resolve to inspectable protocols and runs.

### 19. Backend-specific concepts stay at the boundary
PDBQT details, Vina grids and backend-specific flags belong in adapters/configuration, not in the universal scientific model.

### 20. Rich scientific information should not be destroyed prematurely
A TopoMT pocket may contain geometry, topology and relationships. Converting it to a Vina box may be necessary for one backend, but the richer information should remain available to the protocol and provenance.

### 21. Capability support must be honest
DockingMT must not hide backend limitations behind a misleading common denominator. Unsupported science should fail clearly or require an explicit approximation.

### 22. Architecture should be stressed by difficult future cases
Peptides, covalent docking, blind docking, dynamic pockets, structural waters and metals are useful design stress tests even when they are not MVP features.

### 23. MolSysSuite owns the scientific language and workflow
DockingMT is a native MolSysSuite component. It should compose suite capabilities instead
of rebuilding a parallel molecular-science stack.

### 24. Third-party tools are providers, not abstractions
RDKit, PDBFixer, Meeko, Vina and future tools may implement capabilities behind MolSysSuite
contracts. Their object models must not define DockingMT's scientific API.

### 25. Shared infrastructure is inherited, not reinvented
Use PyUnitWizard for physical quantities, ArgDigest for public argument contracts,
DepDigest for optional dependencies, and SMonitor for structured diagnostics according to
current suite policy.

### 26. Scientific defaults are protocol decisions
Defaults that can change scientific outcomes must be explicit, inspectable and
version-aware.

### 27. Do not silently fork sibling functionality
If a general molecular or infrastructure capability belongs to another MolSysSuite
component, report the requirement to that provider and track any local workaround as
temporary.

### 28. Horizons protect architecture; they do not authorize code
A `DESIGNED FOR` or `HORIZON` concept must not generate speculative modules, abstractions
or dependencies until a real accepted workflow requires them.


### 29. Engine/backend is not executor
The scientific backend defines what docking/scoring code performs the computation.
The executor defines where and how that computation is run. Local, multiprocessing,
Slurm, GPU-node or future distributed execution must not become separate scientific
engines merely because their execution environment differs.
