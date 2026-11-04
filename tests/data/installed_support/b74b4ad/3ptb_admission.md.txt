# Executed 3PTB molecular admission

Owning issues: [#5](https://github.com/uibcdf/dockingmt/issues/5),
[#6](https://github.com/uibcdf/dockingmt/issues/6),
[#4](https://github.com/uibcdf/dockingmt/issues/4) and
[#49](https://github.com/uibcdf/dockingmt/issues/49), all partial/open.
Executed on 2026-10-10. **Molecular preparation and native input parsing only:
zero new fixed evaluations and zero 3PTB searches.**

The [original prospective protocol](3ptb_prospective_protocol.md) remains
unchanged, including its pre-execution registration. The separately registered
[source handoff clarification](3ptb_source_handoff_2026-10-10.md) records the
unsupported compressed-input branch and the admitted plain-input boundary.
The [raw admission](data/3ptb_admission/audit_2026-10-10.json.gz),
[original producer](data/3ptb_admission/producer_2026-10-10.py.txt),
[qualification receipt](data/3ptb_admission/checkpoint_2026-10-10.json) and
[executed notebook](3ptb_admission_2026-10-10.ipynb) retain separate evidence.

## Input boundary and ownership

MolSysMT's public conversion rejects the frozen `.pdb.gz` path before reading.
That reusable capability is proposed in
[MolSysMT #385](https://github.com/uibcdf/molsysmt/issues/385). The caller restores
the original plain PDB with standard archive tooling; the admission command
authenticates its downloaded-byte SHA-256 before passing it to public MolSysMT
conversion with `get_missing_bonds=False`. This qualifies plain input only.
There is no new compressed molecular reader, atom matcher, bond inference,
valence implementation, H generator or molecular geometry algorithm downstream.
The handoff has a provider removal condition and a 2026-11-10 review date.

The original PDB contains 1701 atoms, 287 groups, one frame and 21 declared
bonds. Its protein selection has 1629 observed atoms in 223 residues and six
declared disulfide bonds. The BEN selection has the registered nine heavy names
and original atom IDs 1632–1640. OXT remains original atom ID 1629. All original
IDs and heavy coordinates survive the selected/expanded maps unchanged.
Full-source snapshots preserve the excluded waters, calcium and ligand.

The native reader returns two chain indices carrying author chain ID A across
the protein/hetero TER boundary; source selections and indices disambiguate them.
The public alternate-location getter returns `None`. An independent inventory
of column 17 in these exact frozen input bytes contains only blank alternate
locations; this is fixed-input validation, not a molecular reader. Original
occupancy and B-factor arrays are retained through public getters, with B factors
in square angstroms. No unresolved alternate is silently selected.

## Declared chemistry and models

The public peptide factory receives HID57, HIE40/HIE91, ammonium/carboxylate
termini, standard remaining states, twelve CYX residues and the six registered
disulfide pairs. Exact `(selected_group_index, atom_name)` keys bind the factory
template to all observed protein atoms. The source's six sulfur links agree
with these declarations; no distance-based disulfide classifier is used.
Template assessment accepts the existing links before explicit completion.

The ligand uses the registered benzamidinium +1 template and ordered nine-atom
map. Neutral CCD BEN remains the source reference. Public fixed-state H retains
the N1-double/N2-single declaration: two H on each amidine N and five ring H.
All six declared disulfides have no generated sulfur H; histidine N-H parents
match the chosen HID/HIE states. No repair, relaxation, pH prediction, resonance
normalization or environmental H refinement is performed.

Strict H expansion rejects retaining `b_factor` and `occupancy` across atom
expansion. The explicit public `intersection` policy succeeds and reports both
losses; the original arrays and strict exception remain in the record. No
experimental values are fabricated for generated atoms. Provider-generated
receptor H names exceed PDBQT's four-character field; an explicit public `set`
assigns four-character `H` plus hexadecimal expanded-index names. Both original
names and assignments are retained, without changing chemical identity.

| Input | Observed atoms | Generated H | Full atoms | Prepared atoms | Charge, e |
| --- | ---: | ---: | ---: | ---: | ---: |
| Dry protein receptor | 1629 | 1591 | 3220 | 2011 | +6 |
| Benzamidinium, each arm | 9 | 9 | 18 | 13 | +1 |

Public `gasteiger_marsili` assignment covers every full atom. Public `autodock4`
typing uses `chemical_environment@1`; projection retains polar H and merges
provider-declared nonpolar H charges. Both projected charge audits are consistent
to numerical precision. The ligand exports six `A`, one `C`, two `N` and four
`HD` types. Complete assignments and native parsing do not establish the
scientific suitability of these models for this receptor.

## Torsion and domain admission

The two detached ligand preparations share full geometry, H, chemistry, named
models and charges. MolSysMT's `conjugation_restricted` classifier admits only
the requested C1–C bond, selected-source pair `(0,6)`. Its rigid-fragment tool
returns fragment offsets `[0,11,18]` on the full 18-atom axis. Rigid preparation
has no cut; flexible preparation has exactly one. No automatic torsion policy
or outcome-selected ROOT change is introduced.

Written coordinates, charges, types and names match across arms after mapping
back to the provider source axis. All full-source/expanded/prepared/written maps,
projected charges and literal ROOT/BRANCH bytes are saved. Under the existing
largest-retained-fragment rule the flexible ROOT is the seven retained amidine
atoms, followed by the six-atom phenyl branch; the rigid arm starts with C1.
This representation difference is retained as part of the planned comparison,
not attributed solely to a torsional search mechanism.

Public unweighted `structure.get_center` defines the native box. Its prospective
Vina adapter center is `[-1.759111,14.461000,16.915778]` angstrom; the negative
center is `[58.240889,14.461000,16.915778]`. Both dimensions are
`[20,20,20]` angstrom. All nine reference atoms lie inside native and outside
negative, with ligand coordinates unchanged. Unrounded quantities and the
existing adapter's numerical projection are retained; **no box has been
submitted to a search**. Vina 1.2.7 accepts both prepared ligand/receptor pairs
through `set_receptor` and `set_ligand_from_string`, without calculating maps.

The receipt freezes all 24 ordered rows, their full protocol parameters and
exact receptor/ligand input SHA-256 values. Every row is `not_attempted`.
Seeds `[7,42,2026]`, efforts `[1,8]`, CPU 1, nine requested poses and
`3 kcal/mol` remain the prospective population.

## Human reproduction and qualification

The [case-specific command](../../devtools/qualify_3ptb_admission.py) composes
public APIs; the notebook replays preparation and inspects the complete saved
evidence. It follows the pilots' human Python/Jupyter workflow principle and
uses only public 3PTB inputs. No private pilot material is copied.

Use the source/runtime composition in the raw record: Python 3.14.7, Vina 1.2.7,
RDKit 2026.03.1, Pandas 2.3.3, MolSysMT
`739395d7ea31bec5c3f77cdcb1135ecf7e7c9bac`, ArgDigest
`1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e`, MolSysViewer
`ec4c71e574d798b7c8675b7e7e983da878ce9889` and PyUnitWizard
`2ab37a525ce99728ad8aee846b4a4f7acc4f1b65`. Loaded imports, advertised versions,
verified Python source digests, generated version-file digests and the actual
MolSysMT native artifact SHA-256 are retained separately. In particular, an
advertised generated version is not substituted for the verified source commit.
The consumer source base is `a812916193064c04a6e52e119d4787ca22dd19af` plus the
exact preserved admission producer and recorded source digests.

After selecting that qualified environment/source composition, explicitly stage
the original archive and call the command:

```bash
case_input=$(mktemp --suffix=.pdb)
trap 'rm -f "$case_input"' EXIT
gzip -dc devguide/validation/data/3ptb_prospective/3PTB.pdb.gz > "$case_input"
python -m devtools.qualify_3ptb_admission "$case_input" --output /tmp/3ptb-admission-replay.json.gz
```

The six new guards cover source/template maps, declared states and H parents,
explicit attribute loss, named/projection fields, both torsion arms, boxes and
population, changed-byte rejection, original saved producer identity and a real
pm/fs/degree unit-policy replay with explicit charge units. That replay forbids
native maps, scoring, optimization and docking. The notebook executes five code
cells without errors. The separate receipt records relevant existing-contract
gates; exact-head hosted follow-up is reported in the owning issues after
delivery. Administrative checks do not substitute
for scientific tests or public installed admission.

## Limits and next operation

The provider's stored-field readiness report explicitly lists unassessed checks,
including valence and protonation. Fixed-state H and named-model engines sanitize
the full declared graph under RDKit rules, but that does not supply independent
chemical certification or establish experimental states. Environmental H
refinement (#323), symmetry-aware correspondence (#310), charge unit-policy
clarification (#381) and general projected-object migration (#223) remain
provider boundaries. Preparation assessments stay `unassessed` with no
provisional reason codes; broad issues #5/#6/#4/#49 remain partial.

The next scientific step is to execute the frozen 24-row population using these
exact admitted preparations, retain every attempt and submitted input, then
evaluate all returned poses with the registered source-identity positional RMSD.
Nothing in this admission reports pose recovery, ranking, affinity or general
performance, and no PharmacophoreMT operation is required by this question.
