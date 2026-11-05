# Scientific evidence overview — 2026-11-04

Owner: [DockingMT #29](https://github.com/uibcdf/dockingmt/issues/29), with
[#33](https://github.com/uibcdf/dockingmt/issues/33) for scientific-profile
acceptance. Delivers presentation packet 5 from the
[library audit](../library_audit_2026-11-04.md), reviewed for synthesis at
`be1de30da4c1c5b319533d6b63fcfb2f2266d79c`.

DockingMT has evidence for traceable software behavior and finite pose recovery,
including adverse outcomes. It has no established general recovery probability,
affinity accuracy or complete output-plausibility qualification. The newer panel
remains in admission, with no search results. This page helps a reader distinguish
those claims without repeating calculations or visiting a new publishing service.

## Reproducible finite outcomes

The table is generated from four frozen existing files: the registered 3PTB search
and later evaluation archives, the 5X72 ROOT-order archive and the normal installed
3PTB saved-evaluation report. [The summary JSON](data/evidence_synthesis_2026-11-04/summary.json)
retains exact input hashes, strata, continuous ranges and the original 3PTB
reporting failures. It contains no molecular representation or new measurements.

<!-- BEGIN FROZEN TABLE -->

| Population / stratum | Evaluated results | Returned poses | Cutoff / heavy atoms | First recovered | Any returned recovered | First RMSD range (Å) |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| registered_3ptb / rigid/native | 6 | 41 | 2 Å / 9 | 6/6 | 6/6 | 1.9298–1.9447 |
| registered_3ptb / rigid/negative | 6 | 39 | 2 Å / 9 | 0/6 | 0/6 | 55.5249–65.3124 |
| registered_3ptb / flexible/native | 6 | 41 | 2 Å / 9 | 6/6 | 6/6 | 1.1340–1.9156 |
| registered_3ptb / flexible/negative | 6 | 46 | 2 Å / 9 | 0/6 | 0/6 | 56.9229–66.5009 |
| root_order_5x72 / p59/native | 6 | 25 | 2.5 Å / 24 | 0/6 | 3/6 | 9.8777–9.9106 |
| root_order_5x72 / p59/first_fixed | 6 | 25 | 2.5 Å / 24 | 0/6 | 4/6 | 9.8893–9.9237 |
| root_order_5x72 / p69/native | 6 | 25 | 2.5 Å / 24 | 0/6 | 0/6 | 5.6469–16.5991 |
| root_order_5x72 / p69/first_fixed | 6 | 24 | 2.5 Å / 24 | 0/6 | 0/6 | 5.6498–5.6530 |
| installed_saved_3ptb / native | 1 | 5 | 2 Å / 9 | 1/1 | 1/1 | 1.9337–1.9337 |
| installed_saved_3ptb / displaced | 1 | 4 | 2 Å / 9 | 0/1 | 0/1 | 65.3124–65.3124 |

<!-- END FROZEN TABLE -->

Every denominator here is an evaluated **result/run**, not an independent complex.
The 3PTB rows repeat one protein/ligand hypothesis; the installed 3PTB workflow
does not add another independent complex. P59/P69 are different ligands/sites
within one 5X72 complex. There is deliberately no pooled total or success rate.
All measurements use the recorded receptor frame, positional heavy-atom RMSD,
no alignment and no symmetry correction. The two cutoffs and 9/24-atom populations
remain distinct. A minimum returned RMSD does not describe every state visited
internally by Vina.

| Population | Exact protocol and original evidence | Interpretation and limits |
| --- | --- | --- |
| `registered_3ptb` | [Registered experiment/receiving](3ptb_search.md): rigid versus C1–C cut, native/displaced boxes, seeds 7/42/2026, effort 1/8, CPU 1, at most nine poses; 24 searches/167 poses. Original producer base `105dfc15` plus retained source hashes. | Both native arms recover first poses under the declared 2 Å criterion; displaced controls do not. Dry fixed-state model and ROOT differences remain explicit. The spatial negative is not a nonbinder. |
| `root_order_5x72` | [Prespecified ROOT-order challenge](5x72_root_order_workflow.md): P59/P69, native/first-fixed ROOT order, three seeds, effort 1/8, CPU 1, at most five poses; 24 searches/99 poses. Original base `357cd87f` plus retained source hashes. | P59 returned-set recovery without first-pose recovery supports a ranking/returned-set distinction. P69 has no returned recovery under its declared criterion. This does not isolate sampling, preparation, scoring or filtering causes. |
| `installed_saved_3ptb` | [Saved-pose receiving](installed_3ptb_evaluation.md): seed 7/effort 1 execution, rigid native/displaced controls, later nine-heavy-atom evaluation. Evaluation source `d026434f`; original archive identities remain in that record. | Five/four saved poses are evaluated. Normal and pm/fs receiving are repeat measurements of the same nine poses, not 18 independent poses. No new search is counted in this synthesis. |

**3PTB reporting history matters:** all 24 original searches returned, but all 24
original RMSD reports failed. The separately attributed saved receiver later
evaluated those unchanged results. The original failures are not docking failures,
not observed nonrecovery and not successful original evaluations. The synthesis
checks the original/receiver archive binding and keeps both stages visible.

### Historical narratives outside the generated table

These linked documents retain useful historical observations, but this synthesis
does not have their original standalone experiment manifest/report as a selected
machine-readable input. Their numbers are documented observations, not regenerated
or qualified at the current source:

| Narrative | Recorded result | Purpose and limit |
| --- | --- | --- |
| [181L exploratory baseline](181l_redocking_exploratory.md), source `c044de40` | One run, four returned poses; first positional RMSD 1.8993 Å under a 2.5 Å cutoff; original replay reports zero drift. | Historical provisional-preparation/replay regression. Its raw-PDB replay is not the current named-preparation route. It is not validated docking performance. |
| [External 1IEP prepared-PDBQT control](1iep_external_pdbqt.md), source `c519cca6` | Native run returns one pose at 0.897 Å; displaced run returns three at 22.483–25.364 Å, under a 2.5 Å cutoff. | Upstream prepared-input/adapter evidence in one seed. Earlier defects in coordinate ordering and projected box values are retained; this does not qualify chemical preparation or general predictive performance. |

Both use Vina 1.2.7 with seed 42, CPU 1 and effort 1 in their original records.
Do not replace their original producers with this presentation commit, treat a
successful later regression as the original experiment, or use narrative rounding
as an exact numerical replay oracle.

## What the evidence supports

This compact index follows the audit's E1–E11 claims; the audit retains the fuller
inspection and confidence limits. It does not upgrade the underlying evidence.

| Claims | Best evidence route | Current bounded conclusion / missing evidence |
| --- | --- | --- |
| E1/E2: atom identity and reconstruction | [Prepared reading](prepared_pose_reading.md), [reconstruction](flexible_reconstruction.md), [terminal diagnostic](scientific_panel_terminal_probe_2026-11-04.md) | Complete known-source pose profiles have receiving controls. Partial reading #521 and new terminal reconstruction maps #558 remain separate provider boundaries. |
| E3: scores and executed settings | [Score semantics](score_semantics.md), external 1IEP record above | Adapter transport/fidelity evidence does not calibrate binding free energy or establish Vina model accuracy. |
| E4: saved inspection/recovery | [Installed inspection](installed_result_inspection.md), [prepared recovery](prepared_recovery.md) | Bounded saved workflows are supported; detached JSON is not a complete native molecular/mechanics snapshot. |
| E5/E6: close poses and their ordering | Generated table and original records above | Favorable and adverse finite cases exist. Returned-set and first-pose recovery differ. Additional independent-complex evidence and explicit hypotheses remain needed. |
| E7: preparation/model suitability | [Declared profile](preparation_profile.md), [new panel admission](scientific_panel_admission_2026-11-04.md) | Named fields, hashes, parser admission and charge bookkeeping do not establish experimental state or environmental validity. |
| E8: output plausibility | [Provider inventory](molecular_plausibility_inventory_2026-11-04.md), MolSysMT #555 | Complete output-plausibility acceptance remains unestablished; missing checks are unassessed. No repair is implicit. |
| E9: affinity/screening ranking | [Scientific scope](../SCIENTIFIC_SCOPE.md) | No affinity calibration, screening-specific negatives or corresponding predictive-accuracy dataset is established here. |
| E10: ordinary installation and use | [Private installed receiving](installed_support_receiving.md), [public Viewer failure](public_viewer_receiving.md), [public readiness](public_candidate_readiness.md) | Private installed qualification and source CI are software evidence; actual compatible public delivery and deferred visible C4/C6 remain separate. |
| E11: richer guidance/backends | [Scientific horizons](../SCIENTIFIC_HORIZONS.md) | Architectural provisions and proposals are not comparative scientific benefit. No extra engine or guide is justified solely by this table. |

## Reproduction and maintenance boundary

The subsequent [2026-11-05 seed/effort analysis](saved_search_variability_2026-11-05.md)
adds per-run tables, cumulative top-N and within-seed effort differences for the
same frozen 3PTB and 5X72 campaigns. P59's effort-8 recovered poses first appear
at position four in both ROOT arms for all three seeds, while their first poses
fail. Original producers, separate criteria, failures and denominators remain;
this is additional descriptive resolution, not new independent experiments.
The frozen table above and its four-input synthesis are unchanged.

From the checkout, use the routine Python interpreter:

```bash
python devguide/validation/data/evidence_synthesis_2026-11-04/build_summary.py --check
```

The case-specific producer authenticates four exact source files, reads only saved
JSON, verifies recorded recovery against saved RMSD and checks the generated table
and summary. It imports only the standard library. No molecular read/selection,
geometry, native backend, model inference or generic benchmark framework is added.
Running without `--check` regenerates the same two presentation outputs from the
same immutable inputs; it does not recreate the original experiments.

The original archives, producer scripts, notebooks, failures and scientific
prescriptions remain the evidence authority. This dated synthesis has a bounded
input inventory rather than an automatic claim to include every later experiment.
A changed source or added case requires an explicit reviewed presentation update;
a changed scientific question needs its own registration, not edited historical
thresholds or erased failures. Physical quantities remain those of the saved
schema; a future molecular calculation must use its owning provider.

This is the initial repository presentation for the audit packet. The subsequent
[DMT-044 decision](../DECISIONS.md#dmt-044--publish-evidence-through-a-staged-repository-first-route)
and [local publication policy](evidence_publication_policy.md) now resolve #29's
audience, route and maintenance/lifecycle questions: repository-first presentation,
with rendered documentation when a concrete site or reader need exists. The
original synthesis itself selects no website, periodic service or release claim;
the decision does not upgrade its scientific evidence.
