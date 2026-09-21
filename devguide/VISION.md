# Vision

## What DockingMT should become

DockingMT is intended to become the **docking layer of MolSysSuite**.

Its first goal is not to invent a new docking algorithm. Its first goal is to provide a scientifically clear, reproducible, backend-independent framework for canonical docking workflows.

A minimal conceptual workflow is:

```text
receptor + docking partner(s)
            |
       preparation
            |
       search domain
            |
 constraints / guidance
            |
         sampling
            |
         scoring
            |
       refinement
            |
         ranking
            |
          poses
            |
        analysis
```

Not every protocol or engine must implement every stage.

## Why it belongs in MolSysSuite

Docking rarely exists in isolation. MolSysSuite already provides or is developing complementary layers:

- **MolSysMT** — molecular-system representation, manipulation, selection, conformations and trajectory handling.
- **MolSysViewer** — interactive molecular visualization.
- **TopoMT** — molecular topography, pockets, grooves, channels and related features.
- **PharmacophoreMT** — pharmacophoric models and constraints.
- **ElastNetMT** — structural flexibility information.
- **MolSys-AI** — natural-language and agentic interaction with molecular workflows.

DockingMT can become the point at which these capabilities meet.

## Long-term scientific identity

The distinctive future of DockingMT should not be “a faster Vina clone.” A stronger scientific direction is:

> **From box-based docking to molecular-landscape-aware docking.**

The relevant landscape may combine:

```text
TopoMT          -> spatial and topographic landscape
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

This may progressively support:

- real pocket geometry rather than only rectangular boxes;
- pocket decomposition and topographic features;
- pharmacophoric guidance;
- receptor flexibility fields;
- conformational ensembles and trajectories;
- dynamic pockets;
- water/metal-aware protocols;
- multiple engines and multiple stages;
- physical refinement;
- uncertainty-aware ranking and pose landscapes.

The MVP must remain small. The architecture must remain open.

## Scientific posture

DockingMT should not present a top-ranked pose or a single score as unquestionable truth. Its long-term model should make it possible to represent alternative poses, molecular states, receptor states, score disagreement, protocol dependence and uncertainty where scientifically meaningful.

## MolSysSuite-native implementation

DockingMT should expose docking as one continuous MolSysSuite workflow even when several
third-party engines participate internally. The user should not have to reconstruct glue
code among molecular preparation, backend conversion, docking, analysis and
visualization.

The suite owns the scientific continuity; providers supply individual capabilities.
