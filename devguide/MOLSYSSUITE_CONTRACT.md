# MolSysSuite Contract

## Purpose

DockingMT is not an isolated docking package that happens to interoperate with MolSysSuite.
It should be born as a native MolSysSuite scientific component and inherit the suite's
shared contracts from its first implementation.

The guiding rule is:

> **MolSysSuite owns the scientific language, contracts and workflow; specialized
> components and third-party engines provide capabilities behind those contracts.**

A second rule follows:

> **A third-party implementation is an engine/provider, not the scientific abstraction.**

Examples:

```text
RDKit        != molecular chemistry model
PDBFixer     != receptor-preparation model
Meeko        != docking-preparation model
Vina         != docking model
Mol*         != visualization model
```

They may provide excellent implementations. MolSysSuite provides the coherent scientific
framework in which those implementations participate.

## 1. Layered responsibility

```text
                             MolSysSuite
                                  |
              +-------------------+-------------------+
              |                                       |
        Scientific/domain                         Shared
           components                         infrastructure
              |                                       |
       +------+------+------+                 +--------+--------+
       |      |      |      |                 |        |        |
   MolSysMT TopoMT Pharma  ElastNetMT     PyUnitWizard ArgDigest DepDigest
       |                                      |
 MolSysViewer / DockingMT / MolSys-AI       SMonitor
```

This is conceptual rather than a Python import graph.

## 2. MolSysMT — molecular-system foundation

DockingMT should use MolSysMT whenever a responsibility is general to molecular systems
rather than specific to docking.

Expected MolSysMT-owned or MolSysMT-mediated concerns include:

- molecular-system representation;
- topology and structures;
- atom/entity identity;
- selections;
- molecular forms and conversions;
- general structure manipulation;
- general structure preparation where the capability exists;
- physical-quantity conventions through the suite infrastructure;
- trajectories and conformational collections.

DockingMT must not silently duplicate a missing general molecular capability merely
because docking needs it.

If DockingMT discovers that MolSysMT lacks a capability that scientifically belongs there,
follow the MolSysSuite cross-component feedback contract: report the requirement to
MolSysMT, cross-link any temporary DockingMT workaround, and state its removal condition.

## 3. DockingMT — docking semantics

DockingMT owns concepts whose scientific meaning is specifically docking-related:

- `DockingProblem`;
- `DockingProtocol`;
- docking-specific preparation intent;
- `SearchDomain`;
- `SearchGuidance`;
- `DockingConstraint`;
- sampling/scoring/refinement/ranking composition;
- backend capability negotiation;
- `DockingRun`;
- `DockingResult`;
- `DockingPose`;
- `DockingCampaign`;
- docking-specific validation and analysis;
- docking-specific provenance.

DockingMT may compose MolSysMT operations while adding docking-specific meaning.

For example:

```text
DockingMT prepare_receptor_for_docking(...)
            |
            +-- MolSysMT: diagnose / repair / hydrogen handling / selections
            |
            +-- DockingMT: choose docking-specific state and policy
            |
            +-- backend adapter: produce backend-specific representation
```

## 4. Preparation ownership

Preparation has three conceptually different layers:

```text
general molecular preparation
          |
          v
docking-specific preparation protocol
          |
          v
backend-specific conversion/preparation
```

### General molecular preparation

Prefer MolSysMT capabilities when the operation is generally meaningful outside docking.

### Docking-specific preparation

DockingMT owns the scientific intent that turns a molecular system/state into one suitable
for a particular docking protocol.

Examples include:

- selecting which receptor state enters docking;
- deciding whether a retained water participates in the docking problem;
- enumerating or selecting partner molecular states for a docking campaign;
- resolving engine capability requirements;
- recording preparation choices as docking provenance.

### Backend preparation

Adapters own requirements that exist only because a backend requires them.

Example:

```text
MolSysSuite prepared molecular state
             |
             v
Vina adapter / Meeko provider
             |
             v
PDBQT representation
```

PDBQT generation is not the definition of scientific receptor/ligand preparation.

## 5. PyUnitWizard contract

DockingMT must not invent an independent unit framework.

> **Physical quantities in DockingMT's public scientific API follow the MolSysSuite
> PyUnitWizard contract.**

This applies at minimum to:

- coordinates;
- distances;
- search-domain dimensions;
- RMSD;
- cutoffs;
- angles;
- physical energies.

Backend-native units belong at the adapter boundary.

```text
public quantity
    |
PyUnitWizard
    |
normalized / converted quantity
    |
backend adapter
    |
backend-native numeric representation
```

Never silently interpret a dimensionful bare numerical value when the suite policy would
consider that ambiguous.

Scores require semantic metadata. Not every docking score is a physical energy even when
reported with energy-like conventions.

