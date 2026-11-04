# Explicit 181L receptor composition and bounded BNZ redocking

Measured on 2026-10-06 under DockingMT [#4](https://github.com/uibcdf/dockingmt/issues/4),
[#5](https://github.com/uibcdf/dockingmt/issues/5) and
[#33](https://github.com/uibcdf/dockingmt/issues/33). The
[driver](../../devtools/qualify_181l_receptor.py),
[executed evidence notebook](181l_receptor_workflow_2026-10-06.ipynb),
[original compressed evidence](data/181l_receptor/audit_2026-10-06.json.gz) and
[checkpoint](data/181l_receptor/checkpoint_2026-10-06.json) retain the exact
inputs, decisions, provider reports, maps, submitted bytes and six results.
This advances a real protein–ligand software workflow. It does not certify
protonation, environmental geometry, scoring validity or biological performance.

## Explicit molecular hypothesis

The original MolSysMT 181L PDB fixture remains unchanged, SHA-256
`77018feaaa65bb22dea47c784e8c059b0ccc09cd6dc7442b79cce83f3170985f`.
Public native PDB conversion uses the existing default reader profile with
OpenMM installed. This slice does not qualify selectable native inference or
repair the reader-policy provenance gap in MolSysMT #304.

The chosen frame is zero; the receptor selects only protein and the partner is
the original six-carbon BNZ. All observed waters and remaining nonprotein
components are excluded. This is a declared hypothesis, without an assessment
of those waters' role or a constructed biological assembly. The record retains
the complete original source snapshot and full-system atom selections.

The experimental receptor has 1,289 heavy atoms and 162 residues. Bounded exact
heavy-atom residue coverage from the earlier
[coverage audit](receptor_coverage_consumption.md) did not establish complete
terminal chemistry, H inventory or protonation. The public peptide factory
requires an additional OXT at residue/group index 161. Its generated template
has 1,290 heavy atoms. An explicit fixture map uses `(selected group index,
atom name)`, requiring unique keys and exhaustive source/template coverage;
it is not a reusable atom matcher.

| Decision | Executed choice | Scientific limit |
| --- | --- | --- |
| Histidine | Original HIS at group index 30 declared HIE | No environmental protonation prediction; HID/HIP alternatives are untested. |
| Other residues | Explicit standard factory state for each observed residue | No pH-based selection or ensemble. |
| N/C termini | Ammonium / carboxylate | Caller hypothesis; pH is `None`. |
| Disulfides | None; this selected sequence contains no cysteine | No sulfur-distance perception. |
| OXT repair | Public native `add_missing_terminal_cappings` with no ACE/NME | Generated geometry, without experimental OXT or refinement. |
| Missing H | Fixed chemical state, explicit RDKit through MolSysMT | Local placement, without molecular-environment optimization. |
| Charges | `gasteiger_marsili` | Executed named model, without universal scoring qualification. |
| Types | `autodock4`, `chemical_environment@1` | Experimental bounded provider model. |
| Ligand | Explicit benzene template, fixed-state H, named charges/types, rigid | One symmetric small ligand. |

All preparation operations use public MolSysMT tools. The factory retains its
own curated reference identity, digests, producer software and attribution; no
Meeko runtime import, local chemical assignment or manual completeness flag is
introduced. Template application retains the source group name HIS while the
declared HIE state is explicit in the factory and workflow records. Names alone
do not identify the chosen protonation state.

## Preservation and export boundary

Native terminal completion supplies only the missing OXT for this fixture;
the driver requires this observed inventory before continuing. Existing IDs and
coordinates are preserved through repair, template application, H generation
and preparation. The record retains original-to-repaired indices, reverse
full-source correspondence with `None` for generated OXT, template mapping,
generated-H parent maps, and retained/prepared/written charge/type maps. Heavy
coordinates agree within `1e-12 nm`, including under a pm/fs application policy
that retains its charge and other dimensional standards. The source is unchanged.

Repair explicitly drops B-factors and occupancies with the provider diagnostic.
This is authorized attribute loss recorded in the evidence, not a preservation
claim. Fixed-state H addition then uses `attribute_policy='strict'`.

H generation adds 1,313 atoms, yielding 2,603 evaluated receptor atoms. It uses
names such as `H1291`, which exceed PDBQT's four-character atom-name field. The
driver explicitly renames generated H through public `msm.set` before binding
charges/types: `H` plus three uppercase hexadecimal digits of the expanded
zero-based atom index. Every original/new name, atom ID and index is saved.
Original observed names/IDs remain unchanged; hydrogen-generation history keeps
the original producer report and operation domain.

DockingMT [#44](https://github.com/uibcdf/dockingmt/issues/44) fixes the discovered
receptor writer defect: empty/overwide names now raise an actionable argument
error, matching the ligand writer's constraint, instead of shifting coordinate
columns and reaching Vina as malformed bytes. Valid existing receptor formatting
is preserved. There is no automatic rename or truncation in preparation/export.
General provider export/name transformation remains under MolSysMT #223.

The current polar-H projection retains 1,615 receptor atoms (325 HD); 988 H
charges are transferred to their retained parents. Named charges total +8 e
before and after projection within `1e-8 e`. Three-decimal PDBQT charges total
7.943 e, a -0.057 e precision loss retained in the public charge audit; no
renormalization is performed. BNZ evaluates 12 atoms and retains six aromatic
carbons with conserved zero net charge. Provider #223 still owns replacement
of this temporary consumer projection/export policy.

Unprepared receptor typing and fixed-state H calls remain negative controls.
They fail on incomplete/undeclared chemistry rather than receiving inferred
neutral charges or a completeness flag. The successful named route removes
known provisional reasons, while `assess_preparation` remains scientifically
`unassessed`. Default Vina can execute without provisional opt-in.

## Bounded search observations

Each run uses Vina 1.2.7, scoring `vina`, one CPU, five requested poses, a 3 kcal/mol
energy range and the observed ligand bounds plus 8 angstrom padding. The same
prepared receptor and ligand bytes are captured in all six saved results. The
workflow decisions, provider charge/type reports, maps and assessments survive
result JSON recovery. Public `evaluate_redocking` verifies original ligand atom
keys in the shared receptor frame, without alignment or symmetry correction.
The declared recovery cutoff is 2.5 angstrom.

| Exhaustiveness | Seed | Returned poses | First RMSD (angstrom) | Closest RMSD (angstrom) | Top-1 recovered |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 7 | 2 | 2.1078 | 2.0724 | yes |
| 1 | 42 | 1 | 2.2916 | 2.2916 | yes |
| 1 | 2026 | 3 | 2.7144 | 2.3537 | no |
| 8 | 7 | 4 | 2.2856 | 2.0026 | yes |
| 8 | 42 | 5 | 2.1016 | 1.9806 | yes |
| 8 | 2026 | 5 | 2.1091 | 1.9372 | yes |

All six have a recovered pose within the returned top five; five have a recovered
first pose. The first scores range from -5.494 to -5.474 kcal/mol. These are
observations for one declared preparation, not success probabilities or affinity
validation. A low-exhaustiveness top-1 failure is retained, not filtered out.
The larger search settings do not establish convergence. Benzene symmetry can
affect positional RMSD; provider #310 owns chemically constrained symmetry
correspondence. This slice does not claim symmetry-corrected recovery.

The historical [exploratory 181L baseline](181l_redocking_exploratory.md) remains
unchanged. Its provisional input bytes and observed results belong to that
earlier protocol/provider/preparation; no scientific before/after improvement is
inferred from different inputs. New results are individually serialized, not
silently substituted into that historical manifest.

## Reproduce and assess limits

Use Python 3.14 in `molsyssuite@uibcdf_3.14`, editable DockingMT, released-tag
ArgDigest `1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e` and the existing qualified
viewer `ec4c71e574d798b7c8675b7e7e983da878ce9889`. MolSysMT is a read-only archive
of `5bd893c85fe8d211663b2b1f865f5f1d2c382a90`, selected with `PYTHONPATH`, with
the preserved native extension copied into that archive. The extension digest
is retained without a fresh-build provenance claim. The live provider worktree
at `8ae160fc93ed5bc815bcc24b37c2875ba735623d` was inspected and preserved; no
latest-provider compatibility claim is made. Existing CI source pins are unchanged.

```bash
python -m devtools.qualify_181l_receptor --output /tmp/181l-audit.json.gz
python -m pytest --receptor=llm tests/test_181l_receptor_workflow.py tests/test_preparation.py
```

The gzip archive retains finite original JSON, with compressed and uncompressed
digests in the checkpoint. The notebook reads that original evidence, verifies
its digests/source identities, and independently re-evaluates a recovered result
under pm/fs with an explicitly converted 250 pm cutoff and `1e-12 angstrom`
absolute RMSD comparison tolerance. It does not claim to
rerun all six engine searches. Native objects must be supplied explicitly for
problem reconstruction; saved result recovery/evaluation is not a claim that
the prepared molecular objects have a complete standalone public codec.

Provider environmental H refinement remains MolSysMT
[#323](https://github.com/uibcdf/molsysmt/issues/323); provider export remains
[#223](https://github.com/uibcdf/molsysmt/issues/223). The unexecuted protonation/
water alternatives, additional receptors/ligands, scoring compatibility, clean
installed artifacts and hosted/Python-minor gates remain owning consumer work.
Issues #4/#5/#33 stay partial. This is controlled local source evidence, with the
prior host dependency-closure and synchronized-guide limitations unchanged.

## Final local gate — 2026-10-07

All **985 tests pass without skips in 338.86 seconds** on the stated Python
3.14 source profile. The 171 retained warnings include the known source/legacy
fixture diagnostics and the two new explicit structural-attribute-loss warnings
from the real workflow controls. The first full attempt had 983 passes and two
test/reporting failures: strict float equality after unit conversion (measured
difference `4.44e-16 angstrom`) and an index changed during execution. The final
RMSD assertion uses `1e-12 angstrom` absolute tolerance with every nonnumeric
identity/criterion field exact; indexes were frozen before the successful rerun.
An earlier focused assertion used 2500 pm for an intended 2.5 angstrom cutoff;
it was corrected to 250 pm. No production unit policy or scientific cutoff was
relaxed. Earlier attempts remain in the checkpoint.

Ruff lint and formatting pass for 122 Python files; six notebook code cells
execute on the explicit 3.14 kernel. Original compressed/uncompressed evidence,
consumer/test hashes, local links, report indexes and current component-guide
routes are checked. Existing synchronized SMonitor/ArgDigest drift is unchanged,
tracked by DockingMT #19/MolSysSuite #106. Writer #44 is locally resolved and its
[record archived](../archive/receptor_pdbqt_atom_name_overflow.md). Source commits
remain local, with no new hosted, installed-artifact or public-admission claim.
