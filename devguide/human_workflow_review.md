# Installed Python/Jupyter workflow review

Owner: [#4](https://github.com/uibcdf/dockingmt/issues/4), coordinated with
[#28](https://github.com/uibcdf/dockingmt/issues/28). Publication-route decision:
[#29](https://github.com/uibcdf/dockingmt/issues/29).
Source inspected: `92d31e0bf6aaf128b79f8990732dbd5ac49b45e8`, 2026-11-03.
This is a source/workflow review and bounded next-slice specification, not a new
executed notebook, search, API or scientific acceptance result.

## Workflow and existing public seams

| Stage | Existing operation | Decision that remains with the scientist |
| --- | --- | --- |
| Choose inputs/states | MolSysMT conversion/selection/chemistry tools; DockingProblem and for_redocking. | Actual source, structure, chemical hypothesis, retained components and reference. |
| Prepare | Public MolSysMT builders/assignments; prepare_receptor / prepare_ligand / assess_preparation. | Named H/charge/type options and allowed loss; receptor H/state preparation precedes the preparator. |
| Define search | BoxRegion / from_selection and VinaProtocol. | Physical domain, explicit torsions, search settings/seed and supported engine intent. |
| Execute | dock; optional score; incremental dock_many for already prepared inputs. | Whether a new computation is intended and the prespecified population/controls. |
| Inspect/evaluate | Detached pose/result records, score definitions, audit_result, evaluate_redocking and summarize_redocking. | Reference/correspondence, cutoff, coordinate frame and which cases can be compared. |
| Save/read | DockingResult.to_dict / from_dict; verify_captured_inputs when captures exist. | Output file custody and externally trusted file identity; internal consistency is a distinct claim. |
| Reattach a problem | result.reconstruct_problem with the actual required inputs. | Explicit native/prepared objects or a documented recipe replay, rather than an inferred snapshot. |
| Display | dmt.view with explicit receptor/partner/reference/domain; existing addon. | Whether to enter the deferred interactive/visual review. |

Scientific orchestration belongs in the notebook. Repeated independently useful
molecular construction, correspondence, characterization, geometry or storage
belongs in MolSysMT. DockingMT owns docking policies, result semantics and their
orchestration. A notebook must not implement a missing provider tool to appear
complete; report the concrete need in that provider. No new molecular tool is
identified as necessary for the bounded record-inspection slice below.

## What the existing notebooks establish

The [current 3PTB companion](validation/addon_3ptb_player_receiving_2026-11-03.ipynb)
is an executed qualification workflow. Its setup deliberately requires exact
private archives, a source-free data harness and task kernel tooling. It imports
`devtools.qualify_3ptb_admission.admit` and
`devtools.recover_saved_3ptb_case.recover_saved_case`.

Those tools have distinct purposes:

- `admit` reconstructs the specifically declared 3PTB hypothesis through public
  MolSysMT tools, records original identities/reports, prepares both ligand arms,
  checks actual representations and describes the original prospective matrix.
  It is more than generic `prepare_receptor` / `prepare_ligand` glue. Its case
  assertions and scientific decisions must not become hidden library defaults.
- `recover_saved_case` verifies the frozen case's external trust root, retained
  files and cross-record links before returning a detached result. It is not a
  generic archive reader. `audit_result` alone does not perform that authentication.

The [wheel payload](validation/data/addon_player/consumer_wheel_2026-11-03.json)
ships `dockingmt` and `molsysviewer_dockingmt`, not these developer tools. This is
intentional for qualification; it means the notebook is not yet an example that
an installed-package user can run from arbitrary working directories without
the source/data harness. [README](../README.md) exposes the public primitives and
their preparation prerequisites, but is not a complete replacement for that
scientific recipe and qualification setup.

## Next bounded slice: installed saved-result inspection

Create a separate maintained notebook showing the installed public APIs for
reading and inspecting a caller-supplied DockingResult JSON record. Keep the
historical qualification notebooks and forensic recovery tool unchanged. This
small first slice avoids selecting new chemistry or launching a new experiment;
it is useful independently of a browser or molecular snapshot.

Acceptance for that notebook:

1. Run outside the repository with ordinary-installed core code; no `devtools`
   import or editable/source overlay. Data location and expected identity are
   explicit caller inputs; no personal operational path is embedded.
2. Use existing result schema admission, `audit_result`, `from_dict`, pose/score
   access and `to_dict`. Preserve pose population/order, optional identity/rank,
   named score descriptors/units and original producer. Reader identity is separate.
3. Explain trust precisely: external expected file identity, schema admission,
   record consistency and captured-byte checks establish different facts. A new
   self-consistent hash does not authenticate an original case or its chemistry.
4. Verify available captured inputs through `verify_captured_inputs`; explain
   absent captures instead of manufacturing them. Include one damaged-evidence
   refusal and preserve the supplied data and completed result.
5. Keep `result.problem is None`. Explain that `reconstruct_problem` requires
   actual inputs and validates available declarations/submitted bytes; neither
   PDBQT nor prepared JSON restores a complete native chemical/mechanical system.
6. Preserve quantity meaning under a nondefault application policy; numerical
   displays name their actual units. Reading/inspection performs no preparation,
   maps, scoring, optimization, search, RMSD or viewer action.
7. Retain a compact execution receipt with installed origins, input identity,
   original versus reader identities, observed checks and explicit limitations.
   This is new tutorial evidence, not a new scientific result or public release.

This specification is ready for the next implementation slice under #4. No new
result IO convenience API, generalized bundle format, backend runner or snapshot
is justified merely to write the example. Use standard JSON/file IO for the
docking record and the existing package operations for its semantics.

## Subsequent steps and boundaries

After this example, scope the explicit preparation-to-execution walkthrough
against an actual user need. Keep chemical prescriptions visible and use public
provider tools; register any new scientific computation and controls separately.
Do not extract all of `admit` into a universal public preparation function.

MolSysMT #256 owns future MolecularMechanics persistence, and #521 owns the
remaining partial/reference PDBQT profile. Neither is implemented here. The
declared workflow can retain linked records and require explicit inputs while
those extensions remain open. File/record recovery is not molecular persistence.

Choose the user-facing publication location under #29 before building a new
site/publishing pipeline. The present review and next notebook can live beside
the existing workflow evidence meanwhile. Candidate/package/platform qualification
stays #30/#47, and visible controls/comm/pixels/C6 stay #52/#60. No private pilot
material or scientific assets are required by this public example.
