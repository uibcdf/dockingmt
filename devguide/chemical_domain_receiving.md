# Receiving independent chemical domains

This source migration is owned by `uibcdf/bindingmt#56`, coordinated with
`uibcdf/molsysmt#255` and `uibcdf/molsyssuite#155`.

## Current source contract

The adopted development source is MolSysMT
`00abb958fb93649131d5ce5fe5e12e90cf4900e9` on main, with MolSysViewer
`78ede79e2e345593db5bfe80d246d3f6c70bd005`, received separately for
[public player notifications](validation/player_notifications_receiving.md)
under #60. The ChemicalStates checkpoint's original Viewer `ca7ebea6` and
artifact identities remain frozen. These are source inputs, not a
new installed/public package pair. Source pins do not establish a public minimum.
Keep receiving open until the owner qualifies the final source/installed routes
and justifies the published runtime floor before a release. The earlier draft used
provider `9fb77c358`, followed by development checkpoint `de7ffad2a`. Their original
artifact versions and receipts remain unchanged.

Pass the complete MolSys to `msm.chemical_states.get_rotatable_bonds`,
`get_covalent_blocks`, `get_rigid_fragments` and `get_atom_correspondences`.
Preserve structure-associated state selection, original atom axes and provider
refusals. Stable atoms/groups/chains/molecules/entities belong to Topology;
ChemicalStates owns covalent bonds, assignments and state-local components.
Do not recreate a Topology chemistry facade or infer missing chemistry locally.

## Guards and current audit tools

The torsion, rigid-fragment, readiness, receptor-coverage, problem and symmetry
tests retain their independent expectations. Native state fixtures now construct
and label states in ChemicalStates, without changing their reference/assigned
counterexamples. `devtools.qualify_chemical_domain_receiving.state_scope_probe`
compares the two graphs and verifies unchanged source data. It replaces an
obsolete expected capability failure in the current receiving guard.

`devtools.qualify_chemical_templates.snapshot` uses schema
`bindingmt.chemical_template_snapshot@3`: its stable TopologyDict contains no
bonds, while the complete ChemicalStatesDict remains a separate snapshot. This
keeps multistate bonds and preparation history in the mutation audit.

## Historical producers

The dated entry points in `qualify_1iep_conformers`, `qualify_1iep_flexibility`,
`qualify_3ptb_admission`, `qualify_5x72_reference`, `qualify_5x72_rigid` and
`qualify_torsion_policy` producers retain their original pinned provider, source
fingerprints and dated output destinations. Their reused helpers in the 3PTB and 5X72 modules now consume the current
chemical namespace because the active tests call those functions. Proof constants,
source-fingerprint paths and dated output destinations remain historical; no
stored JSON is overwritten or reclassified. Replay an original producer through
its preserved source/exact Git revision. Owner requalification of a full producer
must use a new output identity, exact provider sources and preserved scientific
expectations. The current state-scope guard is separate from that work.

## Scalar property consumption

`connectivity_completeness` is the scalar property of the selected chemical
state. Preparation retains its existing list-valued evidence field by wrapping
that value once. Staging compares the scalar directly after the one-state guard;
complete sources therefore retain the known-source reader and all its map and
later-pose refusals. A string must not be expanded into individual characters.

## Qualification boundaries

Local source tests use the shared development environment and existing native
backend; full source CI and installed candidate/platform qualification remain
separate. Preserve failure, skip and warning evidence. No release, tag, package
promotion, dependency cap or automatic scientific-profile migration follows from
this source change. See the [receiving record](pending_proposals/receive_chemical_domain_separation.md).

## Expanded owner receiving — 2026-11-02

The owner review targets the provider checkpoint requested on #56. The additional
[`chemical-domain guard`](../tests/test_chemical_domain_receiving.py) exercises
13 consumer cases: absent versus zero-state chemistry, unavailable/partial graphs,
missing associations, a valid structure-assigned state without a reference default,
and an explicitly complete zero-bond graph. Copies, MolSysDict and H5MSM 0.5
round trips preserve nonconsecutive selected atom axes, string IDs, structure state
labels and coordinates under angstrom/pm application policies. A controlled
provider edit of the recovered copy preserves both the source and the already
extracted BindingMT input. No downstream chemical store or reconstruction is added.

The preexisting 103-case receiving selection and all 13 new cases pass against
the new ordinary-built provider wheel in the development receiver. Its inherited
shared environment has unrelated dependency conflicts, so this evidence is source
receiving only. Clean installed-consumer and complete hosted qualification are
recorded separately on #56. No dated scientific producer is rerun or relabelled.

