# PDB reader connectivity policy and native alternatives

Consumer tracking: DockingMT [#33](https://github.com/uibcdf/dockingmt/issues/33)
and [#5](https://github.com/uibcdf/dockingmt/issues/5). Provider improvement:
MolSysMT [#304](https://github.com/uibcdf/molsysmt/issues/304), which requests an
explicit native alternative while preserving OpenMM. The
[executed notebook](pdb_bond_inference.ipynb),
[raw probe](data/pdb_bond_inference/probe.json) and
[reproducible command](../../devtools/probe_pdb_bond_inference.py) retain evidence.

## Diagnosed hosted failure

[CI run 37125369261](https://github.com/uibcdf/dockingmt/actions/runs/37125369261)
failed three tests in each Python 3.11–3.14 lane, with 519 passes. Local exact-source
qualification had passed 522 tests. The two original-source coverage assertions
and automatic redocking coverage assertion expected the graph obtained with
OpenMM available. The hosted Conda environment omitted that optional engine.

MolSysMT's current PDB reader attempts OpenMM inference and catches any exception,
retaining only file-declared edges if inference fails. Blocking only OpenMM imports
in the existing development environment reproduces the hosted results, without
changing Python, pandas, NumPy or the inputs. Thus the different pandas versions
are not needed to reproduce this failure. No package-build experiment or claim
about unrelated pandas behavior is implied.

| Unmodified source | Explicit-only edges | OpenMM edges | Explicit-only coverage |
| --- | ---: | ---: | --- |
| 181L / all | 13 | 1,322 | 162 incomplete; 140 unassessed |
| Original 1IEP hydrogenated PDB | 0 | 4,469 | 274 incomplete |

The reason is `incomplete_stored_connectivity`; supported heavy-atom inventories
remain assessed. The provider coverage tool correctly evaluates the stored graph.
The earlier [residue-coverage record](receptor_coverage_consumption.md) describes
an OpenMM-assisted reader profile, not explicit-only parsing. Its input files,
notebook outputs and performance samples are preserved as dated evidence.

The current native handler route supports an explicit-only request:

```python
handler = msm.convert(path, to_form='molsysmt.PDBFileHandler')
try:
    source = msm.convert(handler, to_form='molsysmt.MolSys', get_missing_bonds=False)
finally:
    handler.close()
```

Direct `msm.convert(path, to_form='molsysmt.MolSys', get_missing_bonds=False)`
currently discards the flag and infers bonds when OpenMM is available. Propagation
of the policy through the direct file converter and meaningful engine-failure
diagnostics are requested in #304. The handler control uses public provider APIs;
DockingMT adds no parser or connectivity algorithm.

## Existing native foundation and unresolved differences

Public `build.get_missing_bonds(engine='MolSysMT', pbc=False)` already combines
native residue templates and geometry. The probe calls it with OpenMM imports
blocked, retains its candidates and stdout, and applies no bonds. Source
coordinates, edges, names, elements and IDs are checked rather than round-tripped
through another chemistry engine.

| Selected input | Native candidate graph | OpenMM comparison | Native-only / OpenMM-only edges |
| --- | ---: | ---: | ---: |
| 181L protein, 1,289 atoms | 1,309 | 1,309 | 0 / 0 |
| Original 1IEP, 4,412 atoms | 4,455 | 4,469 | 2 / 16 |

The graph column includes existing explicit edges plus returned candidates.
Exact edge sets agree for 181L; equal counts alone would not establish agreement.
The 1IEP call emits 224 stdout warning lines, all retained in the raw record.
Their template/naming and geometric fallback behavior, plus the 18 differing
pairs, require provider investigation. OpenMM is a comparison engine, not
independent chemical ground truth. These calls do not qualify native inference
for arbitrary ligands, modified residues, metals or polymer boundaries.

The comparison selects protein atom indices once on the OpenMM-derived source
and reuses those explicit indices on the explicit-only system. Connectivity can
change molecule membership: evaluating the same molecule selection independently
on both graphs can change or empty the population. Pair differences use the
extracted selection's atom axis; the complete selected-to-source index map is
retained in the raw probe. No new correspondence method is invented here.

## Consumer correction and provider ownership

The shared Conda test environment now declares OpenMM because the existing
reference assertions exercise OpenMM-assisted PDB reading. CI and the full matrix
use that same environment. Two new real-source controls verify explicit-only
graphs with inference disabled and with the engine unavailable; they assert
absent connectivity remains incomplete while supported heavy-atom inventories
remain assessed. The blocked-import control checks that the actual provider
attempt occurred, even if OpenMM had been imported earlier in the test session.

OpenMM is a test-profile dependency, not a new DockingMT runtime requirement.
Default preparation and the provisional Vina safeguard are unchanged. This is
an explicit qualification of the existing reader profile. Its dependence can
be reviewed when #304 delivers a qualified selectable native profile; removal
requires requalifying reference graphs and preserving the OpenMM comparison path.

The proposal favors exact local templates and existing reusable native tools,
with explicit file bonds, polymer-boundary rules, geometric limitations, identities,
state/frame selection, and evidence provenance. It keeps unsupported chemistry
unassessed and calls for cold/warm performance and memory measurements. No new
provider API is assumed implemented, and no provider checkout is edited.

## Reproduction and limits

Use `molsyssuite@uibcdf_3.14` (Python 3.14.7, OpenMM 8.6.1, Vina 1.2.7), editable
DockingMT and a read-only provider archive of
`e8e4fff22d0df0d26a3b91d80ea5a85c04981aef` on `PYTHONPATH`:

```bash
python devtools/probe_pdb_bond_inference.py
pytest --receptor=llm tests/test_receptor_coverage_consumption.py \
  tests/test_governance_baseline.py tests/test_redocking.py
python -m jupyter nbconvert --to notebook --execute --inplace \
  devguide/validation/pdb_bond_inference.ipynb
```

The probe records interpreter/import path, software versions, implementation
digests, original file hashes, source atom maps, full pair differences and native
stdout. It performs one candidate call per source and makes no timing, peak-memory,
bond-order, protonation, force-field or docking-readiness claim. The refreshed
suite inventory was inspected and all concurrent sibling work was preserved.

## Local gate (2026-10-03)

All 524 tests pass without skips in 83.83 s against the exact provider archive,
including both new explicit-only controls and real Vina redocking. Twelve existing
provider warnings remain: eleven legacy H5MSM input warnings and one occupancy-loss
warning during concatenation. The focused cohort passes 17 tests in 23.67 s.
All three notebook code cells execute successfully; Ruff lint/formatting, generated
report indexes and diff checks pass. Hosted results are separate from this local gate.
