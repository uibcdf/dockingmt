# Consuming exact receptor residue coverage

DockingMT receptor preparation consumes public
`msm.build.get_residue_chemical_coverage`, delivered by MolSysMT
[#218](https://github.com/uibcdf/molsysmt/issues/218). Consumer preparation remains
owned by DockingMT [#5](https://github.com/uibcdf/dockingmt/issues/5) and
[#33](https://github.com/uibcdf/dockingmt/issues/33). The
[executed notebook](receptor_coverage_consumption.ipynb),
[case evidence](data/receptor_coverage/cases.json) and
[paired profile](data/receptor_coverage/profile.json) retain the observations.

## Preparation and provenance contract

`prepare_receptor` adds
`metadata['source_chemistry']['residue_coverage']` for the extracted selected
source before hydrogen projection. It requests the structure-associated chemical
state at frame zero. The compact summary retains provider schema, method and
rule version; group count and status/reason counts; heavy-atom, hydrogen,
connectivity and protonation status counts; exact template resource/digest/usage;
unassessed checks; and software identity. It excludes per-group atom/bond indices,
hydrogen candidates and diagnostic arrays. Reason counts count group occurrences;
one group can have several reasons. Template digests identify packaged reference
resources, not a chemical qualification of that reference or the receptor.

The combined provider report includes stored chemical readiness, which DockingMT
reuses rather than requesting a second audit. Ligand preparation continues using
the stored-field audit. Group-free receptors retain their existing preparation
behavior and explicitly report `status='unassessed', reason_code='no_group_domain'`;
no residue hierarchy or chemical template is invented. Other provider failures
propagate rather than triggering a local audit.

The group axis belongs to the extracted selected source, not the original full
input, retained atoms or PDBQT ordering. To locate a specific residue or inspect H
candidates, call the public provider on that same source with the same state/frame.
Numeric provider selection denotes groups; atom selection belongs to the earlier
DockingMT extraction. Inter-group chemistry, bonds outside the original selection
and terminal context are not certified by this summary.

## Original-source observations

| Source / selection | Source atoms | Groups | Assessed | Incomplete | Unassessed |
| --- | ---: | ---: | ---: | ---: | ---: |
| 181L / all | 1,441 | 302 | 162 | 0 | 140 |
| 181L / protein | 1,289 | 162 | 162 | 0 | 0 |
| Original 1IEP hydrogenated PDB / protein (also all) | 4,412 | 274 | 274 | 0 | 0 |

181L's remaining groups include waters and benzene; they have no exact supported
residue template. All groups in both original sources have unassessed H inventory
and environmental protonation. An `assessed` group means that the bounded exact
comparison ran, not that its molecular preparation is complete or scientifically
valid. Standard residue H variants remain ambiguous; their candidate inventories
are available only in the full provider report.

The original 1IEP PDB is retained unchanged alongside the Vina fixtures, from
upstream commit `3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645`; its
[fixture record](../../tests/data/vina_torsions/README.md) declares source path,
license and SHA-256. This is the 4,412-atom PDB, not the prepared 2,702-atom PDBQT.
Its public residue audit succeeds, but current receptor preparation still rejects
hydrogens without exactly one explicit heavy-atom attachment. The previous
[1IEP preparation audit](1iep_preparation_audit.md) documents the two missing H
bonds and a separate explicit provider-assisted repair. This qualification applies
no repair to the original input. Assessed heavy-atom coverage cannot override this
preparation failure or establish H completeness.

Controlled sources distinguish a complete ALA from ALA lacking CB, exact MSE/SEP
from their parent amino acids, and unknown PTR/water/zinc from incomplete supported
residues. MSE keeps Se and its exact template; no MET sulfur substitution is made.
MSE/SEP heavy-only templates leave hydrogen assessment unassessed. Their coverage
does not extend the current writer's element support: Se and Zn preparation still
fail clearly. Coordinates in these artificial cases are software fixtures, not
conformers for scientific validation.

## Unchanged chemical admission

No atoms, bonds, formal/partial charges, protonation states or AutoDock types are
assigned. `force_field_coverage`, repair/placement, valence and docking readiness
remain explicitly unassessed. Current native preparation still has zero-placeholder
charges and heuristic atom types. Vina rejects these preparations by default;
explicit exploratory opt-in remains provisional. Existing real-engine tests retain
this safeguard and now verify coverage persistence for both automatically prepared
and supplied receptors through saved-result serialization. External prepared
PDBQT admission remains unassessed. #5 and #33 remain partial.

## Exact-source qualification and reproduction

MolSysMT source: `e8e4fff22d0df0d26a3b91d80ea5a85c04981aef`. CI and full-matrix
workflows pin it for all four Python lanes, preserving the existing ArgDigest and
viewer source routes. This is controlled-source consumer qualification, not
installed-wheel or published dependency-floor admission. The provider's installed
version metadata is stale; the retained source commit, import path and two
implementation SHA-256 digests identify the code actually exercised.

The refreshed suite inventory was inspected and all sibling dirty/ahead/behind
work preserved. A read-only `git archive` of the exact provider source under `/tmp`
was selected with `PYTHONPATH`, without changing the provider checkout or its
installed distribution. Development uses `molsyssuite@uibcdf_3.14`, Python 3.14.7,
Vina 1.2.7 and editable DockingMT.

From this checkout, with the exact provider snapshot on `PYTHONPATH`:

```bash
conda run --no-capture-output -n molsyssuite@uibcdf_3.14 \
  pytest --receptor=llm tests/test_receptor_coverage_consumption.py \
  tests/test_chemical_readiness_consumption.py tests/test_preparation.py \
  tests/test_redocking.py tests/test_engines.py tests/test_governance_baseline.py
conda run --no-capture-output -n molsyssuite@uibcdf_3.14 \
  python -m jupyter nbconvert --to notebook --execute --inplace \
  devguide/validation/receptor_coverage_consumption.ipynb
```

The eight new consumer cases cover original source bytes/counts, pre-projection
axes, reuse of the provider audit, unsupported/modified/incomplete chemistry,
structure-associated states, non-default units, detached/read-only JSON summaries,
group-free systems and provider failure propagation. The focused cohorts pass
22 and 17 tests respectively; the latter includes real Vina execution.

## Measured local cost

Five paired rounds alternate profile order after warming both paths and templates.
Both profiles use the current provider and preparation implementation. The baseline
requests only stored-field evidence; the new profile requests residue coverage and
reuses its embedded stored-field report. Conversion from PDB is excluded.

| Operation | Stored-field median | Residue-coverage median | Extra JSON bytes |
| --- | ---: | ---: | ---: |
| Complete 181L protein preparation | 168.15 ms | 365.58 ms | 4,006 |
| Original 1IEP source assessment only | 33.73 ms | 390.98 ms | 4,183 |

The 1IEP measurement excludes preparation, which fails on the unmodified source;
it cannot be compared directly with complete 181L preparation. The 181L PDBQT bytes
and stored-field summary are identical between profiles. The additional time is
measured provider comparison cost, not inferred from metadata size. These small
samples with uncontrolled OS caches/load are not a general timing or peak-memory
claim. The result establishes a follow-up measurement point for
[#28](https://github.com/uibcdf/dockingmt/issues/28) and provider #218, without a new
local molecular audit, campaign cache or benchmark framework.

The previous readiness-only notebook/raw profile is preserved. Its command
`devtools/profile_preparation_readiness.py` deliberately keeps that original
measurement boundary despite the new receptor keyword; the new notebook measures
the additional residue comparison separately.

## Complete local gate (2026-10-03)

All 522 tests pass without skips in 80.42 s against the exact provider snapshot
on Python 3.14.7 with Vina 1.2.7. Twelve existing warnings remain: eleven legacy
H5MSM input warnings and one occupancy-loss warning during concatenation. Ruff
lint/formatting, report indexes and diff checks pass. The notebook's five code
cells execute with the same interpreter and exact provider implementation digests.

## 2026-10-03 reader-profile correction

The subsequent [PDB inference diagnosis](pdb_bond_inference.md) establishes that
the counts and timings above use OpenMM-assisted PDB reading. Hosted CI omitted
OpenMM and returned explicit-only graphs, correctly marked incomplete by the
same coverage tool. The shared test environment now declares that reference
dependency and two additional original-source controls protect explicit-only
behavior. Original evidence is preserved. Selectable native inference, file-path
policy propagation and reader provenance are requested in MolSysMT #304.
