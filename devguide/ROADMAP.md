# Roadmap

The roadmap defines direction and gates, not dates.

## Phase 0 — Foundations and MolSysSuite-native bootstrap

Status: **NOW**

- establish scientific model;
- establish molecular-state/preparation concepts;
- establish search-domain/guidance/constraint distinctions;
- establish backend capability contract;
- choose and validate Vina integration;
- adopt MolSysSuite shared infrastructure contracts (PyUnitWizard, ArgDigest, DepDigest, SMonitor);
- establish provenance and identity policies;
- make scientific defaults explicit;
- define initial package boundaries;
- select redocking validation cases.

**Exit condition:** architecture can express the Core MVP without leaking Vina-specific
concepts into the public scientific model and DockingMT behaves as a native MolSysSuite
component rather than a parallel software stack.

## Phase 1 — Core canonical docking

Status: **NOW**

- preparation;
- redocking;
- explicit local docking;
- search domain from selection;
- normalized poses/results;
- named scores/ranks;
- provenance;
- basic MolSysViewer visualization.

**Exit condition:** all Core MVP gates pass and redocking validation is scientifically credible.

## Phase 2 — Extended scientific MVP

Status: **NOW after Core**

- explicit scoring/rescoring;
- small virtual screening;
- campaign-level aggregation as needed;
- pose comparison/clustering;
- basic interaction analysis;
- reproducibility audit;
- regression/validation suite;
- user-facing examples and API stabilization.

**Exit condition:** Extended MVP gates pass.

## Phase 3 — Advanced scientific integration with MolSysSuite peers

Status: **DESIGNED FOR**

- TopoMT-derived domains and guidance;
- PharmacophoreMT filtering/scoring/constraints/guidance;
- richer MolSysViewer Docking Explorer;
- ensemble workflows from MolSysMT;
- first meaningful ElastNetMT bridge when scientifically mature.

**Exit condition:** integrations demonstrate scientific value without fragile package coupling.

## Phase 4 — Advanced protocols and multiple backends

Status: **DESIGNED FOR**

Potential work:

- GNINA/ML backends;
- multi-stage protocols;
- consensus docking;
- receptor flexibility;
- macrocycle/peptide-specialized engines;
- ensemble/dynamic-pocket workflows;
- water/metal-aware protocols;
- blind docking.

## Phase 5 — Native scientific innovation

Status: **HORIZON**

Investigate original DockingMT methods, especially:

- molecular-landscape-aware sampling;
- topography-aware search;
- pocket decomposition;
- flexibility-aware search;
- pharmacophore-guided search;
- dynamic-pocket docking;
- fragment placement/growth/linking support;
- hybrid physics/ML scoring/refinement;
- uncertainty-aware pose landscapes.

## Roadmap governance

A feature should enter implementation only when:

1. its scientific purpose is clear;
2. it fits or deliberately revises the scientific model;
3. required dependencies are mature enough;
4. a validation criterion can be stated.

Do not promote horizons merely because the architecture can represent them.
