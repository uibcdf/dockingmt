# Result export optimization

Owned by [#28](https://github.com/uibcdf/dockingmt/issues/28), preserving the
independent-snapshot contract in [#25](https://github.com/uibcdf/dockingmt/issues/25).
The [executed notebook](result_export.ipynb) explores the unchanged
[before](data/result_export/before_2026-10-02.json) and
[after](data/result_export/after_2026-10-02.json) raw reports.

## Measured operation and change

The existing export path built independent pose dictionaries and then deep-copied
the entire result, traversing every pose again. A pose export also deep-copied
coordinate lists that NumPy's `tolist()` had just allocated. Profiling confirmed
these traversals dominate large snapshots: the coordinate-heavy case made
2,119,231 `deepcopy` calls, and the mapped case made 8,415,807 calls. Counts include
recursive calls, not just top-level copies; instrumented cumulative times overlap.

The optimized path copies structured pose fields and result context as before,
retains newly allocated coordinate lists, and uses the base pose serializer's already
independent snapshot. Custom serializers retain the existing defensive copy when
their output ownership is unknown. This removes redundant traversals while preserving arbitrary
structured Python metadata, score validation, IDs, explicit coordinate units,
custom pose serializer dispatch, schema `1.0` and JSON content. Reconstruction is
unchanged. No cache, dependency, molecular operation or viewer integration is added.

## Method and environment (2026-10-02)

`python -m devtools.benchmark_result_export` constructs deterministic nonzero
coordinate fixtures declared in nm, multiple named scores, pose/state identities,
nested annotations and captured-payload-shaped provenance. Mapped cases add
the existing prepared/selected/source atom-index lists and per-atom identity keys.
These synthetic cases exercise the current result API; they are not real docking
systems or campaign capacity estimates. The optional manifest case loads one
existing exploratory 181L result with four poses of six atoms.

Each report uses one process and three elapsed export samples per case. Imports,
construction, garbage collection between samples, hashing and snapshot disposal
are excluded. Memory uses a separate `tracemalloc` call: peak Python allocations
while producing the dictionary, excluding pre-existing input storage. It is not
RSS, total host memory or a campaign memory estimate. `cProfile` also uses a
separate call; neither instrumentation enters the elapsed medians. Before and
the retained final after run were sequential without concurrent tests. OS caches
were retained. No telemetry configuration was changed by the tool.

Environment: Linux x86_64 / glibc 2.39, Python 3.13.14, NumPy 2.4.6, PyUnitWizard
0.27.0, ArgDigest `0.12.1+7.ga2edfe9`, DepDigest `0.10.1+15.g78a9106`, SMonitor
`0.18.0+1.gb308ee0`. A separate fresh-process check of the normal configuration
observed profile `user`, level `WARNING`, trace depth 3 and profiling disabled;
this was not a per-sample configuration capture. No provider checkout was changed.

Both measurements had HEAD `6d1a0669582cefbe58af201719d02c4bee8f08a8`, dirty.
The source digest covers the package and the existing 181L revision helper:

- Before SHA-256: `5db4db57cb25294c5e2865fbced654adcfbdbcc59aad5b3a51050abb7816597c`.
- After SHA-256: `d9168cb5adcf243a408f59b81c2b3a20291670fd1750298c6d53d2d4b12a05a2`.
- Benchmark before SHA-256: `da865e2bf2229c13726f87e93c5a6d65c3355a86aaba97cf88263b3209a08e05`.
- Benchmark after SHA-256: `e7e5efb09f20e697a182c3de7b83f0883d308f33ec434394f8bba00b4eecad46`.
- Retained manifest SHA-256: `44a7c23fa4a6c04cb3ee1a4ced7668b75090d79e7dc5f0426b7540f9ae43e194`.

Between reports the tool added matching clock/method/memory definition checks and
made scientific imports lazy so report comparison can run without scientific
providers. Fixture construction and the measurement loop are unchanged from
the baseline. The final comparison helper accepts the retained reports.

## Results

Every case has the same strict JSON bytes/digest before and after. Raw elapsed
samples, Python peaks, profiles, environment and source identity are retained in
the two reports and displayed in the notebook. Three samples do not establish
a universal ratio; the small real-manifest difference is sensitive to noise.

| Case | Poses × atoms | Before median (s) | After median (s) | Before/after | Before Python peak (MiB) | After Python peak (MiB) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Small with maps | 9 × 64 | 0.009387 | 0.003560 | 2.64 | 0.48 | 0.22 |
| Many small | 256 × 32 | 0.067674 | 0.017690 | 3.83 | 3.35 | 1.56 |
| Large coordinates | 256 × 1024 | 1.453565 | 0.085978 | 16.91 | 87.19 | 40.32 |
| Many poses | 1024 × 32 | 0.241427 | 0.065561 | 3.68 | 13.53 | 6.22 |
| Large with maps | 256 × 1024 | 4.422038 | 1.183333 | 3.74 | 208.16 | 90.66 |
| Existing 181L manifest | 4 × 6 | 0.002031 | 0.001397 | 1.45 | 0.07 | 0.05 |

After optimization, recursive `deepcopy` counts fall to 10,045 in the large
coordinate case and 3,158,333 in the mapped case. Required metadata copying still
dominates the mapped case. These data justify removing redundant copies, not
weakening metadata isolation or sharing mutable pose records.

This measures dictionary export only. It does not imply faster native search,
affinity maps, molecular preparation, JSON encoding or disk writing. The existing
[workflow profiling](workflow_profiling.md) identifies those separate boundaries.
No performance threshold or scientific qualification claim is introduced.

## Reproduction and guards

```bash
python -m devtools.benchmark_result_export --report /tmp/export-before.json --memory --profile
python -m devtools.benchmark_result_export --report /tmp/export-after.json --reference /tmp/export-before.json --memory --profile
```

Run these on the chosen reference and candidate source revisions with the same
environment and fixture selection. `--case small_mapped` selects a quick case;
`--manifest PATH` adds an existing result. Keep the manifest bytes fixed for both
runs. The optional historical manifest is identified by digest; it is not bundled
with these timing reports. A newly generated 181L manifest carries its own
provenance and digest.

`tests/test_result_contracts.py` protects mutation isolation in both directions,
repeated exports/repeated pose entries, arbitrary NumPy/tuple/set metadata,
serializer extensions, score validation and quantities under a non-default session
policy. `tests/test_result_export_benchmark.py` protects comparable definitions,
exact payload identity and operation without molecular or optional-engine calls.
No test asserts a wall-clock speedup. The notebook reads retained reports by
default and adds no runtime dependencies.

Final local validation passes all 368 tests in 45.74 seconds with the same 12
provider warnings, Ruff lint/format, generated report indexes and diff checks.
All five notebook code cells execute successfully; its schema and outputs validate,
and the versioned raw files match the sampled originals byte for byte.
