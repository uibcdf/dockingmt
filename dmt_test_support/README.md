# Unshipped scientific test support

These component-owned qualification helpers orchestrate public DockingMT and
MolSysMT operations and compare the declared scientific fixtures. General
molecular tools remain MolSysMT-owned. This namespace is available in the source
checkout and is excluded by the actual runtime package-discovery patterns.

Installed tests import helpers from `dmt_test_support`. The exact Python/data
selection and SHA-256 values are declared in
`devtools/conda-build/resources.toml`; MolSysSuite's `installed_test_support`
operation validates, stages, checks and retires those inputs. The provider
binds this namespace without adding the source root or staging parent to Python
paths. Keep the SDK's `devtools` namespace separate. There is no local staging
or namespace-loading implementation.

The fixture corpus is the explicit `b74b4ad` validation/test-data snapshot,
excluding two executable historical producer programs. Those programs remain
unchanged; byte-identical `.py.txt` copies are declared as inert fingerprint
evidence. New receiving outputs are not recursively added to the inputs.
The 131 top-level validation guides/notebooks are stored at immutable
`tests/data/installed_support/b74b4ad/` source paths and mapped to their original
staged locations. Editing living guides therefore leaves the exact qualified
support inputs unchanged. Validate the final declaration against committed
bytes after documentation changes.

Source-relative data paths preserve their original layout under managed staging.
Some historical qualification entry points still require their real source/Git
context; their presence in the support selection does not qualify every CLI
operation inside staging. The retained `devtools` delegates preserve source CLI
entry points and explicit imports, including private helper attributes. The
installed test selection separately exercises the self-contained recovery CLI.

Benchmark attribution fingerprints the actually imported core and helper code.
Git head/dirty fields are unknown when they do not share a real checkout.
Keep that distinction, original artifact hashes and the separate test/helper
source identity when qualifying an installed package.
