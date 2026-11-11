---
summary: Preserve allocation exceptions while projecting prepared scoring geometry.
issue: uibcdf/bindingmt#107
status: resolved
opened: 2026-11-10
closed: 2026-11-10
severity: medium
verification: measured
area: [scoring, resources, diagnostics]
guard: tests/test_input_resource_errors.py::test_scoring_geometry_preserves_resource_errors_and_cleans_staging
normative: devguide/validation/scoring_geometry_resource_errors_2026-11-10.md
blocked_by: []
supersedes: []
---

# Fixed-pose geometry translation masks resource errors

## Observation

The `_input_pose` helper's broad Exception translator converts both MemoryError
and OSError(errno.ENOMEM) from MolSysMT geometry reading into ArgumentError/BMT-E002.
A controlled actual installed aeae47d diagnostic confirms this and byte-matches
the current source helper at 02228c3. Original errors remain causes, not the same
propagated objects. Ordinary ValueError correctly becomes the structured argument
error. This is a local BindingMT translator, not a provider defect.

The helper diagnostic raises pre-created failures, with zero actual molecular/
native work or allocation exhaustion. Exact program/registration/outcomes remain
under `.molsyssuite/scoring-resource-probe-20261110/diagnostic-01`, owners #107/#50,
review 2026-11-14. Elapsed 1.025s, peak 78991360 B, no interruption and terminal groups.
Receipt SHA256: `f8a45f004b11eb8c39eddcf61c28587fc12ebbe49bc040f3640807c154201e57`.
Public score reaches this helper before native construction; public regression
coverage is the next step, not an observation claimed for this private probe.

## Correction and acceptance

Propagate the exact resource exception from conversion and coordinate/name/
element reads through public score. Preserve ordinary malformed-value and I/O
ArgumentError diagnostics, exact cause and field, no further provider/native
steps, caller input/protocol and owned staging-file cleanup. Do not inspect error
strings or treat every OSError as allocation failure. No dependency, schema or
scientific definition change is needed.

Add controlled red/green public guards and receive the complete affected input-
resource and pose-audit modules under both caller unit policies, preserving all
original tests/fixtures and the original two tiny live scoring calls. Keep source
and original installed-artifact evidence separate. Existing #92/#95/#106 fixes
have distinct scopes; #73/#47 own wider qualification and #50 resource custody.


## Resolution — 2026-11-10

Public score now propagates the same MemoryError or OS ENOMEM object through
conversion and coordinate/name/element reads. Ordinary malformed-value/I/O errors
retain BMT-E002, exact cause and field. All 16 new cases stop before further
provider/native work, clean owned staging paths and preserve caller snapshots.
The original public guard retains eight resource failures/eight ordinary passes;
both complete 203-case source profiles now pass, with all 187 original cases and
four original tiny native score calls across policies.

The normative evidence authenticates 119 primary/14 reader members, exact handler-
only runtime AST changes, unchanged original test ASTs and complete public/native
outputs without replay. The original installed helper diagnostic and generated
labels retain their actual identity. No provider/schema/scientific fixture or
shared installation changes; genuine new artifact receiving of #106/#107 remains
#47. The implementation defect resolves in source with its public regression.

## Installed receiving addendum — 2026-11-10

[Genuine private wheel receiving](../validation/installed_allocation_fixes_2026-11-10.md)
now receives this correction from exact producer `37a61e6`, actual version
`0.0.0+359.g37a61e6`. All sixteen public geometry-resource/ordinary-diagnostic
guards pass in the actual installed consumer under each unit policy. The whole
155-case input-resource and 48-case pose-audit modules pass, including the
original two tiny native score calls per policy and consistent fresh audits.
All 305 main installed cases per policy pass; independent 419/14-member records
authenticate actual wheel/version/imported bytes, native outputs, bounded original
provider reads and 606 shared support declarations/retirement.

The original installed helper failure and source red/green population keep their
identities. No source/test/fixture/provider change, native rebuild, shared install,
publication or remote CI occurs. This issue remains resolved; full/public/platform
delivery stays #47/#30/#73, with #47/#50 custody reviewed on 2026-11-14.