Temporary verification resources belong to #56/#50, review 2026-11-09, without
automatic deletion. Independent source copies and receivers preserve sibling
worktrees and historical artifacts. Public records retain resource classes;
operational diagnostics remain local.

## Source adoption and executed owner qualification — 2026-11-02

Source implementation `79740b4ce373c8d98da6f1c9f5633456381f73fa` is adopted from
[PR #59](https://github.com/uibcdf/bindingmt/pull/59). Full local source validation
passes **1,381 tests**, zero skips, 857.34 s, 327 warnings, Python 3.14.7/Pandas
2.3.3. Exact-source [PR CI](https://github.com/uibcdf/bindingmt/actions/runs/41578225641)
and [branch CI](https://github.com/uibcdf/bindingmt/actions/runs/41578221426)
each pass **1,381 tests per Python 3.11–3.14**, zero test skips, ordinary installed,
source-context and dependency-closure gates. Policy and publication governance
pass. Coverage publication is intentionally inapplicable on those events; the
final main checkpoint retains its separate workflow evidence on #56.

The ordinary consumer wheel `0.0.0+217.g79740b4` has SHA-256
`ebf1c30bc3c088b9fe707e50103866e2db1202411c2cace8853225ae9113b51d`.
All 58 runtime Python files plus its generated version match Git/wheel/installed
bytes where applicable. Its clean Linux/Python 3.14.8 receiver uses Pandas 3.0.6
and passes dependency closure. The independently built MolSysMT wheel has SHA-256
`4a8e58f40627ff468fab99301674429fba66362f549a31fb4cc747d9cf19a0ba`;
all 3,055 Python/native members match installed bytes. These private verification
artifacts are not public package availability or installed-platform admission.

The initial complete installed selection has **1,376 passes / five failures**,
879.83 s. Missing harness governance files and Git context cause all five failures;
this result remains failed evidence. A corrected independent sparse checkout has
no runtime source packages and retains all 146 existing test/helper files
byte-for-byte. The **131-case correction passes**, zero skips, 76.42 s, including
all five initially failed identities and the domain/state/reader/symmetry controls.
The unchanged artifact, dependencies and scientific fixtures retain their initial
passing evidence. No single clean full installed rerun is claimed.

All **389 historical evidence files** remain unchanged. Original scientific
producers and the earlier draft's provider/results remain distinct. #56 stays
partial for provider-wide final receiving and the installed/public/platform and
real published-minimum questions under #30/#47. Any new historical-producer
experiment requires a separate identity; no old result is rewritten. Source
adoption does not certify broader chemical profiles, visible C4/C6 or a release.

## Main-source receiving and complete installed gate — 2026-11-03

MolSysMT #255 is resolved and its implementation is available at main commit
`00abb958fb93649131d5ce5fe5e12e90cf4900e9`. Direct Git comparison verifies identical
objects for `molsysmt`, `molsysviewer_molsysmt`, `rust`, `tests`, `pyproject.toml`
and `MANIFEST.in` against `de7ffad2a`. The core package tree is
`4dfb3a9419e912d024e0381427337e9383e8ce46`; the Rust tree is
`32cfb07b9c26ae9ad3ed379c1b76fab85669cf67`. Source location and new generated
version metadata are separate from this tracked implementation equivalence.
Controlled CI/dependency routes now select the exact main commit. Viewer and
ArgDigest pins, molecular implementation and scientific expectations are unchanged.

The private ordinary wheels above retain their original producers, versions and
SHA-256 values. Neither wheel is rebuilt or relabelled to represent main. Installed
Python/native members and all 58 BindingMT runtime files are checked again before
qualification. The complete `tests` selection is re-executed through immutable
SDK `738fe8dd731abb99dac421b0bb2acc8564110180` in the verified corrected context:
real Git history, root governance/workflow files, complete fixtures and no runtime
source packages. Inherited pytest source paths remain cleared. Its new full-run
receipt and actual result are recorded on [#56](https://github.com/uibcdf/bindingmt/issues/56),
separately from the failed original run and 131-case correction above. The new
run does not rewrite either earlier result.

The provider's eight-cell source matrix and exact-main smoke gates have succeeded;
the [owner handoff](https://github.com/uibcdf/bindingmt/issues/56#issuecomment-6596245045)
retains disclosed optional skips and separates original versus main execution.
This is not provider package publication. Remaining public coordinates, justified
published API minimum and exact installed/platform admission stay under #30/#47;
#56 records the current receiving disposition. Visual C4/C6 remains deferred.

New verification receipts belong to #56/#50, review 2026-11-10, without automatic
deletion. Existing artifact/receiver resources retain their prior ownership and
review record. Operational diagnostics stay local; historical evidence is frozen.
