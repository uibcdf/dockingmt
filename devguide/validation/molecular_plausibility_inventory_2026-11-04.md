# Molecular plausibility: provider inventory — 2026-11-04

Owners: [BindingMT #33](https://github.com/uibcdf/bindingmt/issues/33) and
[#49](https://github.com/uibcdf/bindingmt/issues/49). Provider proposal:
[MolSysMT #555](https://github.com/uibcdf/molsysmt/issues/555).
This supports audit R6/Q4 and the [proposed panel](scientific_panel_design_2026-11-04.md).

## Scope and inspected identities

Static inspection only: public source signatures/docstrings/exports, representative
test locations and existing provider issues. No molecular calculation, numerical
probe, environment update, pin adoption or provider implementation was performed.
An available symbol is not qualified consumer behavior.

- Consumer: `71287ce86db365c9063846ae7d904c9586a99354`.
- Qualified molecular source context: `00abb958fb93649131d5ce5fe5e12e90cf4900e9`;
  private wheel producer `de7ffad2aef18ff3bccd184133dc69e081cb506e` stays distinct.
- Refreshed provider main examined separately:
  `93d29bf23e2c54f238f7ada984a4b23420b4b3b0`.
- The local provider checkout was clean at `71fbe4f46d3c70e4e973c8025f01752a8c9b1084`,
  88 commits behind fetched main. It was preserved. Git object reads established
  the qualified/current namespace context rather than treating the old checkout
  as the latest API. In particular, chemical graph tools belong to
  `molsysmt.chemical_states` in the qualified source.

The bounded suite-status check reported BindingMT clean/current and MolSysMT
behind; no merge, reset or reinstall occurred. An initial attempt to select the
governance repository itself was rejected as unregistered; the corrected member
selectors produced the status above. No sibling worktree was edited.

## Capability and applicability inventory

Source links below are fixed to the qualified source. The later current-main
inspection found no exported complete assessment contract in the reviewed
physchem, structure and chemical-state namespaces. Coordinate-CIP source has
later changes; neither those changes nor other new provider behavior is adopted here.

| Need | Existing public provider route | What it establishes / what remains |
| --- | --- | --- |
| Declared chemistry/coordinate coverage | [`physchem.get_chemical_readiness`](https://github.com/uibcdf/molsysmt/blob/00abb958fb93649131d5ce5fe5e12e90cf4900e9/molsysmt/physchem/get_chemical_readiness.py) | Coverage, connectivity boundary/integrity and finite-coordinate evidence. Its explicit unassessed checks include valence; present fields are not validated chemistry. |
| Atom correspondence and graph identity | [`chemical_states.get_atom_correspondences`](https://github.com/uibcdf/molsysmt/blob/00abb958fb93649131d5ce5fe5e12e90cf4900e9/molsysmt/chemical_states/get_atom_correspondences.py), actual writer maps and known-source reader | Existing molecular ownership; conditional on complete declared chemistry and the supported atom population. Partial/reference reading remains #521. |
| Output stereochemistry | [`physchem.get_cip_stereochemistry`](https://github.com/uibcdf/molsysmt/blob/00abb958fb93649131d5ce5fe5e12e90cf4900e9/molsysmt/physchem/get_cip_stereochemistry.py), explicit `from_coordinates=True` | Reanalyzes one selected nonperiodic conformer on a copy with a complete graph and explicit chemistry. Stored labels alone cannot verify output geometry; unassigned does not mean achiral. Consumer receiving for retained PDBQT/H profiles is still required. |
| Pair distances and contacts | [`structure.get_contacts`](https://github.com/uibcdf/molsysmt/blob/00abb958fb93649131d5ce5fe5e12e90cf4900e9/molsysmt/structure/get_contacts.py), `get_distances`, `get_minimum_distances` | Unitful geometry/thresholded contacts. Declare `pbc=False` for this nonperiodic panel instead of inheriting contact defaults. A contact is not inherently a steric clash. |
| Bond angles/dihedrals | `structure.get_angles`, `get_dihedral_angles`; state-specific graph queries | Measurements on explicitly selected atoms. Chemical reference ranges, bonded-neighbor exclusions and applicability are not supplied by the measurement alone. |
| Planarity | [`structure.get_least_squares_plane`](https://github.com/uibcdf/molsysmt/blob/00abb958fb93649131d5ce5fe5e12e90cf4900e9/molsysmt/structure/get_least_squares_plane.py) | Fitted plane and unitful deviations for declared groups. It does not recognize chemical planarity requirements or select a validity threshold. |
| Radii | [`physchem.get_atomic_radius`](https://github.com/uibcdf/molsysmt/blob/00abb958fb93649131d5ce5fe5e12e90cf4900e9/molsysmt/physchem/get_atomic_radius.py) | Tabulated physical parameters with a chosen definition. It is not a clash model; coverage, H conventions and tolerance/exclusions need explicit rules. |
| Reference RMSD | `structure.get_rmsd`, `get_symmetry_corrected_rmsd` | Existing positional/conditional symmetry geometry. Agreement with the reference does not establish plausibility or affinity. |
| Rule-based geometry/steric assessment | No complete public contract established by this inventory | Proposed provider disposition in #555. Do not implement local bond/angle/clash/planarity classifiers to fill this gap. |

Representative provider test locations include
`tests/physchem/test_get_chemical_readiness.py`,
`tests/physchem/test_get_cip_stereochemistry.py`,
`tests/structure/test_get_least_squares_plane.py` and structure contact tests.
Their existence was inspected; this task did not execute them or claim that they
cover the new docking assessment profile.

## Requested assessment boundary

The proposal asks the provider to identify a supported composition or scope new
reusable tools. It does not mandate a monolithic API or dependency. Initial needs:

- Read-only bond/angle, aromatic-planarity and intra/intermolecular steric checks
  under named scientific rules, explicit tolerances and bonded-pair exclusions.
- Per-check outcomes and reasons, source atom/bond/pair identities, measured
  quantities/units, model/software/rule versions and applicability.
- Explicit distinctions among assessed pass/fail, unassessed and unsupported.
  No universal `scientifically_valid` certificate.
- Complete chemistry and measured-coordinate requirements checked separately.
  In particular, omitted or merged H must not be restored from unmodified source
  coordinates and then reported as measured output-pose geometry. A heavy-only
  assessment must declare which H-dependent checks it cannot perform.
- No silent bond inference, H generation, minimization, alignment, state change
  or repair. Preserve the original pose and source objects.

Independent expected valid/adverse controls should exercise stretched bonds,
distorted angles/planes, stereo inversion, known excluded bonded pairs and true
overlap, with empty/missing-chemistry/H cases, nondefault units and immutability.
Exact thresholds, scope and implementation belong to the provider's scientific
review. [PoseBusters checks](https://posebusters.readthedocs.io/en/latest/checks.html)
are methodological precedent, not an automatic policy imported into BindingMT.

## Ownership and non-blocking boundaries

MolSysMT #299 (CIP), #310 (correspondence/RMSD), #521 (partial/reference reading)
and #323 (environmental H refinement) remain distinct; refinement is not assessment.
Issue #555 is a post-initial-release proposal, not an added gate for the frozen
MolSysMT 1.0 scope. No PharmacophoreMT operation is needed for this first assessment;
future pharmacophore work retains its own provider.

BindingMT may select the evaluation policy, preserve provider reports and compare
docking outcomes. It must not implement generic molecular characterization.
Unavailable plausibility checks remain visibly unassessed; they do not prevent
source admission or separately scoped positional-RMSD research, but they prevent
claiming complete physical validation. When the provider supplies a contract,
receive it against the actual retained-pose population before integrating it.
