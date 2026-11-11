# Native terminal completion: diagnostic receiving — 2026-11-04

Owner: [BindingMT #33](https://github.com/uibcdf/bindingmt/issues/33), with
[#49](https://github.com/uibcdf/bindingmt/issues/49) for molecular delegation.
Follows the [environment/template checkpoint](scientific_panel_environment_2026-11-04.md)
at `78eef90c781f3eea7e7951a35b275dcdb91baf49`.

**One diagnostic reconstruction executed; no receptor admitted for preparation
or search.** MolSysMT adds the two missing OXT atoms to a detached observed 1HSG
protein copy, but public reconstruction correspondence/history is not established.
The control output is not promoted to the planned panel.

## Declared operation and evidence

The [producer](data/panel_terminal_probe_2026-11-04/probe_terminal_completion.py)
uses only public MolSysMT molecular operations. It verifies the retained input
archive, reads explicit-only PDB connectivity, extracts amino-acid groups and
queries missing standard/terminal atoms. It calls:

```python
completed = msm.build.add_missing_terminal_cappings(
    protein, N_terminal=None, C_terminal=None, pH=7.4,
    keep_ids=True, engine='MolSysMT')
```

The numerical pH is an explicit tool parameter, not an experimental inference.
No N/C capping residue is requested. This software control explores geometry
completion for an assumed free C-terminal model; it does not choose final N/C,
catalytic-Asp or ligand states. 1STP is not reconstructed while its truncation
chemistry is unresolved. No template application, partial-charge/type assignment,
energy, RMSD or docking search is executed.

The [manifest](data/panel_terminal_probe_2026-11-04/manifest.json) binds the exact
producer, prior input manifest, [observations](data/panel_terminal_probe_2026-11-04/observations.json.gz)
and pre-execution #33 note. The single attempt exits 0; a provider warning remains
part of its outcome. Local installed-software metadata is omitted from the public
observation file, with the original receipt digest retained. The unchanged ordinary
installed prefix passed dependency closure before execution; provider source
context stays `00abb958fb93649131d5ce5fe5e12e90cf4900e9`.

The provider checkout remains clean/preserved at
`71fbe4f46d3c70e4e973c8025f01752a8c9b1084`, 92 commits behind fetched main
`5f3af9374f2bf4ce9c3598450e22d43ca14509ae`. The relevant completion/placer
files are unchanged between source context and fetched main; this is static
evidence, not adoption or qualification of the newer complete composition.

## Actual observations

| Observation | Before | Returned output |
| --- | --- | --- |
| Protein atoms / groups | 1514 / 198 | 1516 / 198 |
| Stored bonds under explicit-only input | 0 | 2 |
| Standard missing-heavy report | Empty | Empty |
| Missing terminal report | OXT at group indices 98 and 197 | Empty |
| Explicit H atoms | None in observed input | None generated |
| New OXT output identity | Absent | Atom indices 757/1515, IDs 1516/1517, groups 98/197 |
| Public return form | Not applicable | `molsysmt.MolSys`; no returned map/report dictionary |
| New preparation-history operation | Not applicable | No terminal-completion envelope observed |

The existing PDB connectivity history is preserved with its original operation
domain (1686 atoms/49 bonds in the full source). It is not a record of the extracted
protein or generated OXT and must not be relabelled. Empty terminal coverage after
generation does not establish chemical completeness: the protein graph still has
only the two generated C–OXT bonds, with chemistry unassigned.

The provider emits `StructuralAttributeDropWarning` for `b_factor` and `occupancy`.
It does not fabricate these observables for new atoms. The diagnostic records the
loss; it does not accept it silently for future preparation. A receiving workflow
must decide the attribute policy and retain original observed metadata separately.

Snapshots of the original full source and detached protein input are unchanged
after the call. The output's atom-ID prefix differs from the original sequence,
consistent with adding OXT in residue order. This comparison detects reordering;
it is **not an atom correspondence algorithm**. Output preservation of every old
coordinate remains **unassessed without a provider-supplied map**. Generated-OXT
geometry/energetics, protonation and complete chemical validity are also unassessed.

## Provider handoff and continuation

[MolSysMT #558](https://github.com/uibcdf/molsysmt/issues/558) requests public
terminal-completion atom maps and operation-scoped generation evidence. Static
inspection identifies an internal old/new map in the native expansion path, while
the public return/history does not expose a new completion record. The request
proposes reusing existing map/history and terminal-attachment report conventions,
preserving current public return behavior and earlier history. It does not assert
that the observed OXT coordinates are wrong or add a release gate.

BindingMT does not reconstruct the map using IDs, names, coordinates or a copied
private implementation. Provider #557 still owns the CCD/template route; #556
occupancy and #555 plausibility keep their separate scopes. No response/delivery
of #557 or #556 was observed at this checkpoint.

The concrete next receiving boundary is a provider-supported completion report
or equivalent exact source map, followed by observed-coordinate checks and explicit
attribute-loss acceptance. In parallel, obtain provider CCD templates/maps and
decide ligand/receptor states, water/other-ligand disposition and 1STP boundary
chemistry. Until those are resolved, the proposed 24-search matrix remains
unregistered and unexecuted. This limits the new panel, not all BindingMT work.
