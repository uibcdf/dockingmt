# Offline saved-pose audit

`dockingmt.audit_pose(record)` checks an already loaded `DockingPose` mapping,
including successive fixed-pose Vina/Vinardo evaluations. The caller owns file
access. The audit performs no molecular reads, preparation, engine execution or
viewer operations. Invalid claims become report checks; ArgDigest rejects a
non-mapping argument.

```python
import json
import dockingmt as dmt

with open('saved-pose.json') as stream:
    record = json.load(stream)
report = dmt.audit_pose(record)
print(report['status'])
```

The [executed notebook](pose_audit.ipynb) uses the retained
[scored software control](data/audit/minimal_scored_pose.json). It contains two
real evaluations, Vina then Vinardo, each with eight components, CPU 1, seed 17
and captured inputs. Its input bytes and box come from the existing
[minimal docking control](data/audit/minimal_vina_result.json). State labels
`ligand-control` and `receptor-control` are explicit control declarations, not
independently established chemical identities. Preparation remains unassessed.

## Report contract

The detached JSON-ready report has schema `1.0`, scope
`saved_pose_internal_consistency`, aggregate `status` and ordered `checks`.
Each check contains `check`, `path`, `status` and a bounded `reason`; captured
bytes, coordinates and original context payloads are not copied into reports.
The input is unchanged and identical records produce identical reports.

| Status | Meaning |
| --- | --- |
| `consistent` | Recorded evidence satisfies all supported checks. |
| `incomplete` | A supported check lacks evidence or a method crosscheck. |
| `inconsistent` | A present claim is malformed or contradicts another claim. |

Contradictions take precedence over missing evidence. Independent checks remain
visible after a failure. Unsupported explicit versions stop interpretation of
the affected record; omitted legacy versions remain admitted but incomplete.
Absent evidence never acquires default values or inferred meaning.

## Supported checks

- Pose schema, finite named scores, explicit coordinate length units and finite
  `(N, 3)` coordinate values reuse the existing saved-result validators.
- Each scoring evaluation has an admitted schema and `operation='score'`.
  Resolved protocol parameters are validated before constructing the owned
  protocol: missing parameters remain missing. Applied settings must match the
  protocol, with explicit types and effective seed handling. Search parameters
  `exhaustiveness`, `n_poses` and `energy_range` must be declared unused.
- The evaluation name establishes the expected eight native component keys.
  Historical scores must still exist with matching finite values in the current
  pose; each name has one evaluation owner. Descriptors must agree under strict
  JSON semantics, including the distinction between a boolean and a number.
- Native method/version, component, empirical kind, kcal/mol numeric scale,
  preferred direction, scoring stage, input hashes, backend box and preparation
  assessments reuse the result auditor's native checks. PyUnitWizard handles
  length-unit conversions without changing the caller's unit policy. Weights
  and grid spacing are checked for valid shape, units and finite values; they
  have no independently captured copy of the actual engine settings.
- Both input artifacts use the existing SHA-256/Base64 integrity checks. Missing
  captured bytes are incomplete; malformed bytes or hash contradictions are
  inconsistent. Captured molecular syntax is not parsed.
- Known current state identifiers must agree with preparation records. Unknown
  identifiers remain incomplete. Preparation source declarations must agree
  with their reported assessment/reasons, and provisional execution requires
  recorded opt-in. Geometry declarations retain record order, identity-check
  kind, positive length tolerance and known/unknown state-check consistency.

Current scores without a scoring-history owner remain incomplete. This includes
independent `with_scores(...)` additions and docking scores whose provenance is
held by their enclosing result. Unknown methods receive no invented crosscheck.
Use [`audit_result`](result_audit.md) for docking-result and ranking evidence;
this pose operation does not audit a result assembled from multiple stages.

## Compatibility and limits

New scoring evaluations retain independent `score_name` and `backend_box`
fields in the existing schema-1.0 metadata extension. Earlier records remain
readable by `DockingPose.from_dict`; absence of either field leaves the audit
incomplete. No reader migration, generic stage executor or replay is introduced.

This is internal agreement, not authentication, scientific comparability,
preparation qualification or score correctness. Coordinated edits to both
copies of a claim can agree. Finite stored coordinate edits cannot be compared
with original input geometry by this audit: checking coordinate/PDBQT agreement
requires molecular interpretation through MolSysMT and is outside this scope.
Recorded atom-order and identity-check declarations do not prove atom identity.

The minimal control deliberately overlaps receptor and ligand and has a positive
score. It establishes software behavior, not binding prediction, physical energy
or benchmark performance. Unknown metadata, software authenticity and timing
values are not exhaustively audited.

## Reproduction

Run `python -m pytest tests/test_pose_audit.py --receptor=llm` in
`molsyssuite@uibcdf_3.14`, with this checkout installed editable. Most tests load
the retained JSON and make no engine call; one independent integration test
creates fresh Vina/Vinardo evaluations and audits them. A fresh subprocess blocks
Vina, MolSysViewer and RDKit imports while auditing the retained control.

Select the explicit Python 3.14 Conda kernel to execute the notebook. Its cells
only load JSON and audit records. Full-suite source qualification uses the
unchanged CI pins: MolSysMT `c19a47ada0c2279029abfa296cf915560610ad9a`
and MolSysViewer `ec4c71e574d798b7c8675b7e7e983da878ce9889`.
No sibling implementation is changed. Publication of validation evidence remains
the separate [issue #29](https://github.com/uibcdf/dockingmt/issues/29) decision.

## 2026-10-03 qualification result

All **643 tests pass without skips in 126.39 s**, including 48 pose-audit cases,
on Python 3.14.7 and Vina 1.2.7. The unchanged 27 provider warnings remain visible.
Ruff lint/format, report-index, diff and `pip check` gates pass. The notebook's
three code cells execute successfully using the requested Conda interpreter.
The retained control produces 378 consistent checks; missing bytes produce an
incomplete report and a contradictory score produces an inconsistent report.
This is source-qualified software evidence within the limits above.
