# Scientific Model

This document defines scientific concepts before implementation classes. Not every concept must immediately become a Python class.

## Binding-domain model and operation-specific contracts

[Scientific scope](SCIENTIFIC_SCOPE.md) defines the accepted domain. The numbered
model below describes its docking subdomain, not a universal schema. Existing
class names remain appropriate for docking.

- **Docking** receives prepared partner states and search information; it returns
  bound-configuration hypotheses with explicit molecular maps and scores.
- **Complex prediction** receives fixed identities, supported sequence/chemical
  representations and structural/prior information. Results preserve the complete
  complex, every partner/frame change and original chain/pair/token confidence.
- **Refinement** receives one complex/state and a resolved method. The transformed
  complex, mapping, approximations and evaluations are distinct from its parent.
- **Binding free-energy calculation** receives an absolute/relative binding
  question, molecular states, thermodynamic/standard-state conventions, conditions
  and physical/statistical protocol. Estimates retain physical units, method and
  available uncertainty/convergence evidence.
- **Binding free-energy prediction** receives a defined endpoint and model
  applicability profile. Predicted quantities/evidence remain distinct from
  calculated values and measured affinity; unrelated assay/model output is never
  converted implicitly.
- **Interface characterization** associates a declared complex/selection/frame
  with owner-supplied geometry, topology, physicochemical and energetic
  descriptors. Preserve definitions, units/scales, meaningful direction and
  atom/residue coverage.

Shared invariants are source/chemical identity, state/frame, exact correspondence,
provider/model/code identity, resolved choices, actual artifacts, quantities and
honest failure/unknown states. Native, completed and refined artifacts remain
separate lineage nodes. Confidence/scores do not automatically transfer to changed
atoms or coordinates. These obligations authorize no empty classes or methods.

## 1. Molecular identity and molecular state

### Molecular entity
The chemical/molecular entity being considered.

### MolecularState
A scientifically relevant prepared chemical state of an entity.

For a ligand this may distinguish:

- protonation state;
- tautomer;
- stereochemical state;
- formal charge state;
- other chemically distinct preparation choices.

For a receptor it may distinguish:

- protonation assignments;
- alternate structural choices;
- missing-atom/residue reconstruction;
- selected waters/cofactors;
- receptor conformation/state.

A docking calculation may therefore operate on a **molecular state**, not merely an abstract molecule.

### Conformation
Internal coordinates/degrees of freedom of a molecular state.

### Spatial placement
Translation and orientation relative to the receptor/search frame.

### ReceptorState
A particular receptor molecular/conformational state used in a run.

This becomes essential for ensemble and dynamic-pocket docking.

## 2. DockingProblem

The scientific question to be solved.

```text
DockingProblem
├── receptor / receptor state(s)
├── docking partner(s) / molecular state(s)
├── search domain(s)
├── constraints
├── search guidance
├── environment/context
└── requested protocol
```

A problem should describe scientific intent independently of backend file formats.

## 3. SearchDomain

Describes **where** docking may be explored.

Potential representations:

```text
SearchDomain
├── BoxRegion                 [NOW]
├── SelectionRegion           [NOW]
├── SphereRegion              [DESIGNED FOR]
├── PocketRegion              [DESIGNED FOR]
├── GlobalDomain              [DESIGNED FOR]
├── SurfaceRegion             [HORIZON]
└── TopographicRegion         [HORIZON]
```

`SearchDomain` may remain a useful public term, but the broader conceptual role is a search domain.

Backend adapters may approximate a rich domain using a simpler representation. Such conversion must be explicit, inspectable and recorded.

## 4. SearchGuidance

Describes information that may **guide, bias, prioritize or adapt** sampling without necessarily defining the allowed spatial domain.

Potential sources:

- TopoMT pocket topology/subpockets/mouths/channels;
- PharmacophoreMT interaction patterns;
- ElastNetMT flexibility information;
- prior poses;
- learned models;
- physical/chemical fields.

Search guidance is distinct from both the domain and hard constraints.

## 5. DockingConstraint

Information that restricts admissible solutions or imposes explicit requirements.

Possible future examples:

- pharmacophoric requirements;
- distance constraints;
- required/forbidden residue contacts;
- geometric constraints;
- covalent reaction geometry;
- coordination constraints.

Whether a backend can enforce a constraint directly or only approximate/filter it must be explicit.

## 6. MolecularPreparation / PreparationProtocol

Preparation is a scientific stage.

### Receptor preparation may involve

- structure cleanup;
- alternate locations;
- missing atoms/residues;
- protonation;
- hydrogens;
- charges;
- atom typing;
- selected waters;
- cofactors;
- metals;
- unusual residues.

