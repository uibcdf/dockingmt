# MolSysSuite Integration

## Integration philosophy

> **MolSysSuite owns the scientific language, contracts and workflow; each component
owns its domain science, while third-party tools provide capabilities behind those
contracts.**

> **MolSysSuite integration should happen through shared scientific concepts, not
unnecessary hard coupling to sibling internals.**

The components mature at different rates. DockingMT should define stable integration contracts while allowing adapters to evolve.

## Conceptual map

```text
                       MolSysMT
                          |
                          v
                  +---------------+
       TopoMT --> |   DockingMT   | <-- PharmacophoreMT
                  +---------------+
                          ^
                          |
                      ElastNetMT
                          |
                          v
                    MolSysViewer
```

This represents scientific flow, not mandatory package dependencies.

## Landscape interpretation

A longer-term interpretation is:

```text
MolSysMT        -> conformational landscape
TopoMT          -> spatial/topographic landscape
PharmacophoreMT -> chemical interaction landscape
ElastNetMT      -> flexibility landscape
                       |
                       v
                  DockingMT
                       |
                       v
                pose landscape
```

This is a scientific horizon, not an MVP requirement.

## MolSysMT

**NOW / central integration**

Expected roles:

- molecular-system input;
- selections;
- receptor/partner extraction;
- atom/entity identity;
- coordinate/topology handling;
- unit conventions;
- trajectory/ensemble access in the future.

DockingMT should prefer MolSysMT-native molecular concepts at its MolSysSuite-facing boundary while keeping backend conversion internal.

## TopoMT

**DESIGNED FOR; integrate when stable enough**

A TopoMT feature can contribute at more than one level.

### Search domain

```text
TopoMT pocket geometry
      ↓ adapter
SearchDomain
      ↓
backend approximation if required
```

### Search guidance

Rich information should not necessarily be collapsed into a region:

```text
subpockets
mouths
necks
channels
surface/topology
relationships
      ↓
SearchGuidance
```

A future native engine may use this information directly.

DockingMT must not encode TopoMT's evolving internal representation into its core.

## PharmacophoreMT

**DESIGNED FOR**

Potential roles:

1. post-docking pose filtering;
2. pose annotation;
3. scoring;
4. hard/soft constraints;
5. search guidance;
6. eventually pharmacophore-guided sampling.

These roles must remain distinguishable.

## ElastNetMT

**HORIZON / DESIGNED FOR at the conceptual boundary**

Potential roles:

- identify flexible receptor regions;
- rank candidate flexible residues;
- provide structured/continuous flexibility information;
- guide ensemble generation;
- provide search guidance for adaptive sampling.

`ReceptorFlexibility` must not be defined merely as a Vina-specific list of residues.

## MolSysViewer

Visualization should consume DockingMT scientific objects rather than become a storage layer for docking information.

See `MOLSYSVIEWER_INTEGRATION.md`.

## MolSys-AI

Structured DockingMT objects should eventually allow natural-language/agentic composition and analysis. AI integration must operate on scientific objects and provenance rather than screen-scraping or scene interpretation.

## Cross-package rule

An evolving package may provide an adapter when its scientific model stabilizes. DockingMT's core should not need to change because an upstream package changes its internal class hierarchy.

## Integration tests

Maintain small cross-package scientific workflows rather than testing only object conversion.

## Shared infrastructure

DockingMT must use the current suite-wide contracts rather than invent local equivalents:

- PyUnitWizard — physical quantities and dimensional safety;
- ArgDigest — public argument contracts and normalization;
- DepDigest — optional providers/backends and lazy loading;
- SMonitor — structured diagnostics and execution context.

See `MOLSYSSUITE_CONTRACT.md`.

## Cross-component stewardship

If DockingMT discovers a missing capability that belongs to MolSysMT or another suite
component, follow the central MolSysSuite cross-component feedback policy rather than
silently copying or reimplementing sibling functionality.

A temporary workaround must name its provider issue and removal condition.
