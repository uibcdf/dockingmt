# Native inputs for BindingMT H0/H1

Newly authored analytical inputs, 2026-11-12; owners LMMV/dprada;
PharmacophoreMT#108 consumer continuation of BindingMT#112. The repository
license applies. No external structure, activity measurement or private geometry
is included. A/B/C/D are test-local participant names, assigned explicitly to
atom indices; they are not inferred chain labels or BindingMT records.

`source.h5msm` contains the full four-ion MolSysMT source and three named full
native analyses. `alternative.h5msm` translates C by +0.05 nm in y and contains
fresh analyses. Both use public H5MSM1.0. `primary.json` and `alternative.json`
are separate observed-C hypotheses written by native PharmacophoreMT IO.
`zero_essential.json` and `excluded.json` are explicitly curated decision
controls. `manifest.json` records original hashes, source/analysis/output-site
links, producer versions and independent expected memberships. It is a trusted
test-local content map, not a proposed BindingMT serialization specification.

The main input uses `smiles:[Cl-].[Na+].[Na+].[Cl-]`, explicit formal charges,
no bonds/hydrogens between the disconnected ions, one Cartesian structure,
state0, no PBC and identity atom/structure maps. Coordinates in nm:
A=atom0(0,0,0), B=atom1(.2,0,0), C=atom2(0,.25,0), D=atom3(0,.45,0).
The native `source_id` is unset; exact artifact hashes and manifest links provide
custody for this case. This is not qualification of arbitrary cross-source maps.

Independent expected pairs at0.31/0.35nm are A–B, A–C and C–D. Native strict
`between_selections([0,1], [2], structure_indices=[0], exclusive=True)` retains
only A–C, including its original relation/occurrence IDs in each named analysis.
The evaluated0.01nm analysis stays empty with frame0 coverage. Both labels
support one compatible essential positive-charge sphere, weight1, radius0.02nm.
Repeated observations do not add weight or independent experimental evidence.

Expected `(status, fit_value)` on C alone:

| Hypothesis / input | Expected |
| --- | --- |
| Primary / original | matched, 1 |
| Primary / alternative | not_matched, 0 |
| Alternative / alternative | matched, 1 |
| Alternative / original | not_matched, 0 |
| Extra absent essential site of weight0 / original | not_matched, 1 |
| Exclusion at C / original | not_matched, 1 |
| Two constraints under explicit keep policy / original | not_matched, 0.5 |

Read and inspect through each owner's public tools; hypothesis reconstruction
uses the unchanged **full** recovered source, not an extracted C-only source.
Candidate evaluation performs recognition. Saved reading performs none.

```bash
python -m devtools.qualify_binding_interface_handoff --read-directory tests/data/binding_interface_handoff --length-unit nm
python -m devtools.qualify_binding_interface_handoff --read-directory tests/data/binding_interface_handoff --length-unit pm
python -m pytest tests/test_binding_interface_handoff.py -q
```

Use the declared development environment and the repository's shared-resource
limits. To regenerate, select a **new** destination with `--output-directory`;
existing destinations are refused. Preserve these delivered files and append a
new producer/run identity. H5MSM container bytes are not promised deterministic
across regeneration. The generator lives in
`phmt_test_support/binding_interface_handoff.py`; the thin `devtools` wrapper is
development-only. Neither helper is shipped as a runtime API.

The guard also authors a separate complete carboxylate/Na input for partial
compound-participant refusal and deliberately contradictory native state/map/
coverage controls. These are declared negative controls, not original detector
observations or additional frozen files. Full contract and measured evidence:
`devguide/binding_interface_native_handoff.md` and
`devguide/evidence/binding_interface_native_handoff_20261112.json`.

BindingMT I0/H/I1 admission, construction and saved-readback remain unexecuted
here. This case supplies inputs and consumer expectations for those operations;
it introduces no BindingMT adapter, schema acceptance or integration claim.