### Docking-partner preparation may involve

- protonation states;
- tautomers;
- stereoisomers;
- formal charges;
- conformers;
- rotatable-bond definitions;
- atom typing.

A single input entity may generate multiple prepared molecular states. Those states must retain identity and provenance.

## 7. DockingProtocol

Describes how a problem should be solved.

It is a composition, not a monolithic algorithm:

```text
DockingProtocol
├── PreparationProtocol
├── SamplingProtocol
├── ScoringProtocol
├── RefinementProtocol
├── RankingProtocol
└── AnalysisProtocol
```

Any stage may be absent or delegated to different backends.

This must permit workflows such as:

```text
Vina sampling
    ↓
physical refinement
    ↓
GNINA rescoring
    ↓
consensus ranking
```

## 8. DockingEngine / Backend

A computational provider able to perform one or more stages.

For the MVP, `DockingEngine` is a natural abstraction for Vina-like engines. The broader architecture must not assume that one protocol maps to exactly one engine.

A future generic `Backend` concept may cover docking engines, refinement engines, ML scorers and other providers.

## 9. DockingRun

A concrete execution of one resolved stage/protocol unit with:

- resolved molecular states;
- resolved domain/constraints/guidance;
- backend(s);
- versions;
- parameters;
- seeds;
- transformations;
- execution metadata.

A run is not a campaign.

## 10. DockingPose

A candidate bound configuration.

A pose should be traceable to:

```text
partner molecular state
+
internal conformation
+
spatial placement
+
receptor state
+
run/protocol provenance
```

A pose may carry:

- coordinates/conformation;
- partner identity;
- receptor-state identity;
- multiple named scores;
- rank(s);
- cluster membership;
- interactions/annotations;
- uncertainty/confidence metadata where meaningful;
- provenance.

## 11. DockingScore

A named score produced by a known method/stage.

Prefer a plural model:

```text
pose.scores["vina"]
pose.scores["vinardo"]
pose.scores["gnina"]
pose.scores["interaction_energy"]
pose.scores["pharmacophore"]
```

A ranking must identify which score or policy produced it.

## 12. DockingResult

Structured scientific output of a run or well-defined protocol execution.

```text
DockingResult
├── problem/protocol references
├── run provenance
├── poses
├── scores
├── rankings
├── clusters
├── annotations
└── analysis metadata
```

It must not be defined by an engine output file.

## 13. DockingCampaign

A higher-level collection of related docking work.

Examples:

```text
1 receptor × many ligands
many receptor states × one ligand
many receptor states × many ligands
multiple engines × same problem set
```

Conceptually:

```text
DockingCampaign
├── DockingRun / DockingResult
├── DockingRun / DockingResult
├── ...
└── aggregate analysis
```

The exact implementation can wait, but virtual screening and ensemble/consensus docking should not force `DockingResult` to become an overloaded universal container.

## 14. Identity graph

Identity must survive:

```text
source molecular entity
        ↓
prepared molecular state
        ↓
backend representation
        ↓
backend execution
        ↓
normalized pose/result
```

Useful identifiers may eventually include:

```text
ligand_id
molecular_state_id
receptor_state_id
run_id
pose_id
campaign_id
```

Exact ID schemes should be designed with MolSysSuite conventions rather than invented casually.

## 15. Physical quantities and score semantics

BindingMT inherits the MolSysSuite physical-quantity contract through PyUnitWizard rather
than defining an independent unit system.

At minimum this applies to:

- coordinates/distances;
- physical energies;
- angles;
- search-domain dimensions;
- RMSD and geometric cutoffs.

Backend-native units are adapter concerns and must be converted through the suite unit
layer before crossing the public scientific boundary.

Dimensionless or empirical docking scores must never be mislabeled as physical energies.
A score carries semantic metadata in addition to its numerical value.


## Serialization and versioned scientific representations

Core scientific objects should eventually admit stable, versioned, machine-readable
representations sufficient to preserve their scientific meaning outside a live Python
session or backend process.

Priority objects include:

- `DockingProblem`;
- `DockingProtocol`;
- `DockingRun`;
- `DockingResult`;
- `DockingPose`;
- `DockingCampaign`.

Serialization is not required to freeze a particular storage technology now.
JSON, HDF5 or other representations remain implementation choices.

The invariant is stronger:

> A scientific result must not depend on a live Vina/RDKit/Meeko object in order to
> remain interpretable.

Serialized representations should carry explicit schema/version metadata and preserve
identities, resolved protocol choices, provenance, physical quantities, score
semantics, backend information and approximation/degradation records as applicable.
