# Fixed-pose scoring reference evidence

Owner: [BindingMT #78](https://github.com/uibcdf/bindingmt/issues/78).
Decision: [BMT-047](../DECISIONS.md#bmt-047--record-the-executed-fixed-score-reference-convention).
This is one implementation slice of the [complete pre-stabilization plan](../PRE_STABILIZATION_PLAN.md).

## Executed native convention

The adapter calls `Vina.score()` without a supplied unbound energy. In Vina 1.2.7,
that path evaluates the current conformation's intramolecular reference; search
instead shares its best-pose reference across returned poses. The eighth fixed-
score component records the reference value. This distinction matters before
comparing fixed-score and docking totals. Sources:
[Python API](https://github.com/forlilab/AutoDock-Vina/blob/v1.2.7/build/python/vina/vina.py)
and [native implementation](https://github.com/forlilab/AutoDock-Vina/blob/v1.2.7/src/lib/vina.cpp).

## New optional record fields

Each new score descriptor context adds:

```json
{"reference_energy_policy": "native_current_conformation"}
```

Its scoring-history evaluation adds the following record (the quantity shown
is an illustrative zero, not a new computed molecular observation):

```json
{
  "reference_energy": {
    "schema_version": "1.0",
    "policy": "native_current_conformation",
    "score_name": "evaluation.lig_intra_best_pose",
    "value": 0.0,
    "unit": "kcal/mol"
  }
}
```

The component name follows the caller's evaluation name. The value is copied
from normalized native output, without another energy computation or offset.
Method/backend version, input hashes, captured bytes and existing components
remain separate. No public argument, protocol parameter, backend operation or
runtime dependency is introduced. Existing support-library boundaries remain.

The value is the **reported component**, not recovery of an unrounded internal
quantity. The qualified upstream Python API rounds its returned energies to
three decimals. Matching those reported values does not establish an identical
internal reference between separate evaluations; a future supplied/shared
reference would need its own recorded execution parameter and policy.

## Audit and legacy behavior

`audit_pose` and collection `audit_result` share the checks. When either new
declaration is present they verify the supported schema/policy, component score
name, descriptor agreement and finite real value with an explicit energy unit.
PyUnitWizard converts the quantity to kcal/mol; only conversion roundoff
(`1e-12` relative and absolute) is admitted, preserving application unit policy.
Contradictions are inconsistent; missing required evidence stays incomplete.

With neither declaration present the old report remains unchanged. The auditor
does not infer a reference policy from a software label or alter frozen records.
Legacy consistency remains agreement within its original checks.

Audit tests use detached synthetic declarations over a retained control; these
are not a new producer for historical data. A substituted engine checks adapter
recording. The canonical legacy report digest remains the one retained by #76.
Controls cover wrong policy/value/component/unit/schema/container, missing
evidence, nonfinite/coerced values, nondefault units, detached reports, collection
paths and unchanged strict ranking refusals.

## Remaining workflow boundary

This does not establish molecular identity, prepared-field equivalence, a shared
reference, affinity or permission to rank different pose inputs. #78 still needs
a justified comparison policy and registered representative execution. Molecular
projection/identity are requested in MolSysMT #599/#447; partial/reference reading
remains #521. No molecular editor, parser, matcher or fingerprint is added here.

Original populations and fixed candidate `905abc9` remain separate. New checks
must identify their actual source/artifact/scope. Broad hosted receiving remains
#28; scientific, public/platform and visible acceptance retain their own gates.

## Executed receiving — 2026-11-06

The [separate receipt](data/scoring_reference_2026-11-06/receiving.json) binds
implementation `49a7729866d0ac59f6801e68188a570ab1a1afa0`, source/test inputs,
private artifact and all diagnostic outcomes. Routine Python 3.14.7 passes
**155 selected tests**, one native execution case deselected: 153 saved-record
guards plus two substituted-engine adapter controls. The latter retain existing
public MolSysMT geometry reads; no real native scoring/search runs. Development
provider versions are recorded separately from the controlled CI/private pins.

The qualified local run uses isolated, unchanged published Pytest Receptor
**1.2.2** files verified against the retained Conda artifact records. An earlier
155-pass development-Receptor run is exploratory; the initial overbroad new
guard also remains recorded (154 passed/one failed). Its substring matched
`score_preference`; the corrected guard binds the canonical legacy report digest.
The full selection passes again with the published tool, without changing the
shared environment. These are separate outcomes, not erased failures.

An independent small borrowing installation on Python **3.12.16** passes
**106 record-only tests**, no failures/errors/skips. The new wheel SHA-256 is
`8bc74aa122a41eb4b9514f901a3c747c32a6d685ce428139c7ad8cb07b3c4908`,
actual Git-free version `0.0.0+unknown`. All 63 runtime files match the wheel
before/after; 62 non-generated files match committed source. Original docking
and standalone-pose reports retain the #76 canonical digests. Molecular/native/
viewer operation and optional-provider import guards record zero attempts.
The original 0.1.0 base consumer files/metadata remain intact, and pip check
passes. One SMonitor assertion-rewrite warning is retained. The narrowed
selection consumes no helper namespace and does not replace the full gate.

Both selections run serially on one logical CPU at low priority, native workers
limited and RAM reserve monitored; no resource interruption/heavy restart occurs.
Owned build/source/harness/venv scratch is retired after handoff; exact wheel,
inputs/source hashes and diagnostics stay under #78/#50 for review on 2026-11-13.
No public package, release, scientific-panel or full supported-matrix acceptance
follows. #78 remains partial for molecular receiving/comparison and the actual
representative E1 workflow; the broader goal remains active.

The [separately prescribed installed native receiving](https://github.com/uibcdf/bindingmt/issues/78#issuecomment-6679255611)
then executes exactly two fixed-score calls, Vina and Vinardo, on the unchanged
captured inputs of the deliberately overlapping software control. The
[new producer record](data/scoring_reference_2026-11-06/native_scored_pose.json)
and [receiving](data/scoring_reference_2026-11-06/native_receiving.json) are separate
from the historical fixture and the 155/106 selections. Native Vina 1.2.7,
private MolSysMT `00abb958f`, the same new wheel and Python 3.12.16 produce 16
values/two histories with the new references, independent JSON roundtrip,
consistent standalone audit and incomplete collection audit without invented
contradictions. There are no captured warnings; the 63 consumer files match
before/after. This guarded serial cell finishes without resource interruption.

Existing public MolSysMT geometry reads occur; no search, optimization, new
preparation/repair, ranking or viewer runs. Preparation remains unassessed and
state labels remain declarations of this control. It is installed native
integration evidence, not an independent molecular case, multi-pose E1 acceptance,
chemical validity or recovery/affinity result. The old producer is not relabelled.

### Scalar-declaration refinement

The unreleased initial reader raises `ValueError` if the new policy/component
name is a two-element NumPy array in an already loaded mapping. Refinement
`36c526c8eedb70624dba22e7437021ecd77dceb6` explicitly rejects non-string/empty
declarations as inconsistent, with two regression controls. Its
[separate receipt](data/scoring_reference_2026-11-06/refinement_receiving.json)
records **157 source / 108 installed** tests passing, extending the earlier
155/106 selections by two controls. These overlapping software counts are not
new molecular populations. One installed assertion-rewrite warning is retained.

The refined wheel SHA-256 is
`247afd4f5745a8d3bdcf0960981fee8e18f3af8c78cc4d0517cd074813f7b386`.
Its 63 installed files match before/after; 62 source files bind to the new reader.
The emitter/private native-component files are unchanged from `49a7729`.
The refined reader receives that frozen native producer with identical canonical
standalone/collection audit reports, zero new native calls and zero guarded
external operations/imports. Pip check and original base preservation pass.

The shared routine environment's post-selection pip check reports pre-existing
external-package closure conflicts (missing pdb2pqr and incompatible NumPy/
Biopython requirements). The scoped source results are not clean-closure claims;
no shared environment repair is performed. MolSysSuite #82 owns the workspace
scope. The isolated private receiving remains distinct and passes pip check.
