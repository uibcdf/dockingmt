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

The original 2026-10-20 controlled source composition selected MolSysMT
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

## Executed installed workflow — 2026-10-20

The ordinary wheel from `1decee504b112cfd92026c52dcbe22449de30f4f`,
`dockingmt-0.0.0+180.g1decee5-py3-none-any.whl`, has SHA-256
`24cfe209935b9bcdef371590427dc74818f23eece6711171346c72402c02ba4e`.
All 60 required package files match the installed bytes; PEP 610 identity,
ordinary import origins, addon entry-point declaration and dependency closure pass.
The receiver is a separate prefix outside the checkout, inheriting the task-owned
normally installed fixed provider composition. It is not a public-channel artifact
or platform-admission claim.

The shared source-free installed runner executes **277 tests without skips or
deselections**, 135.56 seconds, 71 retained warnings. Selected evaluation,
serialization, required preparation and frozen 3PTB contracts pass, including
real provider symmetry/input controls. The new template-composition regression
passes separately with the other symmetry controls (14 cases). Administrative
contracts pass 29 cases. Initial test-construction diagnostics and the first
strict historical-source rejection remain recorded; they are not passing gates.

The notebook executes compressed input, the audited explicit preparation, the
registered single rigid/native/seed-7/exhaustiveness-1 search and saved-result
recovery. Five poses return. The first attempt stops at symmetry admission because
template application leaves the original nine atoms' stereochemistry missing.
The native result and its producer remain intact. A subsequent complete notebook
execution restores that exact result, verifies protocol/submitted hashes and runs
no additional search. It explicitly sets `atom_stereochemistry='unspecified'` on
a detached context for this declared benzamidinium case. MolSysMT independently
validates potential stereo and chemical equivalence; this is not a general filler,
chirality classifier or a change to the saved preparation.

The reusable composition/documentation need is proposed in
[MolSysMT #390](https://github.com/uibcdf/molsysmt/issues/390). The first missing
metadata failure is retained as an informative admission result rather than hidden
by a favorable repeat search. These two notebook executions together establish the
bounded human workflow; they are not described as one uninterrupted green run.

Historical receiving evaluates all **24 rows / 167 poses**, with no reexecuted
search. Positional RMSD agrees with the earlier receiver to `1e-10 angstrom`;
complete native energy vectors and containment agree. The independently added
symmetry criterion retains rank-1 recovery in 6/6 rows for each native arm and
0/6 for each displaced-box arm, as does the positional criterion. This bounded
comparison is not general docking accuracy or model validation. Original archived
inputs, errors, metrics and producers remain unchanged.

The [qualification manifest](data/human_3ptb/qualification_2026-10-20.json),
[wheel receipt](data/human_3ptb/wheel_2026-10-20.json),
[original fresh result](data/human_3ptb/native_result_2026-10-20.json.gz),
[new evaluation](data/human_3ptb/evaluation_2026-10-20.json.gz),
[separate historical measurements](data/human_3ptb/saved_receiving_2026-10-20.json.gz)
and [kernel receipt](data/human_3ptb/kernel_receipt_2026-10-20.json) preserve scope,
identities, source paths and digests. The executed notebook contains no error in
the completed recovery run and ends with an explicit pre-visualization stop.

Full exact-head source CI is a separate gate recorded on #49 after the final push;
the installed wheel keeps its original producer above. C6, public distribution,
the missing provider projections/permutations and broader chemical/scoring
acceptance remain open.

## Resource disposition

The old receiving/candidate interpreters and wheel are absent at their registered
2026-10-13 paths; absence does not identify who removed them. Versioned historical
receipts remain in Git. The new task owns `/tmp/dockingmt-human-20261020` under
[#50](https://github.com/uibcdf/dockingmt/issues/50). Retain the qualified provider
environment, ordinary receiver, original wheel, source-free harness, exact source
and SDK identities, initial failure/native result and complete execution/CI
evidence for the immediate visualization discussion or recovery. Review by
**2026-10-27**; no automatic cleanup is scheduled. Only disposable owned build/cache
paths may be removed at closeout, preserving the installed native bytes, artifact
and all still-required evidence. Shared environments and sibling worktrees remain
outside this cleanup scope.

## Subsequent template-stereo receiving — 2026-10-23

[Provider receiving](provider_receiving_2026-10-23.md) at
`128a0bbb94e6804f5663e58a45313c77de1cc30d` consumes MolSysMT #390. The frozen
benzamidinium template now retains all 18 explicit unspecified declarations
through indexed H composition, admitting the two expected heavy-atom maps while
fixing the distinct N roles. Missing/unknown declarations on a detached context
still reject. This replaces the current test's old missing-metadata expectation;
the prior notebook's explicit declaration, producer and observations stay intact.
