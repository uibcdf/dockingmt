# Consuming explicit MolSysMT chemical templates

DockingMT can consume the independent native system returned by
`msm.physchem.apply_chemical_template` through its existing `prepare_ligand`
boundary. This bounded source qualification uses MolSysMT
`c19a47ada0c2279029abfa296cf915560610ad9a`; it does not establish a published
installation floor or validated docking preparation. Work remains owned by
[DockingMT #4](https://github.com/uibcdf/dockingmt/issues/4),
[#5](https://github.com/uibcdf/dockingmt/issues/5),
[#33](https://github.com/uibcdf/dockingmt/issues/33) and
[MolSysMT #298](https://github.com/uibcdf/molsysmt/issues/298).

The [executed notebook](chemical_template_consumption.ipynb),
[raw record](data/chemical_templates/cases.json) and
[`devtools/qualify_chemical_templates.py`](../../devtools/qualify_chemical_templates.py)
retain template snapshots, checksums, exhaustive maps, indexed provider reports
and preparation summaries. Molecular construction, inspection, extraction,
conversion and template assignment use public MolSysMT tools. DockingMT does
not implement matching, aromatic normalization or chemical assignment.

## Cases and independent expectations

| Case | Application | Consumer observation |
| --- | --- | --- |
| Original 181L BNZ, six heavy atoms | Compatible with an explicitly declared heavy-only benzene SMILES template and `stored_counts` H policy | Coordinates/identities retained; six aromatic atoms, one virtual H per C; no H atoms generated; six retained PDBQT atoms. |
| 5X72 P59 absent-field control | Compatible with explicit RDKit-adapter assignments and all 39 atoms mapped in reversed order | R at original atom 7, now source atom 31; two frames, box, time and state associations preserved; 25 retained atoms. |
| 5X72 P69 absent-field control | Same bounded operation with its independently selected template | S at original atom 7, now source atom 31; same preservation and projection checks. |
| Unchanged native 5X72 SDF against adapter template | Unassessed | `aromatic_representation_requires_normalization`; application fails without changing inputs. |
| Native 5X72 SDF used as its own template | Unassessed | Required template fields remain undeclared; conversion alone is insufficient. |
| Conflicting formal charge or stereo assignment | Conflict | No overwrite; failure retains an inspectable assessment and unchanged inputs. |
| Missing stored edge | Conflict | No graph repair; missing pairs appear in the provider report. |
| Map omitting explicit H atoms | Argument failure | No inferred H correspondence or input mutation. |

The two original 5X72 SDF files remain unchanged and retain the digests and license
in [the reference inventory](../../tests/data/vina_torsions/README.md). Their
39-atom/42-bond graphs contain 24 heavy atoms and 15 explicit H atoms. The controls
are built through `MolSysBuilder` from their declared atom identities, elements,
edges and coordinates, deliberately omitting chemical assignments and assigning
one control group. An explicit reversal defines the template-to-source map.
The added second frame is translated by `[10, -7, 2]` angstrom; box and time are
preservation controls. These controls qualify transfer, not a successful repair
of the original SDF's representation mismatch or experimental conformer validity.

The template route is explicit native SDF conversion with `stereo_engine='rdkit'`
and `discard_properties=True`, followed by public native-to-RDKit-to-native
conversion. The adapter supplies aromatic and hydrogen-count declarations.
There are no direct RDKit calls in this consumer workflow. RDKit's version,
the original file digest and the actual native template snapshot digest are
separate records. The latter includes chemical states and the fixed units of
the snapshot protocol. These caller declarations identify the chosen template;
they do not authenticate its chemistry.

The 181L case extracts the original `BNZ` selection after public PDB conversion.
Its fixture-specific C1..C6 ring-order declaration supplies the map to
`smiles:c1ccccc1`, converted through MolSysMT's RDKit adapter. The raw record
retains selected full-system indices. Benzene's symmetry does not establish a
unique general matching algorithm. Its heavy-only H policy does not supply
donor-H geometry or a hydrogen-generation operation.

## Composition and provenance boundary

The existing consumer boundary is sufficient:

```python
assessment = msm.physchem.assess_chemical_template(source, **template_options)
# Inspect the detached assessment before applying the explicitly chosen template.
application = msm.physchem.apply_chemical_template(source, **template_options)
selected = msm.extract(application['molecular_system'], structure_indices=chosen_frame)
ligand = dmt.prepare_ligand(selected, selection='all')
template_report = application['report']  # Retain beside the workflow record.
```

`template_options` includes an exhaustive template-index/source-index bijection,
the actual prepared template, its provenance and hydrogen policy; it is not an
automatic preparation policy. Source/template chemical-state selection is
independent of frame selection. A regression selects state 0 while preserving
an unselected state and existing frame associations. Matching explicit fields
are preserved and only absent fields are assigned.

MolSysMT returns `molsysmt.chemical_template@1` separately. Its indexed report
is not embedded in the native system, H5MSM, `PreparedLigand`, or docking-result
provenance. DockingMT's existing stored-field summary consequently retains
unassessed origins rather than inventing template attribution. This qualification
saves the detached report as a workflow sidecar, including original producer
versions and portable attribution supplied by MolSysMT. Its numeric arrays are
converted to JSON lists; the provider's formal-charge unit and the snapshot's
explicit nm/ps units remain declared. No credit is added when inspecting saved
evidence. Native report attachment remains with MolSysMT #298.

No new DockingMT preparation arguments or automatic template selection are
needed for this slice. A future integrated workflow must retain the report and
compose public provider operations; it must not silently duplicate the provider's
chemical state or matching logic.

## Docking safeguard and units

Successful transfer provides stored formal charges, aromatic assignments and
bond multiplicities. It supplies neither a named partial-charge model nor
qualified AutoDock types. All three preparations retain `zero_placeholder`
charges and `element_aromaticity_heuristic` typing. Vina rejects them by default.
A real-engine software test explicitly opts into provisional preparation using
the minimal synthetic receptor, then checks pose production, provisional
assessment and saved-result summary persistence. Its scores are not scientific
validation evidence.

Application preserves stored source geometry exactly. Preparation's unit
standardization under a non-default pm/fs policy is compared at an absolute
tolerance of `1e-12 nm`, allowing floating-point conversion noise while protecting
the chosen translated frame and retained atom axis. The original two frames,
coordinate units, box, time and frame/state associations survive application.

## Reproduction and remaining work

Use `molsyssuite@uibcdf_3.14` with this DockingMT checkout installed editable.
To isolate the provider from unrelated local work:

```bash
mkdir -p /tmp/dockingmt-template-provider-c19a47ada0c2279029abfa296cf915560610ad9a
git -C ../molsysmt archive c19a47ada0c2279029abfa296cf915560610ad9a | tar -x -C /tmp/dockingmt-template-provider-c19a47ada0c2279029abfa296cf915560610ad9a
export PYTHONPATH=/tmp/dockingmt-template-provider-c19a47ada0c2279029abfa296cf915560610ad9a
python devtools/qualify_chemical_templates.py
pytest --receptor=llm tests/test_chemical_template_consumption.py
python -m ipykernel install --prefix=/tmp/dockingmt-template-kernel --name dockingmt-molsyssuite-314 --display-name "Python 3.14 (molsyssuite@uibcdf_3.14)"
JUPYTER_PATH=/tmp/dockingmt-template-kernel/share/jupyter python -m jupyter nbconvert --execute --inplace devguide/validation/chemical_template_consumption.ipynb
```

The command writes this slice's raw record without overwriting earlier
preparation/performance evidence. Provider import location, implementation hashes,
interpreter and executed adapter versions are retained. No speed or memory claim
is made. CI and full-matrix pins advance to the qualified provider source; shared
workflow shapes and unrelated sibling pins are preserved.

The notebook uses an explicitly selected Python 3.14 kernel and asserts the
interpreter version/environment before calculating; invoking Jupyter from a
Conda environment does not by itself select that environment's kernel.

All 14 focused consumer cases pass in 28.30 s on Python 3.14.7 with Vina 1.2.7.
Fifteen provider `FutureWarning`s arise from `ChemicalStatesDict` object-column
encoding under pandas 2.3.3; they do not change this result and are retained in the
provider feedback. Aromatic normalization, native report attachment, fixed-state
ligand hydrogen addition, charge assignment and named AutoDock typing remain
with MolSysMT #298/#300/#221/#222. DockingMT #4/#5/#33 remain partial.

## Complete local gate and live sibling boundary (2026-10-03)

The complete gate passes **538 tests without skips in 108.31 s**, with Ruff
lint/formatting (92 Python files), generated indexes and diff checks passing.
The executed notebook uses Python 3.14.7 in `molsyssuite@uibcdf_3.14`; an isolated
interpreter check confirms this DockingMT checkout is installed editable.
The full suite uses the new MolSysMT archive above plus the existing Python 3.14
CI viewer pin, `ec4c71e574d798b7c8675b7e7e983da878ce9889`, archived independently
in `/tmp/dockingmt-template-viewer-ec4c71e574d798b7c8675b7e7e983da878ce9889` and
appended to `PYTHONPATH`. No sibling checkout or installed dependency was edited.
The 27 warnings comprise fifteen typed-column `FutureWarning`s, eleven existing
legacy H5MSM warnings and one existing occupancy-drop warning.

The first full run against the live, dirty MolSysViewer checkout had 537 passing
tests and one failure in
`tests/test_redocking.py::test_redocking_benchmark_181l`: no `reference_ligand`
region was retained. The in-progress loading contract under
[MolSysViewer #151](https://github.com/uibcdf/molsysviewer/issues/151) requires
`structure_pairing='by_index'` when combining trajectories. A two-frame public
load probe reproduces the explicit `ValueError`; supplying the declared pairing
creates the reference region. The current DockingMT adapter suppresses reference
load exceptions, so this emerging incompatibility appears as a missing overlay.
The failing test passes in isolation with the unchanged CI viewer pin, before
the complete pinned-profile gate above.

This is consumer feedback for an uncommitted provider contract, not a claim of
committed viewer failure. It is cross-linked to the owning provider proposal and
DockingMT #4/#33. Future viewer adoption must qualify explicit reference frame
pairing and make failed overlay loading inspectable. That migration is separate
from template transfer; the existing viewer pins and its local work are preserved.

### Consumer loading follow-up — 2026-10-03

[DockingMT #37](https://github.com/uibcdf/dockingmt/issues/37) subsequently makes
reference pairing explicit when advertised, rejects incompatible frame counts
and propagates loading/player failures. The [viewer qualification](viewer_reference.md)
retains 706 passing tests with the stable pins and 32 passing integration controls
against a frozen uncommitted viewer candidate. This resolves the consumer
suppression path reported above; it does not certify a published provider or
change the historical template qualification.
