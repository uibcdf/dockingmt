---
summary: Existing summary controls fail on frozen producer fields and pm/fs floating equality.
issue: uibcdf/bindingmt#113
status: resolved
opened: 2026-11-12
closed: 2026-11-13
severity: medium
verification: measured
area: [tests, persistence, units]
guard: tests/test_redocking_summary.py::test_retained_native_reports_show_positive_and_displaced_controls
normative:
blocked_by: []
supersedes: []
---

# Redocking-summary receiving controls

## What

First #112 regression exploration reproduces two existing failures on unchanged
`630f6d6f5595723135fb934d0afdefeea5dce8b2` in fresh source exports:

- `test_retained_native_reports_show_positive_and_displaced_controls` receives
  required evaluator-metadata refusal before its expected `Incompatible` error.
  The frozen producer uses `dockingmt_version`; the reader requires `bindingmt_version`.
- `test_any_returned_recovery_can_occur_beyond_every_requested_top_n` observes
  `8.999999999999998` versus exact `9` under pm/fs.

## How and evidence

Both guards are in `tests/test_redocking_summary.py`. Baseline witnesses and
original expanded selections are retained at
`.molsyssuite/interface-data-core-112-20261112/` (`baseline-01`,
`baseline-pmfs-01`); temporary exports retire. Preserve frozen `cases.json` bytes
and original producer identity. The normal baseline records 27 passes/5 failures:
these include four missing-`unyt` cases, an independent test-environment prerequisite.
The pm/fs baseline independently reproduces the exact floating assertion. The
maintainer subsequently installed `unyt`; the original failed attempts remain
preserved and final complete core-helper controls are rerun with that backend.

## Why and what was refuted

These do not originate in BindingInterface or the unchanged finite-JSON helper
relocation. They prevent calling the broader exploratory selection green. Missing
optional test backends do not establish a PyUnitWizard defect. No docking, molecular
preparation, new native operation or scientific campaign was executed.

## Scope and acceptance

BindingMT owns an explicit historical-input receiving/translation policy and a
meaningful numerical tolerance for the analytical test. Retain independent
recovery/count/hash controls, test both intended retained-report branches, and
qualify normal/pm-fs. Do not rewrite old evidence, relax scientific cutoffs, hide
failures with skips or repair the shared prefix automatically. #30 keeps broader
qualification. #112's bounded source record profile remains separately evidenced.
Custody owner #50 reviews retained input/check receipts on 2026-11-14.

## Selected admission — 2026-11-13, before correction

Retain the original schema-1.0 evaluator metadata exactly. Its pre-rename
`dockingmt_version` field identifies that historical evaluator; it is not renamed,
re-executed or represented as a current BindingMT producer. The offline summarizer
will accept exactly one nonempty version field, historical `dockingmt_version`
or current `bindingmt_version`, plus the existing MolSysMT/method declarations.
Both fields together are ambiguous and refuse. Cohort compatibility continues to
compare the entire original evaluator mapping exactly, so historical/current
declarations are not silently pooled even when their version strings match.
No alias is added to the current evaluator writer or package/API identity.

Keep the unchanged retained positive/displaced reports as real controls for both
the intended incompatibility and the compatible selected cohort. Verify original
file bytes, producer identity and evaluation digests. For the independent 9-Angstrom
translation, compare RMSD with a relative 16-float64-epsilon tolerance and zero
absolute tolerance, covering unit-conversion/squared-mean/root roundoff without
altering any cutoff, recovery decision, count, denominator or hash assertion.
Run the complete summary and evaluator modules serially under normal and pm/fs
policies. No docking, shared-prefix repair, native rebuild or PHMT execution is
needed; concurrent PharmacophoreMT runtime work remains outside this scope.

## Resolution and exact receiving — 2026-11-13

The offline schema-1.0 summarizer accepts one unambiguous evaluator version key
and preserves the original evaluator mapping verbatim. Historical/current keys
are not translated or equated. Both together, a missing recognized version key and empty or ill-typed version
values refuse; other finite metadata retains exact policy comparison. Exact complete evaluator/policy equality still
controls cohorts; matching version strings under distinct producer keys do not
permit pooling. The actual evaluator writer continues to emit only its current
producer. This is historical evidence receiving, not a legacy package/API alias.

