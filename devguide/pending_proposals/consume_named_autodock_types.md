---
summary: Consume named MolSysMT AutoDock types with explicit stages and parent-label projection.
issue: uibcdf/dockingmt#43
status: partial
opened: 2026-10-06
closed:
verification: measured
area: [preparation, vina, validation]
guard: tests/test_named_autodock_types.py
normative:
blocked_by: []
supersedes: []
---

# Consume named AutoDock types

## What

Both preparation helpers consume valid named native AutoDock4 assignments, or
explicitly request MolSysMT's chemical_environment typing. Ligand typing follows
requested H/charge stages. Receptor typing requires already declared chemistry,
H and charges. No implicit parameterization is introduced.

## How

Reuse public assignment/extraction. Classify the complete selected graph before
H projection; retain parent labels, original provider reports and prepared/source
maps. Delegate stale graph/value binding to MolSysMT's checked extraction. Keep
labels separate from atomic elements. Use the named profile's H/HD classification
to decide retained versus omitted H, preserving the existing charge transfers.
Bind saved prepared labels before emitting attributed PDBQT remarks.

## Why

MolSysMT #222 is delivered, but DockingMT still replaces native chemical-context
labels with heuristic N/S and residue/name rules. Supported named evidence should
reach ligand/receptor output without losing chemistry, rules or producer credit.

## What was refuted

An unqualified atom_ff_type column is not a named scheme. An extracted fragment
must not be chemically reclassified as its original full graph. A named profile,
a parseable PDBQT and a Vina pose do not certify scientific docking readiness.

## Scope and exclusions

Bounded consumer adoption under #5/#33, preserving #42's separately committed
qualification. Keep untyped workflows provisional. No provider source edits,
Meeko runtime, implicit H/protonation/charge model, torsion policy, general export
replacement, H5MSM mechanics persistence or biological/performance equivalence.

## Acceptance criteria

Independent chemical cases, unchanged inputs/options, explicit stage order,
full-source/projected labels, stale/manual evidence, provider failure identity,
source/prepared/written axes, charge conservation, nondefault units, BNZ, flexible
ligand order, actual Vina admission and saved-result provenance. Retain finite
raw evidence and an executed notebook, with local regression and quality/reporting
checks. Public/installed/hosted acceptance remains a separate checkpoint.

## Local qualification — 2026-10-06

The [contract](../validation/named_autodock_types.md),
[executed notebook](../validation/named_autodock_types_2026-10-06.ipynb),
[raw receipt](../validation/data/named_types/qualification_2026-10-06.json) and
[checkpoint](../validation/data/named_types/checkpoint_2026-10-06.json) retain
22 cases and ten executed code cells on Python 3.14.7 / Vina 1.2.7. All 64 new
tests and the complete suite pass: **952 passed, no skips, 273.21 s, 145 warnings**.
Ruff (118 files), report/index, changed-document links, finite evidence/hash,
editable identity, component guidance and diff checks pass. Pre-existing
SMonitor/ArgDigest canonical drift and unrelated AmberTools dependency conflicts
remain explicitly recorded; no guide copies or sibling sources are changed.

Independent N/S environments and F/P polar H retain provider classification.
Parent amide N survives selection without a second classification. Native stale
labels/chemistry fail; manual replacement clears provider attribution and keeps
the existing heuristic guard. Malformed consumer evidence/maps and changed
prepared labels fail before export. Requested provider exceptions propagate
unchanged. Virtual H is not silently materialized.

Original BNZ follows declared template → H → charges → types (12 evaluated,
six prepared aromatic C). Flexible 5X72 preserves the written source/label axis.
The pm/coulomb control conserves charges in explicit output units. Real default
Vina accepts the named/charged synthetic receptor/partner, returns one pose and
retains reports/maps/captured exact inputs through finite result JSON. The
preparation assessment remains scientifically unassessed.

The first test attempt refuted three fixture assumptions: collinear ring poses
support H generation, MolSys exposes an atom_ff_type setter through basic.set,
and captured Vina text uses a backend_inputs key. Controls now use declared
nondegenerate polygon poses, the supported native mechanics property and the
actual backend_artifacts capture contract. These are consumer test corrections,
not evidence of provider defects or authorization for a provider workaround.

## Outstanding evidence

This is a local source candidate. Python 3.11–3.13, clean installed artifacts,
hosted CI and public admission remain separate recovery checkpoints. General
scientific preparation/scoring remains #5, explicit torsion policy #6/#17 and
provider H projection/export MolSysMT #223. Keep this issue open until its owning
publication/checkpoint decision. The earlier #42 block is separately committed
locally as `6f193fb`; historical notebooks/receipts were not overwritten.
