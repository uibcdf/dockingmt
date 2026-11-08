# Panel source identity and declared ligand models — 2026-11-07

Owner: [DockingMT #33](../pending_proposals/validate_native_molsysmt_formats.md),
with [#49](../pending_proposals/retire_general_molecular_operations.md) for
provider ownership. Starting source: `70354c4e59c55b961036aaca0d76d357228b40bd`.
The preceding goal turn made progress: exact private occupancy/neutral-reference
receiving. The complete Core/Extended/scientific/public/stabilization goal stays
active; this work does not replace the original two-case panel or its criteria.

Current receiving update — 2026-11-08: [the original full ligand selection](panel_references_editable_2026-11-08.md)
now passes normal/pm-fs on the refreshed editable composition, with both typed
refusals, all snapshots/history/readiness/native persistence and observed source/
caller checks. The hypothesis and full assertion block remain unchanged. The
old failed selection and diagnostics below remain historical failures/reproduction
evidence; this is no bound-source preparation or independent docking case.

## Source identity and literature boundaries

The unchanged original CIF metadata declares entry revision 1.3, dated
2024-02-07 for 1HSG and 2024-02-14 for 1STP. The corresponding PDB REVDAT
records carry those dates; legacy PDB record ordinals are not CIF revision
numbers. This binds the previously reviewed page revisions to the actual frozen
metadata bytes, without claiming a cross-format positional correspondence.

The 1HSG title/citation discusses HIV-2, while its deposited entity/source is
HIV-1 and its refined resolution is 2.00 angstrom. Related 1HSH is the 1.90-
angstrom HIV-2 complex. Keep the selected 1HSG HIV-1 entity; do not transfer
another entry's crystallization conditions or protonation from a shared citation.
These are deposit/citation distinctions, not an established reader defect.
[RCSB 1HSG](https://www.rcsb.org/structure/1HSG),
[RCSB 1HSH](https://www.rcsb.org/structure/1HSH),
[Chen et al., 1994](https://pubmed.ncbi.nlm.nih.gov/7929352/).

The deposited 1STP entity has 159 residues, while the existing provider
observation contains ALA13–VAL133. Freitag's historical discussion identifies
13–133 as the Weber core construct, separately from its own 13–139 construct.
This supports selecting an intentionally truncated **observed-core tetramer**
for the diagnostic model; no missing full-length segment is reconstructed.
It does not prove the experimental charge of either endpoint. Terminal chemistry
and generation maps still need explicit admission.
[Freitag et al., 1997](https://doi.org/10.1002/pro.5560060604),
[original 1STP observations](scientific_panel_environment_2026-11-04.md).

## Intended ligand hypotheses, distinguished from observed state

Choose nominal model pH **7.4**, a dimensionless modelling parameter, not an
experimental measurement or an instruction to infer states from the PDB.

| Case | Intended single ligand model | Basis and limits |
| --- | --- | --- |
| 1HSG / MK1 | Neutral indinavir free-base reference, 45 heavy atoms / 47 stored H, total formal charge 0 e. | The historical EMA physicochemical review gives solution pKa values 6.2 and 3.8. Choosing the neutral model at nominal pH 7.4 is a solution-motivated modelling inference, not a determination of the bound state or catalytic Asp protonation. |
| 1STP / BTN | Biotinate carboxylate, 16 heavy atoms / 15 stored H, total formal charge -1 e. | A primary experimental study states a carboxyl pKa of 4.7. The anionic model at nominal pH 7.4 is a declared hypothesis; neither that study nor the neutral CCD determines this crystal's bound microstate. |

[Historical EMA discussion, page 1](https://www.ema.europa.eu/en/documents/scientific-discussion/crixivan-epar-scientific-discussion_en.pdf),
[Uehara et al., 2025, introductory chemical rationale](https://doi.org/10.1038/s42003-025-09176-4).
No solution population or environmental pKa is calculated here. No alternative
state is searched or selected after viewing a docking result. Changing either
intended state needs a separately attributed pre-search amendment.

The [neutral-reference receiving](scientific_panel_provider_receiving_2026-11-07.md)
does not itself receive the anionic BTN definition. The exact neutral BTN source
has carboxyl C11=O11 and C11–O12–HO2; O3 is the ureido carbonyl oxygen.
For this fixed case, request **O12** formal charge -1 e and stored explicit-H
count 0, keeping every other atom assignment, bond and source identity unchanged.
There is no consumer functional-group detector, chemical parser or pH predictor.

## Prospective bounded provider composition

Before execution freeze a case-specific hypothesis and one worker for two cells:
normal then pm/fs/coulomb, only after complete first-cell PASS and identical
worker/candidate/hypothesis/input bytes. Reuse the exact installed faab Python /
qualified identical-input 9e native composition from the previous receiving;
candidate manifest SHA-256
`c7061d409bf59f8598027588f7dd8589edea16c36a58812436fad0c2adb5e76a`.
BTN input SHA-256 is
`9fff069dc9e0387d49c3ef62cab0867a10dae56274931a779fb87f377b9c11ea`.
No new install, individual module overlay, native build or held #642 restart.

Per cell permit exactly one public CCD constructor with the previously received
explicit policies, one detached public copy, one public O12 selection, fourteen
public getter calls, three read-only readiness reports, two valid setter calls
and two invalid setter controls, four public history reads, one H5MSM write and
one independent H5MSM read. Atom/bond getter snapshots compare the original,
detached copy, changed reference, refusal aftermath and restored artifact.
The invalid fractional formal charge and negative H count must raise the public
ArgumentError and preserve the entire observed current snapshot.

Use only public MolSysMT construction/copy/select/get/set/readiness/H5MSM/history
operations. Integer formal-charge counts retain their explicit elementary-charge
convention under both caller policies. Native H5MSM owns the molecular snapshot
and history encoding; any JSON conversion is restricted to returned NumPy arrays
and scalars, with no custom quantity codec. Original neutral constructor reports
remain historical neutral evidence after editing; never forge a new provider
curation report or relabel that old construction history as anionic production.
A DockingMT case receipt binds the explicit hypothesis, actual assignments and
native artifact bytes separately.

Nested public caps per cell: convert 64, get 1024, get_form 2048, select 256,
has_attribute 256, copy 16, set 32. Retain actual counts and all failures.
Network, Vina/native compiler entry, terminal/H generation, template application,
bound-source preparation, energy/search/RMSD/detectors and Viewer actions are
forbidden. No receptor or docking case is admitted by this reference composition.

Resource policy: serial logical CPU 0, nice 10, one worker, 8 GiB available
reserve checked before and during, group RSS 1 GiB, address space 2 GiB,
CPU 45 / wall 60 seconds per complete cell. Preserve interruptions; no automatic
restart after headroom or owned-memory stops. Retain task
`.molsyssuite/panel-model-receiving-20261107` under #50 review 2026-11-14.

## Remaining admission

Ligand model intent is distinct from received assignments and an admitted full
case. Receptor residue/terminal states, consequential Asp choices, water and other
ligand disposition, actual source/template application and preparation remain.
MolSysMT #558 is still open on refresh; no generation map/history is invented.
The core-model choice does not allow silently adding OXT or asserting free charged
termini. Original observed coordinates, all source files, full assembly context,
24-search proposal, evaluation population/threshold and all prior outcomes stay
preserved. E3 #604, #642 construction and actual canvas holds retain their scope.


## First receiving failure and diagnostic registration

The complete normal cell fails at the fractional formal-charge control after
4.297 s / 212,295,680 sampled group-RSS bytes. Two intended valid assignments
and their exact before/after snapshot assertions are reached, but no complete
receipt, native persistence, final source/caller check or second policy exists.
The original selection remains FAIL, not partially promoted. Actual direct
counts: constructor 1, copy 1, selection 1, getters 6, readiness 2, setter
attempts 3, history reads 2; H5 writes/reads 0. The negative H control is unreached.
No resource interruption occurs and the process group is terminal.

The invalid bare value formal_charge=1.5 leaks PyUnitWizard
NotImplementedFormError instead of public MolSysMT ArgumentError. The current
upstream digester has the same content (Git blob
7c390df276b53f7dbc2dc02a836681df7cd7f132): after handling integer and sequence
inputs, it calls puw.get_value on this nonquantity without a type guard. This
observation belongs to MolSysMT's argument boundary; no ArgDigest/PyUnitWizard
implementation defect is established. Two repository searches find no existing
issue for this exact mechanism. Do not catch/normalize the error downstream or
weaken the original typed-refusal criterion.

Register one separate small diagnostic cell, not another reference run: two
fresh one-atom public ChemicalStates, one per normal/pm-fs-coulomb context;
exactly two append_state, four setters (integer control then fractional input
per profile), and four formal-charge getter calls. Capture the actual exception
class, source preservation, caller policy and origins. This deliberately
reproduces the suspected provider failure; diagnostic completion cannot accept
the failed reference workflow. Network/compiler/Vina remain denied and all
resource bounds remain unchanged. The second full reference cell is unexecuted
until the original acceptance criterion can pass on a separately admitted fix.


The first minimal diagnostic stops before state construction because its
stricter task audit blocks stdlib platform.processor's read-only uname -p during
h5py import (2.456 s / 120,209,408 group-RSS bytes). It is a separate task guard
failure, not another provider diagnostic result; no setter/getter is reached.
Retain it as FAIL. Register diagnostic02 with only the exact /usr/bin/uname -p
platform query additionally allowed and recorded; every compiler, other
subprocess, network and Vina call remains denied. The two-profile minimal
selection, source/caller assertions and original full-reference criteria stay
unchanged. No resource interruption or heavy-work restart occurs.


## Confirmed provider handoff and current outcome

[MolSysMT #644](https://github.com/uibcdf/molsysmt/issues/644) now owns the
formal-charge boundary. Diagnostic02 completes in 3.888 s / 224,428,032 sampled
group-RSS bytes and reproduces the wrong exception in both policies while
preserving [-1] e and caller unit authority. Exactly two one-atom state
constructors/appends, four setter attempts and four getters execute. Its PASS
means **minimal reproduction completed**, not provider acceptance. The full
reference workflow remains FAIL/unreceived; reference02 is unexecuted, as are
native persistence and the negative H control. No complete anionic artifact is
claimed from the partial reference run.

The executed/current digester SHA-256 is
4694d0092bf47cf60041cc30edb5ad12eb057377df7c4e3b32a7aea8bc513cdb.
The handoff includes exact source/wheel/native identities, current-file blob,
minimal public reproduction, supporting package versions, source nonmutation
and normal/nondefault unit observations. The owning component controls its fix;
no sibling source change, duplicate issue or consumer workaround is made.

Next seal the failed whole selection and separate diagnostic, verify them with
a fresh stdlib reader, update current plan/checkpoints and publish with [skip ci].
Resource limits and old inputs/artifacts remain unchanged. Keep this campaign
terminal after sealing. **First receiving action is #644 source/artifact
admission before a complete fresh normal/pm-fs reference selection with both
original negative controls**; no fractional truncation, broad catch, changed
input container or skipped control can replace the original criterion.
Public generation maps/history #558 and receptor/environment choices remain
independent prerequisites before bound-source preparation or docking.


## Sealed checkpoint and resumption boundary

The [44-member primary manifest](data/panel_ligand_models_2026-11-07/manifest.json)
is f295848fe26015b31cd5a5bd9d61a53aa2dad6240370c6f2c127dfdd6dde7270
(73,443 compressed bytes). The
[26-member reader companion](data/panel_ligand_models_reader_2026-11-07/manifest.json)
is 6a1eb8911679c7e87cf26067a2f7b83e6fd24be08a605074e572a15712c250f2.
The fresh isolated stdlib reader passes: exact stored/decoded bytes, linked
original four inputs and candidate, documentary metadata literals, current
source-file blob/hash, actual failed-cell counters and separate two-policy bug
reproduction all verify. It runs no scientific imports or molecular operation.
This authenticates evidence and its failure classification, not the anionic
reference's scientific completeness. No complete reference artifact exists.

All three attempted process groups are terminal; no resource interruption.
The full selection is **one attempted, zero completed/accepted reference cells**;
its second policy remains unexecuted. The minimal diagnostic completes only
its separate reproduction question. New native construction, template application,
H/terminal generation, bound-source preparation, energy/search/RMSD/detector/view
operations and admitted docking cases are all zero. Source-file and prefix/
routine byte preservation is independently rechecked at final qualification;
this does not manufacture the failed cell's missing final in-process receipt.

Current ownership: #33/#49 remain partial, provider #644 open at handoff, #558
still owns generation maps/history. Full #73 stays active and incomplete.
Apply final documentation/index/dependency/publication/resource checks and a
fresh committed export; no full pytest or hosted CI pass is implied by those
administrative checks. Runtime/helpers and their exact resource declaration
remain unchanged. No manual CI, source patch or release is part of this increment.
The task controller rejects further reference/diagnostic work after sealing.
Retain original source/producer identities, prior successful neutral receiving,
all new failures, logs, metadata review and private caches under #50 review
2026-11-14. Do not rerun either failed selection merely because capacity is free.
