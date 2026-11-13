---
summary: Native contact records can fail reading after JSON object-key sorting without any content-digest change.
issue: uibcdf/bindingmt#114
status: open
opened: 2026-11-12
closed:
severity: medium
verification: reproduced
area: [persistence, public-api, interoperability]
guard:
normative:
blocked_by: []
supersedes: []
---

# Native interface records and JSON object-key order

## What

A real experimental 0.2 contact record with endpoint names Z then A restores
through the normal writer/reader. Re-encoding it with `json.dumps(sort_keys=True)`
leaves its canonical content SHA-256 unchanged but the reader refuses:
`Every contact is one unique cross-participant pair.`

The native validator derives positional endpoint orientation from insertion order
of the participants mapping. JSON object key order is not an appropriate carrier
for scientific order; explicit grouping/operation axes and source correspondences
must retain their own meaning. The common digest already treats object order as
irrelevant. This is a BindingMT persistence/correspondence defect, not a missing
MolSysMT tool, altered original measurement or source chemistry failure.

## How

```python
import json
import bindingmt as bmt
import pyunitwizard as puw
from molsysmt.native import MolSys, Structures

system = MolSys(n_atoms=2)
system.structures = Structures(
    coordinates=puw.quantity([[[0, 0, 0], [0.2, 0, 0]]], 'nm')
)
result = bmt.calculate_interface_contacts(
    system, participants={'Z': [0], 'A': [1]},
    cutoff='0.3 nm', structure_index=0, source_id='authored-two',
)
record = json.loads(json.dumps(result.to_dict(), sort_keys=True))
assert record['content_sha256'] == result.to_dict()['content_sha256']
bmt.BindingInterface.from_dict(record, experimental=True)
```

Actual reproduction: `.molsyssuite/interface-characterization-annotation-112-20261112/key-order-probe-01/`,
consumer base f55929d with the uncommitted H-R2 increment, MolSysMT ff25f120,
Python 3.14.10 and historical loaded native SHA-256
`2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`.
The tiny cell exits normally and preserves both success/refusal observations.
No molecular work is required by the failed reader itself.

## Why

The normal native source save/read is qualified for its exact exercised path.
Other JSON tooling may reorder objects, and richer cross-component receiving
must not change participant orientation or analysis identity when that happens.
H-R2 preserves full native records, so it inherits their existing order limits;
its own participant-level annotations do not solve the underlying codec defect.

## What was refuted

The normal JSON round trip succeeds. No coordinate, criterion, atom membership,
measurement value, units, grouping list or canonical content digest changes.
The failure does not indicate a failed original calculation or invalid geometry.
No provider patch/workaround or historical producer rewrite is justified.

## Scope and exclusions

Reproduced for 0.2 native contacts. Audit 0.3 surface and 0.4 named ionic/hypothesis
ordering and nested H-R2 records; those further failures are not all claimed
measured yet. Separate explicit order in list fields from unordered label mappings.
Keep native calculation/recognition, alternative chemistry and the other #112
branches outside this independently closable persistence issue.

## Acceptance criteria

- Real positive/empty and exchanged-side records restore after object sorting,
  retaining scientific orientation, original local/source maps, all witnesses,
  contributor identities, quantities and original checks as historical.
- Footprint projection/independent save/read retain exact membership/alignment.
- Unequal surface sides and labelled ionic contributions keep their original
  identities rather than being silently renamed/reordered by the reader.
- Any experimental format/migration decision is explicit; never invent missing
  old ordering evidence or rewrite frozen original records/producer identities.
- Add mechanically addressable public-API regression controls and exercise normal/
  pm-fs cold readback with molecular work forbidden; update the maintained checkpoint.
