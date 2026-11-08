# Panel receptor-state reference receiving — 2026-11-08

Owner: [DockingMT #33](../pending_proposals/validate_native_molsysmt_formats.md),
with [#49](../pending_proposals/retire_general_molecular_operations.md).
Starting consumer checkpoint: `b014b2598a1194eaee51c139e105e00ee259758a`.
Status: **executed; three whole reference selections FAIL; no receptor or docking
case admitted**. The original prescriptions and amendments below retain their
chronology. Current provider comparison blocker:
[MolSysMT #646](https://github.com/uibcdf/molsysmt/issues/646).

## Delivered decisions, observed outcome and continuation

The two original cases now have explicit protein reference hypotheses, including
the observed-core/terminal and residue-state choices below. They are model
declarations, not measured bound states or prepared receptors. Original water/
other-occupant disposition and #558 completion provenance remain unresolved.

All three complete six-chain selections stop on the first chain of the first
case. The first stops on a wrong task expectation for an absent structural
domain; the second on strict text-dtype identity; the third at valid comparison-
flag digestion. Preserve their FAIL outcomes, three partial copies of the same
first reference, all other unattempted chains/case and all unattempted full pm/fs
profiles. No partial chain is promoted. Final live source/reference/caller checks
and both intended invalid-factory controls remain unreached in those selections.

Two separately completed diagnostics have distinct meanings:

- Public native reading under both unit policies shows that the retained first
  reference preserves topology, chemical values/null masks, history and absent
  structural domain. Only two recorded text dtype descriptors change to the
  owner's documented canonical representation. No persistence data-loss defect
  is established from those annotations, and no native table is rewritten.
- The final minimal argument diagnostic constructs two synthetic one-atom
  systems and runs six public comparisons. Four atom-count controls pass; the
  two valid component-type requests raise ArgumentError, under both policies.
  Caller policies and atom-count results remain unchanged. This establishes
  #646's argument-boundary failure; it does not accept reference persistence.

The executed component digester and freshly fetched main file share Git blob
`5a882f3c084a7f15850e060a7c1578fcc90d658a`. Its Boolean branch permits the get
caller but omits compare. ArgDigest correctly calls the component's named
digester; no separate shared-tool defect is established. First receive #646's
owning correction/artifact, then register a complete fresh six-chain/two-policy
selection with unchanged molecular hypotheses, controls and canonical-storage
contract. Do not bypass digestion, substitute a local comparator or repeat these
terminal selections. #644 anionic-reference and #558 generation/map receiving
still precede full bound-source preparation. Original panel/search/evaluation,
E3 #604/#645, held #642/canvas and public-delivery scope remain separate.

| Process | Outcome | Elapsed seconds / sampled peak group RSS bytes |
| --- | --- | --- |
| Original normal references | FAIL: task expects numeric structural count | 14.951 / 192,643,072 |
| receiving-02 normal references | FAIL: strict storage-descriptor identity | 15.697 / 214,392,832 |
| Persistence diagnostic, both contexts | PASS: saved-artifact inspection completed, original gate unreceived | 15.260 / 187,498,496 |
| receiving-03 normal references | FAIL: valid comparison flag rejected | 16.587 / 214,679,552 |
| First argument diagnostic | FAIL: wrong task constructor namespace; all counters zero | 5.214 / 63,688,704 |
| Corrected argument diagnostic, both contexts | PASS: provider failure reproduced, boundary unreceived | 5.009 / 166,023,168 |

Every owned process is terminal, without resource interruption. All use CPU0,
nice10, one worker and monitored13GiB reserve. There are zero accepted complete
reference selections, admitted receptors/new docking cases, applied source
templates, generated source atoms, energy/RMSD/detection/search calls. The
diagnostic's two synthetic atoms are software controls, not independent cases.
Original source bytes and private payloads are preserved; the later concurrent
routine-metadata additions have the separately recorded disposition below.

## Scientific choices and their limits

The [156-member primary evidence](data/panel_receptor_models_2026-11-08/manifest.json)
has root SHA-256 `8111abe7233e7b21920959c53a8e8407273cbd5f35a822c3875c7bb8faf0d847`
and2,693,276 compressed member bytes. The
[24-member reader/publication companion](data/panel_receptor_models_reader_2026-11-08/manifest.json)
has root `5c21f393735948bc4934962a39225b24753a01a3b4cf6068a91fc9a6620c3b0f`.
Its independent stdlib reader verifies every stored/decoded primary member,
frozen input/producer identity, original failures, two diagnostics and later
metadata additions with zero molecular operations. This PASS authenticates the
records and classifications, not reference/receptor acceptance. Final local
evidence/resource/documentation checks and actual committed-export checks retain
their scope in the machine checkpoint and #33 publication receipt.

Keep both original complexes, their full protein dimer/tetramer, the selected
ligand instances and all original panel criteria. The unchanged
[ligand hypotheses](scientific_panel_ligand_models_2026-11-07.md) remain distinct
from the following protein reference hypotheses. Nominal pH7.4 is a model label,
not experimental pH or an environmental pKa calculation.

| Protein reference | Declared chemistry | Meaning and limits |
| --- | --- | --- |
| 1HSG biological assembly1, protein chains0/A and1/B | Observed PRO1–PHE99 on both chains; ammonium N and carboxylate C termini. Chain0/author A residue25 is ASH, with its stored H on OD2; chain1/author B residue25 is ASP. All other ASP/GLU are deprotonated, LYS/ARG charged, HIS explicitly HIE, CYS reduced neutral, ordinary remaining states unchanged. No declared disulfides or caps. | A fixed monoprotonated catalytic-dyad hypothesis. Choosing chainA/OD2 is explicit and occurs before docking; no crystal proton location or unique bound microstate is inferred. |
| 1STP biological assembly1, protein chains0/A,2/C,4/E,6/G, all author A | Each observed ALA13–VAL133 core is modelled as a separate linear peptide with ammonium N and carboxylate C termini. ASP/GLU deprotonated, LYS/ARG charged, HIS explicitly HIE, CYS reduced neutral, ordinary remaining states unchanged. No declared disulfides or caps. | Intended observed-core tetramer. These charges are a model of its boundaries, not measured experimental endpoint chemistry; residues outside13–133 are not reconstructed. |

The 2017 primary modelling study explicitly compares HIV-protease dyad states
and uses an OD2-protonated Asp25 in its monoprotonated ligand-bound model. Its
structure is 1SDT, not the retained 1HSG. The 2021 indinavir simulation explicitly
protonates chainA for another structure, 1K6C. These support a declared modelling
choice, not transfer of an experimental proton assignment.
[Kulp et al., 2017, Protein structures](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0183327),
[Sohraby and Aryapour, 2021, Methods](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0257916).
Primary NMR work on unliganded HIV protease supports a monoprotonated dyad while
also discussing different inhibitor-dependent states; it does not locate a
proton in 1HSG. [Torbeev and Kent, 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3437676/).

HIE and reduced-CYS choices are explicit conventional reference hypotheses,
not residue-specific titration predictions or a disulfide search. The provider
template factory leaves stereochemistry, environmental protonation, geometry
and force-field coverage unassessed. Keep those limits. Before any application,
inspect actual source compatibility and all retained covalent connections;
incompatible source chemistry stops the selection rather than being overwritten.

The [prior environment evidence](scientific_panel_environment_2026-11-04.md)
retains ten/five observed water groups within5angstrom and the three non-target
BTN copies. Water-site literature prevents automatic dehydration; this increment
keeps their original bytes and leaves actual water/other-occupant modelling
unresolved. It neither silently deletes them nor adds an unqualified water model.
The original two-case panel and at-most24-search proposal stay unregistered.

## Prospective provider selection

This independently receives the **coordinate-free protein reference factory**,
before bound-source geometry completion or chemical-template application. No
terminal generation is needed to construct a reference; missing observed OXT
still requires MolSysMT #558's supported maps/history before application.
The failed anionic-BTN reference and provider #644 remain separate holds.

Use the two unchanged PDB inputs from the
[original input manifest](data/panel_admission_2026-11-04/manifest.json), with
explicit-only connectivity (`get_missing_bonds=False`) and public assembly1.
Public group/chain queries must recover all six previously observed chains,
their exact original chain IDs/names, contiguous author residue IDs, endpoint
identities and99/121 group counts. Query the observed sequences; do not parse
PDB atom tables or restore native molecular systems from inspection JSON.

For every observed chain, form the explicitly declared residue-state list and
call public `physchem.get_peptide_chemical_template` with ammonium/carboxylate,
no declared disulfides. Record source-group versus synthetic-template-group
indices as a declaration association, **not an atom map or applied correspondence**.
Check factory/provenance identities, zero coordinate structures, no indexed H,
stored-H inventory, complete peptide links and explicit unassessed checks.
Formal-charge counts use the provider's declared elementary-charge convention;
independently compare their total with the declared residue charges and the
cancelling +1/-1 termini. This elementary accounting is an analytic hypothesis
check, not a consumer charge-assignment implementation.

Save each of the six native coordinate-free templates through public H5MSM;
reopen them with the public provider reader and compare topology, chemical
assignments, preparation history and coordinate-free status. The synthetic
terminal OXT has no generated or experimental coordinate. Verify caller state
lists, public source/assembly snapshots and all original bytes remain unchanged.
Require two typed refusals: ambiguous HIS and an unsupported C-terminal state.
Neither rejection may mutate the already received templates or source records.

Two fresh complete processes: normal then pm/fs/coulomb, second only after
whole first PASS with identical worker/hypothesis/candidate/input bytes. Each
process selects both original cases and all six chains, without substituting
a smaller/easier case. Stop the whole selection on first failure and preserve
returned artifacts and unattempted members; no outcome-selected retry.

Direct caps per process: PDB conversions2, assemblies2, chain selectors2,
group-table queries6, valid/invalid factory attempts8, template summaries6,
formal-charge reads6, hydrogen inventories6, history reads12, H5 writes6 and
H5 reads6. Existing public snapshot-helper and provider-internal dispatches are
separate. No source mutation, template application, OXT/H generation, charge/type
assignment, energies, RMSD, detectors, browser or docking searches are allowed.

## Composition, resources and custody

Reuse the unchanged whole private faab727ca5b5c9078e2f2e505971fc0ea1cf1a8d provider
wheel SHA-256 c603fbde78a58fcec43d6d0fb8a6b27dabcbef706c19c35b4f5033c8a8dae9c6,
its qualified identical-input9e native, and consumer2ef82d2/private wheel
6db76835f4f3f9c41d06a163cb3a4fbc9e780597bfd89d2fc6a75d29cff31133.
Candidate manifest c7061d409bf59f8598027588f7dd8589edea16c36a58812436fad0c2adb5e76a
binds the whole provider/consumer/Viewer payloads and routine metadata. No
installation, native compilation or public dependency/candidate qualification.

Use Python3.14.10 with isolated/no-site imports, SDK95f693be10c9205ab9b912cb53453710a207bf45
and the unchanged declared unshipped test support. Allow only the exact current
Conda Git for bounded read-only SDK file verification and stdlib `uname -p`;
deny network, compiler, Vina and other subprocesses. Freeze actual producers,
prescription, candidate, hypothesis, inputs and resource declaration before work.

Run serial CPU0/nice10 with one native/build worker. Estimate512MiB group RSS;
cap1GiB group RSS,2GiB address space,CPU45s/wall60s per complete process.
Require at least13GiB available RAM plus1GiB before launch on this host; monitor
the13GiB reserve and owned group throughout. Availability is not a reservation.
No allocation is present; retain the prior bounded Slurm-query failure and fresh
RAM/CPU/swap/pressure observation. This is a finite small reference construction,
not a search campaign or permission to retry held native construction.
Stop only owned work and retain interruptions without automatic heavy restart.
Keep `.molsyssuite/panel-receptor-models-20261108` under #50 review2026-11-14.

## First attempt and prospective receiving-02 amendment

The first complete normal selection stops at the first template summary:
the task incorrectly requires numeric `n_structures=0`. The provider factory
explicitly returns `structures=None`; public MolSysMT `_get_n_structures` returns
`None` for that absent structural domain without interactions. That is a
documented coordinate-free representation, not an established provider defect.
The molecular requirement is no coordinate-bearing domain, not a fabricated
numeric frame count. The original selection remains FAIL; do not relabel it.

Reached calls: one PDB conversion, assembly, chain selection, group-table query,
factory and summary; no charges/inventory/history/H5 read/write is reached.
The first 99-residue reference report is retained, but the whole six-chain
selection and final live/caller checks are unreceived. pm/fs is unattempted.
Resource result: 14.951s, sampled group RSS192,643,072 bytes, no resource
interruption and terminal owned group.

Register a fresh complete `receiving-02` with unchanged two cases/six chains,
states, caps, typed controls, inputs and stop rule. Correct only the task's
coordinate-free check: record the actual summary, require absent `structures`
and public `n_structures is None`, and retain that `None` through persistence
rather than convert it to zero. No coordinate is generated. Source and restored
public representations must still agree exactly; other failures stop the whole
selection. No new source mutation, relaxed chemical control or provider overlay.

## Persistence stop and prospective saved-artifact diagnostic

Receiving-02 reaches the first reference's formal-charge/H inventory and native
write/read, then fails the required exact public-reference snapshot equality.
Its whole normal selection remains FAIL and pm/fs is unattempted. It does not
accept one chain from the incomplete six-chain selection. The native artifact,
original public snapshot and all partial reports remain immutable.

Register one separate read-only diagnostic process with normal and pm/fs contexts:
exactly two public reads of that existing first-reference H5MSM, four public
domain exports (TopologyDict/ChemicalStatesDict), two summary getters and two
history reads. Compare the returned public domains/counts with the original
saved snapshot, without restoring an original MolSys from JSON, constructing a
new template, writing another native file, or normalizing absent/zero counts.
Record actual differences and caller/payload preservation; a completed diagnostic
does not promote the original failed persistence gate. Resource bounds remain
unchanged; no preparation or search follows. Only after this evidence can the
provider's existing persistence contract or missing behavior be identified.

## Diagnostic result and canonical-text receiving registration

The separate diagnostic completes under both unit policies with two native
reads/four public domain exports/two summaries/two history reads. Topology and
coordinate-free status agree; `n_structures` remains `None` and the structural
domain stays absent. The only literal chemical-domain differences are the dtype
descriptors of `components.component_name` and `component_type`: `str` becomes
`string`. Values, null masks, all assignments, bonds, units and history agree.
This is a completed diagnosis, not acceptance of either earlier failed selection.

The exact provider's
[H5MSM format contract](https://github.com/uibcdf/molsysmt/blob/faab727ca5b5c9078e2f2e505971fc0ea1cf1a8d/devguide/h5msm_format.md)
explicitly restores canonical Pandas extension dtypes on read. The owner resolved
[MolSysMT #616](https://github.com/uibcdf/molsysmt/issues/616) by treating equivalent
object/nullable component labels as compatible without rewriting tables or
relaxing chemistry. That append fix is not itself received by this experiment.
No new persistence defect is established from the two documented storage labels.

Register a complete fresh `receiving-03` against that actual owner contract,
with unchanged two cases/six chains, chemical hypotheses, inputs, negative
controls and resource bounds. Require public `msm.compare` to return both
requested component-label comparisons True with `include_none=True`; empty or
missing comparison output fails. Add exactly six direct component comparisons.
Audit the two known dtype descriptors explicitly: source `str` or `string`,
recovered canonical `string`. Require exact equality of their values, null masks
and every other column field; every other component, chemical, history, topology
and structural-count field remains exact. Preserve and publish every descriptor
change; no native object/table, saved snapshot, matcher or codec is normalized
in DockingMT. These are bounded receiving assertions on provider-produced records.

The original strict-annotation selections remain FAIL. The new acceptance is
the full declared coordinate-free chemical reference with the provider's named
canonical text-storage representation, not a claim that raw dictionary dtype
descriptors remain identical. Unsupported changes still stop the whole selection;
no smaller case, omitted chemical field, changed molecular hypothesis or source
repair is introduced. Case/environment/preparation/search acceptance stays open.

## Public comparison stop and prospective argument diagnostic

Receiving-03 fails on the first public comparison before its metadata/value
audit: `msm.compare(..., component_type=True)` raises public ArgumentError for
that Boolean comparison flag. The implementation has a component-type comparison
branch, but the named digester accepts Boolean flags only for `basic.get`.
The freshly fetched upstream digester has the same Git blob as the executed
file. This is a separate suspected provider argument-boundary defect, not a
reason to bypass digestion or weaken the canonical-storage receiving.

The complete six-chain selection remains FAIL; no pm/fs profile or remaining
chains are attempted. Register one separate minimal diagnostic with two fresh
one-atom native MolSys objects, normal/pm-fs contexts, and six public comparisons:
per context, a valid `n_atoms=True` control, the rejected `component_type=True`
request, then the same atom-count control. Capture actual error type/message,
caller preservation and unchanged atom-count result. No protein reference,
geometry, input-file reader, H5 write or new docking case is needed by this
synthetic public-argument reproduction. Constructor cap2, comparison cap6.
Keep all prior failures and their stricter original assertions intact.

The first argument diagnostic stops before construction/comparison because the
task uses a nonexistent top-level `molsysmt.MolSys` alias. The public constructor
is `molsysmt.native.MolSys`. Retain this task failure separately, with zero
constructor/comparison calls. Register argument-diagnostic-02 with that exact
namespace correction and explicit Boolean-scalar recording for returned control
flags; the two synthetic systems, six comparisons, both unit contexts and
expected rejection/control checks are unchanged. This is not a new protein
reference attempt or a correction to the provider's observed comparison failure.

## Administrative shared-environment observation

After the final successful minimal diagnostic verifies its original routine
metadata, the first evidence-sealing attempt detects three added Conda records:
giflib6.1.3, openjdk21.0.10 and xorg-libxt1.3.1. No original package record is
removed or changed; all private provider/consumer/Viewer payloads remain exact.
This task invokes no installer and does not remove or reset those additions.
The failed sealing attempt is retained separately. No further molecular run
follows this change; administrative validation uses the explicitly recorded
current metadata and does not requalify a scientific dependency closure.

A later observation also records swig4.5.1 and tomlkit0.15.2, again with no old
record removal/modification at that observation. The first final-check attempt
stops because it incorrectly expects this shared, unreserved metadata set to
equal the earlier three-addition snapshot. Preserve that administrative failure.
Final documentation checks authenticate task-owned source/artifacts and observe
the live routine metadata separately; they do not certify its scientific closure
or wait for an exclusive environment. Refresh actual composition before future
molecular receiving. The [dated later observation](data/panel_receptor_models_environment_2026-11-08.json)
is historical evidence, not a promise that no later package can be added.
