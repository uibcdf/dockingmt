# Exact-input Vina adapter differential control — 2026-11-04

Owner: [#62](https://github.com/uibcdf/dockingmt/issues/62), following audit
Q1/E3 under #28/#33. This is an existing-input software control, separate from
the proposed two-complex panel and from the original 3PTB scientific populations.

## Pre-execution prescription

The [registration](data/adapter_fidelity_2026-11-04/registration.json) freezes the
[producer](data/adapter_fidelity_2026-11-04/run_control.py), input/native hashes,
independently prescribed calls, strict comparison and failure policy. The owning
issue binds its clean producer commit before execution. At this prescription's
creation, **zero new searches have been attempted**.

Reuse the receptor/ligand bytes captured in the original
[3PTB human result](data/human_3ptb/native_result_2026-10-20.json.gz), preserving
that archive and its producer. Do not reconstruct its molecular system, reprepare
it, assign chemistry, calculate RMSD or download another source. The source-free
PDBQT route retains the existing bounded verifier exception under #49/MolSysMT
#521; this control adds no molecular routine and does not qualify that missing
complete-source/partial-reading contract.

Run the adapter once, then direct Python Vina once, each in a fresh process,
serial CPU 1 and at most 300 s per worker. Fix Vina 1.2.7, scoring `vina`, seed 7,
the recorded 20-angstrom box, exhaustiveness 1, nine requested poses and a
3 kcal/mol output range. Exact constructor, map, clustering and other resolved
defaults are declared in the registration; no alternative settings are selected
after observing outputs. Default weights are bound by the loaded wrapper/native
file hashes and the actual engine-info comparison.

An observer records public arguments/results without modifying them. The direct
route takes its parameters from the frozen prescription, not adapter provenance.
Compare all native energy columns, the native coordinate array in its own output
order, raw native PDBQT bytes and safe engine info exactly. Check published scores,
units, ranks, recorded full matrix/options/input hashes and box against that
independent invocation. No molecular text is parsed by this producer. Empty
outputs do not establish pose/score qualification. Any refusal, error, timeout or
mismatch stops the control without retry or tolerance adjustment.

The [preflight](data/adapter_fidelity_2026-11-04/preflight.json) identifies routine
Python 3.14.7, actual editable runtime hashes, MolSysMT source, loaded Vina files,
versions and native signatures. Its `pip check` fails for existing unrelated
shared-environment requirements tracked by MolSysSuite #82. These remain visible;
no package/environment is repaired, repinned or newly qualified. Installed/public
delivery and the original Python 3.14.8 private receiver remain separate evidence.

## Execution and custody

Read-only input authentication, without search:

```bash
python -I -B devguide/validation/data/adapter_fidelity_2026-11-04/run_control.py --check
```

Execution requires the routine editable environment, a clean checkout of the
producer commit registered on #62, unchanged preflight/input bytes and a fresh
output directory:

```bash
python -I -B devguide/validation/data/adapter_fidelity_2026-11-04/run_control.py --expected-head REGISTERED_PRODUCER_SHA --output NEW_OUTPUT_DIRECTORY
```

This command attempts **two new native searches** if both routes complete; it is
not record reading or a replay of old measurements. Failed/planned routes keep
their disposition. Task-owned inputs/caches are managed and retired, including
parent cleanup after worker timeout. Keep every observation/failure and raw local
log; publish only sanitized observations and exact digests. Evidence ceiling is
32 MiB; custody is #62/#33 with review on 2026-11-11, preserving still-useful data.

Agreement supports only same-host, fixed-input interface fidelity for this one
profile. It is not general stochastic/bitwise reproducibility, chemical identity,
physical plausibility, recovery, affinity, independent-complex performance or
public/visual acceptance. Molecular inspection/manipulation and missing reusable
capabilities retain MolSysMT ownership.
