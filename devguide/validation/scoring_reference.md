# Fixed-pose scoring reference evidence

Owner: [DockingMT #78](https://github.com/uibcdf/dockingmt/issues/78).
Decision: [DMT-047](../DECISIONS.md#dmt-047--record-the-executed-fixed-score-reference-convention).
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