## 6. ArgDigest contract

Public DockingMT API boundaries should follow the MolSysSuite ArgDigest model rather than
grow bespoke validation logic independently in every function.

ArgDigest should provide, as appropriate:

- function argument contracts;
- argument normalization;
- canonical value digestion;
- defaults;
- validation;
- trusted internal delegation.

Docking-specific digesters and domains remain owned by DockingMT unless they become
genuinely suite-wide concepts.

## 7. DepDigest contract

Optional docking engines and chemistry providers are an expected property of DockingMT.

Use DepDigest for:

- soft-dependency registration;
- lazy availability checking;
- lazy imports;
- clear missing-dependency diagnostics;
- architecture audits against accidental top-level imports.

Do not scatter ad hoc `try/except ImportError` dependency management across DockingMT.

Potential optional providers/backends include:

- AutoDock Vina;
- Meeko;
- RDKit;
- future ML docking/scoring engines;
- specialized peptide/macrocycle engines;
- physical-refinement engines.

The exact hard/soft dependency set is an implementation decision and should remain small.

## 8. SMonitor contract

Docking workflows generate scientifically meaningful warnings, limitations and failures.
These should use SMonitor's structured diagnostic contracts.

Candidate diagnostic classes include:

- ambiguous molecular state;
- unsupported metal chemistry;
- retained/removed structural water;
- rich search domain approximated by a simpler backend domain;
- unsupported constraint;
- backend capability mismatch;
- partial molecular-identity mapping;
- backend execution failure for one campaign member;
- nonphysical or non-comparable score semantics;
- reproducibility limitation.

Diagnostics should have stable machine-readable codes and enough structured context for
users, tests and MolSys-AI/agents.

## 9. MolSysViewer ownership contract

MolSysViewer owns visualization infrastructure, not DockingMT science.

Following the MolSysViewer addon model, the docking addon should be shipped from the
DockingMT repository/package rather than implemented in MolSysViewer core.

Conceptually:

```text
DockingMT repository
    |
    +-- dockingmt/
    |
    +-- molsysviewer_dockingmt/
```

The exact package layout is not frozen.

DockingMT owns the scientific information. The addon translates that information into
viewer workspaces, overlays and interactions.

## 10. TopoMT, PharmacophoreMT and ElastNetMT

These components are scientific peers, not implementation libraries hidden beneath
DockingMT.

They should integrate through scientific contracts:

```text
TopoMT           -> SearchDomain / SearchGuidance
PharmacophoreMT  -> Constraint / SearchGuidance / Score / Filter
ElastNetMT       -> ReceptorFlexibility / SearchGuidance / receptor-state strategies
```

Do not copy their algorithms or internal data models into DockingMT.

If a cross-component contract needs to become stable across two or more repositories,
the shared decision belongs in the MolSysSuite governance layer.

## 11. MolSys-AI / agent-first design

DockingMT's scientific objects should be introspectable and diagnosable enough to be
safely consumed by agents.

This does not mean designing the scientific API around natural-language commands.
It means providing:

- explicit scientific objects;
- inspectable resolved protocols;
- structured diagnostics;
- stable argument contracts;
- provenance;
- deterministic identifiers;
- machine-readable capability information.

MolSys-AI should orchestrate DockingMT through the same scientific API used by humans.

## 12. Cross-component stewardship

The MolSysSuite governance contract is normative:

> **Do not silently fork sibling functionality into DockingMT.**

If a missing capability belongs to another component:

1. identify the provider component;
2. report the requirement there with concrete scientific/integration evidence;
3. cross-link the DockingMT issue/workaround;
4. make any workaround explicit and temporary;
5. state the condition for removing it.

If the required change alters a shared suite contract, the decision belongs in
`uibcdf/molsyssuite`.

## 13. External tools and native implementations

MolSysSuite is not philosophically committed to either "wrap everything" or
"implement everything natively."

Use the best architecture for the scientific problem:

```text
excellent external capability + clean integration
                -> provider/engine

need for stronger control, performance, traceability,
or original scientific capability
                -> native MolSysSuite implementation
```

The invariant is ownership of the scientific abstraction, not ownership of every
algorithm.

## 14. Governance onboarding for DockingMT

When the DockingMT repository is created as a MolSysSuite component, its bootstrap should
include alignment with current suite governance, including:

- registration in the authoritative suite registry when accepted;
- the synchronized `MOLSYSSUITE_GUIDE.md`;
- `AGENTS.md` pointing contributors/agents to suite governance;
- current Python/tooling policies;
- shared cross-component reporting rules;
- required canonical infrastructure guides adopted by the component;
- component-local scientific validation and development guides.

DockingMT should not copy old policy from an incubating sibling if the central suite has a
newer accepted rule.
