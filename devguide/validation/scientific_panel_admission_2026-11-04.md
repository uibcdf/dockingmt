# Two-candidate source admission: first observations — 2026-11-04

Owner: [DockingMT #33](https://github.com/uibcdf/dockingmt/issues/33), with
[#49](https://github.com/uibcdf/dockingmt/issues/49) owning molecular delegation.
Continuation of the [panel design](scientific_panel_design_2026-11-04.md) at
`86ac5724ac70870d3892e8ef7b0be71afb1fee9a`.

**Source inspection completed; zero cases admitted for search.** MolSysMT read
both representations of each entry, inspected native data and built assembly 1.
No chemical completion, H addition, docking preparation, scoring, RMSD or search
was executed. Observed ligand geometry is not an admitted chemical state.

**Continuation:** the [environment/template checkpoint](scientific_panel_environment_2026-11-04.md)
records additional provider-only spatial queries, nearby waters, other BTN copies
and terminal/OXT prerequisites. It supersedes none of the original observations;
template support is now proposed in MolSysMT #557, with zero cases still admitted.

## Reproducible records and ownership

The [manifest](data/panel_admission_2026-11-04/manifest.json) binds the
[case-specific producer](data/panel_admission_2026-11-04/inspect_sources.py),
[molecular observations](data/panel_admission_2026-11-04/observations.json.gz),
four acquired files and both execution attempts. The producer only orchestrates
public MolSysMT download, conversion, get, readiness, missing-atom/residue and
assembly operations. Its JSON encoder and file hashing are administrative work;
there is no local molecular parser, classifier, graph or geometry algorithm.

The source-inspection note and correction precede the completed continuation.
The initial attempt stopped after acquiring/converting 1HSG PDB: the consumer
encoder interpreted the plain chain label `A` as a quantity. The correction
serializes labels first and reuses the exact acquired bytes through a supplied
hash ledger. There were four total source acquisition calls, not five. This was
an administrative retry, not an outcome-selected molecular run. The final
producer exits 0; its observed provider operations return without errors/warnings.

Exact local installed-composition identities and original logs are retained in
the local receipt; the public observation file deliberately omits that metadata
and retains its original receipt digest. The source context is MolSysMT
`00abb958fb93649131d5ce5fe5e12e90cf4900e9`. Static current-main comparison uses
`8b6e6d10ef0eb1ed9b738081e24fbadbca2a6e03`, without adopting or qualifying it.
The provider checkout remained clean, 91 commits behind fetched main, preserved
at `71fbe4f46d3c70e4e973c8025f01752a8c9b1084`. No environment was modified;
the selected ordinary-installed prefix passed dependency closure before execution.

## Acquired input identity

Each linked gzip contains the exact downloaded bytes; gzip compression has a
fixed timestamp. The manifest records compressed and original-content SHA-256.
Sources are [RCSB 1HSG](https://www.rcsb.org/structure/1HSG) and
[RCSB 1STP](https://www.rcsb.org/structure/1STP), acquired on 2026-11-04 through
MolSysMT from the RCSB download URLs recorded in the observations. PDB entry DOIs:
[1HSG](https://doi.org/10.2210/pdb1HSG/pdb) and
[1STP](https://doi.org/10.2210/pdb1STP/pdb). Entry/CCD revision and final template
attribution remain admission work; acquisition date does not establish revision.

| Input | Original bytes | SHA-256 of original bytes |
| --- | ---: | --- |
| [1HSG PDB](data/panel_admission_2026-11-04/1HSG.pdb.gz) | 168075 | `d430675c358060808ef614002cfdcfcfa824714d89f1240adf5749d2ba60fed2` |
| [1HSG CIF](data/panel_admission_2026-11-04/1HSG.cif.gz) | 212124 | `d2ba73b5c4be05c45275571bbb4dd042347927f91c6c05038c0df5d1ce23c268` |
| [1STP PDB](data/panel_admission_2026-11-04/1STP.pdb.gz) | 117855 | `6fbb3d5c324e717fe7284703426e74ea58191431720daab1b2faa0bbb6430f30` |
| [1STP CIF](data/panel_admission_2026-11-04/1STP.cif.gz) | 148195 | `36be77b9722ebb9f603b27bf16cbc30057f87ab9923a2d2adab0eadbdb30c30f` |

## Returned molecular observations

| Provider observation | 1HSG/MK1 | 1STP/BTN |
| --- | --- | --- |
| Asymmetric-unit atoms / groups / structures | 1686 / 326 / 1 in both representations | 1001 / 206 / 1 in both representations |
| Group inventory | 198 standard amino acids, one small molecule, 127 waters | 121 standard amino acids, one small molecule, 84 waters |
| Observed ligand source axis | 45 non-H atoms; group index 198, author group ID 902 | 16 non-H atoms; group index 121, author group ID 300 |
| Assembly 1 | Identity operation; 1686 atoms / 326 groups / one structure | Four operations; 4004 atoms / 824 groups / one structure |
| Missing standard heavy atoms | Empty report for both representations | Empty report for both representations |
| Missing residues, PDB reference-sequence query | Empty report | At protein-chain insertion position 0: 12 residues; after position 121: 26 residues |
| PDB raw alternate-location query | False | False |
| PDB occupancy | 1686 values, all 1.0 | 1001 values; 930 equal 1.0, 71 non-unit, minimum 0.42 |
| CIF native occupancy | `None` | `None` |

Ligand axes and atom names/elements come from public provider queries. Their
counts do not prove CCD completeness, chemical equivalence or a cross-format map.
PDB author chain labels can repeat across protein/ligand/water chain segments;
CIF uses distinct label-chain IDs and retains author labels as chain names.
For example, MK1 is author chain B but CIF label chain C; BTN is author A but
CIF label B. These are separate provider axes. Total chain-segment counts are
4/5 for 1HSG PDB/CIF and 2/3 for 1STP; assembly 1 of 1STP has 8/12 segments.
They are not protein oligomer counts. No positional chain/atom map is invented.

The empty missing-heavy report checks supported standard residue templates;
it does not validate the ligand or certify a complete binding environment.
The missing-residue PDB query uses its provider's internal default conversion,
separately from the explicit-only native graph. Terminal insertion positions are
sequence-comparison output, not measured coordinates or proof of safe truncation.
The full missing-residue names remain in the observations.

The native PDB conversions request `get_missing_bonds=False`: 49/17 total stored
bonds for 1HSG/1STP. The separate existing CIF reader returns 1589/940 total bonds;
its policy is not explicit-only. Selected MK1/BTN readiness reports contain 49/17
incident bonds in either representation, but declared connectivity stays partial.
CIF supplies selected ligand bond-order coverage; formal charges, atom stereo
and H declarations remain absent. Its aromatic coverage is partial/missing for
MK1/BTN. PDB lacks bond-order coverage as well. The report's `n_atoms` describes
the entire source axis; its selected `atom_indices` contain 45/16 atoms.

No CIP calculation or complete chemical-readiness claim follows. Use the existing
explicit provider template/assessment/application tools for the next hypothesis;
do not fill missing charge, stereo or H fields in DockingMT.

## Provider finding and interim boundary

[MolSysMT #556](https://github.com/uibcdf/molsysmt/issues/556) reports missing
native CIF occupancy. Inspected source reads occupancy for alternate-site choice
but omits it from the final structure append; that file is unchanged at the
separately inspected main. This supports the suspected cause, not execution of
the latest source. The issue requests primary-site/alternate/selected-axis
preservation with independent controls. No downstream atom-site parser, copied
PDB occupancy vector, zero/default fill or provider edit is introduced.

Occupancy on the affected CIF route remains unavailable. The PDB path preserves
observations for source review, but switching its graph or carrying metadata
between formats requires an explicit provider-supported map and admission.
The existing general plausibility proposal #555 remains a separate assessment
question. No new missing assembly capability was found in this operation.

## Next admission decisions

1. Freeze source/CCD revisions and reference chemistry, then declare ligand states
   and stereo plus receptor residue/terminus states. For 1HSG this includes the
   catalytic-site hypothesis; for 1STP it includes the consequence of the observed
   terminal truncations. Research/model choices need case-specific justification.
2. Select exact protein assembly and one ligand instance through provider axes.
   For the 1STP tetramer, classify the other generated ligand instances explicitly;
   symmetry copies are not independent cases. Review retained/excluded waters
   and occupants with provider queries before adopting a dry model.
3. Assess and apply the declared templates through MolSysMT, preserve observed
   geometry/source maps, and resolve missing metadata or provider refusal. Only
   then select explicit cuts, named H/charge/type methods and export/readback.
4. Register the final admitted cases/software/matrix/resource record before any
   of the proposed searches. This first inspection admits no execution row.

Source byte hashes and count/chain/group inventories were unchanged after queries
and assembly construction. This is not a full coordinate/chemical-state
immutability measurement. Resource execution finished, no worker/kernel remains,
and original evidence is retained for admission review. Administrative checks and
the existing scientific qualification remain separately attributed.
