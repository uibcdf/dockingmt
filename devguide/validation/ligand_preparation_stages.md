# Explicit ligand preparation stages

`prepare_ligand` can delegate caller-requested fixed-state hydrogen addition and
named partial-charge assignment to public MolSysMT builders. Current calls with
neither option retain their existing behavior. Chemistry must already be declared
on one selected state/frame; this does not repair an unresolved chemical graph.

```python
import dockingmt as dmt

prepared = dmt.prepare_ligand(
    ligand_with_declared_chemistry,
    selection='all',
    hydrogen_options={
        'mode': 'fixed_chemical_state',
        'pH': None,
        'engine': 'RDKit',
    },
    charge_options={'method': 'gasteiger_marsili'},
)
workflow = prepared.metadata['preparation_workflow']
charge_audit = dmt.audit_preparation_charges(prepared)
```

These are optional keyword-only mappings. A requested H stage requires all three
explicit choices shown above. A requested charge stage requires a nonempty named
`method`; its scientific arguments, units and supported models are validated by
MolSysMT. Empty mappings do not request defaults. Unknown provider options are
rejected by its public API. Input/report/digestion overrides are prohibited.
Mapping admission and mandatory choices fail before molecular conversion.

H addition runs before charge assignment. Either can be requested independently;
H addition alone can still leave unattributed or placeholder charges. No absent
stage is executed automatically. Provider exceptions propagate unchanged,
without another engine, repaired chemistry or charge-model fallback. All stages
operate on detached selected copies, leaving caller inputs and option mappings
unchanged. Existing explicit-H inputs require the provider's stored inventory
and chemistry even when no new H would be added; atom presence alone is
insufficient to satisfy that contract.

Expanded-attribute handling defaults to `attribute_policy='strict'`. If an input
attribute cannot cover added atoms, the provider rejects the expansion. The
caller can explicitly request `'intersection'` in `hydrogen_options`; its original
report retains dropped attributes and invalidated analyses. In the B-factor
control, strict fails and explicit intersection records the B-factor loss on
the expanded copy; the input retains its B-factor values.

## Provenance and atom axes

The detached finite `preparation_workflow` record has schema `1.0`, scope
`explicit_molsysmt_stages`, the selected input count and requested stage order.
Its `hydrogen_addition` field contains the original provider report: selected
state/frame, inventory, old-to-new correspondence, new-H parent pairs and IDs,
software/references/attribution, coordinate units/evidence and interpretation
limits. Charge provenance lives in the existing `partial_charge_assignment`
record, referenced without duplicating its full report.

`prepared_to_input_atom_indices` and `pdbqt_to_input_atom_indices` refer to the
selected input before requested stages. A generated H has `None` because it has
no original input index. Its parent correspondence remains in the provider H
report. Other existing fields (`source_n_atoms`, `retained_atom_indices`, charge
projection/source indices and active torsion pairs) refer to the H-expanded
selected system before nonpolar-H projection. The provider's append contract
preserves existing indices. Flexible output order is explicitly composed rather
than inferred from names, counts or PDBQT serials.

For methanol, 2 original atoms become 6 after H addition, then 3 prepared atoms.
Three new carbon H atoms are omitted and their charges transferred by the
existing projection; the polar O-H remains with prepared/input mapping
`[0, 1, None]`. Source coordinates and atom IDs remain intact. Repeating H
addition on a valid fully indexed inventory adds zero atoms and retains all
existing coordinates. Numeric charge audit remains separate from molecular
chemistry and local-geometry quality.

Prepared/result metadata retains the H report and composed maps through JSON
save/reload. Template application precedes this boundary if needed; its report
remains a separately retained workflow record while native attachment is owned
by [MolSysMT #298](https://github.com/uibcdf/molsysmt/issues/298).

## Qualification and limits — 2026-10-04

[Executed notebook](ligand_preparation_stages.ipynb),
[reproduction helper](../../devtools/qualify_ligand_stages.py),
[raw receipt](data/ligand_stages/qualification.json) and
[guards](../../tests/test_ligand_preparation_stages.py) use committed provider
`7894435e748bc55254b6c3d2b63ae82c101e5774` and the requested Python 3.14 environment.
Run the helper from the repository root as
`python -m devtools.qualify_ligand_stages` with the qualification archives on
`PYTHONPATH`; the notebook uses the same operation and checks its Conda interpreter.

Provider source bytes, source snapshots, original producer versions and
implementation hashes are retained separately. No dependency/source pin changes
are needed; dirty/unpublished sibling work is preserved.

The supported polar control uses public MolSysMT SMILES conversion and native
Structures composition with declared synthetic coordinates. The existing
composition off-axis `atom_index` diagnostic is preserved, and exact input
identity/coordinates are checked. Original producer reports are normalized for
finite JSON; no downstream credit or scientific interpretation is invented.
A real Vina exploratory docking/save/reload preserves the stage report. The
default heuristic-typing rejection remains in force.

Original 181L BNZ is **not positively qualified**. After the previously qualified
explicit heavy-only benzene template, public fixed-state H addition rejects
missing covalent bond aromaticity. The notebook retains this negative control,
its template report and unchanged experimental pose. Evidence is handed off in
[MolSysMT #314](https://github.com/uibcdf/molsysmt/issues/314#issuecomment-5978374154).
DockingMT #41 stays partial for that real-input acceptance; no local aromaticity
perception, direct RDKit manipulation or alternate template workaround is added.

Generated H positions are local modeled geometry, not experimental observations,
receptor/environment refinement, protonation prediction or energy minimization.
AutoDock typing (#222), provider charge-preserving export (#223) and broader
preparation/scoring qualification (#5) retain their own acceptance criteria.
