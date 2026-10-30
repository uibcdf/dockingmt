# Receiving independent chemical domains

This source migration is owned by `uibcdf/dockingmt#56`, coordinated with
`uibcdf/molsysmt#255` and `uibcdf/molsyssuite#155`.

## Current source contract

The controlled source candidate is MolSysMT
`9fb77c3583b44dda31c0466348369de137301df9` with MolSysViewer
`ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352`. These are source inputs, not a
new installed/public package pair. Source pins do not establish a public minimum.
Keep receiving open until the owner qualifies the final source/installed routes
and justifies the published runtime floor before a release.

Pass the complete MolSys to `msm.chemical_states.get_rotatable_bonds`,
`get_covalent_blocks`, `get_rigid_fragments` and `get_atom_correspondences`.
Preserve structure-associated state selection, original atom axes and provider
refusals. Stable atoms/groups/chains/molecules/entities belong to Topology;
ChemicalStates owns covalent bonds, assignments and state-local components.
Do not recreate a Topology chemistry facade or infer missing chemistry locally.

## Guards and current audit tools

The torsion, rigid-fragment, readiness, receptor-coverage, problem and symmetry
tests retain their independent expectations. Native state fixtures now construct
and label states in ChemicalStates, without changing their reference/assigned
counterexamples. `devtools.qualify_chemical_domain_receiving.state_scope_probe`
compares the two graphs and verifies unchanged source data. It replaces an
obsolete expected capability failure in the current receiving guard.

`devtools.qualify_chemical_templates.snapshot` uses schema
`dockingmt.chemical_template_snapshot@3`: its stable TopologyDict contains no
bonds, while the complete ChemicalStatesDict remains a separate snapshot. This
keeps multistate bonds and preparation history in the mutation audit.

## Historical producers

The dated entry points in `qualify_1iep_conformers`, `qualify_1iep_flexibility`,
`qualify_3ptb_admission`, `qualify_5x72_reference`, `qualify_5x72_rigid` and
`qualify_torsion_policy` producers retain their original pinned provider, source
fingerprints and dated output destinations. Their reused helpers in the 3PTB and 5X72 modules now consume the current
chemical namespace because the active tests call those functions. Proof constants,
source-fingerprint paths and dated output destinations remain historical; no
stored JSON is overwritten or reclassified. Replay an original producer through
its preserved source/exact Git revision. Owner requalification of a full producer
must use a new output identity, exact provider sources and preserved scientific
expectations. The current state-scope guard is separate from that work.

## Scalar property consumption

`connectivity_completeness` is the scalar property of the selected chemical
state. Preparation retains its existing list-valued evidence field by wrapping
that value once. Staging compares the scalar directly after the one-state guard;
complete sources therefore retain the known-source reader and all its map and
later-pose refusals. A string must not be expanded into individual characters.

## Qualification boundaries

Local source tests use the shared development environment and existing native
backend; full source CI and installed candidate/platform qualification remain
separate. Preserve failure, skip and warning evidence. No release, tag, package
promotion, dependency cap or automatic scientific-profile migration follows from
this source change. See the [receiving record](pending_proposals/receive_chemical_domain_separation.md).
