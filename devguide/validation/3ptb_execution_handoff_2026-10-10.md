# 3PTB execution handoff, before the first search

Owning issues: DockingMT #5, #6, #4 and #49. This clarification preserves the
[registered scientific protocol](3ptb_prospective_protocol.md) and the admitted
24-row population. It changes no molecular state, geometry, model, torsion tree,
box, seed, effort, retrieval limit or interpretation threshold.

The admission's protocol rows retain the declared cuts: `[]` for rigid and
`[[0,6]]` for flexible. The existing Vina adapter rejects a nonempty
`active_torsion_bonds` request with an already prepared partner: that argument
controls automatic preparation. Execution therefore records both the original
row and its call projection, replacing only this argument with `None` for both
arms. The independently prepared ligand carries the exact admitted ROOT/BRANCH
bytes and metadata. No automatic preparation is requested, and no torsion is
removed from the submitted flexible PDBQT. Replaying admission once must match
every literal PDBQT byte, box and population before any search.

The adapter will additionally retain the complete native `energies()` array,
its five Vina/Vinardo column meanings and units, engine information, and resolved
call defaults from the loaded Python wrapper. Existing four named scores and
ranking remain unchanged. This is DockingMT's backend evidence responsibility;
no general molecular operation is added. See the
[Vina 1.2.7 source](https://github.com/ccsb-scripps/AutoDock-Vina/blob/v1.2.7/build/python/vina/vina.py).
The installed wrapper declares `min_rmsd=1.0` angstrom and `max_evals=0` for
`dock`, and map spacing `0.375` angstrom with `force_even_voxels=False`.
These defaults are recorded from the actual loaded signatures before execution;
they are not an additional fitted scientific control.

Every returned pose retains its full thirteen-atom coordinates and native
five-component energy vector. Evaluation selects the nine observed atoms through
the admission's written-to-full-source map, verifies original IDs, names,
elements and residue identities against public MolSysMT getters, and passes
the selected pose and original molecular reference to the existing public
DockingMT evaluator. Positional RMSD is supplied by MolSysMT, without fitting
or symmetry matching. Full and heavy-atom containment are recorded separately.

The receiving run records progress before and after each attempt, keeps a
completed search even if its evaluation fails, never retries, and reports
planned, attempted, returned and evaluated denominators separately. A fatal
interruption leaves the current attempt and remaining unattempted rows visible.
The output path must be new; rerunning the command is a new experiment, not a
replacement for the registered archive. The producer snapshot, original runtime
identity, raw search results and later qualification receipt remain separate.

The original admission archive SHA-256 is
`05f82e0ff16592c64d404c216a7e2feff0c0e62a2aebff240dc8653350e21075`.
Its population SHA-256 is
`be87f351c4cd0f2b8af6dc71d12af49c0604c2171b363fa2a62e3561215a1ed6`.
This document's digest and issue registration are retained in a separate record
before the first search. The original admission and prospective protocol are
not rewritten to hide this interface discrepancy.

## Pre-search serialization clarification, 2026-10-10

The public `VinaProtocol` constructor normalizes `None` to `[]` in its serialized
parameters. Execution records that resolved empty preparation request rather
than expecting a literal JSON null. The prepared ligand still supplies its
unchanged tree. The first receiving startup stopped on that record comparison,
before the first attempt; its archive contains all 24 `not_attempted` rows and
is retained separately with its producer. This dated appendix and its new
registration explicitly supersede the initial handoff digest for execution,
without changing the scientific population. An earlier checksum check likewise
stopped before molecular work because compact JSON separators differed from
those used in the original population digest; the original sorted-JSON digest
and all its input bytes remain unchanged.
