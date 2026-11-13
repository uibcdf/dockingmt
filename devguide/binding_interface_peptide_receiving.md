# P: finite PeptideMT receiving checkpoint

Owners: BindingMT #112, [PeptideMT #60](https://github.com/uibcdf/peptidemt/issues/60),
MolSysSuite #195. Recorded: 2026-11-13.
Status: owner input handoff published; exact inputs and public consumer receiving pending.

## What is agreed and what is available

The [accepted work order](binding_interface_implementation_plan.md#13-p-consumer-information-nativederived-context-and-comparisons)
and [P1/P2/P3 offer](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6838743888)
define finite consumer cases. Contacts/independent footprints, native SASA/burial,
ionic H0/H1 and H-R2 have their own source evidence. The
[#114 order correction](archive/interface_json_object_order.md) qualifies their
saved ordering separately. None of those local passes establishes PeptideMT
consumer adoption or supplies the outstanding P case data.

Inspection of PeptideMT checkout `359b778293a6dfcc9ef3f8f8e85a5ee038f63d0e`,
its fetched upstream `db043a4` and the complete #112 discussion finds the case
offer, without an immutable P input/expectation package or an implemented public
BindingInterface consumer seam. The three intervening upstream commits change
guides only. No sibling checkout is merged, edited or installed for this finding.
PeptideMT #60 now owns delivery or an explicit unsupported/deferred disposition.
This is an input handoff, not a reported numerical defect or a commissioned
prediction/preparation/docking campaign. Small synthetic or saved examples suffice.

## Receiving ledger

| Case | Owner-supported inputs and independent expectations | BindingMT checks when supplied | Present state |
| --- | --- | --- | --- |
| P1: original/derived | Original and derived MolSys/H5MSM; public construction/export calls; retained/removed/generated and moved-existing maps; omissions, representation and original confidence provenance; affected observation and separately scoped reference. | Original observations stay on their context; derivative results name their actual context; generated atoms gain no invented parent identity/confidence; affected missing reevaluation is unavailable, not zero/current. Admission is operation specific. | Awaiting PeptideMT #60. |
| P2: sequence/source/local | Nonidentity extraction/capping/permutation; actual MolSysMT maps; sequence-relative positions, original chain/residue addresses and local groups; chemical roles independent of generation history. | Map alignment survives reorder/save/read. Generated terminal groups are not sequence positions/deposited residues. A generated H on a core residue is not automatically a cap. | Awaiting PeptideMT #60; scientific sequence interpretation stays with PeptideMT. |
| P3: complete-system views | Full admitted participants/chemistry/occluders, explicit core/terminal atom/group subsets, independent additive sums where valid, coverage/denominator and partition/overlap policy. | Views preserve the fixed full calculation and its original contributors, with no silent population change/recalculation. Covalent caps remain in their participant. No automatic cap penalty/exclusion or affinity claim. | Raw native atomic/group contributions exist; exact consumer view admission remains pending. |
| K/N information boundary | Actual separate permitted-site and no-supplied-localization requests plus public exported/submitted population, held-out reference and independent expectations. | N inherits no localization from reference, K, prior poses/contacts/crops/restraints or viewer state. Preserve requested/exported/executed facts separately. | Offered specification; no fake request/export is treated as execution. |
| Comparison | Two poses of one pair with observable, criterion, frame, coverage/normalization; changed-criterion/coverage/partner adversary and meaningful/unsupported outcome. | Admit the particular comparison; unavailable is not zero. Structural descriptors, model confidence and affinity retain separate meanings. | Pending actual consumer seam/policy; no universal ranking policy added. |

## Current implemented boundaries that admission must respect

`calculate_interface_contacts` and `calculate_interface_burial` operate through
public MolSysMT tools. Their source metadata accepts actual owner correspondence
and requires every selected atom to have an original source identity. A selected
generated/unmapped member refuses that requested parent-source correspondence.
That refusal is not evidence of a completed empty calculation. A separately
identified derivative may use its own local identity; this does not fabricate
correspondence to the original prediction or implement P1/P2 sequence semantics.
The supplied case must make the intended identity/guarantee explicit before any
extension is designed.

Current burial retains the selected A-union-B environment and performs three
fixed-input calculations. Atoms outside that union are not automatically retained
as occluders. Raw `surface_calculation` includes aligned atomic side losses and
group contributions. A reporting subset can inspect those existing contributions;
changing chemistry/population/occluders requires another explicit calculation
context. A case requiring additional external occluders needs a separately admitted
profile; dropping them does not meet its expectation. No new molecular kernel,
generic map framework or contribution-view API is authorized merely by this ledger.

## Evidence and admission procedure

For each supplied case, record the immutable owner source, license/custody,
file SHA-256, producer identities, public export/read calls and independently
stated expected observations/refusals. Record supplied, unsupported and deferred
fields/cases with owner and revisit condition. Exact native map/chemistry needs
belong to MolSysMT; concrete gaps are reported there before consumer workarounds.

Then admit the operation/profile, prerequisites actually checked, caller
preconditions, units, coverage and correspondence. Execute the real public result
and saved readback with positive/empty/unavailable/refusal controls. Reading keeps
original producers/checks historical, performs no hidden recognition/calculation
and earns no new originating-engine credit. Consumer adoption gets its own
PeptideMT evidence; shared agreements/disposition stay in MolSysSuite #195.
An expected JSON example alone is not proof of actual export or executed adoption.

The finite input request is published in PeptideMT #60. Continue independent
BindingMT work while the owner supplies its cases. Regional H-R1 is conditional;
PISA T0/T1 remains deferred optional interoperability. #111 and #30 keep their
own design, installed/public/platform and full-suite gates. Subsequent PHMT
comparison edits are outside the earlier #114 scientific receiving.

Read-only owner snapshots, issue search/deduplication, publication/readback and
bounded documentation/resource receipts retain #50 custody under
`.molsyssuite/interface-p-and-summary-112-113-20261113/`, review 2026-11-14.
No scientific P workflow, shared-prefix change, native rebuild or hosted CI is
produced by this documentary admission checkpoint.
