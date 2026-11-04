# Panel admission: binding environment and template boundary — 2026-11-04

Owner: [DockingMT #33](https://github.com/uibcdf/dockingmt/issues/33), with
[#49](https://github.com/uibcdf/dockingmt/issues/49) for molecular delegation.
Continues the [source inspection](scientific_panel_admission_2026-11-04.md)
at `d2079282e3fda0783f7c9e7aa4101111c94f8964` and the
[proposed panel](scientific_panel_design_2026-11-04.md).

**Environment inspection completed; no case is admitted for preparation/search.**
The results make environment and template decisions concrete. They do not select
experimental protonation or certify a dry/truncated binding model.

**Continuation:** the [terminal diagnostic](scientific_panel_terminal_probe_2026-11-04.md)
now executes one OXT completion on an unadmitted 1HSG protein copy. It records
source/input immutability, output reordering and missing public completion
map/history, proposed in MolSysMT #558. The observations below retain their
original inspection-only scope and unresolved chemical decisions.

## Executed public-provider composition

[The producer](data/panel_environment_2026-11-04/inspect_environment.py) reads
the two already-bound PDB archives with `get_missing_bonds=False`, constructs
assembly 1 and selects the first ligand group on the returned group axis before
measuring anything. This is a deterministic instance choice, not a ranking by
distance or later docking outcome. No cross-format correspondence is assumed.

All molecular operations are public MolSysMT calls: conversion, assembly, group
and atom queries, nonperiodic spatial selection, minimum distances and readiness.
PyUnitWizard explicitly converts returned lengths to angstrom for serialization.
There is no consumer geometry, water perception, atom matching or chemical repair.
The [manifest](data/panel_environment_2026-11-04/manifest.json) binds the producer,
the earlier input manifest and [observations](data/panel_environment_2026-11-04/observations.json.gz).
The declaration under #33 precedes execution. Both cases complete in one attempt;
there is no error/warning output, download, preparation, energy, RMSD or search.

The unchanged installed provider composition has the same source context as the
earlier receipt (`00abb958fb93649131d5ce5fe5e12e90cf4900e9`). This does not
qualify current main or a public distribution. The clean provider checkout remains
preserved at `71fbe4f46d3c70e4e973c8025f01752a8c9b1084`, 91 commits behind
fetched main `8b6e6d10ef0eb1ed9b738081e24fbadbca2a6e03`.

Before/after digests agree for the coordinate arrays and chemical-readiness
reports of both the original native source and the assembled system. This is
additional evidence for these operations; the earlier source inspection's limited
immutability claim remains unchanged. It is not a digest of every native field.
The distance operation's pair indices are local positions in its declared endpoint
populations, not original atom indices. Full returned values remain in the record.

## Environment observations and dispositions

Water queries select provider-classified water groups with any observed atom
within the declared cutoff of the selected ligand, with PBC explicitly disabled.
These oxygen-only PDB groups have no admitted explicit-H chemical water model.
The 3.5/5-angstrom cutoffs define descriptive shells, not hydrogen-bond recognition,
water bridges, required retained waters or steric-validity criteria.

| Observation | 1HSG/MK1 | 1STP/BTN |
| --- | --- | --- |
| Chosen assembly-axis instance | Group 198, author residue 902, chain index 2 / ID C / author name B | Group 121, author residue 300, chain index 1 / ID B / author name A |
| Water groups within 3.5 angstrom | 7 | 3 |
| Water groups within 5 angstrom | 10 | 5 |
| Other assembled ligand instances | None | Groups 327, 533, 739, chains D/F/H; all author residue 300 |
| Minimum distance from other ligand copies to chosen BTN | Not applicable | 21.8934, 18.7482, 20.6939 angstrom, in listed group order |
| First/last observed protein groups | PRO 1 / PHE 99 on both protein chains | ALA 13 / VAL 133 on all four protein chains |
| Minimum observed endpoint-group distance to selected ligand | First: 18.9578/19.3555; last: 16.1293/16.1672 angstrom | Nearest first: 17.5930; nearest last: 12.9445 angstrom; per-chain values in observations |

For 1HSG the nearby waters include author A residues 332/341 and author B
303/308/313/444/568 at 3.5 angstrom. For 1STP they are author A
315/398/445 in the selected asymmetric-unit copy. Use the recorded assembly
group/chain axes as identity; author residue numbers alone are not unique.

Decisions from these observations:

- Preserve the full protein dimer/tetramer as the receptor-context candidate.
  The primary streptavidin paper discusses coupling across the tetramer, supporting
  this choice over an isolated monomer, without proving any preparation model.
  [Weber et al., 1989](https://doi.org/10.1126/science.2911722).
- Keep water disposition **unresolved**. Nearby observed waters and published
  evidence for an important water site in the indinavir/HIV-protease context make
  silent dehydration unjustified. The inspected water study varies Asp protonation;
  it does not identify the state of this retained structure or establish which
  numbered water to keep. [Water-site and hot-spot study, 2017](https://pubmed.ncbi.nlm.nih.gov/28837642/).
- Keep the three non-target BTN copies explicit in the declaration. Their
  separation supports treating them as distinct sites in this geometry, not
  independence or zero energetic influence. Do not automatically delete them or
  add them as unqualified receptor atoms.
- Keep the 1STP truncation model **unresolved**. The first/last observed residues
  and their distances do not reveal where the missing residues would lie. They do
  not prove that the missing segments are harmless or that observed boundary
  groups are experimentally free charged termini.

## Terminal chemistry prerequisite

The returned last-observed atom inventories contain no `OXT`: PHE99 in both
protease chains and VAL133 in all four streptavidin chains. The existing
`physchem.get_peptide_chemical_template` requires explicit terminal states and
includes OXT in its C-terminal template. The earlier empty standard missing-heavy
report deliberately excludes this terminal atom; it was not a complete terminal
coverage assessment.

MolSysMT already provides `build.get_missing_terminal_cappings` and
`build.add_missing_terminal_cappings`, including native OXT placement. Their
existence is source-inspected, not new executed reconstruction evidence here.
After deciding the boundary chemistry, receive that provider operation with a
source map, explicit generated-atom provenance and preserved observed geometry.
Do not invent OXT coordinates, erase the template atom or claim that a silent
template mismatch is scientifically acceptable. For 1STP, distinguish a deliberately
truncated model from restoration of the full deposited protein; no missing segment
or terminal atom was added in this operation.

## Chemical reference sources and provider request

The following are public page observations on 2026-11-04, separate from the
acquired molecular bytes. They are reference candidates, not frozen CCD files or
validated bound-state assignments:

| Source | Observed published metadata | Admission limit |
| --- | --- | --- |
| [1HSG version history](https://www.rcsb.org/versions/1HSG) | Entry 1.3 dated 2024-02-07 | The page describes the published revision; molecular metadata has not independently bound the downloaded bytes to it. |
| [1STP version history](https://www.rcsb.org/versions/1STP) | Entry 1.3 dated 2024-02-14 | Same distinction between page metadata and file-byte identity. |
| [MK1 CCD summary](https://www.rcsb.org/ligand/MK1) | Last modified 2020-06-05; neutral reference, 92 atoms including H, five reported chiral atoms | Retain exact reference bytes, descriptor policy and source atom identity before application. Neutral CCD does not establish bound protonation. |
| [BTN CCD summary](https://www.rcsb.org/ligand/BTN) | Last modified 2024-09-27; neutral reference, 32 atoms including H, three reported chiral atoms | This component revision postdates the displayed entry revision. Do not assume current CCD and embedded entry definitions are identical; a charged state needs an explicit separate hypothesis. |

Published studies show that HIV-protease catalytic Asp/ligand protonation can
matter and can depend on context. Evidence from another inhibitor or method must
not be promoted to direct determination for 1HSG. Asp25/25' and MK1 states remain
explicit decisions rather than a pH default. For example, the neutron study
concerns **darunavir**, not indinavir. [Neutron proton-transfer study, 2016](https://pubmed.ncbi.nlm.nih.gov/26958828/).

[MolSysMT #557](https://github.com/uibcdf/molsysmt/issues/557) now requests the
reusable CCD-to-template route and preserved atom identity/correspondence. Existing
template assessment/application remains the application mechanism; complete-graph
matching is not used to manufacture its own missing prerequisites. The provider's
EST curation example is explicitly case-specific and records a stereo discrepancy;
it should not become a copied DockingMT CCD parser or a universal stereo policy.
The request asks the provider to identify an existing supported composition if one
already covers this boundary. It does not commit implementation or add a release gate.

MolSysMT #555 is now owner-triaged for a post-freeze contract/method study; no
validator or scientific thresholds have been selected. CIF occupancy #556 stays
separate and unreceived. Neither issue is bypassed by the present PDB observations.

## Next bounded work

Obtain an owner-supported CCD/template route or explicit curated provider artifact
and mapping, decide chemical states and terminal/water/other-ligand treatment,
then receive provider-only terminal completion and template assessment/application.
Register any new reconstruction/preparation operation before execution with its
own controls. The proposed 24-search matrix remains unregistered and unexecuted.
There is useful admission work left, but no current basis for launching its rows.
