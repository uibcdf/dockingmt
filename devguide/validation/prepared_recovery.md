# Prepared-input recovery checks — 2026-10-29

Owner: [#57](https://github.com/uibcdf/dockingmt/issues/57), a bounded follow-up
under [#4](https://github.com/uibcdf/dockingmt/issues/4). This strengthens the
existing `DockingResult.reconstruct_problem(receptor=..., partner=...)` workflow
from the [preparation/provenance profile](preparation_profile.md). It does not
introduce a molecular snapshot, new storage API or implicit preparation.

## Observed defect and resulting behavior

At `12b5360`, a one-atom software fixture records a prepared ligand with state
`partner-A` and supplied 0.0 e. Supplying the same-size object after changing its
state to `different-state` and charge to 0.5 e still recovers successfully.
Existing atom/frame/native-state checks do not bind those prepared declarations.
The reproduction uses an empty result and performs no search or energy calculation.

Recovery now checks the existing saved object declaration against the supplied
object's `to_dict()` using finite canonical JSON. State labels, charges, types,
names/hierarchy, declared torsions and preparation metadata must match exactly.
A backend string cannot substitute for a recorded object declaration. Missing
legacy object declarations stay missing; no molecular identity is inferred.

For a saved Vina role with a recorded PDBQT format and valid input SHA-256,
recovery renders the supplied prepared object through its existing public
MolSysMT-backed writer and requires the same submitted bytes. This also detects
coordinate edits that were not present in the prepared declaration. The existing
artifact inspector checks every retained role before requesting any export;
malformed hashes/records and corrupted captured bytes reject first. A valid hash
still binds the supplied representation when optional byte capture is absent.

Only after all checks pass is `result.problem` attached. A declaration, artifact
or provider failure preserves the previous attachment, original result record and
caller inputs. Provider errors propagate without a fallback. Recovery requests
no H generation, charge/type assignment, energy, optimization, docking or viewer.
The signatures, outer schemas and saved-result reader remain unchanged.

```python
saved = dockingmt.DockingResult.from_dict(record)
problem = saved.reconstruct_problem(
    receptor=original_prepared_receptor,
    partner=original_prepared_ligand,
)
```

Use the actual original prepared inputs and their recorded declarations. An
independent equivalent object is acceptable if the checks match. Matching is
checked at recovery time, not maintained by a cache over later caller edits.
If current preparation declarations or writer bytes differ from an old producer,
that is a different input; declare a new problem/run instead of silently treating
it as the old one. Original result files remain readable and are never rewritten.

## Ownership and limits

DockingMT compares its own saved declarations and operation-specific byte hashes.
The shared artifact inspector validates bytes only. All molecular rendering,
construction, copied views and scientific validation remain in public MolSysMT;
no PDBQT parser, atom matcher, graph checker or coordinate algorithm is added.
A recovery verification export is separate from later engine staging. Its map is
not rebound to saved bytes or reused as a future engine operation's map.

This is **available-evidence consistency**, not authentication of arbitrary caller
claims or full molecular identity. In particular:

- Absent legacy hashes/formats cannot establish coordinate agreement. Matching
  stored declarations remains useful, but missing evidence is not fabricated.
- Identical PDBQT bytes establish equality at the submitted writer precision.
  A coordinate change below that precision can legitimately keep the same bytes;
  this does not prove full-precision source geometry is identical.
- A prepared object's absent original-file fingerprint remains absent. State labels
  do not become experimental protonation evidence; matching bytes do not recreate
  complete chemistry or original transformation history.
- `DockingProblem.from_dict` retains its existing molecular-axis/fingerprint
  contract. The additional checks apply to recovery from `DockingResult`, where
  operation-specific submitted-byte evidence is available.

The [case-bundle contract](preparation_profile.md#source-provenance-is-a-bundle-contract)
and #4's broader persistence/recovery scope remain partial. General mechanics
storage is [MolSysMT #256](https://github.com/uibcdf/molsysmt/issues/256), not a
missing serializer to implement downstream. No new provider capability is needed
for this fix: the native writer and existing DockingMT integrity tool already
cover the accepted recovery operation. The incoming ChemicalStates migration
notice #56 retains its separate receiving scope and does not change provider pins.

## Verification and retained evidence

[The guard module](../../tests/test_prepared_recovery.py) has **38 cases**:
both-role state/charge/type/hierarchy/metadata refusals, torsion changes, input-type
substitution, shifted coordinates with and without captured bytes, corrupt
artifacts, matching public exports under angstrom/pm policies, failed-recovery
atomicity, source-free and real named-source preservation, provider refusal,
legacy missing evidence, subprecision equivalence and absence of engine/viewer/
chemical-preparation calls. These are software fixtures, not new scientific cases.

The initial module reports 30 failures / four passes on the old implementation.
An intermediate selection reports 194 passes / four failures: its coordinate
fixture had silently truncated fractional edits in an integer array. Explicit
floating-point fixture edits correct that diagnostic, with no provider change.
A later 267-case selection passes; final additional controls include a real native
source and the representation-substitution boundary. The final source selection
passes **271 tests**, 67.65 s, zero skips, 25 warnings, including all 38 guards.
Overlapping counts are not added.

[Indexed source evidence](data/prepared_recovery_2026-10-29/manifest.json) retains
the probe, diagnostics, final results and source hashes. Ordinary installed-file
and exact-head hosted receipts are recorded separately on #57; an old wheel does
not qualify this changed runtime code. Source/ordinary-installed checks preserve
original scientific data and producers. No historical search population is rerun.

Task verification resources belong to #57/#50, review **2026-11-05**, with no
automatic deletion. One verified unused prior build checkout is retired while
its qualified wheel, receiver, harness and canonical source remain intact. Public
records use resource categories; machine-specific diagnostics remain local.
Visual C4/C6 stays deferred under #52. No package or release is published.
