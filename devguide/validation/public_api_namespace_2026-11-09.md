# Public exception namespace and API reference

Owners: [DockingMT #94](https://github.com/uibcdf/dockingmt/issues/94),
[#28](https://github.com/uibcdf/dockingmt/issues/28) and
[#19](https://github.com/uibcdf/dockingmt/issues/19).
Registered task: 2026-11-08; completed source receiving: 2026-11-09.
Execution base: `457eb090f0e36b6d2b34e1b7d90cbab4d43a4c00`, with frozen
additive source/test inputs. No molecular or engine calculation is required.

## Delivered behavior

`dockingmt.exceptions` exposes explicit aliases to the existing 13 local catalog
exception classes. Root import exposes the module and adds it to `__all__`.
Class identities, implementation paths, inheritance, codes, context, causes and
provider/native behavior remain intact. No new class, diagnostic registration,
exception translation, dependency or configuration policy is introduced.

The [public API guide](../PUBLIC_API.md) maps all **33 root exports**, **13
model/extension classes** with source-defined public members, and **13 exception
aliases**. It provides work/ownership/unit/position/resource boundaries and two
offline examples, with links from the root README and development navigation.
It distinguishes a live pose from a detached snapshot, collection position
from rank, offline audit from reconstruction, and declared parameters from
engine execution. The actual `cpu=0` default is documented; examples choose
`cpu=1`. No existing execution default changes.

`resources.toml` now requires **67 runtime paths**, including the new exception
module and generated version. All **30 helper/564 data inputs** retain their
existing declarations and SHA-256s. The prior private wheel remains exactly
producer `6310a97`, SHA-256
`13169bd91cc90a16bd3b8f60329856ee2cb1921a0dd69ebb598230f543e6fa92`.
Its historical 66-path receiving does not certify this later namespace; it is
neither rebuilt nor relabelled by this increment.

## Reproduction and source qualification

[The public consumer guard](../../tests/test_public_exceptions.py) contains
12 cases. Seven actual record/protocol/domain/outcome/aggregation/dock failures
are caught through public `ArgumentError`, preserving DMT-E002 and field context.
A refused viewer position preserves its local/native hierarchy and DMT-E007
before viewer construction. A unit-provider ValueError retains its exact cause;
MemoryError, KeyboardInterrupt and SystemExit retain exact identity. Controls
inject failures rather than exhausting memory or invoking a molecular engine.

The original source without the namespace records **12 failures/zero passes**,
all missing `dockingmt.exceptions`. Final complete selections pass **251 normal,
then 251 pm/fs**, zero failures/errors/skips/deselections, using unchanged old
tests and the same final new guard. The selection is:

```text
tests/test_public_exceptions.py
tests/test_model_argument_contracts.py
tests/test_support_contracts.py
tests/test_bootstrap.py
tests/test_input_resource_errors.py
tests/test_preparation_addon_diagnostics.py
```

Two initial complete runs preserve seven **harness failures each**: an overly
broad engine guard rejected DepDigest's `find_spec` availability probes. The
corrected guard allows truthful module discovery while refusing actual engine
module construction. Every original assertion and the complete selection
remain. These failed attempts are not product defects or passing evidence.

Tests use Python **3.14.10**, authenticated published Pytest Receptor **1.2.2**
from the existing private Conda prefix, and the existing authenticated private
unyt 3.2.0/SymPy 1.14.0/mpmath 1.3.0 test support. Shared editable packages and
the Conda environment remain unchanged. Receptor/native JUnit/exit status agree.
No new claim is made for Python 3.11–3.13 or another platform.

The separate complete `devtools/tests/test_distribution_contract.py` selection
also passes **19 tests/five subtests** (24 native JUnit rows), confirming exact
runtime inventory coverage, payload refusals and shared declaration controls.
It takes 10.450 seconds below 147 MB sampled RSS, with the same resource limits
and no interruption. Its two pytest assertion-rewrite warnings come from the
already imported reporting plugin; counts/exit status remain authoritative.
These final administrative records are retained privately at
`.molsyssuite/public-api-map-20261108/distribution-normal`, separately from the
frozen runtime/reference archives below. The editable distribution metadata
label `0.0.0+295.g2fda623` is not the source producer identity; actual consumer
imports and frozen source hashes establish this source receiving.

## Reference and independent receiving

A stdlib AST inventory resolves root re-exports to their source declarations,
signatures and properties. The map is checked against those frozen source
hashes, its exact rendered member inventory and **42 local links**. Both Python
snippets compile and execute verbatim under normal and pm/fs caller policies,
using two synthetic one-atom poses and a task-owned JSON file. The guide reads
that file unchanged, reports incomplete evidence and selects the existing
rank-one pose. Protocol construction fixes one CPU and performs no engine work.
All 13 public aliases are the exact original class objects in both profiles.

Actual molecular get/select/extract/convert/copy/set, viewer construction and
optional engine imports are guarded. No such operation occurs. Caller unit
form/parser/standard units remain as received in each context; registering
documented fast tracks is recorded separately in the normal first import.

The independent reader verifies all original/final counts, selections, frozen
source/test/tool hashes, native JUnit and supported Receptor artifacts, resource
outcomes and exact aliases. It removes only the new root import/export and
recovers the original executable AST. The private implementation stays byte
identical. Removing only the new runtime member recovers the complete original
resource descriptor, including every support hash. The reader imports no
DockingMT/molecular package and replays no tests or snippets.

| Evidence | Members | Manifest SHA-256 |
| --- | --- | --- |
| [Primary records](data/public_api_namespace_2026-11-08/manifest.json) | 157 | `b644b5719a4954cf942d0acd19bdd064554e58d2eb2da5a353ed76714994fdec` |
| [Independent reader](data/public_api_namespace_reader_2026-11-08/manifest.json) | 9 | `cf5b0481b748a4790df109d20583a044b4873d311145ec655ccd862e0a7e8497` |

Final guide receiving also checks that union-type pipes are escaped inside
Markdown tables, preserving the exact displayed source signatures and two
columns. Two earlier successful snippet/source checks remain frozen with their
intermediate document/renderer bytes. The initial unpublished 135/nine-member
seals remain intact under private task custody; the final 157/nine-member seals
above include both intermediate checks and the corrected final guide receiving.
No runtime test or scientific calculation is repeated for that formatting edit.

These are frozen compressed source/qualification records, not new scientific
populations, installed artifacts or interchangeable producer identities.

## Resources, limits and next action

Cells run serially on CPU 0 at nice 10, one native/build worker, with monitored
**13 GiB available-memory reserve**, 1 GiB group RSS, 2 GiB address space and
45 CPU/60 wall-second limits. Final test cells take **4.092/4.706 seconds**,
sampled peaks below 200 MB RSS; reference receiving takes **1.535 seconds**.
Every owned group terminates, with no resource interruption or live descendant.
Sealing/independent receiving uses the same policy without molecular replay.

Final local qualification checks Ruff, formatting, report indexes, shared
resources/publication contract, source-map/link consistency, source scope and
frozen evidence. A fresh committed export repeats applicable source/document/
resource/publication checks. Direct publication follows the maintainer's
`[skip ci]` route; no remote CI is dispatched. Missing hosted exact-head
evidence remains #28, not a pass.

This closes #94's additive source/API slice. #19/#28/#73 remain partial for
wider adoption, user-observed usability, workflow performance and the complete
plan. Public/installed/full scientific/platform/browser/comm/canvas gates remain
with their existing owners. Respect the maintainer's #256 wait and #558's
generation-map/history requirement; do not restart the interrupted native build.
Next advance independent accepted work, or receive the provider's original
handoff when available, with no substitute reference/preparation gate.

Retain `.molsyssuite/public-api-map-20261108` under #94/#28/#19/#50, review
2026-11-14. Preserve the original failures, private published support prefixes,
unchanged previous wheel, migration directory, shared environment and historical
interrupted build. The committed records support reading without those private
prefixes; repeating executable qualification requires the exact declared tools.
