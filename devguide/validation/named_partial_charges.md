# Named partial-charge consumption

DockingMT consumes an explicitly assigned MolSysMT charge model. It preserves
original provenance and observes charge conservation through its existing
hydrogen projection and PDBQT writer. The charge-only qualification below retains
provisional AutoDock typing. The [2026-10-06 named-type adoption](named_autodock_types.md)
adds an explicit consumer route with its own evidence; earlier receipts remain intact.

```python
import molsysmt as msm
import dockingmt as dmt

assigned = msm.build.assign_partial_charges(
    ligand, method='gasteiger_marsili',
)
prepared = dmt.prepare_ligand(assigned, selection='all')
report = dmt.audit_preparation_charges(prepared)
print(report['assessment'], report['total_charge'], report['charge_unit'])
print(report['partial_charge_assignment']['software'])
```

For a supported explicit-H protein graph, the caller can instead use
`method='forcefield', forcefield='AMBER14', expected_total_charge=2` with MolSysMT.
This declaration is specific to the 1VII control here; other inputs require their
own justified inventory and model. DockingMT never chooses, calculates or falls
back to a charge model. Unsupported chemistry, missing providers and invalid
model requests are handled by the public MolSysMT assignment operation.

## Preparation contract

`prepare_ligand` and `prepare_receptor` read supplied charges through public
MolSysMT operations. Values are converted explicitly to elementary charge when
returned as quantities; native numeric charge values already use that unit.
MolSysMT's public indexed extraction checks its stored molecular assignment
binding. DockingMT rejects reports marked stale or carrying an unsupported
schema/status/unit. It imports no private molecular validator.

Prepared metadata contains two detached finite JSON records:

- `partial_charge_assignment`: the original public native MolSysMT report,
  including method, parameters, software versions, references/attribution,
  chemical state, original coverage/totals and projected correspondence;
- `charge_projection`: the selected and retained source indices, original
  selected total, retained total before merging, individual omitted-H-to-heavy
  transfers, prepared total and numeric prepared-value digest.

Source indices refer to the original graph on which the named model was
calculated. Original complete coverage does not become a claim that charges
were recalculated on a selected fragment. The consumer's selected total can
therefore differ from the original total. No charge is renormalized.

The existing hydrogen policy uses public stored connectivity: polar H remains,
nonpolar H is omitted and its charge is added to the retained bonded heavy atom.
This molecular/export operation remains temporary pending
[MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223). These changes record
its transfers; they do not introduce a new molecular preparation algorithm.

`source_molsys` and `to_molecular_system()` retain original individual source
charges on the retained inventory. They do not silently acquire the consumer's
merged charge values or a new provider attribution. The prepared numeric array,
its transfer record and PDBQT describe that existing consumer projection.
H5MSM 0.5 does not preserve molecular-mechanics attribution; no such roundtrip is
qualified here.

## Public numeric audit and export

`audit_preparation_charges(prepared)` accepts a `PreparedLigand` or
`PreparedReceptor`. It returns detached schema `1.0` JSON with scope
`prepared_charge_consumption`, fixed `elementary_charge` units, current total,
original assignment/projection and PDBQT rounding observations. It performs no
molecular reads, graph validation, model calculation or engine execution.

`consistent` means the current numeric array matches the recorded prepared
array and conserves the selected-source total within `1e-6 e`. `inconsistent`
reports changed values or lost conservation. This detects a charge exchange
that leaves the total unchanged. Missing named evidence is `unassessed`;
malformed evidence or incomplete/nonfinite values raise `ArgumentError`.
These are consumer numerical observations, not a current molecular-graph
certificate or protection against intentional metadata rewriting. Reassess
molecular changes with MolSysMT and prepare again.

The PDBQT record gives actual prepared/source atom order, rounded values,
rounded total, rounding difference and the bound `n_atoms * 0.0005 e`.
Full-precision conservation and decimal conservation are separate. The writer
uses three decimals without renormalization. Named preparations include a
bounded `REMARK DOCKINGMT_PARTIAL_CHARGES` with original model/software,
calculated/written atom counts, units, full-precision total and hydrogen policy.
Writers reject changed named prepared values. External or unattributed supplied
charges receive no invented model attribution.

Full reports and transfer maps survive existing prepared/result metadata
serialization. Existing `assess_preparation` remains a separate inspection of
charge/type declarations. The default Vina gate still rejects heuristic types;
named charges do not qualify AutoDock typing or an energy function. Native Vina
parsing/docking checks interoperability only; AD4 scoring is not qualified.

## Qualification — 2026-10-04

[The executed notebook](named_partial_charges.ipynb),
[helper](../../devtools/qualify_named_charges.py) and
[raw receipt](data/named_charges/qualification.json) retain original model
reports, fixed-unit observations, input/source hashes, actual interpreter and
producer distribution versions. The helper verifies loaded provider source
bytes against committed MolSysMT `7894435e748bc55254b6c3d2b63ae82c101e5774`, which
contains #221's implementation `d43648337`. The sibling's dirty worktree is
preserved. Runtime distribution version metadata can lag tested source; both
identities are retained separately. CI/full-matrix pins advance from `c19a47ada0`
to this qualified commit; older Python lanes remain separately qualified by CI.

| Control | Calculated / prepared atoms | H transfers | Prepared total (e) | PDBQT total (e) |
| --- | ---: | ---: | ---: | ---: |
| Explicit-H methanol, Gasteiger–Marsili | 6 / 3 | 3 | approximately 0 | approximately 0 |
| Selected methanol OH projection | 6 / 2 | 0 | -0.190000579171 | -0.190 |
| 5X72 P59, two declared active torsions | 39 / 25 | 14 | approximately 0 | -0.001 |
| 1VII, AMBER14 with declared expected +2 e | 596 / 364 | 232 | +2 | +1.988 |

Methanol is a declared analytical SDF fixture with explicit atoms/bonds and a
synthetic pose. The unchanged 5X72 SDF uses the previously qualified explicit
RDKit stereo engine and authorized property loss. 1VII is MolSysMT's packaged
explicit-H control. All four inputs pass real Vina parser admission, remain
provisional for typing and preserve source coordinates/charge inventories.
Single-run timings include first-use costs and are not a benchmark. These cases
do not establish predictive accuracy or general model/scoring suitability.
