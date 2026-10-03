# Public preparation assessment

`dockingmt.assess_preparation(prepared)` exposes the preparation classification
previously private to Vina. A workflow can inspect a prepared ligand or receptor
before choosing its execution policy, retain the bounded report, and compare it
with the report saved by the backend. It is also exported from
`dockingmt.preparation`. The [executed notebook](preparation_assessment.ipynb)
demonstrates original 181L BNZ preparation and external-input inspection.

## Contract and ownership

The function accepts `PreparedLigand`, `PreparedReceptor`, external PDBQT text or
`pathlib.Path`/string paths, and external objects with a callable `to_pdbqt`.
External representations are unassessed: their content and renderer metadata
are not inspected. Paths need not exist for this declaration-only operation;
the backend still performs its normal input checks before execution.
Unsupported input types raise the catalog-backed `ArgumentError` through
ArgDigest. Unknown keyword names are rejected. Prepared-object metadata must
be a mapping, with charge/type sources represented by strings or `None`.

The returned JSON-compatible mapping has `schema_version='1.0'` and
`scope='declared_preparation_metadata'`. It contains only the two source
declarations, an assessment and ordered provisional codes/descriptions:

| Declaration | Reason code | Assessment |
| --- | --- | --- |
| `charge_source == 'zero_placeholder'` | `zero_placeholder_charges` | `provisional` |
| `atom_type_source` contains `heuristic` | `heuristic_atom_types` | `provisional` |
| Neither marker is declared | No provisional reason | `unassessed` |

Both reasons can coexist; charge precedes typing. Descriptions preserve the
existing Vina diagnostics. Reports are independent across calls and do not
retain coordinates, charges, source systems or nested chemistry reports. The
operation examines two metadata fields, independently of molecular atom count.
It does not read files, render PDBQT, convert molecular forms, or invoke a
backend/viewer. Other preparation functions may perform those operations.

Explicit zero charge values alone do not imply placeholders. A declaration of
an external parameterization method does not certify that it was applied
correctly. Missing evidence, externally supplied PDBQT and unknown source methods
remain unassessed. Molecular coverage, template application and chemical
validation belong to MolSysMT; this tool interprets DockingMT's declarations
under the existing preparation policy. It does not replace provider readiness
reports or assess scoring compatibility.

## Backend integration and persistence

Vina calls the public function for each input after automatic preparation, when
needed. It rejects known provisional chemistry unless
`VinaProtocol(allow_provisional_preparation=True)` is explicitly selected.
Existing `assessment` and `provisional_reasons` provenance fields are retained;
`assessment_report` adds the complete bounded public report. Saved-result
roundtrips preserve it. Historical manifests without this additive field retain
their current reader behavior and outer schema `1.0`.

The public function does not reject a provisional preparation merely for being
provisional; the execution policy belongs to the consumer. Neither successful
template transfer nor successful Vina execution upgrades the assessment.
DockingMT [#4](https://github.com/uibcdf/dockingmt/issues/4) and
[#5](https://github.com/uibcdf/dockingmt/issues/5) remain partial while validated
preparation decisions and parameterization are outstanding.

## Reproduction and guards

Run in `molsyssuite@uibcdf_3.14`, with this checkout installed editable. The
notebook asserts Python 3.14 and the requested Conda interpreter. Explicitly
register/select that interpreter when executing through Jupyter:

```bash
python -m ipykernel install --prefix=/tmp/dockingmt-assessment-kernel --name dockingmt-molsyssuite-314 --display-name "Python 3.14 (molsyssuite@uibcdf_3.14)"
JUPYTER_PATH=/tmp/dockingmt-assessment-kernel/share/jupyter python -m jupyter nbconvert --execute --inplace devguide/validation/preparation_assessment.ipynb
python -m pytest --receptor=llm tests/test_preparation_assessment.py
```

The public API cases protect the distinction between declarations and scientific
validity, explicit zero charges, detached bounded reports, malformed metadata,
external inputs without IO, unknown arguments, and a fresh process with Vina and
MolSysViewer imports blocked. Existing real-engine guards now compare public
reports with saved Vina provenance for prepared and external inputs. The
chemical-template consumer guard checks that successful provider application
cannot bypass default provisional rejection.

## 2026-10-03 source-qualified result

The focused public/real-engine selection passes 30 tests in 14.09 s. The full
gate passes **564 tests without skips in 100.53 s** on Python 3.14.7, with Vina
1.2.7 and this checkout installed editable in `molsyssuite@uibcdf_3.14`. Ruff,
formatting, report indexes and diff checks pass. The three notebook code cells
execute successfully with the explicit Conda kernel; original BNZ reports both
known provisional markers, while the external path stays unassessed.

Tests and notebook use isolated source archives matching the unchanged CI pins:
MolSysMT `c19a47ada0c2279029abfa296cf915560610ad9a` and MolSysViewer
`ec4c71e574d798b7c8675b7e7e983da878ce9889`. Their sibling working trees are
preserved. The full gate retains the existing 27 provider warnings documented
in [chemical-template consumption](chemical_template_consumption.md); no local
warning suppression or chemistry workaround is added. This is API and policy
regression evidence, not scientific parameterization qualification or a speed
benchmark.
