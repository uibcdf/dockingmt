# Isolated installed collection receiving — 2026-11-09

Owner: [DockingMT #102](https://github.com/uibcdf/dockingmt/issues/102), within
installed qualification #47 and functional delivery #73.

Starting source: `9375f3a8b96a651f8944c48105d56d33a0cf4c68`.
Use the retained, normally installed wheel from runtime producer 9a40e385,
SHA256 `0ed16b5a607a684be611b964b1996f56cc3273f7fcf012e6f86403551f3e91dd`.
No runtime or wheel change is authorized by this test-support increment.

The diagnostic uses shared publication SDK 95f693be staging, both installed
runtime origin checks, an exported qualification harness with core/addon source
removed, importlib mode and empty pytest pythonpath. `--collect-only` and a
runtest refusal hook ensure zero executed tests/fixtures. Whole-suite collection
is an import prerequisite; it is never called a scientific installed gate PASS.

Each cell uses CPU0/nice10, one native/build worker, 13GiB available-RAM reserve,
1GiB group RSS, 2GiB address space, 45 CPU/60 wall seconds. Initial estimate 512MiB;
monitor owned descendants and retain every interrupted/failed attempt. No Slurm
allocation is present; the prior scheduler probe was inconclusive.

Initial `collect-01`: exit 2; 1,996 collected; 47 collection failures; zero runtest
reports; 595 support inputs checked/retired; 21.096s; 368,603,136B peak group RSS,
55,859,073,024B minimum available RAM, no resource interruption. Missing optional
Vina and sibling-test imports are separate causes. Pytest Receptor 1.2.2 retains
exit2/COLLECTION_ERROR but conflates collection failures with executed counts;
the existing provider owner is pytest-receptor#46. Native hooks govern scope.

Acceptance: move the shared finite factories/declarations once into unshipped
support; preserve all scientific test/function bodies and data/producers, with
only explicit helper-path/import routing changes. Keep original 595 declarations
exact, register added helper SHA256 inputs and receive guards plus isolated
collection. Optional missing tools and full execution remain separate evidence.


## Delivered support boundary

The 11 new `dmt_test_support/*_fixtures.py` modules (including
`molecular_fixtures.py`) own the shared original factories/declarations from
source 9375f3a8. The source `tests/molecular_fixtures.py` remains a forwarding shim;
source test modules retain explicit historical aliases. No test imports a sibling
`test_*` module or a top-level `molecular_fixtures` module, even inside functions.

Structural receiving checks all relocated bindings and 31 remaining test-module
ASTs: only shared declarations move, import owners change and three helper data
paths rebase to their original `tests/data` targets. Function bodies, scientific
assertions, fixture parametrization and existing data/producers remain intact.
All595 old support source/target/digest rows remain exact.11 added SHA256 rows
make 606 inputs: 42 code and564 data. Both production packages, project metadata,
67 runtime paths, original wheel and installed bytes remain unchanged.

## Executed diagnostic and offline outcomes

| Cell | Exit and outcome | Scope | Seconds / peak group RSS |
| --- | --- | --- | --- |
| collect-01 | 2 / collection error | 1,996 collected;47 collection failures;zero runtest reports | 21.096 /368,603,136B |
| admin-red | 1 / two expected failures | 8 administrative cases;namespace/path guards reproduce missing support | 2.456 /68,345,856B |
| admin-green | 0 /8 pass | Initial support controls | 2.354 /80,482,304B |
| collect-02 | 2 / collection error | 2,116 collected;39 remaining failures all missing Vina;zero runtest reports | 22.133 /369,524,736B |
| collect-03 | 0 / collection complete | All2,593 cases;zero tests/fixtures or molecular operations executed | 24.178 /469,270,528B |
| offline-normal | 0 /1,267 pass | Whole declared 26-module offline selection;four explicit native deselections | 33.485 /390,705,152B |
| offline-pm-fs | 0 /1,267 pass | Same exact worker/selection/wheel;alternate caller unit policy retained | 35.342 /391,868,416B |
| comparison-01 | Diagnostic completed;both pytest exits2 | Minimal native/compact collection error;zero runtest reports each | 4.314 /81,600,512B |
| admin-final | 0 /104 tests plus26 subtests pass | Full applicable administrative selection;zero scientific imports | 21.656 /122,204,160B |

Every resource cell terminates its owned group, has no interruption or surviving
owned process, preserves the 13GiB reserve and stays below its registered 512MiB
estimate. Actual minimum available RAM is at least 55,859,073,024B. Final offline
profiles have zero warnings/errors/skips; no optional engine imports or real
provider molecular/viewer calls occur. The four unchanged native exclusions keep
their original identities in the archived selection. New guards exercise the
original fixture-file request in a fresh source-free subprocess with a provider
stub; the stub performs no molecular calculation.

`collect-03` uses the original retained E5 engine at
`.molsyssuite/e5-timed-replay-20261107/layouts-admission-01/producer/engine`:
all 103 files match the original engine byte receipt,30,217,797B total, before and
after. Only its Python import path and required process-local library path are
added; installed core/addon origins remain checked. Actual Vina construction,
public molecular operations and viewer construction are refused by this
collection process. No shared install, package extraction/build or native
calculation occurs. The environment without this explicit retained engine still
has its honest 39-error missing-dependency result; the repository does not hide it.

The actual editable cohort remains unchanged before/after final collection and
both offline cells: MTefbe67e1,Viewer1187fc18,ArgDigest07126411,
PyUnitWizardf82b618e,SMonitorc1b6ce29,DepDigest032d345b; exact Python/native hashes
are retained. MolSysMT native5715bda2 and its stale distribution label keep their
separate identities. No source-context acceptance follows from these imports.

## Provider feedback and interpretation

On published Pytest Receptor 1.2.2/pytest 9.2.0/Python 3.14.10, the full initial
collection has 47 errors and zero runtest reports; compact counts say 47 executed
failed tests. A fresh minimal native/compact comparison confirms the existing
pytest-receptor#46 problem: one good item collected plus one import error yields
native `1 error`, both exits2 and zero runtest reports, but compact counts say
one executed failure. Exit/status stays authoritative; no false-green claim.

Successful collect-only also intentionally executes zero items: its diagnostic
exit0 is collection completion, while Receptor's generic execution summary says
INCOMPLETE. It is not used as a scientific gate. The shared installed runner's
positive executed-test requirement remains untouched; actual offline profiles
use that runner and execute their full selected population.

## Remaining scope and custody

#102 resolves this installed helper boundary. #47/#30 still require actual full
scientific installed execution, public provider/artifact closure and all eight
OS/minor installed cells. #100 remains partial under MolSysSuite#178's supported
SSH-source route; no remotes/shared metadata/verifier logic changes. MolSysMT#256
and#558 remain open in this review. Actual browser/comm/canvas#52/#60 stays held
for maintainer scheduling; exact-head hosted#21/#28 remains missing and no remote
workflow is dispatched. Collection/test counts are software evidence, not new
molecular cases, general accuracy or complete functional-plan delivery.

Next register the smallest informative installed scientific selection against
this collected graph, preserving the resource/build holds and exact dependency
identities; receive the owning SSH/public-provider routes when delivered.
Retain this task's receiver reference, qualification exports, engine reference,
original failures and raw receipts under #102/#47/#50 through review 2026-11-14;
keep the E5 engine until both its original owner and this consumer release custody.
Do not clean older wheels/native-build interruptions or the human migration folder.

The initial small administrative red/green attempts retain raw logs/JUnit but
predate per-attempt test-source copying. Final administrative inputs, complete
collection/installed qualification file identities and structural original
producer comparisons are frozen explicitly; no unavailable red source snapshot
is reconstructed or represented as an original frozen input.


## Immutable receiving and closeout

The [primary archive](data/installed_collection_2026-11-09/manifest.json) contains
214 records, 1,656,598 stored bytes / 9,682,995 decoded bytes, manifest SHA256
`74e318e6a174d36726102d8d9e22652485c64c0c076c3c123fc7762a7ebe829f`.
The [independent reader](data/installed_collection_reader_2026-11-09/manifest.json)
contains eight records, 10,745 stored bytes / 29,067 decoded bytes, manifest SHA256
`1c701aafc672311bdb30937d56287ffb5216e28e9e763ad402d6998ee295cdb3`.
Its actual reading passes without replay, authenticating every stored/decoded
member, original failed populations, exact qualified inputs, zero-execution
collection, both executed offline profiles, support retirement, unchanged
cohort/engine, final administrative counts and native/compact discrepancy.
The reader explicitly keeps full scientific-gate and actual source-context
acceptance false.

Closing gates are Ruff lint/format, report indexes, shared resource/release
contracts, exact archive/qualified-source bytes and a clean diff check. Repeat
the first six applicable gates on an actual committed export and retire that
export. Retain exact receipts in the task's published checkpoint; `[skip ci]`
is a batching instruction and supplies no hosted PASS. No remote workflow is
started automatically.


### Committed-export correction

The first actual committed export at `5e93414cbd8cdd39e6747ffafa1e04cf0ab5ea1b`
passes the five lint/index/resource/contract commands but fails the sixth archive
admission check: Git's `.pytest_cache/` exclusion omitted five inert compressed
records beneath the minimal comparison's archived input path. All five were
already present locally and declared by the original 214-member manifest. This
is an evidence publication omission, not a test/runtime failure or resource stop.

Preserve the original manifest/records exactly and explicitly version only those
five declared files; keep live caches ignored. Do not reinterpret that first
committed check as PASS. The [13-member export-failure appendix](data/installed_collection_export_2026-11-09/manifest.json)
retains original programs, registration, stdout/stderr, resource outcome and all
five command logs plus the exact missing-member list: 11,213 stored bytes /
30,591 decoded bytes, manifest SHA256
`016b3b86b086c1b15f0561ce9fe39e152d62225a94061d2c2689df3557bce3b3`.
Final admission must verify all 235 primary/reader/appendix members and exact
qualified source bytes on a new actual committed export. The failed export's
owned temporary directory was retired; no scientific/native job was replayed.
