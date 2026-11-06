---
summary: Qualify provider-backed positional pose comparison and declared geometric clustering for E3.
issue: uibcdf/dockingmt#79
status: active
opened: 2026-11-06
closed:
verification: inspected
area: [analysis, scientific-validation, provenance]
guard:
normative: devguide/MVP.md
blocked_by: [uibcdf/molsysmt#604]
supersedes: []
---

# Provider-backed pose comparison and clustering

## Concrete workflow

E3 in the [complete functional plan](../PRE_STABILIZATION_PLAN.md) compares
selected poses of one declared ligand state against a common rigid receptor.
The first receiving study is bounded to at most 32 existing poses and a retained
reference. Preserve the receptor Cartesian frame, original producer/pose/state
identities, atom populations and correspondences, preparation, scores and units.
No alignment is implicit. A geometric group does not establish a probability,
free energy, independent sample count, affinity or biological correctness.

## Provider route and inspected evidence

The [dated inspection](../validation/extended_provider_scope_2026-11-06.md)
separates current provider main from the qualified runtime. Existing public
positional and chemically constrained RMSD tools must be reused. Source-tree and
issue searches did not identify a cluster operation; this is not proof that all
supported public compositions are absent.

[MolSysMT #604](https://github.com/uibcdf/molsysmt/issues/604) requests an existing
supported composition first, or the smallest reusable bounded pairwise-distance
and geometric-clustering tools. MolSysMT owns molecular geometry, correspondence,
matrix construction and clustering. DockingMT owns population selection,
association with docking records and interpretation. No consumer clustering
loop, metric, atom matcher or coordinate writer is introduced.

## Contract and receiving work

Specify the ordered structures and atom/state populations, metric/profile and
chemical mapping scope, original frame and PBC, physical cutoff and inequality,
linkage, tie/ordering rules and work/RAM limits. Complete-linkage is a candidate
for bounded-diameter groups; single-linkage chains have a different meaning.
The provider owns its supported API/method decision. Incomplete or directional
comparisons cannot be silently filled or symmetrized.

Receive empty/singleton/duplicate and repeated-frame behavior, analytic
translations, atom reorder/symmetry, a three-member distance chain, threshold
boundaries/ties, nondefault units, adverse graph/map/frame/budget cases and source
nonmutation. Representatives need an explicit rule. Choosing a best-scored
member requires separately admitted score comparison; clustering cannot relax
#78's ranking requirements.

Then register and execute a bounded representative pose workflow with actual
provider/consumer artifacts, new analysis provenance, all outcomes and detached
receiving. Preserve old poses/scores/producers and unsupported evidence. Native,
installed, public and visible qualification retain their separate scopes.

## Current disposition

Provider request and consumer acceptance contract are delivered. Runtime
composition and representative execution are unimplemented/unqualified; E3 is
not accepted. This request does not expand MolSysMT's frozen initial 1.0 gates
or require a new docking campaign, generic scheduler or visualization engine.

