# 3PTB source handoff clarification, 2026-10-10

Owning issue: [DockingMT #5](https://github.com/uibcdf/dockingmt/issues/5).
Provider: [MolSysMT #385](https://github.com/uibcdf/molsysmt/issues/385).

The original [prospective protocol](3ptb_prospective_protocol.md) and its
registration remain unchanged. Admission probes found that the pinned public
MolSysMT conversion rejects a `.pdb.gz` path during form recognition. The same
original PDB bytes, restored with standard archive tooling, are accepted as a
plain `.pdb` input with `get_missing_bonds=False`. Exploratory preparation probes
have already run; no fixed evaluation or search has run. This clarification is
registered before the durable admission and before the planned searches.

The case-specific admission command accepts a **caller-supplied plain PDB**.
It authenticates that file against the original downloaded-byte SHA-256
`288f7954d4d013fa8eab3808e1037e2958e2dcd12c9eca65a3f1014404a9f9a2`
before molecular conversion. Generic `gzip` archive extraction is an explicit
caller action, outside the molecular command; DockingMT gains no compressed
PDB reader, format adapter, connectivity inference or molecular parser.
The immutable compressed source and acquisition receipt stay authoritative.
Plain input success does **not** qualify direct compressed-input consumption.

The scientific population, source coordinates, chemical declarations, models,
torsion choices, boxes, ordering, evaluation and stopping rules are unchanged.
The admission receipt must name this handoff and retain its registration identity.
The original protocol's H expansion permits an explicit attribute-loss decision:
use public `attribute_policy='intersection'` only after retaining the original
occupancy and B-factor arrays. Record the strict-policy rejection and provider
loss reports. No replacement values are invented for newly generated atoms.

MolSysMT owns compressed molecular-input support. Review this handoff when #385
is implemented, or by 2026-11-10. Remove the plain-input staging requirement only
after separately qualifying the provider's public compressed route for exact
source identity, reader policy and coordinates. This bounded transport handoff
does not retire the existing provider projection/export proposals.
