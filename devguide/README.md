# DockingMT Development Guide

## Purpose

This directory is the scientific and architectural seed of **DockingMT**, the docking layer of MolSysSuite.

DockingMT should begin by reproducing canonical, well-established molecular docking workflows through a clean, inspectable and reproducible MolSysSuite API. Its first implementation is deliberately modest in algorithmic ambition, but its scientific model and architecture must not be constrained by the capabilities of the first docking engine.

The initial reference backend is **AutoDock Vina**. DockingMT is not a Vina wrapper.

## Foundational thesis

> **DockingMT concepts must be richer than the capabilities of its first engine.**

A second long-term thesis is:

> **From box-based docking to molecular-landscape-aware docking.**

DockingMT should eventually be able to combine spatial/topographic, chemical, flexibility and conformational information into guided exploration of binding pose landscapes.

## Status vocabulary

Every proposed capability should be classified as:

- **NOW** — required for the current scientific MVP or its immediate foundation.
- **DESIGNED FOR** — not necessarily implemented now, but the architecture must admit it naturally.
- **HORIZON** — a scientifically interesting future direction that should remain visible without over-engineering the present implementation.

## Reading order

1. `VISION.md`
2. `DESIGN_PRINCIPLES.md`
3. `SCIENTIFIC_SCOPE.md`
4. `MOLSYSSUITE_CONTRACT.md`
5. `GLOSSARY.md`
6. `SCIENTIFIC_MODEL.md`
7. `ARCHITECTURE.md`
8. `ENGINES.md`
9. `MVP.md`
10. `VALIDATION_STRATEGY.md`
11. `MOLSYSSUITE_INTEGRATION.md`
12. `MOLSYSVIEWER_INTEGRATION.md`
13. `IMPLEMENTATION_STRATEGY.md`
14. `SCIENTIFIC_HORIZONS.md`
15. `ROADMAP.md`
16. `DECISIONS.md`

For a one-page index of responsibilities, see `DOCUMENT_MAP.md`.

## Development rule

Do not begin by designing classes around Vina command-line arguments. Begin from the scientific concepts defined here, then map those concepts to backend capabilities through adapters.

Do not infer that every concept documented here must immediately become a Python class, module, dependency or plugin framework. The scientific model is intentionally richer than the first implementation.

## Governance

These documents are a living design constitution, not immutable specifications. Changes are welcome when implementation experience, validation results or scientific evidence justify them. Foundational changes should be explicit and recorded in `DECISIONS.md`.

When implementation pressure conflicts with a foundational principle, do not silently simplify the model. Record the trade-off and decide consciously.

## MolSysSuite inheritance

DockingMT inherits suite-wide contracts rather than redefining them locally. In particular,
physical quantities, public-boundary digestion, optional dependency management and
structured diagnostics should follow the current MolSysSuite contracts implemented through
PyUnitWizard, ArgDigest, DepDigest and SMonitor. See `MOLSYSSUITE_CONTRACT.md`.

## Freeze status

This seed is frozen as `DockingMT devguide v0.1`. See `FROZEN_SEED.md`.
