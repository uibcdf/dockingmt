# Named AutoDock type consumption

DockingMT consumes valid native MolSysMT AutoDock4 assignments in ligand and
receptor preparation. A caller can explicitly request assignment with
`typing_options`, or supply a previously assigned native system. Chemical
classification and graph/value binding remain public MolSysMT operations.
Since 2026-10-10, a valid named assignment or explicit `typing_options` is
required. Untyped molecular inputs fail with an actionable error before PDBQT
generation or Vina execution, including when provisional execution is allowed.
No heuristic fallback or automatically chosen typing model remains.
[DockingMT #43](https://github.com/uibcdf/dockingmt/issues/43) owns this adoption;
[MolSysMT #222](https://github.com/uibcdf/molsysmt/issues/222) owns the provider.

```python
import dockingmt as dmt

prepared = dmt.prepare_ligand(
    ligand_with_declared_chemistry,
    selection='all',
    hydrogen_options={
        'mode': 'fixed_chemical_state', 'pH': None, 'engine': 'RDKit',
    },
    charge_options={'method': 'gasteiger_marsili'},
    typing_options={
        'typing_scheme': 'autodock4', 'method': 'chemical_environment',
    },
)
assessment = dmt.assess_preparation(prepared)
```

These explicit choices describe a bounded software workflow, not a recommended
chemical model for arbitrary docking inputs. Ligand stages run H addition, then
charges, then typing, omitting every unrequested calculation. Receptor
`typing_options` assigns types on already supplied chemistry, indexed H and
charges; it adds no receptor repair or charge/H stage. Empty/ambiguous options
fail before molecular conversion. Provider errors propagate unchanged, without
an engine, model or chemistry fallback. Inputs and option mappings are unchanged.

## Assignment and hydrogen contract

The qualified provider profile is experimental `chemical_environment@1` on
MolSysMT `5bd893c85fe8d211663b2b1f865f5f1d2c382a90`. It requires a supported
complete chemical graph and all required H as indexed atoms. A named method does
not infer protonation or silently materialize virtual H. Its rule coverage is
bounded; it is not universal donor/acceptor chemistry or preparation validation.

Public selection/extraction checks native assignment binding. DockingMT rejects
stale or unsupported named reports. Valid projected parent labels are retained;
an amide N selected from its parent is not reclassified as an isolated fragment.
A bare `atom_ff_type` column identifies no named scheme and is not adopted as
named evidence. Manual replacement that clears provider attribution therefore
requires a new named provider assignment before preparation. Element identity stays in
`atom_type`; force-field labels remain distinct.

For a named assignment, H/HD labels choose omitted nonpolar versus retained
polar H. This preserves provider classification for supported F/P parents as
well as N/O/S. Every H still needs one explicit heavy-atom parent. Existing
nonpolar-H charge transfer and PDBQT serialization remain the temporary
consumer implementation tracked by
[MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223).

## Evidence and atom axes

Prepared metadata retains two detached finite JSON records:

- `atom_type_assignment`: the original native provider report, including scheme,
  method, rule order/evidence, original evaluated inventory, selected state,
  polar/nonpolar H, chemical/value binding, software, references and attribution;
- `atom_type_projection`: selected provider source indices, retained selected
  and original source indices, prepared labels, written atom permutation and
  written-to-provider-source correspondence.

Provider complete coverage and `n_atoms` refer to the graph originally evaluated,
including for a selected fragment. Generated atoms and the original pre-stage
input axis are described separately by `preparation_workflow`; a newly added H
has no original input atom and maps to `None`. For flexible ligands, ROOT/BRANCH
order composes the prepared/source maps explicitly. Counts, names and PDBQT
serials do not infer identity.

Both writers include `REMARK DOCKINGMT_ATOM_TYPES` with original scheme, rule
version/software, evaluated/written counts and H policy. Before writing, they
check saved labels and correspondence. Changed prepared labels, malformed or
nonfinite evidence and inconsistent maps fail. These guards detect accidental
consumer changes; they are not certification of subsequently mutated molecular
graphs or protection against intentional metadata rewriting. Reassign molecular
changes with MolSysMT and prepare again.

Prepared/result JSON retains complete attribution and maps. `source_molsys`
retains checked projected labels; its individual source charges remain separate
from the consumer's merged prepared charges. H5MSM 0.5 rejects nonempty
MolecularMechanics and is not a qualified persistence route for these reports.

## Default admission and scientific limits

Named types remove the known heuristic-type provisional reason. Named charges
remain separately audited for numeric conservation and PDBQT rounding. When
neither known provisional reason remains, the existing preparation assessment
is **unassessed**, not scientifically ready. Missing charges still produce
`zero_placeholder_charges`; unsupported/stale evidence fails rather than hiding
behind an admission flag.

The default Vina gate accepts the bounded named/charged route. Real parser
admission and one synthetic docking pose establish interoperability, not
predictive accuracy, energy-model suitability or AD4 scoring acceptance. No
automatic torsion policy, biological equivalence or general receptor coverage
is established here.

## Qualification — 2026-10-06

This section preserves the original qualification, not a current-source rerun.
The [2026-10-10 compatibility decision](required_named_typing.md) supersedes
untyped preparation behavior; original receipts/notebooks remain unchanged.

The [executed notebook](named_autodock_types_2026-10-06.ipynb),
[reproduction helper](../../devtools/qualify_named_types.py),
[raw receipt](data/named_types/qualification_2026-10-06.json) and
[tests](../../tests/test_named_autodock_types.py) retain independent expected
labels, full provider reports, source snapshots, maps, input/source hashes,
actual interpreter and producer versions. Run from the repository root as
`python -m devtools.qualify_named_types` using the qualified source profile.
The notebook invokes the same helper and saves only this new receipt.

| Control | Expected observation |
| --- | --- |
| Neutral/protonated methylamine | NA/N respectively |
| Amide, pyridine, pyrrole N | N, NA, N with parent context retained |
| Thioether/sulfone S | SA/S respectively |
| F/P indexed H | Retained HD without nonpolar-H transfer |
| Methanol explicit stages | 2 input → 6 evaluated → 3 prepared; `[0, 1, None]` input map |
| Original 181L BNZ | Declared template → 6 new H → 12 evaluated → 6 aromatic A |
| 5X72 P59, two explicit active bonds | Written permutation preserves labels/source correspondence |
| pm/coulomb context | Fixed output units and consistent charge audit |
| Synthetic named receptor/partner | Real default Vina, one pose, retained JSON/captured input evidence |

Polygon/linear poses are declared synthetic controls, not conformer generation.
5X72 retains the unchanged SDF checksum and explicit public RDKit stereo/property
loss/adapter-template route. This does not repair unsupported legacy native MOLI
inputs. Original BNZ uses the same heavy-only template and explicitly reported
intersection policy; its experimental heavy-atom pose is preserved. Local H
positions remain modeled geometry.

The earlier #42 qualification is preserved in local commit `6f193fb`; its dated
receipts and notebooks describe the prior runtime. This new receipt records
current consumer hashes and checks provider source bytes against the same
committed MolSysMT. The
[prior source profile](data/chemical_templates/source_profile_2026-10-06.json)
retains separately verified source identities, native artifact digest and host
limitations. Distribution metadata is not substituted for source identity;
native bytes carry no fresh build-provenance claim. Local Python 3.14 evidence
does not establish Python 3.11–3.13, clean installed artifacts, hosted CI or public
admission. Host AmberTools dependency conflicts and pre-existing shared-guide
drift remain outside this change.

The [local checkpoint](data/named_types/checkpoint_2026-10-06.json) records
**952 passing tests without skips (273.21 s, 145 warnings)**, including 64 new
cases. All ten notebook code cells execute; Ruff (118 files), report/index,
changed-document links, finite receipt/hash, editable identity, component-guide
and diff checks pass. It retains missing hosted/installed/interpreter evidence
and the unchanged canonical-guide drift separately.
