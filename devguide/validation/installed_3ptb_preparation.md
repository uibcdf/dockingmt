# Installed 3PTB preparation and protocol admission

Owner: [BindingMT #4](https://github.com/uibcdf/bindingmt/issues/4), coordinated
with [#33](https://github.com/uibcdf/bindingmt/issues/33). The maintained
[notebook](installed_3ptb_preparation.ipynb) exposes the existing public
MolSysMT/BindingMT preparation recipe without a repository/data harness.
**Run All prepares one receptor and one rigid ligand and admits two problems;
it never executes Vina, evaluates RMSD or opens a viewer.**

## Explicit inputs

Select an ordinary-installed scientific kernel with Jupyter tooling available.
Copy the notebook to your working directory and supply these five inputs before
starting Jupyter, or edit their assignments in the first cell:

```bash
export BINDINGMT_3PTB_SOURCE="3ptb.pdb.gz"
export BINDINGMT_3PTB_SOURCE_SHA256="75b1b8e73b4c197b7dcb217fbcfdd39c451860c0fd5a86cdef587c4dbd9972be"
export BINDINGMT_3PTB_DECLARATIONS="admission_2026-10-20.json.gz"
export BINDINGMT_3PTB_DECLARATIONS_SHA256="79e9283236ebbb645cd75d7c3341d457a8078361466b7a26458c814d8041cd53"
export BINDINGMT_3PTB_OUTPUT="new-preparation-output"
jupyter lab
```

Use the retained [public source](data/3ptb_prospective/3PTB.pdb.gz) and
[original declaration record](data/human_3ptb/admission_2026-10-20.json.gz).
Expected identities are external trust inputs, not fresh hashes calculated to
approve an untrusted replacement. The plain molecular text identity is checked
through MolSysMT against the admitted declaration as well. An existing output
directory is refused. Inputs and old scientific artifacts are never overwritten.

The declaration file supplies human choices, the already-declared 1,629/9 atom
maps and original prepared-value controls. Its molecular snapshots are neither
restored nor interpreted. Reading a scientific decision record with standard
JSON/gzip is distinct from parsing a molecular format: MolSysMT handles the
compressed molecular source, conversion and every molecular operation.

The installation qualified here is a private archive. Public dependency minima,
installation coordinates, platform/minor admission and publication remain
#30/#47; this guide supplies no public installation command or release claim.

## Scientific prescription and nine cells

1. Admit caller configuration and ordinary-installed module origins/version.
2. Verify both files, convert the public source through MolSysMT and extract dry
   protein chain A and the nine-heavy-atom BEN reference. The observed source
   contains 1,701 atoms, 287 groups, one structure and 21 deposited bonds.
3. Construct the provider peptide template for HID57, HIE40/HIE91, ammonium and
   carboxylate termini and six declared CYX links: 22–157, 42–58, 128–232,
   136–201, 168–182 and 191–220. Construct declared benzamidinium +1 from
   `smiles:NC(=[NH2+])c1ccccc1`. Check the caller's supplied identity maps;
   do not discover correspondence locally.
4. Ask MolSysMT to assess both templates; refuse a duplicated source index with
   `MSM-ERR-ARG-001`, structured `argument=atom_correspondence`, using the public
   SMonitor exception base. Apply only the admitted valid templates.
5. Add fixed-state H through MolSysMT/RDKit, `pH=None`, explicitly allowing the
   reported occupancy/B-factor loss. Preserve observed attributes separately and
   check provider-mapped original IDs/coordinates. Apply the existing declared
   receptor generated-H naming rule through public `msm.set`.
6. Use `prepare_receptor` / `prepare_ligand` with explicit Gasteiger–Marsili
   charges, AutoDock4 `chemical_environment@1` types and no active ligand cuts.
   MolSysMT owns assignment, H projection and charge transfer. Charge audits are
   consistent; preparation/model suitability remains `unassessed`.
7. Compare prepared state IDs, counts, names, groups, types, charges and
   coordinates with the original controls, and verify the original source again.
8. Let MolSysMT compute the reference centre; declare native and +60 Å x
   displaced 20 Å boxes. Validate both problems with public `VinaProtocol`:
   seed 7, exhaustiveness 1, CPU 1, at most nine poses, Vina scoring,
   3 kcal/mol energy range and captured backend inputs. These are planned values,
   not an executed native projection or automatic domain derivation.
9. Save provider reports, original observed attribute arrays, prepared
   declarations, the unexecuted plan, current PDBQT representations and a receipt
   using exclusive creation. Print a compact summary without operational paths.

The prescription is case-specific. It predicts neither pH/protonation nor an
experimental affinity. No water, calcium, flexible ligand arm or new chemical
hypothesis is silently added. Ligand template provenance truthfully identifies
the declared SMILES bytes; it does not reuse an old native-snapshot checksum.
Prepared objects honestly retain absent standalone source fingerprints.

`Prepared*.to_dict()` does not include coordinates. Original coordinate controls
come from the admission record's separate `coordinates` / `coordinate_unit`
fields. Prepared JSON and PDBQT are declarations/representations, not a complete
native molecular/mechanics snapshot. Replay the explicit recipe or supply actual
objects when needed. General persistence remains MolSysMT #256; remaining
partial/reference PDBQT reading remains MolSysMT #521. No missing reusable
molecular tool was identified for this preparation/admission slice.

## Executed receiving — 2026-11-03

The [receiving record](data/installed_3ptb_preparation/receiving_2026-11-03.json)
and [manifest](data/installed_3ptb_preparation/manifest_2026-11-03.json) bind the
clean notebook, all nine executed source-cell hashes and both real-kernel
profiles. Each finishes outside source and shuts down explicitly:

| Observation | Normal and pm/fs profiles |
| --- | --- |
| Prepared receptor / rigid ligand | 2,011 / 13 atoms; zero active torsions |
| Projected total charge | +6 / +1 elementary charges within `1e-8` |
| Original prepared controls | Identity/type/state exact; charge and coordinates within `1e-12` in elementary charges / angstrom respectively |
| Invalid caller map | Provider refuses before application |
| Unit policy | Whole caller policy preserved in each execution |
| Current PDBQT | Both role files byte-identical between the two policies |
| Engine, energy, RMSD and viewer attempts | Zero guarded calls; zero new searches |

Python is 3.14.8. The unchanged BindingMT archive is
`0.0.0+225.g50d8e33`, producer `50d8e33f4ccb3354a8d27aea9fa9010c1b13e9a9`,
SHA-256 `5a923951f5e1bec31f41329b7e62fc9a398286bfba10b6951e984c87b0676c98`.
All 63 installed files are verified before/after each kernel; its 62 nongenerated
runtime files equal reviewed source. MolSysMT archive producer
`de7ffad2aef18ff3bccd184133dc69e081cb506e` and controlled main
`00abb958fb93649131d5ce5fe5e12e90cf4900e9` remain separate identities.
Its unchanged archive SHA-256 is
`4a8e58f40627ff468fab99301674429fba66362f549a31fb4cc747d9cf19a0ba`;
all 3,415 payload files are checked before/after. Original human-case producer
`1decee504b112cfd92026c52dcbe22449de30f4f` is not rebound to these new reports.

Validation-only pre/post cells surround the unchanged nine user cells. Loaded
core/support/provider/engine origins belong to the ordinary prefix. No source,
data harness or SDK is on the configured kernel path; developer-tool imports
are blocked. Instrumentation imports Vina and Viewer to install guards; that
does not constitute engine or viewer execution. Counters observe the actual
public molecular calls and both preparators; guards reject search/maps/energy,
RMSD, result reconstruction and rendering. The public receipt records all counts.
Dependency closure is checked separately, not inferred from kernel completion.

Attempts are retained honestly. An initial notebook-generation syntax error stops
before kernel execution. The first kernel stops at the refusal assertion because
the example expected BindingMT's `arg_name` instead of MolSysMT's `argument`.
The next stops at the coordinate assertion because coordinates are in the outer
admission sidecar. Each kernel closes. The two corrections change only client
assertions, not chemistry, controls or tolerances; both final exact-cell profiles
pass. Their [first amendment](https://github.com/uibcdf/bindingmt/issues/4#issuecomment-6618857115)
and [second amendment](https://github.com/uibcdf/bindingmt/issues/4#issuecomment-6618882394)
precede the respective retries. No provider defect or extra scientific case is
inferred. Expected provider warnings report the explicitly accepted attribute loss.

Existing installed backend-contract/preparation-assessment guards pass **64
tests**, zero skips, in 1.174 s. Their source-free test context is `1c34392`,
with both files byte-equal to reviewed source and installed origins checked.
These software tests are distinct from the nine-cell workflow and from previous
full-suite evidence; no new full scientific suite is claimed.

## Next separately registered execution

The final notebook Markdown proposes one rigid/native and one rigid/displaced
`dmt.dock` call with the protocol above: two searches, at most 18 returned poses,
no retries, rescoring, optimisation or new chemistry. Register source, artifacts,
controls, failure policy, resource ownership and denominator **before executing**.
This is a new workflow demonstration, not another run of the old 24-row benchmark.
Retain actual submitted bytes/configuration and original versus new results.

Reference evaluation requires a separate explicit atom-population/correspondence
decision: the nine-heavy-atom reference cannot be compared directly with a
13-atom prepared ligand. Use public provider selection/geometry and BindingMT's
evaluation semantics; do not copy a private heavy-pose projection helper. The
[saved-result notebook](installed_result_inspection.md) already serves detached
audit/inspection afterward. Visual C4/C6 remains deferred under #52/#60.

The task reuses the scientific receiver and kernel tooling; raw executions,
outputs and failed attempts remain #4/#50-owned reproducibility evidence for
review **2026-11-10**. Original data, shared receivers and sibling work are
preserved. No kernel, server or watcher is left running.
