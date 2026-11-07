# Compare fixed interaction components

Owner: [DockingMT #78](https://github.com/uibcdf/dockingmt/issues/78).
The first public comparison profile is deliberately bounded. Its implementation
and separately recorded receiving do not accept the whole E1 workflow.

## Public call

Start with an existing scored `DockingResult` and the matching `DockingProblem`
for each pose, in result order. Each problem needs its complete `PreparedLigand`,
the actual receptor input and the scoring domain. The
[rescoring notebook](../../examples/rescore_existing_poses.ipynb) retains these
as `prepared_problems` alongside `rescored_result`.

```python
import json
from pathlib import Path

import dockingmt as dmt

comparison = dmt.compare_scores(
    rescored_result,
    'vina_fixed.lig_inter',
    problems=prepared_problems,
    ascending=True,
)
with Path('vina_interaction_comparison.json').open('x') as stream:
    json.dump(comparison, stream, indent=2, allow_nan=False)
print(comparison['display_order'])
print(comparison['groups'])
```

`ascending=True` explicitly chooses lower reported values first; `False` chooses
higher first. The descriptor's unspecified preference is retained. Positions
are **one based** in the supplied result. Equal reported values form a group;
source order only determines presentation within that group. No extra rounding,
uncertainty threshold or molecular tie breaker is applied.

## Admission and actual work

The profile `vina_1.2.7_same_axis@1` receives the interaction component
`lig_inter` of fixed Vina or Vinardo 1.2.7 evaluations in their reported kcal/mol
representation. Request each method separately. It requires at least two unique
nonempty pose IDs and matching nonempty partner/receptor state declarations.
State labels are checked alongside molecular evidence, never used as its proof.

Before molecular work, every selected evaluation must have complete, consistent
input captures, descriptors, values and native reference evidence. This is an
audit of that evaluation; earlier docking origins can legitimately require their
collection provenance. Every shared descriptor/context field must match, except
the actual per-conformation `partner_sha256`. Unknown context fields refuse the
profile. Recorded producer versions and applied execution parameters must also
agree. The complete original descriptors and all different hashes survive.

For each preparation, DockingMT reuses its native MolSysMT export, retaining the
actual exported molecular view and atom map. Final bytes, export-map payload
hash and captured scoring input must agree. The supplied receptor and domain
must also match the recorded inputs. Existing fixed-score geometry admission
checks the original pose against that input.

MolSysMT validates one supplied identity candidate between each actual exported
view and the first view, including a self-witness for the first. Ordered native
atom keys must agree before supplying that candidate. A complete declared graph,
named valid charge/type assignments, common prepared types/torsions/axes and
compatible named preparation policies are required. Unrounded written-axis
charges must agree within `1e-12 elementary_charge`. Native and written axes
retain their own maps. These are provider-owned molecular operations.

The call performs molecular export, geometry reading and chemical-correspondence
checks. It does **not** calculate new energies, hydrogens, charges or atom types.
An installed Vina engine is unnecessary. The available MolSysMT must supply this
declared-graph/export capability; private source receiving does not establish a
compatible public package minimum. Provider failures retain their causes.

An unsupported/incomplete/incompatible member raises an actionable
`ArgumentError` (provider failures propagate). No ordered successful subset is
returned. Other atom axes, components, backend versions and energy
representations need their own received profile. This is an applicability
boundary, not a claim of physical incompatibility.

## Saved decision and scientific limits

The detached finite JSON report retains policy, values, groups/display order,
original ranks, descriptors, source-record digests, selected-evaluation audits,
actual export maps, preparation records, assignments and complete provider
correspondence reports. It is an external comparison decision. The original
poses, scores, result order, ranks and `ranking_history` retain their meaning;
`rank_by` keeps its exact-context contract.

Loading this saved JSON recovers the recorded decision without molecular work.
It does not revalidate edited evidence. Record hashes establish consistency,
not an authenticated producer. The supplied molecular model and its relation to
captured bytes are checked now; this does not authenticate its historical
preparation, experimental validity, affinity, a common native total-score
reference or a shared Vina/Vinardo scale. `lig_inter` uses the separately
received component semantics; the reference record remains required documentary
evidence, without being asserted as a physical input to that component.

## Received execution and remaining scope

The [registered private installed receiving](e1_public_comparison_2026-11-07.md)
passes for five existing poses with four positive method/policy reports, eight
refusals and independent saved JSON receiving. The new consumer wheel has all
64 runtime files; provider/support dependencies remain borrowed and identified.
Twenty provider witnesses and five fresh preparations add no new energies or
H. This receives the comparison profile, separately from full multi-pose
reconstruction/additive continuity and public dependency/platform delivery.
