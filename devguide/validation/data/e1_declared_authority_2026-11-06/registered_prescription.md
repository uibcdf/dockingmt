# E1 declared chemical authority receiving — 2026-11-06

Owner: [DockingMT #78](https://github.com/uibcdf/dockingmt/issues/78).
Status at prescription: **prospective**. The
[notebook](e1_declared_authority.ipynb) separates attempted legacy transport from
construction of a new declared source. Code/input identities and resources are
registered before execution. It uses the actual editable development composition;
it is not ordinary-installed, public-package or complete E1 qualification.

## Original declarations and their limits

Read the original [admission](data/human_3ptb/admission_2026-10-20.json.gz),
compressed SHA-256 `79e9283236ebbb645cd75d7c3341d457a8078361466b7a26458c814d8041cd53`.
It is about 97 MB decoded. Select its ligand observed/charged snapshots and
template options once, preserving a JSON selection and original file identities,
then release unrelated receptor records before scientific imports.

The legacy `dockingmt.chemical_template_snapshot@2` records include public
ChemicalStatesDict version 2 payloads whose preparation-history arrays were
converted to JSON lists. Current native transport requires the original array
dtypes/shapes. Public conversion is expected to reject both snapshots at that
history boundary. Do not write a downstream history decoder, remove history or
coerce typed arrays to obtain a different outcome.

Independently, observed9 declares partial connectivity and missing atomic
chemistry. Charged18 has complete connectivity but its nine heavy-atom stereo
entries are masked unknown; neither snapshot contains MolecularMechanics.
Those declarations do not establish a complete prepared13 source or a positive
strict chemical witness. These are inspected limits, not chemical refusals
executed through a restored snapshot.

## New authority and coordinate association

The human record already declares `smiles:NC(=[NH2+])c1ccccc1`. Parse that exact
string anew through public SMILES-to-RDKit-to-MolSys conversion. This executes
new provider interpretation of the chemical declaration and retains its actual
H/stereo representation. No indexed H is generated, and no partial charge,
AutoDock type or experimental state is inferred. This source has its own
producer; never reuse the old native-template checksum as its identity.

The original template correspondence pairs are **template index, observed
source index**. The explicit inverse order for `permute_atoms` is
`[3,4,5,6,7,8,1,2,0]` in new-to-old order. Retain the actual provider permutation
report and check it against that recorded declaration. Check elements and the
known heavy-atom formal charges; do not guess a molecular match. Keep new
template labels separate from historical labels.

Compose the publicly returned Topology and ChemicalStates with public Structures
containing the original observed9 coordinates/box and their explicit nm units.
Restore the declared one-frame/state association explicitly. This creates a new
nine-atom declared authority, not a restoration of the legacy molecular object.

Use all five thirteen-atom PDBQT projections received by the
[previous trial](e1_partial_projection_2026-11-06.md), verifying each actual
digest against its frozen receipt. Through MolSysMT, read each PDBQT, extract
the declared heavy indices `0..8`, verify names/elements and transfer only its
coordinates to an independent copy of the new authority. Read the variant's
actual coordinates back and compare them in nm within `1e-12 nm`. The partial
PDBQT's chemistry, charges and types are not mixed into the new declaration.

## Prespecified population and controls

Run serial normal nm/ps and pm/fs policies, retaining caller policy and original
records. Each supplied correspondence contains one complete candidate map and
uses `max_matches=1` with explicit reference chemical states and structure 0.

| Population per policy | Expected receiving |
| --- | --- |
| Five coordinate variants of the new authority | Five positive declared-graph witnesses, independent of coordinate changes. |
| One reversed native atom axis | One positive witness using the actual provider permutation map. This is not a nonidentity PDBQT export test. |
| One written/read H5MSM authority | One positive witness plus checked coordinates, labels/elements and frame/state association. It does not roundtrip all five poses. |
| Carbon-13 substitution on atom 0 | One incompatible supplied-map refusal with `StructuralInconsistencyError` and no complete-context extension. |
| Each of the two legacy JSON chemical payloads | A separate `ValueError` for inconsistent preparation-history array dtype/shape. These are transport refusals, not negative identity witnesses. |

Totals: **fourteen positive witnesses, two isotope refusals and four legacy
transport refusals**. The identity API has sixteen attempts, not fourteen.
There is one new declared graph, five reused historical coordinate sets, and
two repeated unit policies; these do not add independent complexes or restore
the historical prepared-state identity.

Direct-call caps over both policies are: convert 80, get 300, copy 30, set 30,
extract 12, permute 6, correspondence 16 and readiness 6. Counters observe only
the selected direct function calls; constructors such as Structures and
ChemicalStatesDict, provider internals and other aliases are outside them.
Local wrappers do not patch package globals. Retain complete provider witnesses,
readiness and permutation reports. JSON report projections are inspection
records; H5MSM supplies the provider-owned molecular persistence.

Check the source's typed chemical payload, listed inventory and coordinates for
nonmutation. H5MSM receiving is bounded to its listed checked fields and chemical
witness. Original admission and partial-projection bytes remain unchanged.
No scoring, docking, optimization, H generation, partial-charge/type assignment,
interaction detection or viewer is prescribed. SMILES interpretation and the
declared new construction are actual molecular operations.

## Resources, failure and custody

Execute the registered cells once, in order, in a fresh disposable Python
process. Use one allowed logical CPU, low priority and one native worker. Admit
and monitor an **8 GiB available-RAM reserve**, a **1 GiB task-RSS limit**, a
**2 GiB address-space limit**, **60 CPU seconds**, and a **90-second wall limit**
for the entire trial. The large JSON selection occurs before scientific imports;
its measured peak remains subject to the same process bound.

Stop only owned work on resource limits, retain interruptions and do not
automatically retry. An unexpected refusal stops the population before the next
policy; it does not authorize filling missing fields or discarding history.
Any correction gets a separate registered code identity/attempt. Preserve
started/completed/failed cells, direct counters, warnings and partial outputs.
Existing output directories and original inputs are never overwritten.

Keep exact pre-execution code/prescription, selected original diagnostics,
source H5MSM files, witnesses and resource outcomes under #78/#50; custody review
is **2026-11-13**. The earlier local E4 hold remains unchanged. Complete prepared13
chemistry/mechanics, comparison/reference admission, native rescoring and full
E1 acceptance remain separately required.
