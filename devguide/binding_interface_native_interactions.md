# Native ionic observations and observed-participant pharmacophores

Owner: BindingMT #112; provider handoff: PharmacophoreMT #108 at cb6af716.
Admission: 2026-11-12, before implementation. Status: bounded Pint native source profile received; unyt construction pending PyUnitWizard #156.

## Maintainer priority and finite scope

After contacts and SASA/burial, the maintainer selects native chemical
characterization and H0/H1 integration. PISA T0/T1 stays deferred optional
interoperability/comparison under #112; it is not the automatic next milestone.
Revisit its priority after this native/consumer slice or a concrete external-result
workflow is selected. Its frozen evidence, obligations and owner adapter remain
intact. No PISA parsing, execution or dependency is introduced.

The first admitted chemistry is MolSysMT's native formal-charge ionic profile,
using supplied complete chemistry and one explicit Cartesian frame/state, no PBC,
identity source atom/structure axes. Other chemistry, remapping/state transfer and
arbitrary cross-source authentication remain separately qualified. The caller
admits the unchanged full source used by the existing named native analyses.
All selection, chemical recognition, observation queries, native serialization
and pharmacophore construction remain with their public providers. BindingMT
owns the binding grouping, scoped characterization, contribution associations and
original/current-use distinction. No new molecular filter/kernel/codec is added.

## Public route and evidence ownership

`characterize_interface_interactions` accepts the native MolSys, named participant
selections, binary grouping (including composite sides), an explicit nonempty
ordered list of existing analysis names, source label and structure index.
MolSysMT resolves molecular selections and its public `between_selections` applies
strict exclusivity. Internal A–B and unrelated C–D stay in the full native carrier;
only A–C contributes to the (A+B)|C characterization. Preserve original
analysis-qualified relation/occurrence keys, coverage, participants, source axes,
criteria, measurements, producer/attribution and original claim. Evaluated empty
is retained; absent/unsupported/uncovered/incompatible inputs refuse this operation.
No detector runs in this composition entry point. New ionic observations are
calculated through public `msm.interactions.ionic.get_ionic_interactions` before
composition; this initial slice adds no automatic detector-selection policy.

Experimental 0.4 `BindingInterface` stores domain observation summaries/references,
not a replacement for the full native Interactions codec. Public MolSysMT
H5MSM 1.0 remains the complete source/analysis persistence route. Core save/read
resolves no assets or molecular tools. Fields interpreted as lengths/charges use
sealed QuantityRecord handshakes; opaque original parameters remain attributed.
Historical checks never certify a different present input.

`build_interface_pharmacophore` explicitly rechecks the characterization's scoped
facts against the caller-supplied unchanged full MolSys and delegates to public
PharmacophoreMT `from_interaction_collection`. The target participant is observed,
not complementary. Radius and duplicate policy are explicit. This first route uses
same_participant or keep; compatible repeated evidence adds contributions without
increasing weights. Each alternative source/context has its own characterization
and hypothesis. Required child failures publish no partial successful query.

`BindingInterface.with_pharmacophore` associates the exact native hypothesis's
site/contributor references with an explicit caller-owned saved-asset reference.
It creates a new record/immediate parent without rewriting original observations.
No query reconstruction, evaluation or molecular detection happens on core read;
native hypotheses are saved/read through PharmacophoreMT. Query construction and
candidate evaluation retain actual owner attribution, while saved reuse gains no
new originating execution credit. Annotation alone changes no flags/weights/radii.

## Independent receiving and limits

Receive frozen authored four-ion inputs at PharmacophoreMT cb6af716 without
regeneration. Independent expectations are full pairs AB/AC/CD, strict scoped AC,
one positive-charge sphere on C with two labelled contributions and weight one,
and explicit coverage for empty analysis. Original chemistry, source/native maps,
relations/occurrences and alternative references survive real public save/read.
Two compatible analyses do not become independent physical evidence.

Exercise actual fresh public ionic detection, characterization/construction,
I0/H0/I1 association, owner-native persistence and cold readback. Independent
primary/alternative expected decisions are (matched,1)/(not_matched,0); absent
essential weight-zero and exclusion controls keep fit1 but reject; keep-policy
competition yields fit0.5 and a failed decision. These are authored consistency
controls, not biological/affinity validation. Incompatible state/maps/coverage,
cut compound charge participants, changed required context, malformed quantities
and missing/corrupt native assets refuse without inventing successful zero.

