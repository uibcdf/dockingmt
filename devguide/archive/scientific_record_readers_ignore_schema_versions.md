---
summary: Validate scientific record schema versions before reconstruction
issue: uibcdf/dockingmt#27
status: resolved
opened: 2026-10-02
closed: 2026-10-02
severity: medium
verification: measured
area: [serialization, compatibility]
guard: tests/test_serialization_contracts.py::test_reader_rejects_unsupported_schema_before_payload
normative: devguide/ARCHITECTURE.md
blocked_by: []
supersedes: []
---

# Scientific record readers ignore schema versions

## What

Explicit unsupported result schema versions are accepted and relabeled as 1.0.
Existing scientific readers write version fields but do not perform version
admission before interpreting fields.

## How

At `181000a4fd63b40d750fd739414fb651f5631fbc`:

```python
record = {'schema_version': '999.0', 'poses': []}
restored = DockingResult.from_dict(record)
assert restored.to_dict()['schema_version'] == '1.0'
```

This reproduction uses no engine or molecular operation. Inspection of the
problem, pose, protocol, and box readers also found no schema-version admission;
the measured reproduction above is specifically the result reader.

## Guarded correction (2026-10-02)

The five existing readers (`BoxRegion`, `DockingPose`, `DockingResult`,
`DockingProblem`, and `VinaProtocol`) share a private admission validator.
It accepts the explicit string `1.0` and interprets an absent field as legacy
1.0. Explicit unsupported or malformed values are rejected through
`ArgumentError` (`DMT-E002`), with record type, received version, and supported
versions in structured fields. Non-mapping records also receive a local
argument diagnostic. Supplied records are not modified or migrated.

Pose/result headers are checked before snapshot copying. Result readers also
check nested pose headers before copying their payloads. Problem reconstruction
delegates nested box admission before reading molecular inputs. Opaque context
and metadata dictionaries are retained rather than reinterpreted recursively.
No readers were invented for prepared-object records that only export data.
The accepted policy is recorded as DMT-030 in `devguide/DECISIONS.md`.

Public-reader guards cover unsupported versions before payload access,
supported/legacy round trips and input preservation, malformed records, nested
pose/domain versions, rejection before payload copying, and operation without
molecular calls or optional Vina/viewer imports.

## Measured validation (2026-10-02)

Before the fixes for #26 and #27, the selected contract modules had 86 failures
and 30 passing cases. After the initial correction, 131 focused cases passed in
12.66 seconds. Two additional nested-schema guards were then added.

Full `pytest --receptor=llm`: 344 passed in 48.96 seconds on Python 3.13.14,
versus the preceding 237-test baseline. The same twelve provider warnings remain.
Ruff, format checks (74 Python files), generated indexes, and whitespace checks
pass. Existing replay, redocking, and supported round-trip guards pass. These are
local checks against editable sources, not hosted compatibility qualification.
Resolution covers schema admission; no new schema, migration system, or quantity
interchange codec is introduced.

## Why

Versioned records must protect their interpretation as scores, domains, protocol
stages, and result schemas evolve. Ignoring an unsupported version can silently
discard new fields or reinterpret changed scientific semantics with an old reader.

## What was refuted

Emitting a version field is insufficient when readers ignore it. Independent
mutable snapshots from #25 protect ownership, not schema compatibility. A generic
migration or storage framework is unnecessary for initial version admission.

## Scope and exclusions

Define supported-version admission for DockingMT's existing readers, with an
explicit legacy rule for absent versions. Do not invent migrations for schemas
that do not exist. General quantity interchange remains owned by PyUnitWizard.
No MolSysMT or MolSysViewer change or coordination is needed. The broader review
is [DockingMT #28](https://github.com/uibcdf/dockingmt/issues/28).

## Acceptance criteria

- Reject explicitly unsupported versions before interpreting scientific payloads.
- Document and guard the compatibility rule for missing-version legacy records.
- Preserve supported pose/result/problem/protocol/domain round trips.
- Use a small shared local validator if the owned readers share an admission rule.
- Add durable regression guards and record validation before closing.