The original retained report bytes remain SHA-256
`383a3b1c75d66881d59862b0ff3e0676e1116b71530b72fe1af7d4c326870e1a`.
Their evaluator stays `dockingmt_version: 0.0.0+101.gbe39d74.dirty`, with its
historical MolSysMT version. Summary `summarizer.bindingmt_version` identifies the
executing summarizer separately; imported static version metadata is not a claim
about its Git source. Per-case SHA-256 continues to cover the original report.
The frozen original reports, old summary/notebook, scientific helper and all
support-resource hashes are unchanged. Current-summary output is a new private
receiving population rather than an overwrite of original scientific evidence.

The 9-Angstrom independent translation assertion uses relative
`16 * numpy.finfo(float64).eps`, absolute zero. It admits the measured
`8.999999999999998` conversion-roundoff case while preserving the independently
expected late-recovery position, top-N/any-returned counts, denominators, report
hash and immutability controls. No scientific cutoff or runtime comparison is
relaxed; inclusive recovery remains literal.

The **complete directly affected summary module passes 97 cases per policy**,
normal Pint and pm/fs: eight new identity/ambiguity controls plus the existing
89 controls, including strengthened actual retained positive/displaced evidence.
The same source/test/provider/native hashes are checked before/after each cell.
A public workflow reads the unchanged original three reports, refuses the mixed
policy and emits four separate summaries for single/cohort/empty/declared-failure
controls. An independent unyt/pm-fs cold reader retains exact original evaluator
identity, fractions, hashes and current summarizer identity, with molecular/engine
operations forbidden, zero originating uses, unchanged files and caller policy.
Reading and aggregation are not a new RMSD, docking or biological benchmark.

### Resource interruption and remaining evidence

One **additional complete evaluator-module** attempt (outside the directly
modified summary module) was stopped at the task's conservative 512-MiB aggregate
owned-group cap: sampled 605,999,104 bytes; about 55.9 GB remained available. Its
owned group terminated, its logs/source snapshot are retained, and it supplies
no pass count or completed evaluator qualification. It is not automatically
restarted, split to hide the interruption or counted as an ordinary test failure.
The planned broader evaluator receiving remains pending under #30; the two
complete affected summary selections pass independently. The issue's original
acceptance is historical summary admission and physical assertion correctness,
not a new complete evaluator/full-suite gate. The initially proposed broader
selection above is thus explicitly partial, not relabelled successful.

Required summary cells use CPU0/nice10/one native worker, a monitored 13-GiB
available reserve, 512-MiB group RSS, 2-GiB address space and bounded CPU/wall time.
They complete without resource interruption, peak sampled RSS below 400 MB. The
separate saved-report workflow/readback peak below 160 MB. No broad evaluator
pm/fs rerun is attempted. Legacy Python 3.14.10 and sources MolSysMT ff25f120,
PyUnitWizard cc51c8e, ArgDigest 7be790b, SMonitor 4a4cd1e and DepDigest 5e93eaf
are recorded. No PharmacophoreMT runtime participates; its concurrent work stays
untouched. Historical loaded MolSysMT native SHA-256 remains
`2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`, with
unauthenticated original builder/source identity. No prefix edit, rebuild,
held-suite restart, installed/public/platform or hosted CI evidence is supplied.

Final workspace and fresh committed-source checks cover Ruff/format, report
indexes, documentation references, shared noarch resources and Conda contract.
Exact outcomes, preserved interruption, source/provider/native/resource snapshots,
public workflow and independent cold-reader receipts retain #50 custody under
`.molsyssuite/interface-p-and-summary-112-113-20261113/`, review 2026-11-14.
Source is delivered by authorized direct commit/push with `[skip ci]`; public
issue state is synchronized after successful push. #112 stays open for
[PeptideMT #60's exact P inputs](../binding_interface_peptide_receiving.md) and
MolSysSuite #195 actual shared/consumer adoption. No P receiving is claimed by
these independent summary controls.