Normal and pm/fs source cells run serially on CPU0/nice10, native workers one,
13-GiB available reserve and monitored 512-MiB owned RSS cap; no reservation,
shared-prefix modification, native rebuild or held-suite restart is implied.
Exact provider/source/native identities, all original attempts and source hashes
around receiving belong to task-local #50 custody. Report missing/broken generic
operations to MolSysMT, pharmacophoric semantics to PharmacophoreMT. Source-only
receiving leaves #112/#30/#195, broader chemistry, P and installed/public/platform
acceptance with their own gates.

## Delivered workflow

```python
from hashlib import sha256
from pathlib import Path

import molsysmt as msm
import bindingmt as bmt
import pharmacophoremt as phmt

# system is the complete admitted native MolSys.
observed = msm.interactions.ionic.get_ionic_interactions(
    system, '0.31 nm', selection='all', selection_mode='internal',
    structure_indices=[0], pbc=False,
)
system.interactions = {**system.interactions, 'ionic': observed}
initial = bmt.characterize_interface_interactions(
    system, participants={'A': [0], 'B': [1], 'C': [2]},
    grouping=[['A', 'B'], ['C']], analysis_names=['ionic'],
    structure_index=0, source_id='my-admitted-source',
)
print(initial.summary()['native_interactions'])
initial.save('I0.json')
model = bmt.build_interface_pharmacophore(
    initial, system, participant='C', radius='0.02 nm',
    duplicate_policy='same_participant',
)
phmt.io.to_json(model, 'H0.json')
# Independently compute the exact saved file's SHA-256; retain custody yourself.
linked = initial.with_pharmacophore(
    hypothesis=model, participant='C',
    hypothesis_ref={'uri': 'H0.json', 'sha256': sha256(Path('H0.json').read_bytes()).hexdigest()},
)
linked.save('I1.json')
msm.h5msm.write(system, 'full-source.h5msm', format_version='1.0')
```

The indices, cutoff and matching radius above are illustrative caller choices.
The complete carrier retains all original observations; replacing its interaction
mapping uses the public setter, never mutation of its read-only mapping view.
Store/locate the full native source separately under caller custody. Original
analysis references are scoped to the admitted source label; no general source
locator or authentication is invented. `hypothesis_ref` is a supplied reference,
not a claim that BindingMT opened or authenticated its file. Actual owner save/read
and exact byte checks supply that evidence in the receiving workflow.

The public characterization has finite admission (4,096 source atoms and 65,536
full input occurrences by default), with explicit configurable bounds. These are
application limits, not measured large-system performance or RAM reservations.
All requested analyses must share source identity (including unset), complete
identity axes, the selected associated state and evaluated frame. Public owner
charge-center checks reject cut compound participants. Metadata snapshots check
selected-frame coordinates, elements/formal charges and exact scoped observation
views on explicit new use; the caller still admits unchanged full topology and
analysis origin. No general molecular matcher/fingerprint or atomic concurrency
observer is implemented. A relevant coordinate edit may invalidate native coverage;
that owner refusal is preserved instead of a fabricated context-match result.

`interaction_analyses` exposes detached binding views, including known criteria,
sealed distance/charge arrays, original occurrences and whole participants. Full
native serialization remains H5MSM/InteractionsDict. The emitted hypothesis gains
one namespaced BindingMT construction marker; original producer/contributor
metadata and all query flags remain intact. Linking checks its original
characterization identity/context and the unchanged native site snapshot. An
edited hypothesis needs a separately admitted curation/linking route. Core 0.4
reads/copies/reinterpretations preserve original observations without recalculation.
Earlier declaration/contact/surface formats remain readable. Site references keep
original I0 context even when I1 is later reinterpreted.

## Measured source receiving — 2026-11-12

