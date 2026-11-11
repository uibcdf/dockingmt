# Published test-reporter receiving — 2026-11-05

Owner: [BindingMT #19](https://github.com/uibcdf/bindingmt/issues/19).
Hosted source observation: [#28](https://github.com/uibcdf/bindingmt/issues/28).
Starting source: `74bf2cc9d046a4e00695b864f76e9d8f38b56ded`.

## Change and public-file identity

The scientific source-test environment and test extra previously left Pytest
Receptor unpinned. They now select published **1.2.2**. Both existing source
workflows check its installed metadata and print its actual module origin with
`python -I` before the unchanged `pytest --receptor=ci` command. The normal test
selection, coverage, four Python minors, cadence and scientific provider pins
remain unchanged. `receptor_rerun_command = "python -m pytest"` supplies usable
wrapper commands for local runs.

[MolSysSuite #133](https://github.com/uibcdf/molsyssuite/issues/133) records the
provider release at `531bafde5d48ddd8974e29ac91ae53ecae0fd787` and its original
eight Linux/macOS arm64 × Python 3.11–3.14 installed cells. The independently
downloaded files match those published identities:

| Route/file | SHA-256 |
| --- | --- |
| PyPI `pytest_receptor-1.2.2-py3-none-any.whl` | `48c290fba7e12d19015fa436989fdad465d5ff7bba78fa94f7825e305ccf7961` |
| uibcdf Conda `pytest-receptor-1.2.2-py_0.tar.bz2` | `c0b075286f45e8fce5ab5852947611bfba82b7d509115fc5dadf1a9572b9dd74` |

All six runtime package files are byte-identical across these archives. The
[file receipt](data/test_reporter_2026-11-05/public-files.json) records that
comparison. This is a fresh hash/payload check, not another Conda solve or a
repeat of the provider's original installed matrix. Pytest Receptor retains
the maintainer-confirmed additional PyPI route; our other suite-package public
guidance uses uibcdf Conda (MolI #81 / MolSysSuite #167).

## Executed consumer checks

A private Python 3.14.7 environment inherits the routine scientific dependencies
and installs the verified published wheel without dependencies. Isolated-mode
metadata/origin checks confirm **1.2.2 from that environment**. The routine
editable Pytest Receptor `1.2.2+2.gb9676f8` is preserved; its earlier observations
retain their development-source identity.

| Check | Outcome |
| --- | --- |
| Support, bootstrap, preparation assessment, prepared/view arguments and reporting protocol | 122 passed, exit 0 |
| Distribution, installed support and coverage workflow controls, unchanged SDK `738fe8dd731abb99dac421b0bb2acc8564110180` | 27 passed, exit 0 |
| Both actual YAML-installed-package commands executed with the private Python and `-I` | Exit 0; reporter 1.2.2 and private module origin verified |
| Same deliberate pass/warning/failure/skip control with human and CI rendering | Each exit 1; JUnit agrees on two passes, one failure and one skip; warning and skip reason retained |
| CI-profile versioned artifact read through `pytest_receptor.read_artifact` | Complete, integrity valid, matching counts/exit, one warning; wrapper rerun retained |

The compact [receiving receipt](data/test_reporter_2026-11-05/receiving.json)
and [four-case control](data/test_reporter_2026-11-05/reporting_control.py) retain
the bounded comparison. To repeat the latter with a verified reporter environment,
run the same file with each `--receptor=human` / `--receptor=ci`, `-c /dev/null`,
`-o 'receptor_rerun_command=python -m pytest'`, `-rs` and a distinct
`--junitxml=...`; add `--receptor-events=...` for CI. The expected command exit
is **1**, deliberately. An initial invocation incorrectly supplied a nonexistent
CLI rerun option and exited with usage error before collection; the comparison
above uses the documented configuration override.

This local environment still uses the source BindingMT checkout. It does not
qualify an ordinary installed BindingMT artifact, a fresh dependency closure,
another platform or new molecular/scientific behavior. Administrative CI and
the independently pinned shared installed-test caller retain Pytest Receptor
1.2.1; this source-science receiving does not silently change those profiles.

## Hosted handoff and remaining scope

The preceding source `74bf2cc` completes CI `41959731242` (seven jobs), Addon DOM
`41959731330`, policy `41959731686` and publication governance `41959731585`
successfully. Published GH Run Receptor 1.4.0 inspects its CI. These observations
belong to that preceding source, not the reporter change.

The new exact head requires its own hosted installation probe and four required
source-test lanes. Record that outcome in #19/#28 before treating the published
CI pin as verified. Scheduled full-matrix execution retains its existing cadence;
its local command check is not a hosted full-matrix result. #19 remains partial
for DepDigest #47 / owner-review PR #48, remaining tool adoption and public
compatibility. No release, new scientific population or visible C4/C6 acceptance
is claimed. Task-owned environments/downloads are temporary; keep only these
bounded receipts after the durable handoff.

### Hosted source receiving observed — 2026-11-05

At exact source `cddf8941482e410a62fd191923f1e26fdf69015b`, CI
[42051846017](https://github.com/uibcdf/bindingmt/actions/runs/42051846017)
passes all four Linux Python **3.11–3.14** science jobs, **1,613 tests each**.
Native job/step facts and the actual completed-job logs confirm reporter
**1.2.2**, its site-packages origin, the isolated installed-package probe,
dependency closure and unchanged full source-test command. Published GH Run
Receptor 1.4.0 supplies the initial inspection; the bounded
[hosted receipt](data/test_reporter_2026-11-05/hosted.json) retains the exact
job identities without raw logs or runner paths. This verifies the outstanding
published source-CI pin item in #19. Quality and distribution jobs also pass;
the overall CI workflow still awaits its coverage-publication job at this
observation, owned by #28.

Addon DOM `42051846044`, policy `42051847342` and publication governance
`42051847212` succeed on the same source. Scheduled run `42056029256` succeeds
only at the backlog decision and **skips** the full-matrix job. It is not six
executed Linux/macOS cells. The matrix retains its actual cadence and evidence
requirements. These observations belong to `cddf894`; later source changes need
their own hosted observation. #19's broader provider/helper review remains open.
