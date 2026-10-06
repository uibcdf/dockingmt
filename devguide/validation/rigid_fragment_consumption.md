# Consuming MolSysMT rigid fragments

The original 2026-10-03 qualification is retained below. The subsequent
[explicit policy adoption](explicit_torsion_policy.md) removes local chemical
eligibility and preserves the original byte hashes/maps. Retained-axis
connectivity stays separately tracked in MolSysMT #348.

DockingMT now delegates the final rigid-fragment partition to
`msm.topology.get_rigid_fragments`. Issues [#6](https://github.com/uibcdf/dockingmt/issues/6)
and [#33](https://github.com/uibcdf/dockingmt/issues/33) own this migration.
The [executed notebook](rigid_fragment_consumption.ipynb) retains the four-case
comparison and explicit atom maps. This qualifies software correspondence for
selected cuts; charges, types and automatic chemical torsion eligibility remain
unqualified.

## Contract and ownership

The provider receives the complete selected ligand before hydrogen projection,
with `chemical_state='structure', structure_indices=0`. DockingMT translates
selected atom pairs to bond identifiers obtained through public `msm.get`.
It projects the provider's source-index memberships onto its retained atom axis,
then chooses ROOT and branch orientation. Partitioning makes no molecular copy.
Sorting projected memberships by retained index preserves ROOT tie breaking,
branch endpoints and serialization order even for a nonmonotonic retained axis.

Partial or unavailable connectivity fails at the provider boundary. DockingMT
propagates that diagnostic without computing a fallback partition. PDBQT's
BRANCH records alone cannot qualify a complete chemical graph for this operation.
The existing local checks for connected retained atoms and individually eligible
cuts remain temporary. In particular, amide, terminal, hydrogen, ring and single
bond controls have not been replaced by a provider chemical policy.

## Retained comparisons

The [pre-migration fixture](data/fragments/legacy_trees.json) was captured from
DockingMT `be39d74b5d437b958d0dde16e284453ecc7eef28` before changing the partition.
It retains original SDF/reference PDBQT digests, active atom pairs, retained atom
indices, PDBQT permutations and generated PDBQT byte digests. These bytes reflect
the existing provisional preparation; they are not scientific ground truth.

| Ligand | Selected branches | Retained atoms | Migration comparison |
| --- | ---: | ---: | --- |
| 1IEP | 7 | 40 | Exact prior permutation and PDBQT bytes; eight reference fragments. |
| 1S63 | 6 | 29 | Exact prior permutation and PDBQT bytes; seven mapped reference fragments. |
| 5X72 P59 | 2 | 25 | Exact prior permutation and PDBQT bytes; three reference fragments. |
| 5X72 P69 | 2 | 25 | Exact prior permutation and PDBQT bytes; three reference fragments. |

The independent reference comparison matches atoms uniquely by element and
coordinates within 0.002 angstrom, then compares undirected cuts and fragment
memberships. The reference-only 1S63 hydrogen is explicitly omitted from that
source-index comparison, as in the existing matrix. Its aryl–nitrile cut remains
explicitly selected; no RDKit Strict default replaces it. Original 1IEP/1S63 SDF
dialects still use the existing RDKit-to-MolSysMT bridge pending MolSysMT #215.

`tests/test_rigid_fragment_consumption.py` covers all four before/after cases,
public provider consumption, unchanged source coordinates/bonds/IDs, nonmonotonic
retained axes, ROOT ties, invalid selected cuts, incomplete graph rejection and
a complete structure-assigned state with a partial reference state. Existing
flexible-ligand tests retain the chemical eligibility controls and optional real
Vina execution. The source provider is `bd65456e0` (test/documentation continuation
of `eb0549b50`); the consumed partition implementation is unchanged between them.

Development now uses `molsyssuite@uibcdf_3.14`, Python 3.14.7, with this checkout
installed editable via `python -m pip install --no-deps --editable .`. After the
maintainer installed Vina 1.2.7, the 43 fragment, flexible-ligand and native-format
tests pass without skips in 30.37 s, including real Vina execution and pose mapping.
The preceding implementation's
[hosted CI](https://github.com/uibcdf/dockingmt/actions/runs/37114604512) passed
all four required Python jobs; that is separate from this migration's evidence.

## Remaining removal conditions

The final local fragment partition has been retired. Chemical eligibility remains
under MolSysMT #224 and DockingMT #17; selected cuts and ROOT decisions stay in
DockingMT. Temporary PDBQT writers, atom parsers and chemical preparation heuristics
retain their [separate qualification conditions](native_molsysmt_formats.md).
Issues #6 and #33 therefore remain partial.

## Complete local gate (2026-10-03)

All 507 tests pass without skips in 72.62 s on Python 3.14.7 with Vina 1.2.7.
The twelve existing provider warnings concern legacy H5MSM input (eleven) and
occupancy loss on concatenation (one). Ruff lint, formatting (86 Python files),
generated report indexes and diff checks pass. All four notebook code cells
execute on the same interpreter; Vina accepts the four generated ligand inputs.
