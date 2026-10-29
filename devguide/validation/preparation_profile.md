# Declared preparation and provenance profile — 2026-10-29

Owners: [#33](https://github.com/uibcdf/dockingmt/issues/33) (representation and
profile), [#5](https://github.com/uibcdf/dockingmt/issues/5) (preparation/scoring
acceptance), and [#4](https://github.com/uibcdf/dockingmt/issues/4) (source and
scientific decisions). This follows the [Core audit](core_mvp_audit_2026-10-28.md)
and [domain-provenance implementation](domain_derivation.md).

## Decision and meaning of support

The first supported molecular workflow is **one explicitly declared protein and
small-molecule state, a rigid receptor, and a rigid or explicitly cut ligand**.
General molecular work is composed through public MolSysMT. DockingMT records
scientific choices, builds its domain/protocol, runs Vina and preserves results.
This document defines the bounded admission contract; it adds no runtime preset,
chemical model, automatic state choice or new default.

A workflow is supported when its actual input representation and requested
operations pass their documented contracts and retain the evidence below.
That does not upgrade `assess_preparation` from `unassessed` to scientifically
validated. The absence of provisional reason codes means that known placeholder
markers were not declared, not that experimental protonation or the scoring
model has been certified. The current [assessment contract](preparation_assessment.md)
and its safe execution policy remain unchanged.

## Molecular and engine boundary

| Boundary | Admitted workflow | Limits and separate ownership |
| --- | --- | --- |
| Source and structure | Public MolSysMT conversion; one selected structure with an explicit chemical hypothesis and available source/state association. | Select among structures before preparation; do not infer experimental state or repair incomplete data in DockingMT. |
| Receptor | Explicitly chosen rigid protein state; declared termini, disulfides, waters/ions/cofactors and any intentional repair or attribute loss. | The 3PTB evidence is a dry, protein-only hypothesis, not general water, metal or cofactor support. General preparation belongs to MolSysMT. |
| Ligand | Declared chemical state and complete graph for the native known-source reader. | Source-free/partial representations are a separate compatibility route, not evidence of complete chemistry. |
| Hydrogens | Explicit public fixed-state H generation when requested, with original maps, parents and loss reports. | No implicit H addition, pH inference or environmental H refinement. The receptor workflow composes H generation before `prepare_receptor`. |
| Charges | Complete finite supplied charges, or an explicitly chosen MolSysMT assignment. The declared 3PTB model is `gasteiger_marsili`. | Supplied zeros are legitimate data. Missing charges do not become zeros; unnamed supplied values do not acquire named attribution. Other models need their own recorded scope. |
| AutoDock labels | A valid named public MolSysMT assignment, or explicit typing options; the declared case uses `autodock4` / `chemical_environment@1`. | No name-based classifier, bare-label model inference or automatic method choice. Field coverage alone does not establish chemical suitability. |
| Projection | Public MolSysMT nonpolar-H reduction and charge transfer, retaining original/derived assignments and atom maps. | Unknown H inventory rejects; no consumer inventory inference, H-parent algorithm or charge correction. |
| Ligand flexibility | Rigid by default, or explicit source-axis cuts accepted by MolSysMT and retained with the actual ROOT/BRANCH policy. | No automatic torsion choice, receptor flexibility or outcome-selected ROOT. Complete disconnected single-ROOT inputs retain the provider refusal under MolSysMT #214. |
| Export | Public MolSysMT native PDBQT writer; actual written order and completed export map. | Native presentation may change bytes. Preserve the actual view/map/payload rather than rebind an older map to new output. |
| Pose reading | One complete native chemical state, read against its actual export through public MolSysMT. | External/unmapped, partial and multiple-state profiles retain the explicit bounded route in [the reader contract](prepared_pose_reading.md), with review 2026-11-04 under #49/#33. MolSysMT #521 remains open. |
| Domain | An explicit physical box, or a selection-derived box with its recorded recipe, and the actual backend projection. | Explicit legacy boxes need not invent a recipe. Visible C4/C6 acceptance remains #52. |
| Scoring/search | Explicit Vina protocol, actual backend/version/options, named score semantics and complete returned results. The declared 3PTB case uses Vina 1.2.7, `scoring='vina'`. | AutoDock4 atom labels do not declare an AD4 scoring run. Vina scores and rank are not affinity measurements or general accuracy claims. |

Successful PDBQT parsing establishes format acceptance. An export/readback control
establishes representation consistency. Neither is a redocking result. Missing
provider capabilities are proposed in MolSysMT, never implemented here to make
this profile appear complete. No PharmacophoreMT operation is needed by this
workflow; future pharmacophore needs retain that provider's ownership.

## Source provenance is a bundle contract

The supported human workflow keeps a linked case bundle, using the existing
admission, qualification and result records. No new molecular snapshot or generic
archive format is introduced. A reproducible case retains:

1. **Original input identity:** acquisition/source identifiers, exact input-byte
   hashes, chosen atom/structure axes, original reference and original-to-derived
   correspondence. A file hash identifies bytes; it is not chemical identity.
2. **Declared decisions and transformations:** human state labels separately from
   provider state IDs, explicit state/terminus/disulfide and exclusion choices,
   template/model identities, allowed losses and original provider reports/maps.
   Unknown pH or experimental validity stays unknown.
3. **Execution evidence:** actual prepared/written correspondence, submitted
   receptor/ligand bytes and hashes, domain and numerical projection, actual
   protocol/backend/software identity, every result or failure and score context.
   Enable the existing `capture_backend_inputs=True` when retaining replay bytes.
4. **Persistent links and interpretation:** a manifest binding the records and
   their producer identities, preserved references/evaluation criteria and all
   attempted/completed/failed denominators. The notebook expresses scientific
   decisions and interpretation; reusable molecular operations remain in MolSysMT.

