# E2 named rigid preparation receiving — 2026-11-07

Owner: [BindingMT #81](https://github.com/uibcdf/bindingmt/issues/81).
Registration status: **prospective**. Qualification base: `782fe9e`.
Custody: `.molsyssuite/e2-preparation-20261107`, reviewed under #50 on
**2026-11-14**. This is the next bounded increment of the
[complete plan](../PRE_STABILIZATION_PLAN.md), not whole E2 acceptance.

## Population, question and immutable inputs

Receive two fresh named preparations from the already admitted P59(R) and
P69(S) sources. The question is whether the public source recipe and explicit
Gasteiger–Marsili/AutoDock4 rigid preparation preserve the declared axes,
geometry, hydrogen inventory, stereo interpretation and mechanical provenance
through actual exported inputs. No docking, rescoring or comparison of energies
is registered here.

Keep the [candidate inventory](data/e2_ligand_collection_candidate_2026-11-07.json)
at SHA-256 `898b26fa60561bb99f823d2dd0c27216cc5771ac7dceacdb103760fed2e22284`
and the [source archive](data/e2_source_admission_2026-11-07/manifest.json) at
SHA-256 `a5a60b65715b466bd04dc5e2bdb41a73489fdf9a13254552870628d387221b8d`.
Verify actual stored and decoded bytes. Two source states are two distinct
declared stereochemical entities from one experimental complex, without activity
labels. Their 39-atom starting conformations are not crystal reference poses.
The common external protein-only receptor and joint two-site box remain context
only; this increment does not assess or prepare the receptor.

Reproduce each exact source through public `msm.convert`: SDF to native with
`stereo_engine='rdkit', discard_properties=True, return_report=True`; native to
RDKit; RDKit to the new native authority. Compare actual native inspections to
the previously received records, including complete declared chemical-state and
structure fields, IDs, elements and physical coordinates. Reports and raw source
properties remain separate. Inspection JSON is comparison evidence, never a
molecular/mechanical restoration input. A difference refuses preparation; do
not patch old observations or synthesize missing chemistry.

## Named preparation and receiving boundaries

Explicitly request public MolSysMT charge assignment with
`method='gasteiger_marsili'` and the declared neutral total
`expected_total_charge=puw.quantity(0, 'elementary_charge')`, then AutoDock4 atom typing with
`typing_scheme='autodock4', method='chemical_environment'`. Preserve each actual
return/report and the untouched source representations. Assignment produces new
evidence; it does not restore a historical assignment or establish biological
validity. No H builder, coordinate optimization or implicit model selection is
permitted.

Pass the named typed authority to public
`dmt.prepare_ligand(..., state_id=<declared candidate state>,
active_torsion_bonds=[])`. The chosen new model is rigid. It does not replace
historical two-cut torsion models. MolSysMT owns nonpolar-H projection,
mechanical derivation, chemical inspection and the molecular writer/reader.
BindingMT owns its preparation and charge-consumption records.

Receive, without inventing expected chemistry:

- Actual source/typed/prepared atom axes, identities, coordinates and complete
  source-to-retained/export maps. The historical expectation is 25 retained
  atoms, one indexed polar H and fourteen merged nonpolar H; actual provider
  reports and inventory must establish the new outcome.
- Public hydrogen inventories before/after projection, retaining indexed,
  virtual explicit and implicit roles, parent assignment and any uncertainty.
  Preserve total H accounting without asserting unrestricted graph equivalence
  between different H encodings.
- Actual declared CIP reports on the 39-atom authority and retained native
  preparation, with `engine='rdkit', from_coordinates=False`, one selected
  structure/chemical state, and source index 7 transported through provider maps.
  Complete retained-axis self-witnesses apply only to that new representation.
- Named source and projected charge/type reports, finite values, explicit
  elementary-charge extraction, actual charge transfers and conservation within
  `1e-6 elementary_charge`. Public `audit_preparation_charges` must receive the
  consumed values and PDBQT rounding evidence. This is integrity, not model
  accuracy or force-field validation.
- Public `PreparedLigand.to_molecular_system()` and `to_pdbqt()` results. Capture
  the actual public MolSysMT writer return/map used by the export; never call a
  local molecular serializer. Save exact final text bytes/digests, remarks,
  rigid tree, expected traversal and corresponding provider readback. Quantized
  coordinates/charges retain their explicit tolerances and original precision.
- Original source, assigned source and prepared live-object nonmutation during
  receiving/export, source-file/archive nonmutation, detached records, caller
  policy preservation and restoration. Record all unassessed chemical checks.

The unexecuted qualification notebook and its exact direct operation caps are
frozen at launch. Caps for the complete two-candidate selection are:

| Direct operation | Cap |
| --- | ---: |
| SDF/native, native/RDKit, RDKit/native reproduction | 2 each (6 total) |
| Named partial-charge assignments | 2 |
| Named AutoDock4 type assignments | 2 |
| Public rigid ligand preparations | 2 |
| Hydrogen inventory, authority/prepared | 4 |
| Declared CIP, authority/prepared | 4 |
| Prepared readiness and prepared self-witness | 2 each |
| Prepared native conversion and PDBQT export | 2 each |
| Public preparation-charge audit | 2 |
| Provider pose readback, composed atom map and torsion-tree receiving | 2 each |
| H generation, geometry optimization, scoring, searches, H5/MM persistence | 0 |

Internal getters/conversions, export-internal charge audits and the requested
preparation's two provider projections are observed separately from these direct
calls. Full-axis source self-witness/readiness are already received; new source
inspections are compared with that evidence before assignments. Do not grow the
population to obtain a passing subset or introduce a generic workflow engine.

The reviewed [preparation notebook](e2_ligand_preparation_receiving.ipynb) has
SHA-256 `76df8d7656c8e3ca37564f8c4a44d614f63a5629ffb2052db3d76b5dc2b8b26e`:
one Markdown cell and three unexecuted Python cells. Static API review, AST,
Ruff and formatting pass before launch. Derived mechanical reports are bound
to their actual projected source assignments; complete live PreparedLigand
declarations and physical coordinates are checked before/after receiving.

## Runtime, resources and failure policy

Reuse consumer wheel/source `a7422df`, SHA-256
`93d76f898575fb64b39520f33ceded25708270c8042c2a53c9a451acd834bcdd`,
the existing 3,867-file private target and borrowed MolSysMT source
`9e1f1b1ad8bf09446374ab6f04ca7208e2717936`. These are controlled private
identities, not public dependency minima. No provider install/rebuild, editable
fallback, native Vina overlay or Vina import is needed. Freeze actual module,
helper, native-library and routine environment identities; verify private
payload, source archive and routine metadata before/after. Use the unchanged
shared staged installed-test support declaration, outside the runtime payload.

One complete two-candidate selection runs under an explicit pm/fs/coulomb
caller policy. Use physical target units at every numerical/wire boundary.
Serial CPU 0, nice 10, one native/build worker including descendants, monitored
8 GiB available-RAM reserve, 1 GiB owned-group RSS, 2 GiB address space,
60 CPU seconds and 90 wall seconds per process. Check available headroom before
launch and each cell, monitor throughout, stop only owned work on threatened
limits, and preserve resource interruptions without automatic restart.

Record each attempted stage and actual returned data before qualification
assertions. A failure stops the complete selection, preserves its producer and
not-attempted denominator, and receives an explicit diagnosis. No automatic
retry, source substitution, silent repair or relabelling. Any new molecular
capability gap goes to MolSysMT with linked consumer evidence.

After a passing selection, a fresh standard-library reader receives sealed
records, source/state associations, maps, physical units, numeric conservation,
actual export identities and all operation/resource outcomes, without molecular
imports or recalculation. The reader checks recorded evidence; it is not an
independent chemical validation or producer authentication.

The later native success/refusal/success collection, finite search protocol,
all five native energy columns, separate study-prioritization policy and full
E2 receiving still need their own registration and execution. The broader
scientific panel, public delivery, exact-head hosted gates and E4/live-visual
holds retain their owners. No runtime API, dependency, release or package is
selected by this prescription.

## Received molecular selection — 2026-11-07

`prep-01` passes the complete two-candidate selection. The exact public source
recipe reproduces both previously admitted initial/authority inspections before
new assignments. Each fresh named Gasteiger–Marsili calculation and AutoDock4
chemical-environment assignment preserves its input chemistry and geometry.
Both rigid preparations have 25 atoms and 28 bonds, retaining one indexed polar
H and fourteen virtual explicit H after provider projection. The public stored
inventory remains fifteen represented H; no H is generated. R/S is preserved
at the mapped chiral atom, and the two prepared self-graph digests are distinct.

All direct caps are met exactly. The two requested preparations invoke two
provider merges internally; two actual PDBQT exports are observed. The new
projected/derived mechanical records retain their actual source assignments.
Both public charge audits are `consistent`, with zero observed full-precision
total difference. The full-precision total is approximately
`-6.94e-18 elementary_charge`; the written three-decimal charges total
approximately `-0.001 elementary_charge`. Preserve that actual rounding and its
bound, rather than changing exported charges to force a zero total.

The original authority/typed/prepared axes, projected coordinates and actual
export maps pass, including provider-composed original-to-written maps. Public
PDBQT readback receives the same payloads within the registered quantization
tolerance; it deliberately does not restore mechanical parameters. Rigid trees,
live molecular systems and complete PreparedLigand declarations/coordinates,
detached witnesses, raw sources and the admitted source archive pass their
controls. The pm/fs/coulomb policy and restoration, all 3,867 private payload
files/origins, routine metadata and 594 staged support files pass. Support
imports/resources are retired. Original stdout/stderr are empty.

This source/preparation process takes 22.13 wall seconds and a sampled peak
owned-group RSS of 336.04 MiB, without interruption or signal. These include
imports, payload hashes and receiving overhead; they are not throughput
measurements. Zero searches, energies, new H, H5/MM restoration or Vina imports
occur. The 96-member original phase manifest is SHA-256
`5e60d80d82d4ec6da2b3b3d7e4c419e61e295f4098eb506f77c665ff2649e769`.

The prepared aromatic representation retains partial integer bond-order
coverage. Provider readiness still lists unassessed valence, protonation,
experimental missing-H inventory, aromaticity perception, stereogenicity,
periodic geometry, conformer quality, charge-model validity, docking readiness
and property origin. An available stored H inventory and named parameters do
not clear those independent scientific questions.

The fresh `reader-01` passes against all 96 sealed preparation members and the
80-member admitted source archive. It independently checks stored/decoded bytes,
the frozen cell budgets and actual operation journal, source reproduction,
state/CIP associations, projection/export/composed maps, stored H accounting,
numerical charge transfers/conservation and rounding, physical units, readback,
support/payload/origin/environment receipts and original nonmutation controls.
It imports no scientific package and performs zero molecular operations. This
is saved-record receiving, not new chemical validation or producer authentication.
It takes 0.82 seconds and 36.58 MiB sampled peak group RSS, with no interruption.
Its 17-member original phase manifest is SHA-256
`0b3b30e5fee3c8023e6edba204b67148abdbb77dac6a72c3bc0b3d0ce97c32a5`.

The [immutable preparation archive](data/e2_preparation_receiving_2026-11-07/manifest.json)
contains 120 members, 1,054,243 stored bytes and 5,045,298 decoded bytes, plus its
manifest. Manifest SHA-256:
`bd4f34c7c696efa1c864c9ea410630398b5ec164726eeaaf6462ea9d9b78d326`.
Every member uses transport gzip with original/decoded hashes, including exact
SDF whitespace and actual PDBQT bytes. The registration, frozen notebooks and
harnesses retain the actual producer. The reader script SHA-256 is
`2fcb67a098a4f1970a840dc34e8c9262d98f805361699335f90a747bcb1654db`.
No historical source file, helper declaration or runtime module is changed.

| Prepared input | Actual PDBQT SHA-256 |
| --- | --- |
| P59(R), `e2-5x72-p59` | `ae0e9d3beb4d14363ea6edb1bff591c56d53b02295082bae8c281d9284d84b9e` |
| P69(S), `e2-5x72-p69` | `1cbe49d31e1859e34b7cc71af1a8514fef9314401401b2b76b6a7e07dfc7ebaa` |

Next register the finite native three-item success/refusal/success collection
and separate study comparison. Reproduce the admitted source/assignment/
preparation recipe and require these actual prepared byte identities before
native use; inspection JSON does not restore molecular mechanics. Retain the
same common receptor/joint domain and every requested/attempted/failed/empty/
completed identity. Preserve five native energy columns and four public scores;
strict same-state `compare_scores`/`rank_by` are unchanged. The native selection
needs its own registration and executed evidence. Whole E2, public delivery, exact-
head hosted gates and the complete product objective remain unproven.

The final local selection passes thirteen applicable checks covering the exact
notebook AST/lint/format, maintained report
indexes/links, all archive stored/decoded hashes, declared dependency/publication
contracts and shared package resources, including fresh source exports. Runtime
and installed helper/data declarations are unchanged; prior software guards
retain their applicable scope without relabelling them as new observations.
Exact-head hosted CI remains missing under #28 and `[skip ci]`; no manual
remote execution is dispatched. The final committed-source checks retain their
own source identity and do not rerun the molecular selection.

## Subsequent native collection — 2026-11-07

The later [registered native receiving](e2_native_collection_2026-11-07.md)
reproduces these exact prepared bytes and receives the real three-item
success/refusal/success collection, five poses, the separate empirical study
decision and a fresh standard-library reader. These original preparation
records/producers remain unchanged. [#81's bounded acceptance](../archive/qualify_small_ligand_collection.md)
is resolved; current work advances independent pose comparison/clustering and
the other full-plan requirements without another search for this acceptance.
