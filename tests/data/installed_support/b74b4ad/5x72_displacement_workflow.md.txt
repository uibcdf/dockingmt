# Prespecified positional sensitivity in 5X72

[DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17),
[#6](https://github.com/uibcdf/dockingmt/issues/6) and
[#33](https://github.com/uibcdf/dockingmt/issues/33) own this follow-up to the
[saved-input distance diagnostic](5x72_contact_workflow.md). The
[prescription](https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6094392354)
precedes the original observations. The [driver](../../devtools/qualify_5x72_displacement.py),
[original producer](data/5x72_displacement/producer_2026-10-09.py.txt),
[raw archive](data/5x72_displacement/audit_2026-10-09.json.gz),
[receiving checkpoint](data/5x72_displacement/checkpoint_2026-10-10.json),
[executed notebook](5x72_displacement_workflow_2026-10-09.ipynb) and
[guards](../../tests/test_5x72_displacement_workflow.py) retain the complete population.

## Question, fixed inputs and ownership

How sensitive are the original-rigid and earlier experimental-heavy/generated-H
points to a small positional displacement with internal geometry and each arm's
H fixed? Do the previously declared protein-pair distances change alongside
the score within that complete finite population?

This is a human-executable Python/Jupyter scientific workflow: state the question,
fix the inputs and observations, execute public domain operations, inspect all
results including negative outcomes, and document the limits before deciding
on another experiment. This receiving step adds no generalized campaign framework
or agent orchestration, and promotes no constructed point to a scientific candidate.

The original producer uses public MolSysMT `copy/set/structure.translate`, native
PDBQT conversion and `structure.get_distances/get_rmsd`. DockingMT owns fixed-score
execution, explicit ROOT/cut choices, captured inputs and score history. NumPy
independently checks outputs; it never constructs the molecular transformation.
No molecular reader, translation, distance kernel, charge model or pharmacophore
operation is introduced downstream.

Both ligands retain 39 atoms and their own arm's full internal geometry/H. There
is no new chemical state, conformer search, H addition, charge/type assignment,
preparation, rotation or fitting. The original 25-atom prepared representation
retains source indices 0..23 and 29, including one polar H. Both original ROOT
orders, two selected cuts, receptor contexts and the box remain fixed.

## Seven offsets and complete observations

Offsets in the crystal Cartesian frame are **0, -x, +x, -y, +y, -z, +z**, with
each nonzero offset **0.25 angstrom** along its named axis, in that order. All 39
atoms move together through public detached translation. Independent checks retain
all **741 unordered pair distances per point / 20,748 across 28 points**, unchanged
chemistry/identity, signed handedness and exactly the requested displacement.
Positional heavy RMSD uses the original 24 experimental heavy atoms without
alignment. Original-rigid P59 spans 0.5131–0.5708 angstrom and P69 0.6795–0.7240;
the earlier-reference arm spans approximately 0–0.25 for both. These constructed
near-reference points are not returned-pose recovery observations.

The producer retains **112 fixed evaluations**: seven offsets × two ligands ×
two coordinate arms × two ROOT orders × two sham/occupied contexts. All **16
zero anchors** precede the **96 nonzero evaluations** and match the corresponding
historical submitted bytes and all eight score components exactly. There are
**zero new searches or optimizations**. All input bytes, maps, original state,
unrounded coordinates, components and matched-zero deltas remain saved.

Pair measurements use the actual three-decimal submitted PDBQT projections.
The declared P59 pairs are source16 O17/OA with ARG61 NH1/N and GLN78 NE2/N;
P69 pairs are source4 C5/A with GLN116 OE1/OA and source16 O17/OA with TYR149 OH/OA.
Native conversion explicitly discards the ligand torsion tree for measurement;
the original tree and maps remain captured. Distances use CPU, no PBC and explicit
angstrom extraction. Protein-pair distances agree between contexts because their
protein prefix and ligand coordinates are fixed; the occupied companion remains
a separate scoring context.

## Observations, including negative controls

Both ROOT orders agree exactly on the explicit source axis and all reported
components at each matched point. The notebook displays all seven totals, all
eight-component deltas are archived, and every selected protein-pair distance is
retained. Table minima refer only to the finite prespecified population; ties use
the original offset order.

| Ligand | Arm | Context | Zero total (kcal/mol) | Lower nonzero points / 6 | Minimum offset | Minimum minus zero (kcal/mol) | Maximum minus zero (kcal/mol) |
| --- | --- | --- | ---: | ---: | --- | ---: | ---: |
| P59 | Original rigid | Sham | -7.618 | 3 | +z | -0.790 | +1.344 |
| P59 | Original rigid | Occupied | -8.551 | 1 | -x | -0.619 | +1.204 |
| P59 | Earlier reference | Sham | -9.661 | 1 | +z | -0.727 | +1.438 |
| P59 | Earlier reference | Occupied | -10.534 | 0 | Zero | 0.000 | +1.117 |
| P69 | Original rigid | Sham | -1.666 | 3 | -x | -2.512 | +3.700 |
| P69 | Original rigid | Occupied | -2.667 | 3 | -x | -2.554 | +3.758 |
| P69 | Earlier reference | Sham | -9.626 | 2 | -x | -0.626 | +1.346 |
| P69 | Earlier reference | Occupied | -10.499 | 2 | -x | -0.724 | +1.423 |

At original-rigid P69's -x point, the two selected distances change from
2.223982/2.420689 to 2.436205/2.432022 angstrom while occupied total decreases
by 2.554 kcal/mol. The same translation changes every ligand–environment pair;
this association assigns neither an atom-pair energy nor a cause. Even the
lowest occupied P69 original-rigid point remains 5.278 kcal/mol above its earlier
reference zero. The differing original/generated H remains a confound between
arms. No cross-ligand affinity comparison is made.

P59's earlier-reference occupied arm has **no lower nonzero point**. Retain that
negative result alongside favorable displacements. Seven points do not establish
a local optimum, derivative, barrier, convergence, recovery probability,
chemical preparation validity or a general ROOT/torsion/H/ranking policy.
No contact-based remedy or optimization default follows from this control.

## Original identity and receiving qualification

The original observations were captured on 2026-10-09 with consumer base
`b793075e8a06bea6d8704eb0db24239b16671e57` and the separately preserved, then
untracked driver bytes. Its SHA256 is
`ed2db70e65c8248e6502169c8043f3f7e0dbe5b8b278af6b0c0eb44370fd9e23`.
The archived producer and integrated driver remain byte-identical. Gzip SHA256:
`afb8bfa4092abc78f8cd2daf33da7248fe39fbd1856b23e24a192f4813fb72a8`;
uncompressed JSON SHA256:
`0bbf5990234cec5b739d7f32f00e035ada42d9bd3277932eab831c9f3545226c`.

Original provider source is `5bd893c85fe8d211663b2b1f865f5f1d2c382a90` with
native SHA256 `c535c7d2f0e2a92b6ebf8298a60b19e4b5555467b4aa087e9563c6760619827e`.
The receiving step checks the archive's 35 provider and 58 tracked consumer
source digests against those original Git identities; the driver and generated
version module were not tracked in the base. Do not rewrite the original
`original_sources_verified=False` nested archive flags: they record the original
loader scope. Historical tracked-source checks now have a separate receipt;
the original generated-version digest is recorded without claiming fresh
verification of its historical runtime bytes.

New receiving tests use the unchanged CI-pinned `739395d7e` source, preserved
native binary and qualified ArgDigest/Viewer composition on Python 3.14.7.
Current and pm/fs/degree/inferred-string controls compare molecular values,
identity, axes and geometry, without requiring historical dataframe annotation
equality. A bounded **four-evaluation live slice**, original-rigid P69 -x with
both ROOT orders and contexts, checks current fixed-score execution and exact
saved components. It does not rerun, replace or regenerate the original 112
observations. The three-cell notebook reads saved results only; its managed
kernel and temporary resources are cleaned after execution.

Running the original scientific driver requires its original authenticated
consumer/provider profile. The receiving checkout is a later identity and must
not pass the producer's historical-source proof by updating the expected hashes.
The saved-result notebook and receiving tests are the current inspection routes.

Local qualification passes **127 tests without skips in 174.26 s**, including
the ten new guards. Ruff lint/format (155 files), reporting/index/local links,
synchronized-guide checks and diff checks are recorded separately. An initial
negative fixture modified the selected score rather than the frozen calculation
history; its failed diagnostic does not qualify the change. The final passing
test mutates the actual recorded anchor input and observes rejection.

Local and exact-head hosted gate results are recorded in the receiving checkpoint
and owning issues. Newer provider inspection, scientific production, receiving
source tests, installed checks and public admission remain distinct claims.
Dependencies, environment, sibling worktrees and all earlier scientific archives
are preserved. Existing provider ownership/removal conditions remain unchanged;
#17/#6/#33 remain partial/open.
