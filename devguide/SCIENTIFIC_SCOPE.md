# Scientific Scope

## NOW — Core scientific MVP

DockingMT initially targets canonical **protein–small-molecule local docking** with AutoDock Vina as the reference engine.

The Core MVP should support:

- reproducible receptor preparation through a documented path;
- reproducible ligand preparation through a documented path;
- explicit local docking regions;
- regions derived from molecular selections;
- redocking of a known ligand;
- docking of one small molecule;
- normalized pose/result representation;
- pose ranking from named backend scores;
- MolSysViewer basic visualization;
- complete provenance and molecular identity tracking.

Redocking is the primary end-to-end scientific gate.

## NOW — Extended MVP

After the Core MVP is scientifically reliable:

- scoring/rescoring as an explicit operation;
- small virtual-screening collections;
- pose comparison and basic clustering;
- basic interaction analysis;
- richer result exploration.

The MVP is not intended to be a production-scale million-compound screening platform.

## DESIGNED FOR

The scientific model should not block:

- fragments;
- macrocycles;
- peptides;
- multiple docking partners;
- receptor side-chain flexibility;
- receptor ensembles;
- trajectory-derived receptor states;
- blind/global docking;
- optional or multiple search domains;
- structural waters and cofactors;
- metals and coordination-aware protocols;
- pharmacophoric/geometric constraints;
- search guidance distinct from hard constraints;
- multiple scoring functions;
- multiple engines/backends;
- consensus docking;
- multi-stage docking/refinement;
- GPU/ML engines;
- campaign-level execution and analysis.

Support is not promised merely because a concept is represented.

## HORIZON

Longer-term research directions include:

- topography-aware sampling;
- non-box search domains;
- pocket/subpocket decomposition;
- pharmacophore-guided sampling;
- flexibility-aware docking;
- ensemble and dynamic-pocket docking;
- water-aware docking;
- metal-aware docking;
- covalent docking;
- fragment placement, growth and linking workflows;
- physically refined pose landscapes;
- uncertainty-aware docking;
- native DockingMT search/scoring methods;
- adaptive and hybrid physics/ML protocols.

## Explicit non-goals for the first MVP

- implementing a new docking engine from scratch;
- rewriting AutoDock Vina in Rust;
- peptide docking as a validated general workflow;
- protein–protein docking;
- covalent docking;
- production-scale HPC screening infrastructure;
- solving every receptor/ligand preparation problem;
- committing to one universal preparation implementation;
- rebuilding general MolSysMT molecular capabilities inside DockingMT;
- creating DockingMT-specific substitutes for MolSysSuite shared infrastructure;
- hiding engine limitations behind a misleading common denominator.
