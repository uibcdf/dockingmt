# Finite real pose-coordinate records

Owner: [#63](https://github.com/uibcdf/bindingmt/issues/63); public-boundary review:
[#19](https://github.com/uibcdf/bindingmt/issues/19). DockingPose coordinates are
finite real length quantities of shape `(N, 3)`, stored in nanometers. This is
result-schema admission, not molecular geometry, identity, plausibility or repair.

## Admission and snapshots

Construction checks numerical contents before float conversion and rejects
normalization overflow. Complex arrays, including zero-imaginary complex dtype,
boolean arrays and nonnumeric data are not coordinates. Deserialization checks
scalar types before NumPy/quantity factories can erase mixed boolean or numeric-
string types. Invalid data raises BMT-E002 for `coordinates`.

Snapshot export also checks current numerical contents: mutating a live quantity
to NaN/infinity cannot produce a new valid record. Validation adds no coordinate
copy before the existing independently allocated `tolist()` snapshot. Valid
integer/floating inputs, units, identities and independent roundtrips retain
schema 1.0. Explicit `(0, 3)` poses keep their existing construction/export
behavior; this adds no new empty-record reconstruction policy.

Malformed old records may now be refused earlier. Keep their original bytes for
dictionary-based audits/diagnosis rather than manufacturing repaired coordinates.
PyUnitWizard owns physical conversion; all molecular interpretation, geometry,
matching and manipulation remains MolSysMT-owned. No molecular tool is added.

## Source evidence

At `8087603`, 18 new controls fail/four valid cases pass. After the fix all
**22** coordinate cases pass, including normalization overflow, malformed records,
invalid mutable snapshots and nondefault caller units. Their guards forbid
MolSysMT get/set/convert/select/extract/copy throughout admission/export.

The disjoint relevant selections pass **243 + 210 = 453 tests**, no failures/skips,
in 76.62 s and 9.19 s on routine editable Python 3.14.7. They cover result/score,
evaluation/summary, actual native-output integration, serialization/audits and
export-helper behavior. The first retains 39 LegacyH5MSMWarning and one
StructuralAttributeDropWarning; the second emits none. These source checks
include existing provider/native controls; they are not a new registered
redocking population, installed release or relabelled #62 experiment.

## Bounded quantity-form probe

Source composition: PyUnitWizard `0.29.0+4.g9d74f0e`, full source
`9d74f0e1e911d78c1906948e74ce8da93935557d`, Pint 0.25.3, unyt 3.1.0,
OpenMM 8.6.1, Astropy 8.0.1, Linux/Python 3.14.7. The provider's six fetched newer
commits are documentation-only; its clean local source is preserved.

| Boundary | Observed disposition |
| --- | --- |
| Pose admission/roundtrip, all 16 incoming/default pairs over four forms | Passes; angstrom values survive nanometer storage. |
| Protocol energy, nine Pint/OpenMM/unyt pairs | Passes; 12.552 kJ/mol normalizes to 3 kcal/mol. |
| Protocol energy, seven pairs involving Astropy | Refuses: kcal/kilocalorie is not recognized by Astropy parsing. |

The last limitation reproduces with PyUnitWizard alone and belongs to
[PyUnitWizard #137](https://github.com/uibcdf/pyunitwizard/issues/137), related to
#19/MolSysSuite #127. BindingMT retains the provider cause and adds no local alias,
forced quantity-form switch or fallback. This does not imply that Astropy itself
promises a built-in calorie or invalidate the passing length profiles.

```python
import pyunitwizard as puw

with puw.context(default_form='pint'):
    energy = puw.quantity(12.552, 'kJ/mol', form='astropy.units')
    puw.get_value(energy, to_unit='kcal/mol')
    # ValueError: kilocalorie is not a valid Astropy unit.
```

This probe covers only the named entry points/forms. It does not qualify other
translator families, exact public files/minima, environment closure, another
platform, whole #19 adoption or chemical/physical validity. Known shared-
environment findings remain MolSysSuite #82; public/visual gates retain their owners.
