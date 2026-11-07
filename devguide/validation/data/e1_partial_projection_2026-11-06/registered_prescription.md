# Bounded E1 supplied-representation projection — 2026-11-06

Owner: [DockingMT #78](https://github.com/uibcdf/dockingmt/issues/78).
Status at prescription: **prospective**. This is molecular contract receiving
on a development installation, not an administrative check or full E1 acceptance.
The [notebook](e1_partial_projection.ipynb) uses public MolSysMT operations.
Its exact bytes, code-cell identities, input identities and actual source
versions are recorded before execution in the attempt registration.

## Inputs and authority

Use all five poses from the original
[human 3PTB result](data/human_3ptb/native_result_2026-10-20.json.gz), without
choosing poses after observing the projection outcomes:

- Compressed SHA-256: `4b1f51cdeb135fd6785a181f6bb09a0d0f631ec3d9de7c169c88703748924249`.
- Decoded SHA-256: `ed0eeb3ade25e54f8a5829729578fcbec9f0d73d6c0ceb03d146b0c3492d7fac`.
- Actual captured partner PDBQT SHA-256: `a36bd740cc47045c2f2f6756bd8c11b41cbcc960a76ce42c2f2114b3c4b7be46`.

The original capture contains thirteen atoms and a rigid declared ligand tree.
Keep its original bytes, preparation remarks, scores, state labels and producer
unchanged. Source-native atom IDs and written PDBQT serial IDs are different
recorded axes. The original identity-order prepared/written maps and available
names/elements bind this bounded positional use; they do not prove complete
chemical-state equivalence.

The inspected custody set has no directly reusable complete prepared native
thirteen-atom snapshot. Preparation receipts explicitly record that no molecular
snapshot was created. The later E4 models materialize five additional ligand H;
they are not substituted for that missing authority. Extracting thirteen atoms
would not restore the original virtual-H inventory, aggregate charges or typing
assignments. No preparation replay or H transformation belongs to this trial.

## Population, operations and controls

Run the same five original poses serially under normal nm/ps and nondefault
pm/fs policies, with elementary-charge versus coulomb session standards. There
are five distinct poses of one case and ten projected records, not ten
independent observations. Stop before the second profile if the first fails.

For each profile, convert the original captured PDBQT through MolSysMT with
explicit torsion-tree discard into native domains, retaining its tree separately.
For each pose, copy that partial native representation, set explicit coordinates
in angstrom and export through the native PDBQT writer with the original tree
and `return_atom_map=True`. The provider owns every molecular read, write,
permutation and coordinate operation. There is no downstream PDBQT parser,
coordinate rewriter or molecular matcher.

Assert the actual written map, thirteen-atom axis, coordinates within
`0.000500001 angstrom`, explicit charges within `1e-12 elementary_charge`, types,
IDs/names/elements and tree. The native-source nonmutation check covers the
listed coordinate/name/ID/type/charge fields, not every native domain. Original
saved records and captured bytes are checked separately. Verify exact caller
unit-policy preservation, retain each output/hash and original pose/score
association, and require equal output bytes across the two unit profiles.
Groups/chains, occupancy/B, ATOM/HETATM and remarks are outside these field
assertions. The writer canonicalizes presentation; original preparation remarks
stay in the unchanged capture and are not relabelled as fresh evaluations.

Three adverse controls per profile must refuse for their declared reasons:

1. The partial source cannot supply the complete chemical authority required by
   `chemical_states.get_atom_correspondences`; use one supplied identity map,
   `max_matches=1`, and expect the complete-connectivity refusal.
2. A public atom permutation followed by an unchanged old tree must refuse the
   stale tree/atom-ID axis. The consumer does not repair it.
3. Nonfinite coordinates must not produce an exported PDBQT.

Direct consumer-call budgets over both profiles are: at most sixty conversions,
four hundred getters, forty copies, twenty setters, four atom permutations and
exactly two attempted graph-correspondence calls. Internal provider calls and
other aliases are outside these counters. The wrappers enforce only this
experiment's direct-call caps and do not patch package globals. No call may
silently exceed its cap. Zero searches, scores, optimizations, preparations,
H generation, charge/type calculations, detectors or viewer calls are prescribed.
The graph-refusal control can import RDKit and the provider's native module;
absence of those imports is not claimed.

## Environment, resources and failure policy

Use the actual installed editable DockingMT and MolSysMT revisions recorded in
the attempt registration, separately from the controlled ordinary-install pins.
This receives that development composition only. The isolated import check
passed before this prescription; it did not run molecular operations.

Use a fresh disposable process with one allowed logical CPU, low priority,
one native worker, a measured **8 GiB available-RAM reserve**, a **1 GiB task-RSS
limit**, a **2 GiB address-space limit**, and a **60-second wall limit** for the
complete two-profile trial. Monitor available RAM and the owned process during
execution; descendants inherit affinity/worker limits. Stop only owned work on
a threatened reserve or limit. Preserve the attempt, cell progress, counters,
partial files and diagnostics. A resource interruption does not authorize an
automatic retry. Any corrected assertion or contract amendment gets a new
registered code identity and attempt; prior outcomes remain intact.

Inputs and existing output directories are never overwritten. Retain the new
projection population separately from historical experiments and keep the
local E4 computational hold intact. Task evidence belongs to #78/#50, with
custody review on **2026-11-13**.

## Interpretation

A passing trial establishes preservation of the listed supplied PDBQT fields
and pose association for this rigid partial representation. The expected
chemical refusal is not chemical equivalence, biological absence or a
preparation-validity certificate. No score comparison/ranking is admitted and
`rank_by` is unchanged. Complete native-source/identity receiving,
flexible/nonidentity export controls, comparison policy and representative
native/installed rescoring remain E1 work. No provider pin, public package,
release or platform claim changes.
