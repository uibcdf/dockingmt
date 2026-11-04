# Consuming stored chemical readiness evidence

DockingMT preparation now consumes public
`msm.physchem.get_chemical_readiness`, implemented by MolSysMT
[#217](https://github.com/uibcdf/molsysmt/issues/217). Consumer ownership remains
under DockingMT [#5](https://github.com/uibcdf/dockingmt/issues/5) and
[#33](https://github.com/uibcdf/dockingmt/issues/33). The
[executed notebook](chemical_readiness_consumption.ipynb) preserves examples and
the [raw preparation profile](data/readiness/preparation_profile.json).

## Stored coverage and source axes

`prepare_ligand` and `prepare_receptor` retain a compact summary under
`prepared.metadata['source_chemistry']['chemical_readiness']`. The earlier
connectivity-completeness and bond-order-availability fields remain available.
The provider receives the selected molecular source before hydrogen projection,
with `chemical_state='structure', structure_indices=0`. Summary counts therefore
refer to that selected source, not the retained or PDBQT-ordered atom axis.

The summary retains provider schema/method/rule identity, selected state/frame,
state provenance pointer, field coverage statuses/counts, field-origin counts,
connectivity integrity counts, explicit H count, unassessed scientific checks and
software identity. It excludes the provider's per-atom/bond values and index lists.
This bounded summary is additive metadata, not the complete provider report under
the provider schema. To locate individual missing/conflicting atoms or bonds, call
the public provider tool on the same selected molecular source and inspect its
source-index report. No local chemical completion or competing audit is added.

The assessment follows the existing extraction boundary. Crossing-bond counts
describe the extracted selected source; they do not certify its separation from
atoms outside the original preparation selection. Formal-charge coverage is
distinct from partial-charge model assignment. The provider's finite-coordinate
assessment reports nm, and formal charges use elementary charge; numerical values
are not duplicated in this summary. Count/status semantics remain stable under a
non-default pm/fs application policy.

## Limits and preserved admission

Present fields have unassessed origins unless the provider has declared evidence.
Complete connectivity does not validate valence, protonation, stereogenicity,
conformer quality or AutoDock assignments. Explicit H count is neither a complete
hydrogen inventory nor an instruction to add H atoms. The summary has no universal
`ready` flag. Provider failures propagate; there is no fallback audit.

Caffeine illustrates the distinction: its SDF has formal charges and complete
connectivity, while current DockingMT preparation still uses zero-placeholder
partial charges and heuristic AutoDock types. The default Vina rejection remains
in force. Explicit exploratory opt-in remains provisional, and its saved-result
provenance retains the coverage summary. External prepared PDBQT remains unassessed.
The notebook inspects all four original ligand PDBQT files through the provider,
preserving their bytes and declared trees, and reports partial chemical connectivity
and missing formal charges. No input is rewritten to satisfy the audit.

## Exact-source qualification

MolSysMT source: `3edbf8ad0a13b9a56a009c0bd3f707e54b807351`. Both CI and full-matrix
workflows pin this commit for all four Python lanes. Existing ArgDigest/viewer
routes and the dependency-driven source-install variation remain unchanged.
This is controlled-source integration, not public-package dependency admission.

The refreshed suite inventory was inspected and sibling dirty/ahead/behind work
was preserved. MolSysMT continued evolving during this work, including a private
optional `domains` argument for receptor coverage. Qualification therefore uses a
read-only `git archive` of the exact provider commit under `/tmp`, selected through
`PYTHONPATH`, without changing the provider checkout or its installed distribution.
The notebook and benchmark record the imported path and SHA-256 of the audit
implementation (`62b715f2dc63dbee6e4bfd79437b1ed61e82e144e80ef35c88b4878bc9747540`).

Development uses `molsyssuite@uibcdf_3.14`, Python 3.14.7 and Vina 1.2.7; DockingMT
remains installed editable. Seven new consumer cases cover both preparators,
pre-projection counts, compact JSON serialization, incomplete PDB chemistry,
detached summaries/source immutability, structure-assigned partial formal charges,
non-default units and nonfinite coordinate conflicts. The existing real Vina
guard verifies unchanged default rejection, explicit provisional opt-in and summary
persistence through `DockingResult` serialization. The 37 focused cases pass
against the pinned provider in 23.05 s.

## Preparation cost

`python devtools/profile_preparation_readiness.py` compares only the old
`chemistry_evidence` operation from `559f7c3` with the new summary, sharing the
source, selections and other preparation code. Git history containing the baseline
is required. Five paired warm-cache rounds per role alternate profile order after
one warm-up per profile. Raw samples and metadata byte sizes are retained; process
load and OS caches are uncontrolled, so the small sample does not establish a
universal timing bound or memory claim.

The summary adds roughly 3.6–3.7 kB of JSON metadata in the 181L ligand/receptor
examples, without retaining the provider's atom/bond value arrays. Timing outcomes
from the retained paired samples are:

| Selected source | Prior median | Coverage median | Metadata growth |
| --- | ---: | ---: | ---: |
| 181L benzene ligand (6 retained atoms) | 145.74 ms | 151.99 ms | 3,575 bytes |
| 181L protein receptor (1,289 retained atoms) | 160.89 ms | 175.47 ms | 3,734 bytes |

These are observed local preparation costs, not inferred from metadata size.
Chemical qualification, supported charge/type/H/projection methods and complete
preparation remain open; #5 and #33 are not resolved by stored-field coverage.

## Complete local gate (2026-10-03)

All 514 tests pass without skips in 69.45 s against the exact provider snapshot,
on Python 3.14.7 with Vina 1.2.7. Twelve known warnings remain: eleven legacy
H5MSM input warnings and one occupancy-loss warning during concatenation. The
initial full run exposed a stale CI-pin expectation in the configuration guard;
it now agrees with the new provider commit. Ruff lint/formatting (88 Python files),
generated report indexes and diff checks pass. All four notebook code cells
execute with the same interpreter and exact provider implementation digest.

The upstream `fda469f` policy update arrived before push. Its synchronized guide,
policy 1.5.4 caller and Python 3.14 quality baseline are preserved. After reapplying
this work and aligning the policy guard, all 514 tests pass again without skips
in 69.60 s, with the same twelve warnings; the other local gates remain green.

## 2026-10-03 receptor-coverage successor

The [exact residue-coverage integration](receptor_coverage_consumption.md) advances
the CI/full-matrix provider pin to `e8e4fff22`. Grouped receptor preparation now
reuses the stored-field audit embedded in that provider operation. Ligand and
group-free receptor preparation retain the direct stored-field path. The samples
and executed outputs above remain historical evidence against `3edbf8ad0`; the
readiness profiling command keeps its original measurement boundary and labels
that commit as the original qualified source rather than asserting the currently
imported source. New residue-comparison samples are retained separately.
