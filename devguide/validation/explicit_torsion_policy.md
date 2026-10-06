# Explicit ligand torsion policy

DockingMT delegates chemical eligibility to public
`msm.topology.get_rotatable_bonds` and fragment partition to
`msm.topology.get_rigid_fragments`. The named consumer policy
`explicit_docking_cuts@1` decides which **caller-selected** cuts to accept and
records provider disagreement. It chooses no automatic cuts: `None` or an empty
`active_torsion_bonds` keeps the ligand rigid and calls neither operation.
[DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17) owns this policy;
[#6](https://github.com/uibcdf/dockingmt/issues/6) owns active-cut adoption and
[MolSysMT #224](https://github.com/uibcdf/molsysmt/issues/224) owns classification.

```python
import dockingmt as dmt

prepared = dmt.prepare_ligand(
    ligand_with_declared_chemistry,
    selection='all',
    active_torsion_bonds=[(6, 7), (17, 18)],
)
selection = prepared.metadata['torsion_selection']
print(selection['policy'], selection['selected_bonds'])
```

Pairs refer to the complete selected ligand before nonpolar-H projection, after
any requested H/charge/type stages. The example pairs belong to the bounded 5X72
control; choose bonds appropriate to the actual input. Existing
`VinaProtocol(active_torsion_bonds=...)` uses the same policy during automatic
MolSysMT ligand preparation. Prepared/external PDBQT inputs keep their protocol
torsion restriction; prepare a custom ligand separately.

## Policy and compatibility

The provider receives `method='conjugation_restricted'`,
`chemical_state='structure', structure_indices=0` on the entire selected graph.
Its experimental rule is `conjugation_restricted@1`. Classifying only requested
endpoints or the H-projected graph would lose chemical context. No local
aromaticity, amide perception, ring detection or classifier fallback is used.
Missing/partial/unsupported chemistry and provider failures propagate unchanged.

| Provider result on a selected bond | DockingMT decision |
| --- | --- |
| No exclusions | Accept as `provider_candidate`. |
| Restricted conjugation on C–O/S | Accept explicit ester/thioester cut as `explicit_override`. |
| Adjacent triple bond | Accept explicitly requested axis as `explicit_override`. |
| Restricted conjugation on C–N | Reject, including amide/thioamide/amidine and tertiary amide. |
| H endpoint, nonsingle/aromatic bond, ring or terminal heavy atom | Reject. |
| Unknown exclusion | Reject. |

An exception never clears the provider mask or changes `is_rotatable=False`.
This preserves existing explicit ester and aryl–nitrile requests, including the
published 1S63 sixth branch. Adjacent internal-alkyne axes remain explicit choices;
replacement torsions or dummy atoms are not generated. Admission establishes no
energy barrier or universal flexibility. The former local C–N guard checked
carbonyl/thioamide environments only; named-policy amidine rejection is an
explicit stricter behavior for previously unqualified chemistry. Tertiary-amide
symmetry exceptions and automatic RDKit/Meeko equivalence are absent.

## Evidence and atom identity

Existing `torsion_policy='explicit_selected_bonds'` and selected-pair fields stay
compatible. New finite JSON `torsion_selection`, schema
`dockingmt.explicit_torsion_selection@1`, contains:

- the complete original classification, evaluated scope, state, versioned
  criteria, exclusion bits/masks, software and attribution;
- selected atom/bond positions and original IDs, decisions and provider reasons;
- retained source atom indices and exact PDBQT-to-source correspondence.

Indices and IDs are distinct. Bond positions refer to the selected, possibly
H-expanded graph supplied to the provider. Public extraction can normalize bond
rows; IDs preserve source identity. Generated/pre-stage input correspondence stays
in `preparation_workflow`. ROOT, tie breaking and branch orientation remain local
docking choices over provider fragments. Source coordinates/chemistry and caller
pairs are unchanged. Prepared/result metadata retains this evidence. PDBQT gets
no new torsion remark; original provisional reference bytes and permutations
remain exact. Named charges/types retain their separate attribution and assessment.

## Temporary retained-connectivity exception

The old per-cut chemical traversal and amide classifier are removed. One existing
local traversal checks connectivity of the actual retained inventory in the
structure-assigned graph. Public covalent-block/bond-graph operations cannot
request that state; full-graph partition followed by membership projection does
not establish induced-subset connectivity.

[MolSysMT #348](https://github.com/uibcdf/molsysmt/issues/348) owns the public
capability. The two-state control gives assigned fragment offsets `[0, 3, 6]`,
versus one reference-default block; explicit state request raises
`UnknownArgumentError`. Reference defaults are not alleged to be incorrect.
DockingMT contributors own this bounded exception, reviewed by 2027-01-06. Remove
the traversal when a public state-aware induced-connectivity operation passes
assigned-state, disconnected and nonmonotonic-subset controls. No reference state
rewriting or sibling implementation is added. PDBQT/H/charge-preserving export
remains separate under [MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223)
and DockingMT #33.

## Qualification — 2026-10-06

[Executed notebook](explicit_torsion_policy_2026-10-06.ipynb),
[helper](../../devtools/qualify_torsion_policy.py),
[raw receipt](data/torsion_policy/qualification_2026-10-06.json) and
[tests](../../tests/test_torsion_policy_consumption.py) retain original reports,
source/input/runtime hashes, source immutability and decisions. Run the helper
from the root as `python -m devtools.qualify_torsion_policy` with qualified sources.
The notebook saves only this new receipt.

The unchanged four curated ligands use the existing explicit RDKit reader bridge
for original SDF dialects; classification is native and tested with RDKit/Meeko
imports forbidden. Original branches remain 7/6/2/2 for 1IEP/1S63/5X72 P59/P69;
provider restricted candidates are 7/5/2/2. The extra 1S63 axis is a recorded
exception. Prior hashes/permutations match exactly; existing coordinate/element
tests independently compare branch/fragment identities. Published files are
comparison inputs, not chemical ground truth. Unsupported native SDF dialects
are not repaired here.

Six analytical admitted cases retain independent expected decisions; four
restricted C–N cases fail. Tests also cover formamide, H inventory, unknown
exclusions, unchanged provider exceptions, reordered bond axes, assigned states,
full-graph evidence outside selected cuts, default rigidity, named charge/type
coexistence and saved Vina pose identity.

The default Vina control automatically prepares a named/charged 5X72 ligand with
two protocol-selected cuts under pm/fs units, retains reports/maps and verifies
captured exact inputs. The helper pairs it with an unrelated external 1IEP
receptor for software testing; this is not biological redocking or affinity
evidence. Scientific assessment stays `unassessed`. Its regression test uses
the existing minimal external receptor separately.

Loaded provider bytes match MolSysMT `5bd893c85fe8d211663b2b1f865f5f1d2c382a90`.
A bounded suite-status fetch found the sibling 14 commits behind remote, with
consumed topology files unchanged through `8ae160fc9`; its worktree is preserved.
The [prior profile](data/chemical_templates/source_profile_2026-10-06.json) retains
distribution/source identities, native build-provenance limits, AmberTools host
conflicts and unchanged shared-guide drift. #42/#43 receipts/notebooks stay intact.
This is local Python 3.14 source evidence; other required interpreters, clean
installed artifacts, hosted CI, public admission and scientific qualification
remain separate.

The [local checkpoint](data/torsion_policy/checkpoint_2026-10-06.json) records
**977 passed, no skips, 271.81 s, 169 warnings**, including 25 new cases. All eight
notebook code cells execute. Ruff (120 files), report/index, changed-document
links, finite receipt/hash, editable identity, component-guide and diff checks
pass. Unchanged SMonitor/ArgDigest canonical drift remains under MolSysSuite #106.
Installed/hosted/public checkpoints are not inferred from these local gates.
