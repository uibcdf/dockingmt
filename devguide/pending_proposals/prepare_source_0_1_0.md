---
summary: Prepare the fixed 0.1.0 source milestone with truthful version, payload and gate evidence.
issue: uibcdf/dockingmt#74
status: partial
opened: 2026-11-05
closed:
verification: measured
area: [releases, distribution, provenance]
guard:
normative: https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_version_policy.md
blocked_by: []
supersedes: []
---

# Prepare the 0.1.0 source milestone

## What

Fix candidate `905abc9698cf9d4add78a52d57dab707859a148d` for the first `0.1.0`
source-only milestone under #73. The [candidate dossier](../releases/0.1.0.md)
records immutable inputs, intended route, release/use/notice drafts, private
metadata/payload evidence and the actual pending gates. Later evidence commits
do not move the target automatically.

## How

Use an independent disposable Git repository without remotes to test the actual
canonical version configuration. Build a private wheel without dependency
installation; inspect all declared runtime bytes, generated version, license,
metadata and addon entry point, then import the unpacked wheel in a fresh
isolated-path child. Keep private version/build evidence separate from ordinary
installed, full scientific and public-provider qualification. Extend the same
wheel through an ordinary installation in a new venv borrowing the preserved
private Conda base; consume the existing shared installed runner and record
effective closure/provenance without calling it a clean solve.

## Why

A prospective number alone does not consolidate a working checkpoint. Fixing
the source and checking actual versioned payloads makes the first-tag decision
reviewable without repeating science or presenting private/development evidence
as a publicly installable dependency combination.

## What was refuted

The private tag does not touch the real checkout or upstream and is not a
release event. The private wheel is not a PyPI/public package. Its intended
version differs from the untagged source-CI version; matching 62 non-generated
files does not accept every consuming scientific/installed gate. A later
documentation commit or earlier green source cannot silently replace the fixed
candidate. No local molecular fallback is needed.

## Scope and exclusions

Release preparation and bounded software checks only. No public tag, GitHub
Release, registry write, dependency installation/update, provider change or new
scientific/native operation. The later ordinary consumer installation is confined
to the new private venv. Original artifacts, frozen helper/fixture inputs,
source pins and workflows remain. Core plus Extended stays the 1.0 target;
provider-issue and live-visual deferrals remain in force.

## Acceptance criteria and current evidence

The local metadata/payload/import projection passes at intended version `0.1.0`:
63 declared runtime files, 62 unchanged source files and a separate generated
version. Exact private wheel/input/receipt identities and explicit limitations
are in the dossier. Source dependency composition and the bootstrap's non-lock
boundary are recorded. Thirty existing non-native support contracts pass against
the unpacked `0.1.0` wheel with published Pytest Receptor 1.2.2 and zero final
warnings; the initial launcher-only warning is retained. The separate 38-test
administrative selection passes with its existing published Receptor 1.2.1
profile. These are scoped software checks, not installed/scientific acceptance.
The separate ordinary installed population passes 139 non-native cases with
published Receptor 1.2.2 and one retained SMonitor assertion-rewriting warning.
It verifies 4,151 exact wheel payloads/import origins before/after, retires shared
support and preserves all 45,015 inventoried original file/link entries. The
observed inventory records 206 base Conda packages, 97 effective Python metadata
records and private overrides. Neither population qualifies full installed
science, clean source-CI reconstruction or public delivery. Local Ruff/index/link
and final committed-export resource/publication controls must pass before handoff.

The issue remains partial: receive candidate CI/closure, qualify the actual
source-use route and complete the required gate/reuse decision before releasing.
The central source-release notice is drafted but currently deferred with
other-repository issue work; it must not be omitted after an actual event.
