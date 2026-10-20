# Optional declared-state symmetry evaluation

Owners: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49) and
[MolSysMT #310](https://github.com/uibcdf/molsysmt/issues/310).

`evaluate_redocking` retains its original positional RMSD, result order, thresholds
and summaries. Supplying `symmetry_options` explicitly requests a separate
`symmetry_evaluation` record. `summarize_redocking` continues to aggregate the
original positional criterion; it does not silently switch to corrected recovery.

```python
report = dockingmt.evaluate_redocking(
    result,
    reference,
    rmsd_cutoff=pyunitwizard.quantity(2, 'angstrom'),
    symmetry_options={
        'molecular_system': complete_query_chemical_context,
        'chemical_state': 'structure',
        'reference_chemical_state': 'structure',
        'max_matches': 100000,
    },
)
```

The molecular reference and explicitly supplied query context must provide complete
compatible chemical graphs and retain the verified pose identities. Coordinate-only
and DockingPose references cannot supply that evidence. A nonempty common pose
population is required. Optional provider options are `chemical_state`,
`reference_chemical_state`, `method`, `max_matches` and `tie_tolerance`; other keys
are rejected. The initial integration enumerates the provider's unrestricted
declared-state chemical scope, without consumer anchor or map-search algorithms.

DockingMT copies the declared query context and sets only measured pose coordinates
through public MolSysMT operations. Unselected coordinates retain context values
and are not represented as reconstructed pose geometry. In particular, omitted H
coordinates are neither predicted nor included in a heavy-atom metric. MolSysMT's
public topology operation enumerates admitted maps; its public geometry operation
validates/reuses those maps and computes each RMSD. Provider failures propagate.
No matching, graph normalization, fitting or molecular transformation is implemented
in DockingMT.

Both source-identity and corrected measurements use the shared receptor frame,
without translation, rotation, periodic imaging or implicit superposition. The
provider's original-map RMSD must agree with the existing positional baseline
within `1e-10 angstrom`. The detached optional report records the fixed angstrom
unit, cutoff, maps and complete-context witnesses, graph/payload digests, explicit
chemical scope, chosen correspondence, ambiguity counts, software and scientific
attribution. Original metrics, scores, ranks, provenance and inputs remain intact.

This is an experimental declared-state profile. Resonance, protonation and
explicit/implicit-H normalization are not admitted. In declared benzamidinium +1,
phenyl equivalence does not exchange the distinct neutral single-bonded and charged
double-bonded N roles. A rejected graph or exceeded search bound never becomes a
successful positional fallback. These controls do not validate the chemical
hypothesis, affinity or broad docking accuracy.

## Provider and regression boundaries

The controlled source composition selects MolSysMT
`c35252d89a28a8faff11e0014bda91312167f549`, containing delivered #310 and compressed
PDB input [#385](https://github.com/uibcdf/molsysmt/issues/385). ArgDigest
`3d1ec53c374098016452abab74706e9d80df5462` and Viewer
`a61b75bc994e3ad674c3e7eafe53bb6b2a989c5f` retain the previous source pins. This
is controlled integration evidence, not a new published MolSysMT version floor
or public package admission.

`tests/test_symmetry_evaluation.py` exercises actual provider calls, a permitted
benzene correspondence, a translated negative control, non-equivalent same-element
sites, fixed amidinium N roles, pose-axis permutations, incompatible state/H
representation, search bounds, caller immutability and nondefault units.
`tests/test_compressed_molecular_input.py` compares the frozen compressed source
with plain truth through public MolSysMT input and DockingMT selection routes.

The original strict 3PTB receiver keeps its original source-hash gate. It must
reject changed source and is not relabelled as a new producer. The current
receiving regression separately evaluates all saved poses, preserves original
failure evidence and compares original positional values, energies and containment.
No historical archive is rewritten to accommodate a new consumer.

The [human notebook](human_3ptb_workflow_2026-10-20.ipynb) combines compressed input,
the accepted explicit preparation recipe, one preregistered fresh control search,
both evaluation records, saved-result restoration and the historical receiver.
**It stops before visualization**, as requested by the maintainer.
