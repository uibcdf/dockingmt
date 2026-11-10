---
summary: Run the fixed-pose scoring example from ordinary installed environments.
issue: uibcdf/dockingmt#105
status: resolved
opened: 2026-11-10
closed: 2026-11-10
severity: medium
verification: measured
area: [documentation, workflow, scoring, installation]
guard: devguide/validation/fixed_pose_scoring.ipynb
normative: devguide/validation/installed_fixed_score_2026-11-10.md
blocked_by: []
supersedes: []
---

# Portable fixed-pose scoring notebook

## What

The existing executed developer example asserts Python3.14 and a particular Conda
environment path, then searches ancestors for a DockingMT checkout and silently
reads a repository fixture. Its scientific/developer qualification remains valid,
but those assumptions prevent ordinary installed use outside that checkout.

## How

Follow the existing installed-result example's explicit input path/external SHA256
pattern. Admit the saved record through public schema/audit/capture APIs before
native setup. Consume only the actually captured PDBQT conformation and declared
box; do not select or reconstruct a historical output pose. Keep CPU1 and the
existing Vina/Vinardo evaluations, independent histories and detached roundtrip.
Remove interpreter-name/current-directory assumptions and use a public exception
base for the duplicate-score refusal. Keep missing captures/chemistry explicit.

## Why

The accepted fixed-pose workflow should expose public API choices rather than
require knowledge of the contributor's checkout/environment. The input record
supplies original submitted bytes; its trusted file identity and original producer
must stay distinct from the current scoring reader/evaluations. Existing source
fixtures/producers and the immutable installed-test corpus remain untouched.

## Scope and acceptance

Retain original notebook bytes, prove its installed refusal, then receive all four
exact revised code cells from an outside-source directory with the genuine same
wheel and both caller unit policies. Refuse bad external identity or missing
captures before native setup. Preserve all 16 native score definitions/histories,
physical coordinates and input bytes. Keep headless source-cell receiving separate
from actual Jupyter/browser/public-platform acceptance. No runtime API, native
engine/force-field, fixture or dependency floor changes; no new search/optimization,
remote CI or shared installation.


## Resolution — 2026-11-10

The notebook now admits an explicit file path and trusted SHA256 through public
record/audit/capture APIs. All four exact cells pass outside the checkout with
the genuine ordinary installed wheel under normal and pm/fs units. Eight then
sixteen native values, unchanged coordinates, two histories and a detached
seventeen-score roundtrip survive. Bad file identity and absent captures stop in
cell one with zero native calls; the frozen original developer notebook retains
its expected ordinary-prefix refusal. The original installed-support snapshots
and all runtime/test/fixture bytes remain unchanged.

The normative receiving record authenticates 365 primary and 14 independent reader
members, including exact notebook sources/outputs and actual native mappings.
The associated 31+89-case admitted installed selections pass under both policies;
the single larger-input case remains explicitly excluded. Actual Jupyter/kernel/
browser/public-platform gates retain separate owners and no new evidence claim.
Next follow #47's uncovered-workflow ledger; this portable-source proposal is
resolved without changing any runtime API or dependency.
