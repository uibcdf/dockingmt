# Meeko methods for native MolSysSuite preparation

## Scope and evidence

This source review supports DockingMT #5 and #17 and MolSysMT #221–#224.
The user explicitly requests native implementation in MolSysMT/DockingMT,
without importing Meeko. Accepted decision DMT-029 remains unchanged: Meeko
is not a runtime or installation dependency. This record identifies useful
methods, contracts and test cases; it does not vendor implementation or
parameter tables and does not establish numerical agreement with Meeko.

The inspected clean checkout is `~/repos@others/Meeko`, commit
`1eac18bd6d1111f35f9f1abaa8af502c2668d054`, whose package identifies itself as
0.8.0. Official documentation was also consulted on 2026-10-03. Findings below
are source-inspected, not a performance or chemical-accuracy benchmark. An
initial unnecessary import check failed on absent `gemmi`; no dependency was
installed, and the review does not rely on executing Meeko. Subsequent work
follows the user's explicit source-only/native implementation scope.

The suite inventory was refreshed before the provider handoff. All sibling
working trees and ahead/behind states are preserved, including ongoing
MolSysMT fixed-state hydrogen work. No sibling implementation is changed here.

## Useful operations and ownership

| Method inspected | Native owner and existing track | Present consumer gap |
| --- | --- | --- |
| Ordered chemical-context atom typing, with specific rules overriding general ones | MolSysMT #222: public named-scheme assignment and validation | DockingMT's temporary ligand rule assigns every N as `N` and every S as `SA`; chemical context must distinguish acceptors, aromatic/protonated atoms and polar H. |
| Named partial-charge assignment, explicit read mode, finite-value checks | MolSysMT #221: public state-specific assignment | Source charges can be preserved, but absent charges still use declared zero placeholders. A named method and provenance are missing. |
| Type-driven terminal-H merging, charge aggregation, ignored/retained atom identities | MolSysMT #223: public loss-aware projection and maps | DockingMT already merges source H charges and retains an atom map; the two preparation helpers still own temporary element-based H decisions. |
| Chemical rotatable-bond classification followed by rigid-fragment partition | MolSysMT #224: public eligible bonds with exclusion reasons; existing public `topology.get_rigid_fragments` | Fragment partition is already consumed. Chemical eligibility remains temporary and active bonds must be supplied explicitly. |
| Exact residue templates, linkage/padding and explicit residue choices | MolSysMT #218/#298/#300: coverage, explicit templates and fixed-state H | Coverage/template tools are consumed; matching a template is distinct from selecting protonation and adding missing H geometry. |
| Source/serialized/SMILES atom maps and H-parent records for reconstruction | MolSysMT #223/#214 for general conversion; DockingMT #8 for pose interpretation | Mapped pose reconstruction exists with an original source; external raw PDBQT remains unassessed and has no reconstructible molecular source map. |
| Rooted flexibility trees, flexible receptor partition and special docking protocols | DockingMT #6/#7/#17 for policy and engine intent, consuming provider graph/serialization | ROOT/BRANCH export exists for selected ligand cuts. Root optimization and flexible receptor execution need their own accepted workflow and evidence. |

Native public operations should use MolSysMT systems, selected chemical states,
source indices and physical quantities. Provider internals may use appropriate
existing primitives behind those APIs; there is no Meeko package dependency or
Meeko object in the user-facing contract. API names/storage are provider design
decisions, not established by this review. Assignments must expose scheme/method,
version, coverage, conflicts and source correspondence independently of Vina.

## Concrete differences worth testing

1. **Types:** aromatic versus aliphatic carbon; pyridine versus pyrrole N;
   amine/ammonium/amide N; accepting versus nonaccepting S; polar/nonpolar H;
   unsupported elements; contradictory or incomplete chemical states. Ordered
   rule precedence must be explicit and auditable. Atom names are not evidence.
2. **Torsions:** amides, thioamides, amidines, tertiary-amide policy, rings,
   conjugation, terminal groups, and single–triple–single systems. Meeko's
   `BondTyperLegacy` treats some tertiary amides differently and handles nitrile
   chains explicitly. Existing 1S63 aryl–nitrile and ethyl-acetate differences
   in DockingMT #17 must be explained by a declared policy rather than matching
   a torsion count. Compare exact source bond pairs and fragment memberships.