Actual focused source receiving reports **271 passed, 1 xfailed per unit policy**,
Pint normal and Pint pm/fs with the matching operation's angle standard retained. The new module has **33 passed and 1 xfailed**; previous
238 contact/surface/data/result/outcome/core/bootstrap controls remain included.
The strict expected failure is only native construction under unyt, blocked by
[PyUnitWizard #156](https://github.com/uibcdf/pyunitwizard/issues/156). The separate
core reader does succeed under unyt/pm-fs with recognition forbidden. No xfail is
counted as a pass or a qualified backend, and no consumer registry alias, fallback
or global policy reset conceals the owner defect.

Known sealed domain fields use an explicit Pint interchange boundary regardless
of application quantity form. Public owner charge-center recognition still reaches
the failing elementary-charge conversion under unyt; native construction for that
backend remains pending. The reproducer fixes the parser explicitly to Pint.
Matching uses an explicitly complete application policy: pm, fs, K, mole, dalton,
e, kJ/mol and radians. An earlier length/time-only evaluation attempt lacked an
angle standard and failed during PoseEvaluator argument normalization. The
misleading invalid-angle diagnostic is reported as
[PharmacophoreMT #202](https://github.com/uibcdf/pharmacophoremt/issues/202); this
is a diagnostic/usability improvement, not an admitted partial-policy guarantee.
That attempt remains
separate from successful pm/fs receiving and from the unyt charge defect.

An earlier parser-unspecified probe returned the distinct missing-unyt-parser
message; it is not evidence for the conversion defect. Upstream `c1cf832` has the
same converter blob `49d4a8d3106a71d5a94bfd4adfaa4d752ad0b8c5` as tested cc51c8e.

The positive/empty public workflow emits four actual I0/I1 core records, two
native hypotheses and the complete H5MSM source. Independent processes inspect
core records with PharmacophoreMT/TopoMT/Vina unavailable, and explicitly use
owner native readers with detection, recognition and public molecular operations
forbidden. Source files, markers, constraints/contributors and active unyt/pm-fs
policy remain unchanged; capture records zero new originating uses on saved read.
Alternative and constraint decisions come from actual BindingMT construction plus
public owner evaluation, with the independent expectations above.

Frozen inputs are exact PharmacophoreMT cb6af716 files (unchanged at a50c16f),
received at `tests/data/interface_native_handoff/cb6af716/`, with original manifest,
producer identities and MIT notice. All support files have exact SHA-256 entries
in `devtools/conda-build/resources.toml`; no historical input was regenerated or
renamed to a new producer. Source query/construction helpers remain test-local;
there is no dependency on PharmacophoreMT's unshipped helper namespace.

Actual clean providers: MolSysMT ff25f120, PharmacophoreMT a50c16f, PyUnitWizard
cc51c8e, ArgDigest 7be790b, SMonitor 4a4cd1e and DepDigest 5e93eaf. Reported
editable version strings, including stale installed version metadata, are retained
separately from Git/file identities. The loaded historical MolSysMT native SHA-256
is `2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`;
its original builder/source identity remains unauthenticated, distinct from the
owner-reference binary. Refreshed remote commits were explicitly preserved as
unmerged: this finite profile needs no provider replacement/build. The older local
MolSysSuite registry's unknown-bindingmt attempt was superseded by its immutable
received registry/tool at bb641488; no sibling worktree was altered.

Source/test/provider hashes around final cells, original failed fixture/API
attempts, the independent owner reproducer, emitted assets/readers, environment,
resource and final workspace/fresh committed-export receipts retain #50 custody
in `.molsyssuite/interface-native-chemistry-112-20261112/`, review 2026-11-14.
All cells use CPU0/nice10, native workers one and monitored 13-GiB available
reserve/512-MiB owned RSS. Optional Beartype absence emits the provider's declared
warnings; no installation or private suppression is introduced. Source receiving
is not installed/public/platform, broad chemistry or the held full scientific suite.

## Next owner actions

Receive PyUnitWizard #156's supported correction, then rerun the strict unyt
construction control and affected policies; do not silently retain an xfail after
owner repair. Additional chemical families require their own definition/receiving,
not reclassification of geometric contacts. Receive the remaining exact PeptideMT
P cases, distinguish local consumer use from provider-team adoption, and record
finite shared disposition under MolSysSuite #195. Regional H-R1 is conditional;
H-R2 still needs its explicit before/after characterization-annotation control.
PISA T0/T1 remains deferred optional work under the maintainer disposition;
#111, complete H/P obligations and #30 retain separate gates. #112 stays open.
