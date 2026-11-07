# Prospective E2 ligand-collection admission — 2026-11-07

Owner: [DockingMT #81](https://github.com/uibcdf/dockingmt/issues/81), under
the [small-collection contract](../archive/qualify_small_ligand_collection.md)
and E2 in the [functional plan](../PRE_STABILIZATION_PLAN.md).

**Initial status: source-reviewed candidate draft.** The later
[source-only receiving](e2_source_admission_2026-11-07.md#received-source-population--2026-11-07)
now admits both current interpreted sources; preparation and collection
execution remain pending. The following prescription and source-review
statements retain their original pre-receiving scope. This document identifies existing inputs and
the next bounded receiving evidence. It registers no scientific execution,
native call allowance, numerical hypothesis or resource budget. No download,
MolSysMT/RDKit operation, preparation, energy evaluation or search was performed
for this draft. Historical observations below keep their original producers.

## Question and finite candidate population

Use the existing P59 and P69 source records from 5X72 to exercise a serial
distinct-ligand collection with one fixed receptor/domain, an informative item
failure, independent outcome records and a declared study-level presentation.
The question is whether the public composition preserves identities, preparation
evidence, outcomes and comparison limits across the collection. This is not an
affinity, enrichment, stereoselectivity or screening-effectiveness experiment.

The source PDB names P59 as the (2R) entity and P69 as the (2S) entity of
2-(2-fluorophenyl)-3-phenyl-1,2-dihydroquinazolin-4-one, both with formula
C20 H15 F N2 O. These are two declared stereochemical entities with the same
connectivity, not two conformers of one declared stereochemical state. Current
provider interpretation must still receive the R/S distinction; filenames and
PDB names alone do not establish an admitted native chemical state.

Both entities occur in the same experimental complex at **different sites**.
There are two candidate ligand identities, one complex and no experimental
activity labels. Extra poses, H inventories, prepared projections, repeated
loads, seeds or adverse controls do not increase the ligand denominator.

The [machine-readable candidate inventory](data/e2_ligand_collection_candidate_2026-11-07.json)
retains this declaration and its exact source hashes. The separate
[source-only prescription](e2_source_admission_2026-11-07.md) registers the next
molecular receiving without authorizing native docking or comparison.

## Exact existing sources and custody

All paths below are relative to the repository root. The existing
[fixture inventory](../../tests/data/vina_torsions/README.md) attributes the
unmodified files to AutoDock-Vina commit
`3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645`, under
[Apache License 2.0](https://github.com/ccsb-scripps/AutoDock-Vina/blob/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/LICENSE).
DockingMT's root license does not replace that attribution. These upstream
examples are reference inputs, not chemically validated ground truth.

The exact upstream directory below `example/` is
[`mulitple_ligands_docking/solution/`](https://github.com/ccsb-scripps/AutoDock-Vina/tree/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/example/mulitple_ligands_docking/solution)
(including its spelling). Each local basename below is unchanged upstream.

| Role | Repository path | SHA-256 |
| --- | --- | --- |
| Candidate P59 input | `tests/data/vina_torsions/5x72_ligand_p59H.sdf` | `ef26c05a198a16972efcf8baae644f6b38fd953561f130ee230626088766b08a` |
| Candidate P69 input | `tests/data/vina_torsions/5x72_ligand_p69H.sdf` | `637a992134b2038a0ea3cff0c1f8355ea232720c9eae5347100b7186170fcdf1` |
| Common external receptor | `tests/data/vina_torsions/5x72_receptor.pdbqt` | `25d4e9b5f3932bc2953152dffc2d9dadf13726ae029e5e88712a0dc9525361e6` |
| Common domain authority | `tests/data/vina_torsions/5x72_receptor.box.txt` | `e1e87f640b1976109f7358e871e8e63b6f965ad7e76a54b9e848c10518ac3354` |
| Experimental context | `tests/data/vina_torsions/5x72.pdb` | `3694cbd211e444f0a56150be2fe8ca7f7ed584a7ca448c40d45699ac80490e77` |
| P59 heavy-coordinate context | `tests/data/vina_torsions/5x72_ligand_p59.sdf` | `a476b0d62652664596801fc88024fbd756294e9e2faf9234c8d90c2288aaa373` |
| P69 heavy-coordinate context | `tests/data/vina_torsions/5x72_ligand_p69.sdf` | `e8c2df94d37439aa558f47eee8f20504d01d11b2d974bbb3cf3d9675a88b1ea1` |

The first four files are the proposed execution inputs. The last three retain
experimental/source interpretation context; they are not additional ligands or
instructions to substitute coordinates. The external ligand PDBQT fixtures are
not proposed complete chemical authorities. Preserve original bytes and SD
property blocks in source custody even when a conversion explicitly declines
to retain those properties inside a native object.

The [original ROOT-order study](5x72_root_order_workflow.md) records the roles:
each H-suffixed SDF contains 39 atoms, 42 bonds, 24 heavy atoms and 15 indexed
hydrogens. These are prepared starting conformations near the origin, outside
the common receptor box. Their original H coordinates belong to those starting
conformations; they are not experimental hydrogen positions. Retain them for
the candidate search-input interpretation. Do not generate replacements,
translate them into a reference pose, optimize them or silently place them in
the box. Search admission and fixed-initial-geometry score admission are
different questions.

The unsuffixed 24-heavy-atom SDFs match P59 A201 and P69 A202 in the PDB's common
coordinate frame in the historical receiving. That observation does not map
new hydrogens or admit a future source through positional matching. No new RMSD
or experimental-reference recovery measurement is needed for this E2 increment.

## Fixed environment and site limitation

Use the same exact protein-only rigid receptor PDBQT bytes for both candidates.
The historical source study records 1,481 PDBQT atoms and absence of the other
experimental ligand. Its external preparation, charge/type origin and chemical
readiness remain externally prepared/unassessed unless separately evidenced;
PDBQT bytes do not supply a complete native receptor chemical history.

The pinned box file declares center `(-15, 15, 129)` angstrom and dimensions
`(30, 24, 24)` angstrom. It covers both experimental sites. This joint domain
is a deliberate functional collection case, not a claim that P59 and P69 bind
the same site. Keep its original physical frame and authenticate the actual
native box after unit conversion. A current web tutorial's conflicting 1IEP
snippet is not this domain's authority.

Do not import the fixed-companion receptor arms into this population. P59 with
fixed P69 and P69 with fixed P59 have different receptor contents and hashes.
The [seven-stage synthesis](5x72_control_synthesis_2026-11-05.md) preserves those
separate scientific contexts. Their scores, poses and favorable/unfavorable
observations do not become new E2 runs or a common-environment ligand ranking.
If a single-site question is required later, admit a new site policy explicitly
rather than relabeling this joint-domain case.

## Next receiving: explicit current source interpretation

The next useful increment is admission of these two exact sources, before any
new energy or search. The reviewed MolSysMT checkout is
`9e1f1b1ad8bf09446374ab6f04ca7208e2717936`; a future receiving must seal its
actual provider, optional RDKit, DockingMT and support-artifact identities. An
installed snapshot and historical helper are not interchangeable producers.

Use the public supported composition, with each intermediate retained as a
distinct declaration:

1. Convert each unchanged H-suffixed SDF through
   `msm.convert(path, to_form='molsysmt.MolSys', stereo_engine='rdkit',
   discard_properties=True)`. This explicitly authorizes SD-property loss from
   the native representation and the provider's interpretation of declared
   stereochemistry. Raw source properties remain preserved separately. Do not
   perform caller-side or additional coordinate-based stereo inference or edit
   the CTAB record. Retain the provider's actual SDF interpretation, including
   its supported wedge/3D handling.
2. Explicitly convert that interpreted object to `rdkit.Mol`, then back to
   `molsysmt.MolSys` through `msm.convert`. This is a fresh provider-interpreted
   chemical representation with an explicit RDKit sanitization/aromatic/H-count
   policy, not silent normalization or assignment of a template to the original
   native source. Preserve both objects' declarations and the intermediate
   producer choice. A refused conversion stays refused; no local fallback.
3. Inspect both representations using public
   `msm.physchem.get_chemical_readiness` with one explicit structure and its
   associated chemical state. Receive explicit CIP on each new authority with
   `msm.physchem.get_cip_stereochemistry(..., engine='rdkit',
   from_coordinates=False)`. The initial SDF interpreter already records its
   source stereo interpretation; partial original chemistry is not forced
   through a complete-graph CIP query. Readiness supplies field coverage and
   unassessed checks, not a universal chemical-validity certificate.
4. Retain conversion atom axes, native IDs, element/connectivity declarations
   and unchanged physical coordinates through public reports and getters.
   Receive the predeclared fixture axis using the actual fields; do not guess
   a correspondence. Require complete provider graph evidence on the newly
   interpreted authority. The historical source-index-7 R/S observation is an
   expected control, not permission to insert labels or assume today's axis.
   Do not implement a downstream matcher or require P59/P69 same-state
   equivalence as admission of these distinct stereochemical entities.

The initial native SDF may legitimately retain unknown virtual/implicit H or
aromatic fields. RDKit interpretation can make those fields explicit. Preserve
that declared transformation and its before/after readiness coverage; a complete
graph witness on the new authority does not retrospectively certify the partial
source as equivalent, complete or chemically valid. Axis/coordinate custody and
received chemical authority have separate scopes.

The current SDF adapter documents support for the blank legacy version marker
as V2000, explicit source hydrogens and optional declared-stereo interpretation.
Older dialect refusals in the historical workflow describe their original
provider, not a demonstrated current blocker. Public RDKit conversion requires
the chemical prerequisites it actually receives; it must not be assumed to
complete every missing field. Missing H-count declarations must not be filled
with local zeros. A source read, normalization, stereo or readiness failure
excludes that candidate from the proposed native population until its actual
cause is reviewed; it does not authorize repair or substitution.

| Receiving field | Source-reviewed expectation or proposed choice | Current E2 disposition |
| --- | --- | --- |
| Source identity | Exact P59H/P69H hashes above; raw properties retained | Inventoried; not newly interpreted |
| Native populations | 39 source atoms / 42 bonds / 15 indexed H each | Historical expectation; not currently received |
| Chemistry | Full elements/connectivity/order, formal charge, aromaticity, stereo and H policy needed by the chosen provider profile | Coverage and any unknown/conflict values pending |
| Distinct entities | P59 R and P69 S; source index 7 historical control | Current provider labels/maps pending |
| Geometry | Preserve each original 39-atom SDF conformation physically | Current round-trip/map evidence pending |
| State IDs | Candidate labels `e2-5x72-p59` and `e2-5x72-p69`; separate run/state declarations | Provisional caller labels; no admitted chemical identity yet |
| H treatment | Retain the 15 indexed source H; no H generation proposed | Compatibility with virtual/implicit-H declarations pending |
| Named charges/types | Fresh explicit Gasteiger-Marsili / AutoDock4 chemical-environment assignments if a later preparation is registered | No current assignments or claims of historical mechanics restored |
| Torsion policy | Minimal rigid `active_torsion_bonds=[]` proposed for functional admission; historical two-cut policy remains historical | Must be fixed before preparation; no current prepared object |
| Projection/export | Provider/DockingMT maps, merged-H accounting, finite charges/types, tree and actual PDBQT bytes/capture hash | All current preparation evidence pending |
| Receptor/domain | Fixed external protein-only bytes / pinned joint domain | Custody identified; actual native capture pending |

Named charges and types, if later registered, use public
`msm.build.assign_partial_charges(method='gasteiger_marsili')` and
`msm.build.assign_autodock_atom_types(typing_scheme='autodock4',
method='chemical_environment')`, followed by public `dmt.prepare_ligand`.
Those are new assignments, not recovered historical parameters. Their reports,
source-state binding, charge units/total, full typed axis, H merge ledger and
prepared projection must be retained. Do not restore MolecularMechanics from
H5MSM 0.5 or inspection sidecars. No historical 25-atom output count, ROOT order,
charge sum or successful export is imposed as a current result in advance.

The source-admission receiving should emit a finite manifest, original input
hashes/license, provider identities, per-candidate conversion/readiness/stereo
reports, atom maps, physical-coordinate checks and an explicit admit/refuse
disposition. Source property loss, residual unknowns and unassessed checks must
remain visible. No new fixture download or generated dataset is needed to
answer this admission question.

## Subsequent three-item serial control, not yet registered

Only after source/preparation admission and a separate registered scientific
prescription, consume the existing `dmt.dock_many(..., on_error='record')`
composition serially:

| Position | Caller run identity | Molecular identity | Intended disposition |
| --- | --- | --- | --- |
| 0 | `p59-main` | Admitted P59 state/preparation | Successful finite result, possibly successful-empty |
| 1 | `p59-unsupported-intent-control` | Same admitted P59 state/preparation | Expected capability refusal for an explicitly nonempty `constraints` request unsupported by Vina |
| 2 | `p69-main` | Admitted P69 state/preparation | Successful finite result, possibly successful-empty |

The control is a deliberately unsupported execution request, not a third
compound, invalid chemical state, inactive ligand or invented pharmacophore.
It should refuse before native work; preserve its concrete exception/code and
the following outcome. Missing optional engines are not this intended control.
If either scientific item fails or is empty, retain that outcome honestly; the
desired failure-between-nonempty-successes evidence has not thereby passed.

The caller manifest must associate input position with study/run/ligand/state
IDs, exact prepared/receptor/domain hashes and original outcomes. Keep each
`DockingResult`, local pose IDs, original scores/ranks/history and producer
unchanged. Record submitted items (three), distinct candidate ligands (two),
attempted items, native invocations, completed outcomes, returned poses,
evaluated representatives, refusals, failures, missing and successful-empty
results separately. Unexpected memory/process-control/source-iterator failures
propagate; no automatic retry, reseeding, extra ligand or favorable replacement.

## Prospective study comparison and remaining gates

Before scientific registration, freeze one explicit comparison policy. The
minimal proposed policy is to select the original backend-ranked first pose
from each nonempty successful ligand result and present its recorded `vina`
total docking score in ascending order, within one declared Vina version,
weights, grid settings, fixed receptor/domain and preparation profile. This
uses the four public docking scores and their actual descriptors. Preserve
the complete **five-column** native `Vina.energies()` record
(`total/inter/intra/torsions/intra_best_pose`), including its fifth native
reference column, alongside those public scores. It does not substitute an
eight-component fixed `Vina.score()` total. The
proposal is not yet an admitted cross-ligand comparison or a selected native
protocol. Backend version, seed, effort, requested poses and all resource/call
bounds still require the later prescription.

Record original and display units, physical conversion and the native score's
actual definition/reference semantics. Different ligands have intentionally
different molecular states and potentially different native internal reference
contributions. Do not assert a shared unbound reference from equal rounded
numbers, subtract invented references, combine Vina/Vinardo scales or interpret
the order as binding affinity. The joint two-site domain further limits even
this empirical prioritization to the declared functional case.

Missing/nonfinite/unknown-definition/context-incompatible values, failures,
refusals and successful-empty results remain explicitly unranked; no zero or
infinite imputation. Equal recorded values remain ties, with input order only
for stable presentation. Predeclare any precision/tie tolerance before seeing
values; no post hoc epsilon or best-of-seeds selection. The adverse control
stays in outcome denominators and outside the two-ligand order. Preserve
selected-pose attribution and any inability to compare rather than forcing
two numeric rows.

This is caller-owned study policy over separate outcomes. Do not concatenate
ligands into one result, weaken `rank_by`, or use E1 `compare_scores` as a
cross-ligand identity gate. No runtime API/schema extension is selected by this
draft. Existing composition must be received before proposing one.

Whole E2 remains pending: actual current source/chemical/preparation admission;
prospectively registered serial native evidence and controls; an admitted
study-comparison policy; honest outcome/pose/ligand denominators; exact-source
installed receiving; a fresh detached record-only reader, nondefault-unit
evidence and immutable custody. The two-source admission alone closes none of
those later gates. The independent scientific panel, E3/E4/E5, public delivery
and functional pre-stable delivery, open-ended 0.x stabilization and 1.0.0
readiness retain their own scope and evidence requirements under
[DMT-048](../DECISIONS.md#dmt-048--let-pre-10-versions-follow-verified-progress).

#81 owns this collection workflow. #33/#49 retain chemistry/provider integration
ownership; #6/#17 retain the historical 5X72 scientific questions. Closed #36
provides the serial executor, not this study's acceptance. No current provider
defect is established by static inspection: hand any reproduced uncovered
molecular capability to MolSysMT with its actual evidence. Preserve the E4
computational hold and all shared-workstation limits. The next increment
registers a separate source-admission prescription and exact receiving
artifacts before molecular work; this draft itself starts no computation.

## Subsequent bounded receiving — 2026-11-07

This original candidate declaration retains its prospective dispositions.
[Source admission](e2_source_admission_2026-11-07.md),
[named preparation](e2_preparation_receiving_2026-11-07.md) and the later
[native collection/independent receiving](e2_native_collection_2026-11-07.md)
now pass their own complete selections. [#81's archived acceptance](../archive/qualify_small_ligand_collection.md)
resolves this finite two-ligand joint-domain workflow; original raw files,
candidate inventory, populations and producers are not relabelled. Follow the
maintained operational checkpoint for the next independent work.