3. **Projection:** aggregate each omitted H charge into its declared retained
   parent; preserve total charge before PDBQT rounding, chosen state, retained
   coordinates, source IDs and both mapping directions. Polar-H decisions
   follow the named scheme. Molecule and receptor paths should consume one
   reusable provider operation rather than repeat their current local loops.
4. **Assignment:** missing graph/valence/H prerequisites, finite values, full
   selected-state coverage, explicitly read charges and supported chemical
   domains. Small-molecule evidence does not qualify protein receptors.
5. **Persistence:** original 181L and the 5X72 P59/P69 stereoisomers, deliberately
   permuted atom order, multiple frames and non-default quantity policies.
   Existing template application and public preparation assessment must keep
   their distinct scopes and their default provisional safeguards.

## Behavior that needs an explicit native decision

- Ligand parameterization requires declared chemistry and H prerequisites.
  Meeko's ligand preparation does not generate missing H coordinates or select
  the chemically appropriate protonation state. The heavy-only 181L ligand
  still needs the provider's explicit fixed-state H route.
- Meeko's Gasteiger helper temporarily removes selected metals and substitutes
  sulfur for selenium before computation. These are method-specific
  approximations, not a generic supported-domain guarantee. A native bounded
  method should reject unsupported chemistry or expose an explicitly accepted
  approximation, never silently change the selected chemical state.
- `Polymer.rectify_charges` can infer an integer target and distribute rounding
  residuals. Native assignment/export must distinguish calculated charges from
  representation rounding and use an explicit total-charge policy.
- Its exporter can regenerate H coordinates from a reconstructed graph.
  DockingMT currently leaves omitted atoms absent. Adding reconstructed H is a
  separate MolSysMT operation with its own state/map/geometry provenance.
- Macrocycle ring breaking and glue pseudo-atoms, reactive/covalent docking,
  hydrated docking and specialized metal protocols remain later workflows.
  A pseudo-atom must not silently acquire the identity of a source atom.

## Recommended next slice

Prioritize the public named AutoDock typing tool in MolSysMT #222 and consume it
from both DockingMT preparation helpers. Keep charges (#221), loss-aware
projection (#223) and bond eligibility (#224) as independently useful public
operations, each with explicit contracts and standalone tests. DockingMT owns
scoring-specific requirements, chosen active torsions and result provenance.

The Vina documentation states that `vina` and `vinardo` do not require computed
partial charges. Consequently Meeko's default Gasteiger calculation is not a
universal prerequisite for our currently supported scoring modes. This source
fact motivates typing/chemical eligibility priority; it does **not** alter the
existing rejection policy in this change or qualify placeholder chemistry.
Future scoring-aware admission must distinguish unused charge fields from
missing required chemical typing and handle AutoDock4 separately. No automatic
policy relaxation, new provider API or Meeko integration is implemented here.

The unchanged implementation regression gate passes 564 tests without skips in
117.46 s on Python 3.14.7 in `molsyssuite@uibcdf_3.14`, with editable DockingMT
and the existing exact CI provider archives (MolSysMT `c19a47ada0` and
MolSysViewer `ec4c71e574`). Ruff, formatting, report indexes and diff checks
pass. Those gates protect the existing consumer behavior; they do not execute
Meeko or validate the proposed native operations, which remain provider work.

## Sources

- [Exact source: preparation configuration and pipeline](https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/preparation.py).
- [Exact source: atom typing](https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/atomtyper.py), [bond policy](https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/bondtyper.py), [terminal merging](https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/molsetup.py).
- [Exact source: Gasteiger helper](https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/utils/rdkitutils.py), [polymer templates/rounding](https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/polymer.py).
- [Exact source: export maps](https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/writer.py), [reconstruction](https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/rdkit_mol_create.py), [flexibility](https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/flexibility.py).
- [Official ligand overview](https://meeko.readthedocs.io/en/develop/lig_overview.html), [configurable typing/merging/torsions](https://meeko.readthedocs.io/en/develop/lig_prep_advanced.html).
- [Vina/Vinardo charge requirement](https://autodock-vina.readthedocs.io/en/latest/), [Vina partial-charge FAQ](https://autodock-vina.readthedocs.io/en/latest/faq.html).
