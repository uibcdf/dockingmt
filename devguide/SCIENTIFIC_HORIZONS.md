# Scientific Horizons

This is a design stress-test and research-idea registry, not a committed roadmap.

For each horizon, the present architecture should avoid obvious blockers without implementing speculative machinery prematurely.

## Unifying horizon: molecular-landscape-aware docking

> **From box-based docking to molecular-landscape-aware docking.**

Potential information layers:

```text
TopoMT          -> spatial/topographic landscape
PharmacophoreMT -> chemical interaction landscape
ElastNetMT      -> flexibility landscape
MolSysMT        -> conformational landscape
                       |
                       v
                  DockingMT
                       |
                       v
               guided exploration
                       |
                       v
                  pose landscape
```

## 1. Topography-aware docking

Replace the assumption of a rectangular search box with sampling informed by actual pocket geometry.

Potential TopoMT information:

- pocket volume;
- mouth;
- neck;
- groove;
- channel;
- subpockets;
- boundary;
- surface geometry/normals.

A future native engine could operate directly on these descriptors.

## 2. Pocket-decomposition docking

Treat a binding site as a structured landscape:

```text
Pocket
├── subpocket A
├── subpocket B
├── groove
├── mouth
└── buried core
```

Sampling could adapt to ligand fragments and subregions.

## 3. Pharmacophore-guided sampling

Move beyond post hoc filtering:

```text
pharmacophore information
          ↓
constraint / guidance
          ↓
biased or constrained sampling
```

Potentially combine chemical features with topographic subregions.

## 4. Flexibility-aware docking

Possible progression:

```text
rigid receptor
→ selected flexible side chains
→ receptor ensembles
→ structured/continuous flexibility field
→ adaptive receptor response
```

ElastNetMT may become a source of flexibility guidance.

## 5. Ensemble docking

```text
trajectory / conformational collection
   ↓
clustering/selection
   ↓
representative receptor states
   ↓
docking
   ↓
aggregate pose landscape
```

## 6. Dynamic-pocket docking

```text
trajectory
   ↓
time-dependent TopoMT analysis
   ↓
dynamic pocket states
   ↓
docking across pocket landscape
```

The scientific object may become a pocket conformational landscape rather than a single structure.

## 7. Multi-stage docking

```text
coarse pose generation
      ↓
local refinement
      ↓
ML rescoring
      ↓
physical relaxation
      ↓
final ranking
```

Different backends may implement different stages.

## 8. Consensus docking

Normalize multiple engines into common pose representations, then analyze:

- pose agreement;
- cluster agreement;
- score agreement;
- receptor-state dependence;
- method disagreement.

## 9. Physics-based refinement

Docking should feed physical workflows:

```text
pose
 ↓
minimization
 ↓
local relaxation
 ↓
interaction/solvation estimates
 ↓
short MD or other refinement
 ↓
re-ranking
```

DockingMT need not implement every physical method itself.

## 10. Uncertainty-aware docking

Move away from “pose #1 is the answer.”

Represent where defensible:

- pose clusters;
- score disagreement;
- engine agreement;
- receptor-state dependence;
- sampling recurrence;
- molecular-state dependence;
- uncertainty/confidence metadata.

## 11. Macrocycle docking

Macrocycles stress internal conformational sampling and should be supported by specialized protocols/backends without redefining the core result model.

## 12. Peptide docking

Peptides are a major architectural stress test because ligand flexibility, receptor flexibility and scoring differ substantially from ordinary small-molecule docking.

The core should allow peptide-specialized protocols/backends without pretending that Vina-style docking is a universal solution.

## 13. Water-aware docking

Structural waters may be:

- retained;
- displaced;
- mobile;
- mediators of ligand–receptor interactions.

Future protocols may need to represent water state and water-mediated interactions explicitly rather than reducing preparation to “remove waters.”

## 14. Metal-aware docking

Metals introduce issues such as:

- coordination geometry;
- metal-specific chemistry;
- charge/parameterization;
- explicit coordination constraints;
- scoring limitations.

Metal handling should be scientifically explicit.

## 15. Covalent docking

Covalent docking is both a future capability and an architectural stress test.

Potential concepts:

```text
reactive residue
ligand warhead
reaction definition
reaction geometry/constraint
covalent pose/product state
```

This tests the assumption that receptor and ligand remain permanently separate entities.

## 16. Fragment docking, growth and linking

TopoMT pocket decomposition may naturally support:

```text
subpockets
    ↓
fragment placement
    ↓
multiple fragment poses
    ↓
growth / linking hypotheses
```

DockingMT need not become a molecule-generation package, but it can provide the structural/scoring layer consumed by design workflows.

## 17. Blind/global docking

Not every docking problem begins with a known local region.

Blind docking stresses the model of `SearchDomain` and may interact naturally with TopoMT-based pocket discovery or adaptive search.

## 18. Molecular-state ensembles

Docking may need to consider multiple:

- protonation states;
- tautomers;
- stereochemical states;
- receptor protonation states.

Results should eventually permit state-aware aggregation rather than losing this information during preparation.

## 19. Native DockingMT engine

A native engine is plausible if MolSysSuite integration suggests genuinely new algorithms.

A distinctive direction is:

> docking driven jointly by molecular topography, conformational flexibility and physical/chemical constraints.

Implementation language and acceleration strategy should follow the scientific algorithm rather than precede it.

## 20. Hybrid physics/ML docking

ML may contribute to:

- pose proposals;
- scoring;
- uncertainty estimation;
- adaptive sampling.

Physics/structural models may contribute to:

- constraints;
- relaxation;
- energetic discrimination;
- interpretability.

DockingMT should allow composition rather than forcing an “AI versus physics” architecture.

## 21. Adaptive search

A future protocol may alter sampling based on information acquired during the run:

```text
initial exploration
      ↓
identify promising regions/poses
      ↓
adapt search guidance
      ↓
focused exploration
```

This is another reason not to model a protocol as a static Vina invocation.
