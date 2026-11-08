---
summary: Qualify provider-backed positional pose comparison and declared geometric clustering for E3.
issue: uibcdf/dockingmt#79
status: blocked
opened: 2026-11-06
closed:
verification: inspected
area: [analysis, scientific-validation, provenance]
guard:
normative: devguide/MVP.md
blocked_by: [uibcdf/molsysmt#604, uibcdf/molsysmt#645]
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

## Experimental-reference receiving checkpoint — 2026-11-08

The [separately registered reference selection](../validation/e3_experimental_reference_2026-11-08.md)
reaches public SDF interpretation and fixed-state H generation, preserving the
experimental heavy coordinates within the original 1e-12 angstrom tolerance.
Full39 correspondence reports two candidates but zero retained maps: the indexed
H's stored implicit-H permission differs between the two public producers.
Both saved axes retain R at atom7; this does not waive the strict policy check.
The whole normal selection stays FAIL; pm/fs and rigid25/persistence are unreached.
An earlier task Git-audit failure remains separately failed with zero molecules.

[MolSysMT #645](https://github.com/uibcdf/molsysmt/issues/645) now owns the explicit
H-policy normalization/composition question. First receive the provider's
supported route and register a complete fresh reference selection. No local
normalizer, guessed map, graph relaxation or repeated native search is added.
#604 still owns matrix/clustering; every original E3 criterion above remains.

## Provider and population admission checkpoint — 2026-11-07

The [fresh source/record inspection](../validation/e3_provider_admission_2026-11-07.md)
verifies all 193 E2 archive members and identifies the three original P59 poses
without changing their producer, scores or state. P69 remains a different-state
control candidate. The experimental-reference SDF is identified by exact bytes;
graph/H representation, chemical correspondence and common-frame admission
against rigid25 remain unperformed. Excluding H from RMSD does not normalize
the provider's required indexed-H representation.

At MolSysMT fetched `82bfa1c82f1d48035679fa4630e81a2506b67bd6`, six inspected
metric/correspondence/export/test files remain identical to preserved local
`9e1f1b1`. Inspection and still-open #604 with zero comments provide no accepted
N×N/clustering composition. This theme is blocked on that provider contract,
not resolved or reduced to RMSD alone. Preserve every original criterion above;
no local algorithm, scientific import, RMSD, search, installation, sibling
checkout or pin change occurs.

The next E3 calculation needs the applicable supported provider route: #645 for
reference/H-policy normalization, #604 for pairwise/clustering, with a separately
registered whole selection. The original static admission below remains
historical; the new failed reference attempt does not make E3 accepted. Meanwhile,
[E4's independent saved-analysis admission](../validation/e4_saved_analysis_admission_2026-11-07.md)
can be prepared without hidden recalculation; its local/visual holds remain.

