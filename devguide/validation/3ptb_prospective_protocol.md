# Prospective 3PTB redocking protocol

Registered on 2026-10-10 under DockingMT [#5](https://github.com/uibcdf/dockingmt/issues/5)
and [#6](https://github.com/uibcdf/dockingmt/issues/6), with preparation-state scope
in [#4](https://github.com/uibcdf/dockingmt/issues/4) and provider migration in
[#49](https://github.com/uibcdf/dockingmt/issues/49). **Planning only: no 3PTB
preparation, fixed evaluation or docking search has been executed for this slice.**
The [registration record](data/3ptb_prospective/registration_2026-10-10.json)
binds the protocol bytes to its owning issue comment; it is not a molecular
admission or execution receipt.

## Question and case selection

Can an independently selected conventional protein–ligand case be prepared
through public MolSysMT tools, and does the resulting Vina workflow generate
near-reference poses and rank them first under a small, fixed search population?
Report generation and ranking separately. Admission can fail before any search;
that is an informative outcome, not permission to replace molecular tools locally.

[RCSB 3PTB](https://www.rcsb.org/structure/3PTB) supplies a 1.70 angstrom X-ray
structure of bovine beta-trypsin, one modeled protein chain with 223 residues,
benzamidine and calcium. It is a different protein/ligand case from the existing
181L, 1IEP and 5X72 controls. Selection uses public structural and methodological
evidence, not observed DockingMT performance on 3PTB. One additional case does
not establish generalization or an unbiased multi-complex benchmark.

The [BEN chemical definition](https://www.rcsb.org/ligand/BEN) has formal charge
zero. The [2022 primary study](https://doi.org/10.3389/fmolb.2022.922361) describes
cationic benzamidine and sensitivity to His57 state in molecular dynamics.
This motivates an explicit cationic ligand/HID57 hypothesis; it neither predicts
the experimental protonation state nor transfers MD outcomes to Vina redocking.
No numerical affinity, kinetic or experimental success target is imported.

## Frozen sources and source admission

The unchanged public inputs are retained beside [the acquisition receipt](data/3ptb_prospective/acquisition_2026-10-10.json):

| Input | SHA-256 |
| --- | --- |
| [3PTB.pdb.gz](data/3ptb_prospective/3PTB.pdb.gz), decompressed | `288f7954d4d013fa8eab3808e1037e2958e2dcd12c9eca65a3f1014404a9f9a2` |
| [BEN.cif.gz](data/3ptb_prospective/BEN.cif.gz), decompressed | `a7ce813cbbac599168d4772f635ae23d7c6edb4d83a9891ebabcbe9e8bb66849` |
| [RCSB entry metadata](data/3ptb_prospective/entry.json) | `72f53e884a08dc758905d3e3ec663a1b2f00327cdbe148d7bf45dc380da25899` |

Compressed storage preserves every original downloaded byte; the acquisition
receipt separately records downloaded and stored-file digests. Future execution
reads these bytes through public MolSysMT conversion with
`get_missing_bonds=False`; do not silently accept optional reader inference.
Retain source-declared bonds and assess compatibility before completing chemistry
from explicit templates. Confirm one source frame, protein author chain A,
BEN author chain A/residue 1, and exactly nine ligand heavy names
`C1,C2,C3,C4,C5,C6,C,N1,N2`. Retain original atom IDs, group/chain IDs,
coordinates, occupancy/alternate-location inventory and full-source selections.
Reject unresolved alternate locations, ambiguous identity, conflicting declared
chemistry, or missing observed heavy atoms rather than selecting by score or
inventing repairs. The original protein includes terminal OXT; verify it through
MolSysMT rather than adding another atom. No crystal-neighbor receptor expansion
or assembly reconstruction is authorized in this population.

## One declared chemical hypothesis

All extraction, copying, templates, chemical application, H generation, named
charges/types, molecular projection and geometry use public MolSysMT tools.
DockingMT owns the explicit state/torsion choices, search, reporting and evaluation.

- Select the observed protein chain A as a rigid receptor. Exclude all observed
  waters, calcium and BEN from it, preserving their source identities in the
  record. This is a dry protein-only hypothesis: no calcium parameter, water-role
  assessment, structural relaxation or metal-interaction claim is made.
- Declare HIS57 as HID, HIS40/HIS91 as HIE; verify this is the complete source
  histidine inventory. Use explicit factory states ASP/GLU carboxylate and
  LYS/ARG cationic, standard remaining residue states, ammonium N terminus and
  carboxylate C terminus. No pH or state prediction is performed.
- Declare the six deposited disulfides by author residue IDs
  `(22,157),(42,58),(128,232),(136,201),(168,182),(191,220)` in chain A.
  Resolve them to exact selected group indices, declare those twelve residues
  CYX and supply the pairs to `physchem.get_peptide_chemical_template`.
  Confirm the deposited source and resulting chemical links agree. Do not
  classify links from sulfur-distance thresholds in DockingMT.
- Declare ligand benzamidinium, total formal charge +1, with the explicit
  template `smiles:NC(=[NH2+])c1ccccc1`. BEN's neutral CCD remains a source
  reference, not an automatically adopted state. In this template the declared
  ordered atom-name correspondence is `N2,C,N1,C1,C2,C3,C4,C5,C6`.
  Public template conversion and assessment must verify the nine-atom map,
  elements, ring/aromatic bonds and chosen N1-double/N2-single resonance
  representation before application. Do not infer an atom matcher from this
  fixture-specific table or silently overwrite conflicting source chemistry.
- Complete only missing compatible chemistry through the provider's explicit
  template application policy. Preserve every observed heavy coordinate and ID.
  Add missing H in the declared fixed state through MolSysMT's RDKit route;
  verify source-to-expanded maps, H parents, disulfide H absence, formal charge,
  complete valence coverage and source immutability. Retain any explicitly
  required attribute-loss decision and all preparation reports. Environmental
  H refinement remains unassessed under MolSysMT #323.
- Request `gasteiger_marsili` charges and `autodock4` types with
  `chemical_environment@1`, both through public MolSysMT. Require complete finite
  values, conservation of charge through existing prepared projection, retained
  polar H, full original/expanded/prepared/PDBQT maps and original calculation
  attribution. Successful typing is not a validation of this model for trypsin.
  Use explicit elementary-charge units; the provider unit-policy question remains
  [MolSysMT #381](https://github.com/uibcdf/molsysmt/issues/381).

Use the already qualified provider `739395d7ea31bec5c3f77cdcb1135ecf7e7c9bac`
and receiving source/runtime profile recorded in
[the 5X72 checkpoint](data/5x72_displacement/checkpoint_2026-10-10.json).
Record actual consumer/provider source and native artifact digests and package
versions at execution. Any dependency change requires its own qualification
before admitting the population. General projected-object/charge-provenance
retirement remains [MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223);
the existing bounded consumer route is not a new provider capability.

## Fixed population and ordering

The two ligand arms share the same full precision heavy/H geometry, chemical
state, charges/types and source selection. Prepare independently from detached
copies of that common state. The **rigid** arm has no active bonds; the
**explicit flexible** arm requests only the source-name bond `C1–C` between
the phenyl ring and amidine carbon. MolSysMT must validate that this is a
supported non-ring single heavy bond and derive the two rigid fragments.
Record cuts, fragments, ROOT orientation and exported atom order; do not enable
amidine C–N bonds, automatic torsion perception or outcome-selected ROOT orders.
Require source-axis equality of coordinates and charge/type fields across arms,
within the actual writer precision. A rejected explicit cut is an admission
failure, not a reason to choose another bond after observing results.

Define the native box center as the unweighted geometric center of the nine
original ligand heavy atoms through existing public molecular/region tools.
Its dimensions are exactly `[20,20,20]` angstrom. Define the negative box as
that center plus `[60,0,0]` angstrom with identical dimensions. Preserve ligand
coordinates; change the search region only. Verify that every native heavy atom
lies inside the native box and outside the negative box before launching Vina.
Retain unrounded quantities and actual backend center/size serialization.
Never resize or reposition a box after seeing search output.

Exactly **24 searches**: two torsion arms × two boxes × seeds `[7,42,2026]`
× exhaustiveness `[1,8]`. Execute in that nested order (rigid before explicit
flexible, native before negative, then listed seed and effort order).
Vina 1.2.7, `scoring='vina'`, CPU 1, requested maximum nine poses,
`energy_range=3 kcal/mol`, `allow_provisional_preparation=False` and
`capture_backend_inputs=True`. Record the backend's actual pose-clustering
defaults and resolved options. Requesting nine poses does not guarantee nine
returns. Do not retry for favorable results, extend the matrix, optimize saved
poses separately or compare scores across different prepared ligand arms as
affinity. No new fixed-score calculation is part of this population.

Both boxes must submit identical ligand/receptor bytes within each torsion arm;
seeds and effort do not authorize re-preparation or H regeneration. Record every
attempt, native exception, partial completion and returned result. A scientific
negative outcome does not justify removing a run from the denominator.
Incomplete execution reports attempted/completed/planned counts separately.

## Prespecified interpretation

Evaluate every returned pose against the original nine heavy atoms with verified
source correspondence, **positional RMSD without alignment or symmetry matching**,
in explicit angstrom. Near-reference means RMSD **at most 2.0 angstrom** in
this protocol only. Report every pose's rank, complete returned score vector,
RMSD, atom map and box containment; top-1 success, any-returned-pose success,
best returned RMSD and first near-reference rank (nullable) for each search.
Retain raw score components and declared backend meanings; a total Vina score
is not an experimental binding free energy.

Summarize the six planned runs separately for each torsion arm/box; retain
seed/effort strata and failure counts. This finite population supplies neither
recovery probabilities nor population-level confidence intervals. A returned
near-reference pose outside rank 1 separates generation from ranking under
these conditions, without proving a unique search/scoring failure mechanism.
Scores alone do not establish pose correctness.

The negative box is a **methodological search-domain control**, not a nonbinder
or enrichment experiment. Any apparent near-reference return there requires
investigation of containment, reference/mapping and units before interpretation.
Benzamidine ring symmetry and amidinium resonance can make source-identity RMSD
conservative. Retain this ambiguity; do not add a local symmetry algorithm or
label every over-threshold pose biologically incorrect. Any symmetry-aware
extension belongs to the provider route (MolSysMT #310) and a separate protocol.

## Admission, delivery and stopping conditions

First qualify the source inventory, exact heavy/template maps, declared states
and disulfides, fixed-state H, named models, both torsion trees and box geometry
without searches. An unsupported operation is reported with bounded evidence in
its owning provider issue and cross-linked here; do not introduce general
molecular or pharmacophore routines downstream. No PharmacophoreMT operation
is required by the current scientific question.

Before the first search, retain a separate executed admission receipt with
prepared-input digests, the frozen 24-row population, software/source identity
and this protocol's Git blob/registration identity. Do not rewrite this protocol
to conceal an admission failure or outcome; append dated amendments and register
any replacement population before its execution. The present acquisition
receipt is not an executed molecular admission receipt.

Deliver a human-executable Python/Jupyter workflow through public APIs, immutable
raw results and a separate qualification receipt. The notebook expresses the
scientific decisions and inspects complete saved evidence; reusable molecular
work remains in its provider. This follows the pilots' general human-workflow
principles without copying private project data or introducing an agent-only
workflow or a new benchmark-publication platform (#29).

This planning change needs reporting/index, local-link, synchronized-guide and
raw-input digest checks. It changes no executable behavior and requires no
scientific rerun. Future executable work needs targeted molecular/preparation,
torsion, result/reference, quantity and reporting gates, a real non-default-unit
control, executed notebook and applicable exact-head CI. Stochastic recovery is
an observation, not a deterministic pass condition. Broad chemical preparation,
torsion-policy, scoring and public-admission issues remain partial.
