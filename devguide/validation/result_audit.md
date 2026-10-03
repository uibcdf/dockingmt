# Offline saved-result audit

`dockingmt.audit_result(record)` checks an already loaded saved DockingResult
mapping. The caller owns file access. It does not reconstruct molecular systems,
prepare inputs, run a backend, or invoke a viewer. Invalid record claims produce
report entries; a non-mapping API argument is rejected by ArgDigest.

Standalone scoring/rescoring poses use the separate
[`audit_pose(record)` contract](pose_audit.md). Their evaluation history does
not replace a docking result's provenance or establish ranking evidence.

```python
import json
import dockingmt as dmt

with open("saved-result.json") as stream:
    record = json.load(stream)
report = dmt.audit_result(record)
print(report["status"])
```

The [executed notebook](result_audit.ipynb) reads the retained
[minimal native Vina control](data/audit/minimal_vina_result.json) and demonstrates
complete internal agreement, absent captured bytes, changed bytes, and an edited
ranking policy. The fixture comes from the existing minimal raw-PDBQT software
control, using Vina 1.2.7, seed 123, one CPU, exhaustiveness 1 and two requested
poses. Inputs are explicitly **unassessed**. This is software evidence, not a
scientific benchmark or preparation qualification.

## Report contract

The detached JSON-ready report has schema `1.0`, scope
`saved_result_internal_consistency`, an aggregate `status`, and ordered `checks`.
Each check exposes `check`, a record location in `path`, `status`, and a bounded
`reason`. It contains no coordinates, original context payloads or captured bytes.
The input is never mutated. Identical records produce identical reports.

| Status | Meaning |
| --- | --- |
| `consistent` | Available evidence satisfies every supported check below. |
| `incomplete` | Supported checks lack evidence, including legacy meaning or an unavailable method crosscheck. |
| `inconsistent` | A present claim is malformed or contradicts another recorded claim. |

Contradictions take precedence over missing evidence. Independent checks remain
visible when another check fails. Unsupported explicit outer schema versions
stop interpretation; omitted outer versions retain the existing legacy admission
but are reported as implicit evidence. A missing field does not acquire a default
unit, method, input, ranking observation or source identity.

## Supported checks

- Existing result/pose schema admission, finite named scores, score descriptors
  and recorded-ranking validation are shared with the existing readers.
- Both retained PDBQT inputs: recorded format, SHA-256 shape, strict Base64
  decoding and hash agreement. Present invalid bytes remain contradictory even
  when a digest is absent. Digests without retained bytes are incomplete.
- Explicit coordinate length units, finite `(N, 3)` values, and native box/grid
  length units. PyUnitWizard interprets and converts units; no defaults are used.
- Native `AutoDock Vina/vina` and `AutoDock Vina/vinardo` declarations: backend,
  selected scoring function, version, retained component meaning, native
  kcal/mol numeric scale, preferred direction, docking stage, input hashes,
  projected box and preparation assessments. Weights must be nonempty finite
  real lists; grid spacing must be a positive scalar length. These settings have
  no independent provenance copy: their agreement with actual engine settings
  cannot be established offline. Unknown methods remain incomplete rather than
  receiving inferred semantics. A literal `unknown` version lacks evidence.
- Protocol snapshots must agree. Recorded rankings must follow their explicit
  direction; `rank_by` additionally preserves stable ties. Consecutive recorded
  decisions retain pose/state membership and order. The latest policy, output
  membership, identities, selected numeric values, assigned ranks and declared
  semantics must agree with the current poses. Earlier observed scores may differ
  after explicit rescoring. Legacy policy-only entries retain missing observations.

The check list is bounded: this is not complete validation of every metadata,
problem, protocol or search-domain extension. Unknown metadata is not interpreted.
Numeric agreement and coherent ranking do not establish scientific comparability.

## Shared integrity operation

`dockingmt.verify_captured_inputs(artifacts)` accepts the existing
`provenance['backend_artifacts']` mapping and returns receptor/partner byte sizes.
Missing or invalid evidence raises the catalog `ArgumentError` (`DMT-E002`). Audit
and the existing replay tools share the same private byte-integrity operation;
the developer replay wrapper preserves its historical `ValueError` contract.

A matching SHA-256 only checks the captured bytes against a retained claim. It
cannot authenticate the record, validate PDBQT chemistry, or detect coordinated
changes to both bytes and hashes. This audit does not qualify charges, torsions,
atom mapping, scientific accuracy, public dependency admission or full replay.

## Verification

The durable tests in `tests/test_result_audit.py` cover the retained native control,
byte tampering, absent evidence, malformed scores/units/history, native-context
contradictions, stable ties, successive rankings and stale policy/current poses.
Guards forbid file access, molecular operations and live backend/viewer imports
during the supported operations. Replay regression tests exercise the shared
integrity rule. Issue [#32](https://github.com/uibcdf/dockingmt/issues/32) owns this
bounded Core C5 follow-up; validation publication remains the separate #29 decision.
