# Scientific scope

## Accepted molecular binding domain

BindingMT models and characterizes molecular binding. The maintainer accepts the
canonical identity and conceptual expansion under
[#108](https://github.com/uibcdf/bindingmt/issues/108), including the explicit
future free-energy/interface direction, on 2026-11-11. This is one continuing
component, broader than a docking method or any initial provider.

| Operation | Scientific promise | Current status |
| --- | --- | --- |
| Molecular docking | Explore relative placements and allowed conformations of declared partners, with explicit preparation, constraints and search information. | Implemented Vina/Vinardo profiles; broader flexibility/partner/provider support needs its own receiving. |
| Fixed-identity complex prediction | Predict complete multicomponent structures from declared identities, sequences and optional structural/prior information. Every partner may move. | Accepted domain; Boltz-2 proposal [#110](https://github.com/uibcdf/bindingmt/issues/110), no received prediction runtime/API. |
| Complex refinement | Transform a declared complex through an explicit physical or model-based protocol, preserving correspondence and changes. | Accepted domain; provider-specific design/qualification pending. HADDOCK3 [#109](https://github.com/uibcdf/bindingmt/issues/109) proposes a physical docking/refinement route. |
| Binding free-energy calculation | Estimate a declared binding thermodynamic quantity with a physical/statistical method, states, conditions, units and available uncertainty/convergence evidence. Absolute and relative binding questions belong here. | Accepted future capability; no provider, implementation or scientific profile qualified. |
| Binding free-energy prediction | Predict a defined binding free-energy endpoint using an applicable model, retaining domain limitations, conditions, scale and supplied uncertainty. | Accepted future capability; not implied by structural confidence or generic affinity output. |
| Binding-interface characterization | Investigate contacts, geometry/topography, physicochemical organization and changes at a declared interface through explicit native calculations and composition of owner-provided molecular analyses. | The first Cartesian contact/footprint source profile is implemented through MolSysMT under #112. Fixed-input SASA/burial and bounded native ionic/H0/H1 source profiles are also implemented; richer profiles remain pending; source receiving is not broad scientific or public-package qualification. |

Future domain acceptance neither implements an operation nor makes it a new
automatic release/1.0 gate. The existing Core/Extended objective and separate
provider proposals retain their commissioning, owners and evidence requirements.
No new engine, molecular campaign, weights download or native calculation is
part of the naming/conceptual transition.

The [first interface data profile](binding_interface_data_core.md) now preserves
caller-declared questions and analysis outcomes through immutable core JSON.
The [native contact profile](binding_interface_contacts.md) now adds actual
MolSysMT Cartesian cutoff contacts/distances, group witnesses and participant
footprints. The [SASA/burial profile](binding_interface_burial.md) adds both side
losses with supplied H, element-vdW radii and an explicit probe/density. Broader
environment-aware/chemical/energetic characterization remains planned;
contact geometry is not binding strength or biological association evidence.

The [bounded native ionic profile](binding_interface_native_interactions.md)
adds strict binary/composite grouping of owner observations and an optional
observed-participant pharmacophore. It retains supplied formal-charge chemistry,
original occurrences and independent query semantics. Those ionic observations
are geometric evidence between recognized charge centers, not an electrostatic
energy or binding prediction. Pint source receiving is finite; unyt native
construction remains pending at its unit provider. PISA is deferred optional
interoperability/comparison under the maintainer's native priority.

The [H-R2 continuation](binding_interface_characterization_annotation.md) associates
actual contact/surface evidence at participant level while preserving native
hypothesis references and query semantics. It introduces no feature detection,
site importance, burial-membership threshold or energetic interpretation. Relevant
source mismatches refuse annotation; stored checks retain their historical scope.

## Scientific distinctions and applicability

Physical docking and joint complex prediction receive different inputs and make
different promises. An operation may accept sequence-only or coordinate-free
identity when supported. A Vina box, prepared PDBQT, pre-existing ligand pose and
unchanged receptor are not universal requirements. Current
`DockingProblem`/`VinaProtocol` contracts retain their received docking scope;
future operations receive their own scientific obligations.

Free-energy calculation and prediction need an explicit endpoint and molecular
states, thermodynamic/standard-state conventions and relevant conditions. A
method identifies what is estimated and what uncertainty/convergence evidence
is available. Do not relabel an empirical docking score, interaction energy,
confidence, dissociation constant or assay endpoint as a binding free energy
without a scientifically justified relation and its assumptions. An affinity
predictor is admitted only for its actual endpoint and applicability profile.

Interface geometry, contact counts, buried/exposed surfaces, interaction networks
and energetic descriptors remain method-specific observations. They do not alone
establish affinity, biological function or a physically populated binding state.
General molecular analysis and surface/topographic kernels remain with MolSysMT,
TopoMT and specialized owners. BindingMT supplies the binding question,
associations and interpretation.

Keep native, completed and refined artifacts distinct. Generated/removed atoms,
representation approximations and changes to every partner require explicit
maps and provenance. Native model confidence belongs to its original prediction;
new atoms or transformed coordinates do not automatically inherit it. Unsupported
chemistry, incomplete output and failed completion remain inspectable outcomes.

## Current received software and scientific profiles

The initial reference profile remains canonical **protein-small-molecule local
docking** with AutoDock Vina. The source-only 0.1.0 milestone belongs to its exact
historical BindingMT source, wheel/providers and evidence. Renaming does not
qualify those artifacts as new BindingMT packages or broaden their science.

The Core objective includes reproducible preparation, declared local/selection
regions, redocking, normalized poses/results, named ranking, visualization and
molecular/provenance identity. The Extended objective includes explicit
scoring/rescoring, small collections, comparison/clustering, bounded interaction
analysis and exploration. Consult the owning evidence/plan for received profiles
and remaining public, platform, scientific and canvas gates.

Current starting workflows use one declared small-molecule state and rigid
protein, a physical search box and Vina. Broader partner domains, receptor motion,
covalent chemistry, metal/water handling and production-scale screening need
independently admitted profiles. Code, metadata or a concept in this guide does
not establish scientific support.

## Architectural directions and boundaries

Design for fragments, macrocycles, peptides and multiple partners; receptor
flexibility/ensembles; non-box/global domains; waters/cofactors/metals; restraints
and guidance; multiple providers/stages; refinement; binding-energy methods;
interface/landscape analyses and meaningful uncertainty. Add concrete operations
when accepted workflows need them. Preserve public contracts; do not implement a
universal framework or rewrite numerical engines without a measured need.

- MolSysMT owns molecular representations, chemistry, preparation, selections,
  transformations, formats, maps and general interaction analysis.
- TopoMT owns topography and physicochemical observations on its own supported
  spatial regions; BindingMT consumes them for association-specific questions
  or directly composes MolSysMT. Specialized suite components retain pharmacophore,
  elastic-network, visualization and numerical responsibilities.
- BindingMT owns binding-domain scientific operations and provider adaptation,
  composing public tools and reporting missing owner capabilities.
- PeptideMT owns peptide generation/redesign and peptide-specific selection;
  Praxis and other MolI components keep their established boundaries.
- Single-molecule folding, general conformational sampling, sequence generation,
  a universal AI model platform, generic project/evidence management and a new
  scheduler are outside this component's present ownership.

External methods remain optional and independently inspectable. Their operation,
execution route, dependencies, source/model terms, hardware/resource limits and
failure modes are explicit. Core import and saved-result inspection remain
independent of optional runtimes, accelerators and remote services.
