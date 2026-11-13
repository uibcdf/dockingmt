---
summary: Native contact records can fail reading after JSON object-key sorting without any content-digest change.
issue: uibcdf/bindingmt#114
status: resolved
opened: 2026-11-12
closed: 2026-11-13
severity: medium
verification: reproduced
area: [persistence, public-api, interoperability]
guard: tests/test_interface_json_object_order.py
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

## Selected correction and compatibility admission — 2026-11-12

Contact 0.2 and surface 0.3 retain sufficient ordered operation axes. Resolve
endpoint labels bijectively against their saved public call axes, independently
of mapping iteration, and cross-check the saved original grouping/projections.
Footprint 0.1 inherits those same explicit facts. No scientific field, stored
record, method definition, digest algorithm or numerical result is rewritten.

For ionic collections, new format 0.5 requires `context.analysis_names`, a unique
ordered exact cover of native analysis labels. A 0.4 reader must refuse 0.5;
there is no silent older-reader guarantee. Continue reading actual 0.4 records
unchanged. A saved 0.4 construction already retains its explicit analysis list;
use that history when unambiguous. A bare 0.4 I0 contains no such fact: report
unknown order and require explicit `analysis_names` for a new construction,
recording caller-supplied order authority. Never recover that historical fact
from object order or alphabetical spelling. Order-independent source rechecks
may inspect named old observations without claiming an execution order.

Audit native contact/surface validators, original claims, footprint projection,
ionic construction/linking, summaries and nested H-R2 annotations. Preserve real
old emitted 0.4 records and original hashes as fixtures. Qualify sorted/reversed
objects, positive/zero evidence, unequal surfaces and nonlexical analysis labels,
with cold readers and molecular operations forbidden. Keep indexed arrays,
grouping lists, original operation lists and contributor order meaningful.

## Resolution and bounded source qualification — 2026-11-13

The correction uses persisted explicit axes, rather than JSON object insertion
order. Contact 0.2 and surface 0.3 resolve endpoint labels bijectively against
their original public operation axes; footprint 0.1 preserves their aligned
contributors and local/source maps. No format/digest change is needed for those
records. Nested H-R2 contact/surface evidence follows the same rule. Ambiguous or
inconsistent axes refuse; no molecular matcher or calculation is introduced.

New native ionic results use **experimental record 0.5**, with ordered unique
`context.analysis_names` covering every labelled native observation. Construction,
linking and summaries share that saved order. This record version is distinct
from the package's unchanged 0.1.0 source tag. The actual reader at dad9cdf refuses
0.5 before molecular operations; an older reader is not silently compatible.

Actual previously emitted 0.4 I0/I1/I2 records remain readable without upgrading,
rewriting or changing their digests, checks and producers. A saved construction's
explicit list supplies original order when unambiguous. Bare I0 reports
`interaction_analysis_order is None`. New construction then requires explicit
`analysis_names`, records `analysis_order_authority='caller_explicit'`, and never
asserts that choice was the original recognition order. Saved known order cannot
be overridden. Alphabetical iteration used solely for order-independent source
checks does not become original analysis history. Adding an unsanctioned 0.5
order field to a 0.4 record refuses rather than disguising a migration.

### Public regression evidence

`tests/test_interface_json_object_order.py` supplies **30 passing controls**:
sorted/reversed objects; positive/zero contacts and independently persisted
footprints; nonidentity source/local maps; unequal surface sides; nonlexical
ionic labels, real native construction and linking; actual frozen 0.4 records;
unknown/explicit/known order authority; malformed and downgraded records; nested
H-R2 annotation and unresolved axes. Indexed arrays and ordered lists keep their
meaning. Fixture hashes/provenance are in
`tests/data/interface_order_compat/original_04/manifest.json`; five new declared
support files have exact entries in `devtools/conda-build/resources.toml`.
Original scientific inputs and hashes remain intact.

The final selected source population is **229 passed and 1 strict xfailed per
unit policy**: records 160 passes, applications 69 passes/1 xfail. Policies are
normal Pint and explicit pm/fs/K/mole/dalton/e/kJ/mol/radians. Complete selected
modules are JSON order, contacts, burial, data core, ionic integration, H-R2 and
unit bootstrap. The sole xfail remains PyUnitWizard #156's native unyt charge
construction gap; there is no local conversion fallback. The 105 unrelated
redocking-result/outcome/core-helper cases in the prior 305-case H-R2 selection
were not rerun. These counts describe different selections, not a regression or
an extension of full-suite/installed/public/platform evidence.

A real public workflow emits ten new contact/footprint/surface/ionic/linked/
annotated records plus one native hypothesis. Separate sorted derivatives of
those ten and the three original 0.4 records are cold-read under unyt/pm-fs.
A core-only reader forbids PharmacophoreMT/TopoMT/Vina; a second reader explicitly
uses the native hypothesis IO. Both inspect all 13 sorted records with molecular
operations/recognition forbidden, zero new originating uses, unchanged files and
unchanged caller policy. Native component order remains zeta/alpha/middle.
The archived dad9cdf decoder independently refuses actual newly emitted 0.5.
Its temporary source export is retired; no install or provider change occurs.

### Source, resource and evidence limits

Development interpreter: unchanged legacy Python 3.14.10 in
`molsyssuite@uibcdf_3.14`; read-only import origins and `pip check` pass. No shared
prefix migration, reinstall or native rebuild is performed. Participating source:
MolSysMT ff25f120, PharmacophoreMT 296cc8f, PyUnitWizard cc51c8e, ArgDigest 7be790b,
SMonitor 4a4cd1e and DepDigest 5e93eaf. Each scientific cell binds runtime Python
hashes, Git heads and actual native bytes before/after. Separate concurrent
provider test/documentation work is preserved rather than overwritten. Historical
imported version strings remain distinct from those source/content identities.
After these stable final cells, PharmacophoreMT began separate uncommitted runtime
work on its comparison API. A later custody check detects and preserves those
changes. They are not this tested 296cc8f runtime, are not overwritten here, and
are not qualified by the earlier observations. The post-receiving snapshot binds
the changed paths; their next committed source needs its own receiving before
further dependent scientific work. No automatic rerun uses a moving provider.
Loaded MolSysMT native SHA-256 remains
`2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`;
its original builder/source identity remains unauthenticated.

All attempts, source/provider/native snapshots, XML outcomes, workflow files,
cold/old-reader receipts and monitored workspace/fresh committed-export checks
retain #50 custody under `.molsyssuite/interface-json-order-114-20261112/`, review
2026-11-14. Scientific cells run serially, one logical CPU/nice10/native worker,
13-GiB available reserve, 512-MiB owned-group RSS, 2-GiB address space and bounded
CPU/wall time. Final selected cells have no resource interruption; peak sampled
owned-group RSS is below 445 MB. Initial old-reader attempt 01 stopped in launcher
path resolution before a child started; corrected attempt 02 passes and both are
retained. Earlier focused controls remain exploratory, outside the final count.

Local acceptance requires Ruff/format, report indexes, proposal/reference checks,
shared noarch resources and Conda release contract on both final workspace and
fresh committed source. Exact receipts retain each result; `[skip ci]` supplies
no hosted evidence. Public resolution is synchronized after the source push.
#112 stays open for the remaining exact PeptideMT P controls and MolSysSuite #195
shared/consumer disposition. Regional H-R1 is conditional. PISA T0/T1 stays deferred
optional interoperability; #111/#30, broader chemical profiles and installed/
public/platform qualification retain their separate gates. PyUnitWizard #156 and
PharmacophoreMT #202 remain owner issues rather than hidden consumer workarounds.
