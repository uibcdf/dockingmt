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

## Reproducible performance evidence

The [workflow profiling record](validation/workflow_profiling.md) defines the
measurement boundaries, environment and limits of the current 181L baseline.
Its [Jupyter notebook](validation/workflow_profiling.ipynb) explores the
[versioned raw reports](validation/data/workflow_profiling/) with tables and plots,
and can explicitly invoke the existing command to collect new samples.
The [result export comparison](validation/result_export.md) and its
[executed notebook](validation/result_export.ipynb) retain before/after measurements
for the optimized independent dictionary snapshots.

The [score/ranking contract](validation/score_semantics.md) and its
[executed offline example](validation/ranking_history.ipynb) document declared
score meaning and successive ranking evidence. The saved example is synthetic
software data, not a scientific validation or runtime benchmark.

The [fixed-pose scoring contract](validation/fixed_pose_scoring.md) and
[executed notebook](validation/fixed_pose_scoring.ipynb) demonstrate the public
prepared-input operation and independent score attachment without pose search.

## Development rule

The [public preparation assessment contract](validation/preparation_assessment.md)
and [executed notebook](validation/preparation_assessment.ipynb) expose declared
provisional chemistry before engine execution and retain the same report in
Vina result provenance.

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

The [offline result audit](validation/result_audit.md) and its
[executed notebook](validation/result_audit.ipynb) retain bounded consistency
checks for captured bytes, score provenance, units and ranking decisions.

The [offline pose audit](validation/pose_audit.md) and its
[executed notebook](validation/pose_audit.ipynb) check saved standalone scoring
and rescoring histories against current pose scores and declarations.

The [incremental prepared-docking contract](validation/incremental_docking.md)
and [executed notebook](validation/incremental_docking.ipynb) demonstrate lazy
serial execution, explicit item failures and independent outcome records.

The [pose/reference viewer contract](validation/viewer_reference.md) and
[executed notebook](validation/viewer_reference.ipynb) demonstrate frame
correspondence, repeated loading and observable integration failures.

The [native MolSysMT format profile](validation/native_molsysmt_formats.md) records
prepared-input consumption, current SDF gaps and staged removal conditions. Its
[executed notebook](validation/native_molsysmt_formats.ipynb) runs the real 1IEP path.

The [rigid-fragment migration](validation/rigid_fragment_consumption.md) and its
[executed notebook](validation/rigid_fragment_consumption.ipynb) retain four-ligand
before/after equivalence and source-to-retained atom maps for the MolSysMT partition.

The [chemical-readiness consumer record](validation/chemical_readiness_consumption.md)
and [executed notebook](validation/chemical_readiness_consumption.ipynb) distinguish
stored-field coverage from docking validity and retain preparation-cost samples.

The [receptor residue-coverage record](validation/receptor_coverage_consumption.md)
and [executed notebook](validation/receptor_coverage_consumption.ipynb) qualify
exact MolSysMT template consumption with original 181L/1IEP sources, controlled
modified/incomplete residues and paired preparation-cost measurements.

The [PDB connectivity-policy diagnosis](validation/pdb_bond_inference.md) and
[executed notebook](validation/pdb_bond_inference.ipynb) reproduce the optional
OpenMM difference and retain native candidate comparisons for MolSysMT #304.

The [explicit chemical-template consumer record](validation/chemical_template_consumption.md)
and [executed notebook](validation/chemical_template_consumption.ipynb) qualify
MolSysMT transfer on original 181L BNZ and controlled 5X72 inputs, retaining
explicit maps, conflicts, pose preservation and the provisional Vina safeguard.
