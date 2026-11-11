# PEP 639 license metadata and private archive checks

Owner: [BindingMT #47](https://github.com/uibcdf/bindingmt/issues/47).
Coordination: [MolSysSuite #162](https://github.com/uibcdf/molsyssuite/issues/162).
This is BindingMT's local packaging migration; it establishes no new suite rule
and changes no sibling source or project license.

## Source and build requirement

Committed producer `50d8e33f4ccb3354a8d27aea9fa9010c1b13e9a9` declares
`license = "MIT"`, `license-files = ["LICENSE"]` and removes the deprecated
license classifier. The actual LICENSE bytes match baseline `94f42e1` exactly.
Setuptools >=77.0.3 is aligned in build metadata, the Conda host recipe, scientific
test bootstrap and administrative CI. Existing runtime requirements, Python
range, source pins and scientific commands are preserved. The CI tooling-floor
change has its own updated fingerprint in the ten-route/four-context inventory.

[Setuptools documents PEP 639 support](https://setuptools.pypa.io/en/latest/userguide/license_migration.html)
from 77.0.0; [77.0.3 includes subsequent license-validation fixes](https://setuptools.pypa.io/en/latest/history.html#v77-0-3).
The selected patch floor is also used by the inspected PharmacophoreMT source.
Actual successful builds below justify it for this measured profile, without
claiming that every earlier patch fails or that all platforms/minors are tested.

## Executed artifact checks — 2026-11-03

Two independent build-only virtual environments use Python **3.14.7**, Build
1.6.1, Versioningit 3.3.0, Wheel 0.48.0, Packaging 26.3 and PyProject Hooks 1.2.0.
Their Setuptools versions are **77.0.3** and the development environment's
**84.0.0**. Both tool environments pass dependency checks before artifact work.
Pinned public tool wheels and their digests remain in the task evidence.

Each backend successfully builds a wheel and sdist from the exact committed
producer, then a second wheel from the extracted sdist without Git metadata.
These are **six newly produced private archives**, version
`0.0.0+225.g50d8e33`. Identical filenames in separate backend/route directories
retain separate archive digests; no file is substituted for another candidate.

The [receipt](data/license_metadata/checkpoint_2026-11-03.json) verifies:

- Core metadata 2.4, SPDX `License-Expression: MIT`, the declared LICENSE file
  and absence of deprecated license headers/classifiers.
- Exact LICENSE contents in both source archives and each wheel's
  `.dist-info/licenses/LICENSE`.
- Consistent archive/metadata/generated versions, the original Python range
  and unchanged normalized runtime/extra requirements.
- All **63** core/addon resources: 62 tracked files match the producer and the
  generated version matches the candidate. All six payload maps are byte-identical.
- The addon entry-point target in every wheel, source pyproject bytes in both
  sdists, and absence of administrative/Node dependencies from wheel payloads.
- No table/classifier license deprecation appears in the four build logs.

The current-backend sdist-derived wheel is then installed normally, with
`--no-deps --no-compile`, into the task-only inspection prefix. PEP 610 binds
its original archive digest; version/license metadata, all 63 installed files
and addon entry-point **metadata discovery** pass outside the source clone.
Scientific dependencies are absent there: runtime imports, entry-point loading
and scientific dependency closure are not qualified by that inspection.

All **24 administrative tests** pass without skips (2.92 s), including the
existing resource/recipe/route controls. Declaration preflight, Ruff lint/format,
report indexes and whitespace checks pass. No new mirror assertion test is
introduced for these metadata edits; actual builds and archive/install checks
exercise the relevant boundary.

To reproduce, use a clean checkout of the producer and one task-owned Python
3.14 environment per recorded backend, installing the pinned tool versions from
the receipt. From the checkout, run:

```bash
python -I -m build --no-isolation --sdist --wheel --outdir /path/to/new/source-artifacts
```

Extract the new sdist outside any Git checkout, enter its root and run:

```bash
python -I -m build --no-isolation --wheel --outdir /path/to/new/sdist-wheel
```

Use new output locations for each profile and retain each artifact's digest.
The recipe/declaration checks use the existing immutable SDK; no Conda publication
is needed for these Python archive checks.

## Setup recovery and resource custody

After the minimum-backend builds complete, the second full source checkout fails
on the temporary filesystem's quota. Its partial clone is retired. The current
backend then reuses the verified exact-producer checkout after removing only
its prior ignored build directory, egg metadata and generated version file.
The tracked checkout stays clean and every archive is bound to the same producer.
The failed setup and corrected route retain their own record; this is not a
failing backend build or a passing first setup attempt.

The five task-only build/inspection/source/extraction trees are retired after
verification, without cleanup errors. Six original new archives, pinned public
tool wheels and private logs/operational records remain useful under #47/#50,
review **2026-11-10**. Actual closeout is recorded on #50; original scientific
receivers and shared scientific providers remain protected. The earlier qualified wheel
from `376679c` still has digest
`aa5626e1ee7073a2df32fdce75cf10c132eeedffc807aa71a5421d1a55a9391e`.

## Qualification limits and next steps

The preceding runtime/test head `94f42e1` independently completes hosted CI
`41711368701`: all four Linux Python 3.11–3.14 lanes have **1,436 passed**;
quality/distribution and coverage publication jobs succeed. Its separate DOM
run `41711369065` has **21 passed**. These terminal results retain their original
source and do not become full science/platform qualification of this packaging
producer. New exact-head CI/recovery is recorded separately on #47.

The local license-metadata subtask is verified for the measured private profile.
Public dependency coordinates/minima, actual Conda candidate/archive and installed
platform gates remain #30/#47. The future release plan must include the addon DOM
gate. No tag, package upload, promotion or release occurs; no scientific search,
new molecular operation or visual C6 acceptance follows.

MolSysMT #541 and MolSysViewer #292 own their separate build-floor findings.
The suite's canonical starter/adoption proposal remains #162. For continuation,
inspect exact-head hosted gates, review the remaining public dependency/plan
inputs, and receive provider/browser work when available.
