# BindingSite offline domain geometry increment

Owner: [BindingMT #111](https://github.com/uibcdf/bindingmt/issues/111).
Admission: 2026-11-13 before implementation. Status: implemented/source-received
C2 internal geometry slice; public placement application pending.
Base: `08356484a6e30ab173fb0b123ae9c6b8b652f30b`.

## Work commissioned and public boundary

Implement the offline geometric substep of the accepted C2 plan, independently
of actual client molecular receiving of the [reviewed MolSysMT #746 offer](binding_site_molecular_contract_receiving.md). The private
`derive_geometry_box` operation consumes an actual BindingSite and returns an
existing BoxRegion with a complete, independently validated offline derivation.
No public `to_search_domain` stub or molecular application is advertised. Its
future public route still requires the assurance decision, actual problem/input
placement and final check/use profile in the implementation plan.

Keep the new BoxRegion recipe readable/inspectable through ordinary records,
but refuse numerical backend export while placement is not assessed. Existing
plain boxes and strict `bindingmt.box_derivation@1` selection recipes retain
their exact contracts. A readable or mathematically valid saved geometry never
becomes a placed molecular application by being loaded into a problem.

## Admitted geometry and effective request

Only the existing one-view BindingSite 0.3 geometry profile is eligible. Omitted
`view` resolves its sole `geometry` key; another key, nongeneric declaration or
unsupported method refuses. Require an explicit method:

- `sphere_enclosure`: preserve the center and produce full lengths
  `2 * (radius + padding)` in each Cartesian direction.
- `axis_aligned_box`: preserve center and full lengths, adding `2 * padding`
  per direction. Require axes exactly equal to the identity; no rotation,
  snapping, transform or silent axis-aligned approximation is commissioned.

Padding is either None (no requested enlargement, effective zero) or a finite
explicit nonnegative scalar length. Preserve that request distinction and seal
the physical value. The output is canonical nm with finite positive extents;
overflow refuses without repairing values. Source structure/state scope, frame,
definition, evidence and original claim references remain in the exact original
site record. No molecular coordinates, selections, maps or optional tools are
accessed. A geometric enclosure supplies no new binding evidence or membership.

## Experimental local recipe and reader

Use nested `format="bindingmt.site_domain_geometry"`, `format_version="0.1"`,
`experimental=True`. This is a local offline recipe, not the proposed shared
site-application `@1` schema or a new package/BoxRegion schema version. Older
actual readers must refuse it rather than discard the recipe.

Retain the complete original site, its exact record/content/definition/view
reference, requested method/view/padding, sealed resulting center/full lengths,
geometric relation and limitations. Use public PyUnitWizard QuantityRecord with
owned fields `bindingmt.site_domain_geometry.padding`, `.center`, `.lengths`;
verify field, length dimension, target unit and scalar/vector shape. Readers
recompute the admitted recipe from its retained inputs and compare the output
and current BoxRegion geometry under the declared numerical convention. They
must not trust an edited result merely because it was resealed.

The fixed assurance state is `geometry_only`, placement/current-finding and
molecular correspondence `not_assessed`, membership `not_requested`. An exact
unexpanded axis-aligned box has relation `equal`; spheres and enlarged boxes
have relation `encloses` and unquantified added support. No binding-region
volume, exclusion, contact cutoff, state equivalence or source authentication
is inferred. The recipe remains intact on failed placement/export requests.

The mathematical check uses exact binary64 operation results from canonical nm
inputs through an explicit internal Pint handshake, independently of the active
public quantity form. Retained output versus recomputed recipe is exact; binding
to the current BoxRegion permits only representation roundoff, relative tolerance
8 binary64 epsilons and zero absolute tolerance, after explicit nm conversion.
This is a numerical convention, not a new scientific distance cutoff. Ordinary
BoxRegion records retain their existing serialization. Object-key order is not an axis;
sorted/reversed JSON must keep all identities and ordered geometric data.

## Receiving and remaining gates

Use analytical sphere/box cases and explicit equivalent units under normal and
pm/fs policies, including active unyt, zero/positive/None padding, overflow,
orientation refusal, bad quantities/fields/seals, exact source/evidence custody,
detached ownership, modified input/output/ref/assurance refusal and stale current
box geometry. Test ordinary BoxRegion/problem/result record propagation without
turning it into molecular-placement evidence. Backend projection must refuse
before native Vina work. Preserve original resource exceptions and all prior
resource interruptions.

Qualify the complete affected selected modules serially with one CPU/native
worker, low priority and monitored resource bounds; preserve task source/input
hashes and all attempts. Add actual saved records, fresh unyt/pm-fs reading and
an archived prior decoder refusal without source/prefix/native rebuilding.
Keep original compatibility producers and installed-test support hashes intact.
Run the six applicable documentation/resource gates in the workspace and fresh
committed export, and record exact evidence here before publication.

C1, the public C2 application, real input/normalization/placement lifetime,
stronger finding assurance, rich/oriented geometry application, T/H/P and shared/
consumer/installed/public/platform/hosted receiving remain separate. No prior
held evaluator or scientific campaign is restarted. Raw inspection/receiving/
publication receipts retain #50 custody in
`.molsyssuite/site-domain-geometry-111-20261113/`, review 2026-11-14.

## Actual source receiving — 2026-11-13

The final complete selection passes **557 cases per policy**, normal and pm/fs:
520 core/record/recipe cases plus 37 argument/bootstrap cases, including
**62 new offline-geometry controls**. The complete existing 22-case
`test_domain_derivation.py` module is newly selected relative to the prior
473-case checkpoint. Its orchestration-only stand-in now explicitly provides
software Vina availability/module/version, following existing test patterns;
it needs no real Vina installation and retains all projection/result assertions.
This is not native Vina evidence. The selection retains 30 legacy-H5MSM warnings
and two warnings from deliberate shape-corruption controls, with no test skips.

The actual producer saves seven domain variants (None/zero/positive padding,
both shapes, annotations and reinterpretation), one authored empty-result control
and a plain box. Original plus sorted forms total **18 files**. A fresh
unyt/pm-fs reader restores the recipes, physical values, original site/claim refs
and result propagation, refuses backend export of all seven unplaced domains,
and retains ordinary plain-box export. It performs zero molecular operations,
optional engine imports or new originating uses; input bytes and policy stay
unchanged. Normal problem/result propagation and pre-preparation/native-engine
refusal are also tested through actual public APIs with explicit software controls.
No successful molecular placement or executed binding study is claimed.

The actual archived 0835648 decoder refuses both new sphere/box recipes, rather
than silently discarding provenance. Its temporary export is retired and the
copied existing generated version module is separately hashed metadata context.
Five original 0.3 site outputs are frozen unchanged under
`tests/data/site_domain_geometry_compat/0835648/`; seven exact support entries
cover them and their producer/source manifest and README. Production-base e1e6a33
and source-qualified 0835648 remain distinct; existing scientific fixtures,
producer identities and earlier compatibility inputs are unchanged.

Initial focused attempts retain their assertion/setup failures: exact integer
comparison did not admit the original sphere's binary64 conversion roundoff,
and an engine-refusal sentinel initially intercepted DepDigest's intended
availability probe. The final implementation computes/seals recipes through
explicit internal Pint and permits only the documented BoxRegion representation
roundoff. The final software control supplies availability while still refusing
any real optional engine import/preparation. The early 60-case focused and
518-case core populations precede the final two shape controls and are not
relabeled as final evidence. Every attempt remains in the task ledger.

Executed source closure remains MolSysMT
`ff25f120243319ca9515009b4971e24a2eb0dc22`, PyUnitWizard
`cc51c8e600f78f108bc563edd3221bd8788ead86`, ArgDigest
`7be790b7334e16715fceebbfa8a2b400edf768bb`, SMonitor
`4a4cd1e415ea57e50c22925c36c2e727772fb3ab` and DepDigest
`5e93eaff314fe7cddf4eee89842977023b3a8b00`. Existing provider floors are unchanged
(PyUnitWizard >=0.29.3 covers the used public record handshake). Runtime/test/
support/resource hashes are retained before/after each final selected cell.
The historical on-disk MolSysMT native SHA-256 remains
`2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`;
build/source authenticity and wider provider qualification are not inferred.
Existing small MolSysMT domain controls execute under that recorded closure;
the data-only producer/cold reader make no molecular calls. No sibling worktree,
prefix, native binary or concurrently changing PharmacophoreMT source is changed.

The published central status tool records fetched advances without merging.
The older sibling MolSysSuite registry could not recognize BindingMT; the
rename-aware official bb641488 snapshot supplies the bounded six-member status
instead, preserving that inspection limitation. Missing MolSysMT #746 and
PeptideMT #60 owner dispositions remain pending.

Execution is serial on CPU 0/nice 10 with one native worker, 512 MiB group RSS,
2 GiB AS, 45 CPU/120 wall seconds and a monitored 13 GiB available reserve.
Final selected-test peak stays below 363 MiB; all owned groups terminate without
resource interruption. The previous #30 evaluator hold is not restarted.
Six applicable workspace and fresh committed-export gates cover Ruff, format,
indexes, documentation references/sketches, exact shared resources and the Conda
contract; exact outcomes/public commit/readbacks remain in #111/#30 and the
task's publication/closeout receipts. No hosted/installed/public/platform or
consumer-adoption pass, new package/tag/release or scientific campaign is claimed.

The separate authored normalization probe reproduces an OS ENOMEM wrapper;
[BindingMT #116](archive/molecular_input_os_resource_error.md) owns that
follow-up. It changes no C2 input or receiving result. Next fix that admitted
resource path, receive #746's finite C1 facts, and settle/qualify the public C2
placement/assurance and actual normalized-input check/use lifetime. This internal
geometry delivery is not M2 completion and does not add a public application stub.

## Current molecular/resource disposition — 2026-11-14

[MolSysMT #746's finite offer is reviewed](binding_site_molecular_contract_receiving.md),
and [#116's normalization fix](archive/molecular_input_os_resource_error.md)
has separate source-only software receiving. The dated owner-wait and next-fix
statements above retain their original 2026-11-13 scope. Actual client source/
native qualification and public C1/C2/M2 still need their real operations and
placement/check-use evidence; the 557-case geometry population is unchanged.