An already prepared or native object has no inherent knowledge of the file from
which a caller previously constructed it. Its `source_fingerprint=None` is honest.
A descriptive `state_id` is not an experimental state measurement. Do not fill
missing fields from filenames, object identity, equal atom counts or an unrelated
source hash. The case's actual source maps and admission records establish the
link; a standalone prepared-result JSON does not become a self-contained original
molecular source record.

`DockingProblem.from_dict` requires explicit receptor/partner objects for stored
object inputs. Captured PDBQT can support backend-byte replay, but cannot recreate
missing complete chemistry, named assignment history or original source decisions.
General native mechanics persistence remains [MolSysMT #256](https://github.com/uibcdf/molsysmt/issues/256).
An arbitrary-input persistence/bundle helper is **not delivered by this decision**;
#4 remains partial for that broader workflow. Supported case-level provenance does
not require inventing a molecular storage implementation downstream.

## Evidence and interpretation

The [original prospective protocol](3ptb_prospective_protocol.md),
[admission](3ptb_admission.md), [24-search population](3ptb_search.md) and
[human workflow qualification](data/human_3ptb/qualification_2026-10-20.json)
retain their own sources, package/native identities, chemical hypothesis and
unchanged bytes. Under that historical population, both native-box arms recover a
near-reference rank-1 pose in six rows each; displaced boxes recover none among
the returned poses. This is finite, one-case evidence under the registered metric,
not an affinity, nonbinder, enrichment or multi-complex performance experiment.
The later human run is a separate five-pose result, not another execution of those
24 rows.

Current software qualification at `8d40870724e21cf579ce4d5289d46b5d8a5aaa1c`
passes 1,301 source tests per Python 3.11–3.14 and all exact-head CI jobs, with
ordinary installed checks separately recorded in [#55](https://github.com/uibcdf/dockingmt/issues/55).
That supports current software contracts; it does not relabel an older scientific
experiment as execution on the current composition.

### Separately registered current-composition admission

[Pre-execution registration](https://github.com/uibcdf/dockingmt/issues/33#issuecomment-6501548627)
freezes the unchanged chemical hypothesis and an admission-only control on the
ordinary installed `0.0.0+207.g8d40870` artifact with qualified MolSysMT
`e395e52646dab2ecb480d3d67aa7254be99b8524`.
[Registration](data/preparation_profile_2026-10-29/registration.json) and
[producer](data/preparation_profile_2026-10-29/producer.py.txt) are retained
separately. Native maps, score, optimization, randomization and docking are blocked.

The preselected controls cover compressed input, original heavy identity and
coordinates, declared states/disulfides, both torsion arms, actual named fields
and charge conservation, native input parsing, actual export/map/native readback,
pm/fs units and honest absence of a prepared problem's original-file fingerprint.
Reader input is its actual export, not a generated pose ensemble. The original
helper's 24 prospective rows are only a template in this control; no search is
attempted, and the historical population is neither rerun nor reset.

The [executed receipt](data/preparation_profile_2026-10-29/receipt.json.gz)
passes for both policies: receptor 2,011 atoms, rigid and flexible ligand 13 atoms
each; projected totals +6 e and +1 e within 1e-8 e. Both ligands have one complete
native chemical state, accepted native input parsing and successful readback
against their actual export/map. The pm/fs control preserves exact PDBQT payloads
and backend box projections and restores the caller policy. All 44 registered
historical/authority files remain unchanged. No native maps, energy, optimization,
randomization, docking or generated poses occur. Four expected provider warnings
report the explicitly accepted occupancy/B-factor loss across the two admissions.
Preparation assessments remain `unassessed` with no provisional reason codes.

The ordinary wheel and its 58 runtime files retain the previously qualified
identity; this control verifies installed import origins, runtime byte hashes and
the native provider digest before execution. Source and input identities, maps,
reader reports, charge audits and limits are retained in the receipt. The new
receipt has no machine-specific filesystem paths.

A separate source-free ordinary-installed guard selection passes **108 tests** in
63.79 s, zero skips, 35 warnings: required charges/types, declaration assessment,
both public projection consumers, actual writer and known-source reader. These
are software controls, not 108 scientific cases. An initial selection named two
nonexistent modules and was refused before pytest; the corrected selection alone
qualifies. [Indexed evidence](data/preparation_profile_2026-10-29/manifest.json)
retains the separate admission and test receipts; overlapping counts are not added. Useful verification artifacts have
owner #33/#50 and review 2026-11-05; no automatic deletion. Machine-specific paths
and environment diagnostics remain in the local operational record.

## Next acceptance gates

- The current-composition admission is complete. Additional scientific experiments
  must have their own question, registration and informative controls; this receipt
  does not authorize a new search or expansion of the historical population.
- #33 remains partial for remaining representation/input profiles and complete
  retirement of its tracked verifier; receive MolSysMT #521 when delivered.
- Resolve #5 for its original unsafe placeholder mechanisms, protected by the
  [charge](../../tests/test_required_partial_charges.py),
  [typing](../../tests/test_required_autodock_types.py) and provider-consumption
  guards. Its remaining scientific model/scoring question is retained explicitly
  in #33, with no change to `unassessed` or the execution safeguard. This transfers
  an existing follow-up to its profile owner; it does not declare that question
  solved. Additional chemical/model claims need registered informative cases.
- #4 remains partial for general prepared-source and replay persistence. The
  bundle contract above states the supported bounded route and its explicit gaps.
- Resume visible C4/C6 only on the maintainer's decision. Public delivery keeps
  #30/#47 gates. This work changes neither runtime nor dependency defaults.
