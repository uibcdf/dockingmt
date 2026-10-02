# Current-workflow phase profiling

Owned by [DockingMT #28](https://github.com/uibcdf/dockingmt/issues/28).
This is software performance evidence for existing workflows. The 181L
chemistry remains provisional; timings do not qualify docking accuracy.

The [companion notebook](workflow_profiling.ipynb) contains executed tables and
plots from the retained raw samples. Its default execution reads the reports
without docking or importing the scientific package. Jupyter/IPython and
Matplotlib are needed to run the analysis; the notebook's optional final section
uses the existing fresh-process command to collect new measurements. The recorded
baseline remains separate from newly generated reports.

## Measurement boundaries

`VinaProtocol(collect_timings=True)` adds a per-run `provenance['timings']`
record on successful execution. It contains `unit: second`, `clock: perf_counter`,
the consecutive phases below, and their elapsed total. These are wall times,
including I/O and instrumentation bookkeeping, rather than CPU times. The total
starts after the protocol type check and ends after cleanup; it excludes default
protocol construction, public decorators, and the final timing-record attachment.

| Adapter phase | Included work |
| --- | --- |
| `validation` | Capability, unsupported-intent, and protocol problem checks |
| `search_domain_projection` | Explicit-unit Vina box projection and admission |
| `preparation` | Automatic receptor/ligand preparation, source maps, chemistry checks and preparation metadata; supplied inputs pass through these checks |
| `backend_import` | Lazy Vina import and temporary-path bookkeeping |
| `input_projection` | PDBQT generation/resolution, immutable input staging, digests and optional byte capture |
| `engine_setup` | Vina construction and receptor/ligand loading |
| `affinity_maps` | Vina map computation |
| `native_docking` | Vina global search and its timer bookkeeping |
| `result_normalization` | Pose/energy retrieval, identity verification, quantities, scores, provenance, problem snapshot and result construction |
| `cleanup` | Temporary-file cleanup |

The existing `elapsed_seconds` remains native search duration, now measured with
the monotonic clock. It overlaps `native_docking`; do not add the two together.
With profiling disabled the adapter creates no phase recorder and reads no
additional clocks. There are ten inexpensive conditional checks. No shared
telemetry framework, new dependency, global collector, or molecular operation
has been added. SMonitor's function/tag aggregate telemetry remains distinct
from these named per-execution adapter boundaries and serialized provenance.

`devtools/profile_workflow.py` runs each sample in a fresh interpreter, alternating
the ordering of three enabled/disabled pairs. Both modes retain seed=42, cpu=1,
exhaustiveness=1, n_poses=5 and backend input capture in the measured 181L case.
The tool records independent import, input normalization, public docking call,
dictionary export, JSON encoding and file-write times. Adapter timings are
contained in the docking-call measurement. Input normalization includes protocol
construction and input-identity bookkeeping; the PDBQT route also reads and validates
the captured manifest. Report/helper bookkeeping and interpreter startup are
excluded. OS caches are not reset; writes do not `fsync`.

Each report keeps raw samples, input/source digests, protocol, versions, environment
and code identity. The command rejects mismatched captured-byte hashes before
execution, requires an explicit seed and cpu=1 for captured cases, and writes
the report before returning failure on unequal output/input/execution contexts.
Pose snapshots and submitted-input/box records are compared exactly within each
route. A captured-input run carries PDBQT identity rather than the molecular
source atom map; cross-route identity or chemistry equivalence is not claimed.

## Local observations (2026-10-02)

Linux x86_64 / glibc 2.39, Python 3.13.14; Vina 1.2.7, NumPy 2.4.6,
ArgDigest `0.12.1+7.ga2edfe9`, DepDigest `0.10.1+15.g78a9106`, PyUnitWizard
`0.27.0`, SMonitor `0.18.0+1.gb308ee0`, MolSysMT
`0.22.4+118.g03b318549.dirty`. No sibling checkout was modified by this work.
This environment differs from the earlier import/export baseline; no cross-version
speedup is inferred. The editable DockingMT version string was
`0.0.0+14.g25b6e0b.dirty`; exact inspected source, rather than that stale installed
version string, identifies this measurement:

- HEAD before implementation commit: `df77c1789c547275981678c720d59684f701e1c1`, dirty.
- Package plus existing 181L helper SHA-256: `5db4db57cb25294c5e2865fbced654adcfbdbcc59aad5b3a51050abb7816597c`.
- Profiler SHA-256 during sampling: `edac408de66f6783944503ecea04d8ab9e580c3c5630b63e18c7d86276a5e4a9`.
- Molecular source SHA-256: `77018feaaa65bb22dea47c784e8c059b0ccc09cd6dc7442b79cce83f3170985f`.
- Captured manifest SHA-256: `44a7c23fa4a6c04cb3ee1a4ced7668b75090d79e7dc5f0426b7540f9ae43e194`.

The final profiler adds an execution-context comparison and retains recorded
constraints/guidance (empty in these cases) after sampling; these do not alter
the adapter phases. Applying the context comparison to the retained samples
passes for both routes. All six samples per route had identical pose snapshots,
backend inputs, input identity and execution context.

Median seconds for the three profiling-enabled samples:

| Measurement | Molecular 181L route | Captured PDBQT route |
| --- | ---: | ---: |
| Import MolSysMT, PyUnitWizard and DockingMT | 0.472851 | 0.453780 |
| Input normalization / problem construction | 5.498096 | 0.010935 |
| Public docking call | 1.300083 | 1.008789 |
| Adapter preparation | 0.273936 | 0.000015 |
| Adapter input projection | 0.008094 | 0.001302 |
| Engine setup | 0.031056 | 0.029962 |
| Affinity maps | 0.652852 | 0.650054 |
| Native docking | 0.326389 | 0.321114 |
| Result normalization | 0.001562 | 0.001499 |
| Dictionary export | 0.001449 | 0.000366 |
| JSON encoding | 0.000859 | 0.000946 |
| File writing | 0.000162 | 0.000206 |

Rows contain nested timings and cannot be summed. Medians of individual phases
also need not sum to the median total.

Raw public-docking-call seconds in pair order:

| Route | Pair | First mode/time | Second mode/time |
| --- | ---: | --- | --- |
| Molecular 181L | 1 | disabled / 1.333756 | enabled / 1.300083 |
| Molecular 181L | 2 | enabled / 1.285159 | disabled / 1.320067 |
| Molecular 181L | 3 | disabled / 1.366023 | enabled / 1.404931 |
| Captured PDBQT | 1 | disabled / 1.046106 | enabled / 1.008789 |
| Captured PDBQT | 2 | enabled / 1.029100 | disabled / 1.002368 |
| Captured PDBQT | 3 | disabled / 1.028671 | enabled / 0.999279 |

Enabled-minus-disabled median docking-call differences are -0.033674 s and
-0.019882 s respectively. This noisy sample does not resolve profiling overhead
or establish a speedup. Deterministic tests instead protect the disabled path's
two existing native timer reads, phase attribution, result equivalence and cleanup.

The molecular route is dominated by problem construction/normalization. Within
the adapter, maps dominate, followed by native search and automatic preparation.
The direct captured route avoids preparation, but still computes maps each time.
No cache or provider optimization is justified without separate ownership/reuse
and repeat-work evidence. Small-result export is not a bottleneck here; the larger
synthetic export workload in #28 remains a separate optimization candidate.

## Reproduction

```bash
python devtools/profile_workflow.py --repeats 3 --report /tmp/181l-profile.json
python devtools/redocking_181l.py record --manifest /tmp/181l-manifest.json
python devtools/profile_workflow.py --manifest /tmp/181l-manifest.json --repeats 3 --report /tmp/pdbqt-profile.json
```

The original raw reports are now versioned as
[`181l_molecular_2026-10-02.json`](data/workflow_profiling/181l_molecular_2026-10-02.json)
and
[`181l_captured_pdbqt_2026-10-02.json`](data/workflow_profiling/181l_captured_pdbqt_2026-10-02.json).
They preserve all twelve samples and their original hashes, versions, protocol
and timing definitions. They were copied unchanged from the development reports
in `/tmp/dockingmt-181l-profile.json` and `/tmp/dockingmt-pdbqt-profile.json`;
the commands regenerate equivalent evidence,
not identical wall times or manifest hashes. No CI runtime limit, public package
dependency qualification, campaign claim or scientific recovery claim is made.
