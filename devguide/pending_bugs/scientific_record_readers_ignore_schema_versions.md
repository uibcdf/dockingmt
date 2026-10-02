---
summary: Validate scientific record schema versions before reconstruction
issue: uibcdf/dockingmt#27
status: open
opened: 2026-10-02
closed:
severity: medium
verification: reproduced
area: [serialization, compatibility]
guard:
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
