# Prospective saved nine-atom evaluation

Owner: [#4](https://github.com/uibcdf/dockingmt/issues/4), coordinated with
[#33](https://github.com/uibcdf/dockingmt/issues/33) and
[#28](https://github.com/uibcdf/dockingmt/issues/28). This contract is fixed
before measuring the saved two-search demonstration. Search outcomes/scores
and the older 3PTB benchmark are already known; this is a retrospective workflow
receiving, not a blinded or independent benchmark.

## Fixed inputs and comparison

Read the unchanged raw native/displaced JSON produced by workflow source
`1ef85cbdcbe75fb0c8a2f4dd37228f52a987f020`, published in checkpoint
`9bffd93f221c296115b16205e612629be1c2935d`. Expected native file SHA-256:
`3dcbebda7d816c097f6e61dbea429fd7eea82389ea172d2220748bbd49913b27`;
displaced: `b43f9612c4fff73d7be24c2124dda1a08b2dc81cb3af0295bc2ba91885b7e6b3`.
The [execution record](installed_3ptb_execution.md) retains raw custody and a
labelled public scientific projection; that projection is not either raw file.
Use the original public 3PTB PDB SHA-256
`75b1b8e73b4c197b7dcb217fbcfdd39c451860c0fd5a86cdef587c4dbd9972be`.

Include all five native and four displaced full thirteen-atom poses in their
original order, scores and ranks, with no exclusions or reranking. The measured
population is the nine originally observed BEN atoms, source IDs 1632–1640,
ordered names C1, C2, C3, C4, C5, C6, C, N1, N2. Compare in the unchanged receptor
frame: positional RMSD, no fit/translation/rotation or symmetry correction,
inclusive **at most 2.0 Å**, first-N positions **1 and 5**. Report first and
closest pose separately. This follows the established positional criterion;
no threshold or population is selected after these new measurements.

MolSysMT reads the original source and actual captured partner representation,
selects non-H atoms and extracts coordinates. The representation has 13 atoms
and its resolved heavy indices are 0..8 for this case. A mapping-only preflight
checks the complete written names/elements and all selected source ID/name/
element/group fields against the reference order, for every pose, with **zero
RMSD calls**. The notebook repeats these checks before measurement; mismatch or
missing evidence stops the workflow. This validates an already-declared order,
not a new matcher or chemical correspondence. PDBQT chemistry remains partial;
its format-specific tree is explicitly discarded, never reconstructed as a graph.

## Public route and preserved evidence

The [notebook](installed_3ptb_evaluation.ipynb) uses public MolSysMT coordinate
extraction and fresh public DockingPose/DockingResult constructors to create
coordinate-only comparison views. It copies parent IDs/ranks/scores/descriptors
and records explicit parent file/position/population/producer/input bindings.
It neither slices original preparation metadata nor asserts a fabricated
verified molecular map. New views have no claimed engine producer/captures;
parent provenance remains explicitly parent evidence. Original full records
remain detached, unchanged and independently preserved.

Call public `evaluate_redocking` with the declared coordinate reference and
cutoff/top-N, then `summarize_redocking`. Positional correspondence is honestly
labelled caller-declared. MolSysMT performs every RMSD. Refuse the original
13-atom result against the nine-atom coordinate reference before geometry as
an informative population control. No private heavy-pose projection helper,
downstream molecular selection/matching/geometry routine or new runtime API is
introduced. No missing provider capability is identified for this bounded route.

Run the exact seven source cells in normal and pm/fs real kernels outside
source: **nine distinct saved poses, nine RMSD measurements per policy, eighteen
measurements total**, not eighteen independent poses/cases. Expected physical
values agree within absolute `1e-12 Å`; criteria/order/counts/recovery must agree
exactly. Preserve each profile's actual record/geometry hashes independently.
Guard all preparation/H/charge/type operations, maps, energy, searches,
reconstruction and viewer actions. Count the expected 13-versus-9 refusal as
zero geometry calls. Verify actual installed payloads/origins and policy before/
after, save reports/summary/view/axis/receipt files without overwriting, and
close kernels on success/failure. On failure retain evidence and correct only
the failed receiving stage; no search or chemical replay is permitted.

Reuse private consumer `0.0.0+225.g50d8e33`, archive SHA-256
`5a923951f5e1bec31f41329b7e62fc9a398286bfba10b6951e984c87b0676c98`, and
MolSysMT archive producer `de7ffad2a`, SHA-256
`4a8e58f40627ff468fab99301674429fba66362f549a31fb4cc747d9cf19a0ba`, controlled
main `00abb958f`. Freeze the new notebook source separately before evaluation.
No archive/environment is rebuilt; the actual Python 3.14.8 receiver and task
kernel tooling retain their own identities. Original receivers, results and
sibling worktrees are preserved. Task-owned raw evidence remains under #4/#50,
review 2026-11-10; publish no personal operational paths or raw diagnostics.

The two boxes are observations of one hypothesis, not independent complexes or
a general success-rate estimate. Environmental protonation/model suitability,
affinity, new chemistry, public artifact/platform admission, native persistence
and visible C4/C6 are outside this receiving. #4/#33/#28 remain partial unless
their broader acceptance is separately satisfied.
