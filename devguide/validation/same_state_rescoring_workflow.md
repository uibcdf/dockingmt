# Add named evaluations to prepared poses

This guide uses the current public API for **already prepared, matching inputs**.
It runs fixed-pose scoring, not docking or optimization. A complete compatible
public installation is still tracked in [the distribution review](public_candidate_readiness.md).
The [complete rigid two-pose receiving](e1_rigid_continuity_2026-11-07.md#native-receiving-outcome--2026-11-07)
passes original-result reconstruction, matching repreparation, both named methods,
separate component comparisons and independent saved-record reading. This is the
bounded profile accepted under [#78](../archive/qualify_same_state_rescoring.md#bounded-acceptance-and-resolution--2026-11-07).
Earlier [five-pose receiving](e1_installed_receiving_2026-11-06.md) and the
flexible-source attempt below retain their own compositions and limits.
Original scores/ranks/history remain intact; public installation and broader
input models still require separate qualification.

## One prepared pose

You need two existing objects:

- `problem`: a `DockingProblem` with an already prepared receptor and ligand,
  or their PDBQT inputs, and an explicitly chosen physical search box.
- `pose`: the `DockingPose` to reevaluate. Its atom order and coordinates must
  match this problem's prepared ligand. Known state declarations must agree.

For an example of an explicit recipe, see the declared
[3PTB preparation](installed_3ptb_preparation.md); its molecular choices are
specific to that case. Choose and admit the preparation for your own input,
following the [prepared-input scoring contract](fixed_pose_scoring.md). Merely having a
saved docking pose does not supply its corresponding prepared input.

Choose unused evaluation names. This example saves each completed evaluation
before requesting the next one, keeping partial results if a later call fails:

```python
import json
from pathlib import Path

import dockingmt as dmt

current = pose
for method in ('vina', 'vinardo'):
    protocol = dmt.VinaProtocol(
        scoring=method, cpu=1, seed=7, capture_backend_inputs=True
    )
    current = dmt.score(
        problem, protocol, pose=current, score_name=f'fixed_{method}'
    )
    with Path(f'pose.fixed_{method}.json').open('x') as stream:
        json.dump(current.to_dict(), stream, indent=2, allow_nan=False)
```

Use fresh output paths. Each call adds eight components and an evaluation
history entry, returning a detached pose. Existing scores, ID, state labels,
rank and earlier histories remain intact. An existing score name causes a
refusal; it is not replaced. A retained rank still belongs to its earlier
ranking decision. Adding a score does not rank the pose again.

Read values together with their descriptors, and audit the saved record:

```python
name = 'fixed_vinardo.lig_inter'
definition = current.score_definitions[name]
print(current.scores[name], definition['unit'], definition['method'])
report = dmt.audit_pose(current.to_dict())
print(report['status'])
```

The audit checks recorded agreement and missing/contradictory evidence. It does
not establish chemical validity or affinity. For saved files, the existing
[inspection example](installed_scoring_inspection.md) reads individual poses
and explicit result collections without scoring again.

## Complete-source reconstruction example

The maintained [public notebook](../../examples/rescore_existing_poses.ipynb)
starts from an existing scored result and its complete prepared source, resolves
caller-selected bonds through MolSysMT, reconstructs/prepares each pose and adds
both named methods. Supply its explicit input objects before running it; no
qualification supervisor is a user dependency. It saves the original collection,
each completed evaluation, the updated collection and its audit/ledger.

For the received **rigid** source/preparation profile, the unchanged notebook
completes both actual original poses. Eight original scalar scores, their ranks
and histories survive alongside 32 added scalar values and two evaluations per
pose. Both public interaction-component comparisons retain all rows as separate
reports. The [exact receiving](e1_rigid_continuity_2026-11-07.md#native-receiving-outcome--2026-11-07)
records its artifacts, recipe, source/map checks, domains and refusals. The
original generator's post-save qualification remains failed; the complete fresh
saved-result receiving does not relabel that producer.

The earlier [flexible-source attempt](e1_public_composition_2026-11-06.md)
receives only one actual returned pose and leaves its intended two-pose
population incomplete. It is a different profile from the complete rigid
receiving. Full preparations still need their native source and explicit recipe;
inspection JSON is not a complete MM codec.

A standalone pose audit can correctly be incomplete for earlier docking scores
whose provenance belongs to its collection. Keep that evidence with the result
and use `audit_result` for the complete collection. Do not manufacture standalone
evaluations to remove an incomplete status.

## Several existing poses

The same calls can be used in an ordinary serial loop. Pair each original pose
with its **own matching prepared problem** first; each different conformation
needs corresponding ligand coordinates. Reusing one unchanged ligand input
is rejected when a supplied pose's coordinates disagree beyond the documented
geometry tolerance. Different IDs or sub-tolerance differences alone do not
establish that refusal. Do not match atoms or overwrite PDBQT
coordinates in client code to force admission.

For example, if `prepared_cases` is an explicitly constructed sequence of
`(matching_problem, original_pose)` pairs, iterate those pairs and apply the
two calls above. Preserve the source collection and save each completed pose
under a unique caller case ID. Retain failed/not-attempted cases explicitly;
an ordered successful subset must not silently replace the intended population.
This small loop needs no batch/campaign framework.

Reconstruction, per-pose preparation and collection preservation are important
parts of the workflow, not details supplied automatically by `score`:

| Starting input | Current route and limit |
| --- | --- |
| One prepared input for each pose | Public `score(..., pose=...)` checks the prepared geometry and known declarations and preserves earlier observations. |
| A complete molecular source and a verified pose/source map | `pose.to_molecular_system(source)` and `prepare_ligand(...)` provide a candidate public composition. Its reconstruction → repreparation → rescoring path is received for the complete rigid two-pose profile above. The earlier flexible profile remains incomplete. Source axes, charges/types, assignments and declared torsions must be preserved explicitly. |
| External PDBQT or a positional pose without a verified map | Score the admitted prepared bytes directly. Molecular reconstruction cannot infer missing chemistry, a source map or historical hydrogens. |

The earlier private five-pose study constructed new complete conformations and
retained old docking observations as historical associations; it does not
authenticate historical missing H/MM. The later rigid receiving uses its own
complete source authority and actual original two-pose collection. Preserve this
distinction when reading the [earlier public-workflow review](e1_public_workflow_review_2026-11-06.md)
and [bounded criterion-by-criterion resolution](../archive/qualify_same_state_rescoring.md#bounded-acceptance-and-resolution--2026-11-07).

## Comparing the new values

The public [prepared-input comparison](score_comparison.md) receives matching
problems explicitly and checks their actual exports and molecular relationship
through MolSysMT. `compare_scores(result, name, problems=prepared_problems,
ascending=True)` returns a separate report for its bounded fixed `lig_inter`
profile, preserving original ranks/history. The call performs molecular checks
without calculating new scores. The complete rigid two-pose receiving passes
both method-specific comparisons; the earlier five-pose comparison remains
separately attributed. These do not qualify every reconstruction/input profile.

`DockingResult.rank_by(name)` requires identical described contexts and state
declarations. Separately scored conformations normally have different actual
ligand-input hashes, so this operation conservatively refuses them. This is an
intentional admission rule; deleting hashes or descriptors is not a comparison
policy. Equal units, method names or rounded reference values do not establish
comparability.

The received [E1 interaction-component policy](e1_lig_inter_ordering_2026-11-06.md)
orders reported `lig_inter` values separately per method, lower first, **only
for its frozen, fully received case**. It retains distinct input hashes and
complete evidence and produces an external study report. Its notebook is not
a public comparison API for arbitrary caller data, and its report does not
become `DockingResult.ranking_history`. The new public operation consumes actual
matching preparations rather than that notebook's frozen roots. Follow its
own profile and receiving limits for a user comparison. Vina and Vinardo do
not become a common affinity scale.

## Controls available through the public API

| Need | Public control |
| --- | --- |
| Choose a scoring function | `VinaProtocol(scoring='vina')` or `scoring='vinardo'`. |
| Keep successive evaluations | Distinct `score_name` values and the returned pose as the next call's `pose`. |
| Inspect actual submitted inputs | `capture_backend_inputs=True`, retained histories and `verify_captured_inputs(...)`. |
| Inspect the component meaning | `pose.score_definitions` and each history's `reference_energy`. |
| Diagnose execution cost | `collect_timings=True`; the retained phases have explicit second units. |
| Check persistence offline | `to_dict`, `DockingPose.from_dict`, `audit_pose`; `audit_result` for collection-level evidence. |
| Attach a separate caller evaluation | `pose.with_scores(...)`, with explicit descriptors when available; caller declarations are not scientific admission. |

The box determines the map domain. Search-only `exhaustiveness`, `n_poses` and
`energy_range` are unused in fixed scoring. Declare torsions during preparation;
nonempty protocol cuts do not rewrite prepared inputs. Provisional opt-in does
not supply missing charges, types or chemical identity. Defaults, refusals,
geometry tolerance and persistence details are in the
[fixed-pose contract](fixed_pose_scoring.md) and
[score/reference contract](scoring_reference.md).

The [earlier five-pose comparison receiving](e1_public_comparison_2026-11-07.md)
retains its separate two-unit-policy evidence. It is not the same population as
the complete rigid two-pose reconstruction above. Both are bounded private
installed profiles; broader inputs and public delivery keep separate gates.
The snippets require the explicit input objects above and define no new
preparation recipe or scientific search. Preserve original failures and unknowns.
