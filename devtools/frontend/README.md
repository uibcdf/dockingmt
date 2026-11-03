# Docking addon DOM tests

Owner: [DockingMT #60](https://github.com/uibcdf/dockingmt/issues/60).

From the repository root, with Python 3.14 and Node 26 available:

```bash
npm ci --prefix devtools/frontend --ignore-scripts --no-audit --no-fund
npm test --prefix devtools/frontend
```

`PYTHON` can name the interpreter used for extraction. `extract_panels.py` reads
the literal `_ESM` strings with the standard-library AST, without importing any
scientific package. Node's native test runner executes those exact ES modules
inside isolated jsdom VM contexts. The VM-module flag is development-only and
currently emits Node's experimental-feature warning. Neither exports nor code
are rewritten, and no production JavaScript is copied into the tests.

The only widget double is its used model surface: attributes, change/custom
events and JSON-serializable outgoing messages. This verifies addon DOM state,
click/change handlers and local subscription cleanup. It does not implement or
qualify MolSysViewer's comm transport, callback delivery or lifecycle. Each DOM
window is closed after its test, and asynchronous DOM handler errors fail tests.
Subresource loading is not enabled. No browser, server or kernel is launched.

`panel_states.json` contains protocol examples built by the production Python
panels. `tests/test_viewer_frontend_contract.py` compares them with fresh actual
states in the existing Python suite, so the JS examples cannot silently drift
from the backend. This includes missing identity/rank, a zero Vina value with
undeclared meaning, a separately declared kJ/mol score, and supplied-but-unrendered
search geometry. Test mutations cover subsequent host states and error cases.

The dependency and lockfile are private development tools, excluded from the
Python distribution. They add no Python/runtime requirement, scientific source
route or registered-member dependency-graph edge; jsdom and Node are third-party
test tools. Existing Python CI/full-matrix/installed gates remain unchanged.

The separate `Addon DOM` workflow follows the starter's checkout, explicit tool
setup and direct failing-test-command pattern. Its local addition is needed
because the Python jobs do not execute panel JavaScript. Owner #60; reassess
under [MolSysSuite #161](https://github.com/uibcdf/molsyssuite/issues/161).
When a qualified shared frontend gate can execute these same addon assertions,
then replace this local workflow without dropping coverage. It does not replace
the source-science, distribution or full-matrix workflows.

jsdom implements DOM behavior without layout or rendering; these tests establish
no pixels, camera/clipping behavior, real frontend/backend round trip, maintainer
review or C6. See [jsdom's documented limits](https://github.com/jsdom/jsdom#unimplemented-parts-of-the-web-platform)
and [Node's native test runner](https://nodejs.org/api/test.html).
