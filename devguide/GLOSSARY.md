# Glossary

This glossary exists to prevent scientifically important terms from becoming accidental synonyms.

## Backend
A computational provider used by one or more protocol stages. A docking engine is a type of backend.

## Campaign
A coordinated collection of related docking runs/results, for example many ligands, receptor states or engines.

## Conformation
Internal molecular geometry/degrees of freedom for a given molecular state. It is not the same as spatial placement.

## Constraint
A requirement or restriction imposed on admissible poses or sampling.

## Docking engine
A backend specialized in docking/search/scoring operations. AutoDock Vina is the initial reference engine.

## Docking partner
The molecular entity playing the ligand/partner role in a docking problem. The term is intentionally broader than “small molecule.”

## Docking problem
The scientific question: receptor, partner(s), molecular states, search domain, constraints/guidance and requested protocol.

## Docking protocol
The composed scientific procedure used to solve a docking problem. It may include preparation, sampling, scoring, refinement, ranking and analysis, potentially using multiple backends.

## Docking result
Structured scientific output associated with a run or well-defined protocol execution. It is not synonymous with an output file.

## Docking run
A concrete resolved computational execution with specific states, parameters, backend(s), versions, seeds and provenance.

## Molecular entity
The underlying chemical/molecular object before choosing a particular prepared chemical state.

## Molecular state
A scientifically distinct state used in computation, potentially differing in protonation, tautomerism, stereochemistry, charge, selected waters/cofactors or other preparation choices.

## Pose
A candidate bound configuration tied to a partner molecular state, internal conformation, spatial placement, receptor state and provenance.

## Preparation
Scientific transformation/selection of molecular states for computation. It is distinct from conversion to a backend file format.

## Rank
An ordering produced by an explicit ranking policy. Rank is not a score.

## Receptor state
A specific receptor molecular/conformational state used in a run.

## Score
A named value produced by a specified scoring method/stage. Scores may have different semantics and units and are not automatically comparable.

## Search domain
Where sampling is allowed or intended to occur. A rectangular box is one possible representation.

## Search guidance
Information that biases, prioritizes or adapts search without necessarily defining a hard admissible domain.

## Spatial placement
Translation/orientation of a docking partner relative to the receptor frame.

## Backend approximation
An explicit conversion from a richer DockingMT concept to a simpler representation supported by a backend, such as a topographic pocket converted to a Vina box.


### SearchDomain naming

`SearchDomain` is the canonical general term for the spatial region in which a docking
protocol may search. Concrete domain types may include `BoxRegion`, `SphereRegion`,
`SelectionRegion`, `PocketRegion`, `GlobalDomain`, and future richer domains.

The earlier term `DockingRegion` is considered historical wording and should not be
introduced as a parallel public abstraction.
