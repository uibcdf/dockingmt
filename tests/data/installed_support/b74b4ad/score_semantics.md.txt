# Score semantics and ranking evidence

DockingMT keeps finite numeric scores in `pose.scores`. A score's name does not
declare its unit or establish comparability. Optional descriptors are supplied
through `DockingPose(..., score_definitions=...)`, stored in
`metadata['score_definitions']`, and exposed as independent validated snapshots
through `pose.score_definitions`.

The [executed ranking notebook](ranking_history.ipynb) reads a saved synthetic
fixture and shows two ranking decisions, preserved observations, JSON round trips
and independent snapshots. Its numbers are invented software examples, not
docking predictions, rescoring output or scientific validation. Default execution
does not perform molecular operations or import Vina or MolSysViewer.

## Descriptor contract

Every descriptor has exactly these fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | `1.0`; omission is normalized to `1.0`. |
| `method` | Explicit scoring method, including the selected provider/function. |
| `method_version` | Method/provider version; `unknown` remains an explicit lack of evidence. |
| `component` | Interpretation of this value, such as total docking score. |
| `kind` | `empirical` for conventional energy-like docking scores, or `dimensionless`. |
| `unit` | Explicit energy-per-mole unit for empirical values, validated/canonicalized by PyUnitWizard; exactly `dimensionless` for dimensionless values. |
| `preferred_direction` | Advisory `lower`, `higher` or `null`; it never overrides an explicit ranking request. |
| `context` | Nonempty finite JSON object declaring the inputs and settings relevant to comparison. |

Descriptors refer to existing scores and own their context. A subset of scores
may be described; absence stays unknown. This block does not add physical-energy
scores, probability calibration, automatic unit conversion of score numbers, or
consensus semantics. A probability-like number is not certified as a probability
by a dimensionless descriptor. Empirical values retain their conventional units
and are not promoted to physical energies.

Descriptors accompany the numbers inside each pose record using the existing
metadata extension point. Outer pose/result schema 1.0 is unchanged. Legacy
records without descriptors retain their numbers and unknown meaning; readers
never guess a unit or method from a name. If the reserved metadata key is present,
it must now meet this documented contract.

## Current Vina/Vinardo adapter

The [upstream Vina 1.2.7 Python API](https://github.com/ccsb-scripps/AutoDock-Vina/blob/v1.2.7/build/python/vina/vina.py#L338-L358)
defines the columns returned by `energies()`. DockingMT continues to retain its
existing first four columns with unchanged numeric values:

| DockingMT name | Interpretation | Kind / conventional unit | Preference |
| --- | --- | --- | --- |
| `vina` or `vinardo` | Total docking score for the selected function | Empirical / kcal/mol | Lower |
| `inter` | Intermolecular term | Empirical / kcal/mol | Unspecified |
| `intra` | Intramolecular term | Empirical / kcal/mol | Unspecified |
| `torsion` | Torsional term | Empirical / kcal/mol | Unspecified |

Each descriptor names `AutoDock Vina/<selected function>` and the imported
provider version. Context records submitted receptor/partner PDBQT SHA256s,
the projected box and its explicit angstrom unit, actual scoring weights and grid
spacing from `Vina.info()`, and the existing preparation assessments. No inputs
are re-prepared or molecular identities inferred to produce these descriptors.
The adapter records the native pose order as the initial `backend` ranking.

New docking results also retain `provenance['backend_output']`, format
`vina_python_docking@1`: the entire native `energies()` matrix in kcal/mol,
ordered columns `total`, `inter`, `intra`, `torsions`, `intra_best_pose`, actual
`Vina.info()`, and supplied/default arguments resolved from the loaded wrapper
signatures for maps, docking and energy retrieval. The fifth column is retained
as native evidence rather than another ranking score. Vina/Vinardo execution
remains unchanged; older results need not have this optional evidence block.
`tests/test_vina_output.py` compares the saved matrix directly with the native
return and verifies serialization and default capture. Capturing wrapper defaults
does not establish defaults for a different backend version or document internal
C++ decisions that are absent from the wrapper interface.

`engine_info` preserves literal native values, including the receptor's temporary
staging filename. That filename is local to one invocation and can remain as a
recorded value after cleanup. Compare captured `backend_artifacts` bytes/hashes
for molecular input equality; temporary filenames do not define molecular
identity. The seeded individual/batch contract verifies those bytes, checks
staging cleanup, and excludes only that path and elapsed time when comparing
otherwise complete results.

Input hashes and matching settings define a deliberately conservative comparison
boundary. They do not qualify provisional/unassessed chemistry, establish physical
binding affinity, or authorize cross-ligand, cross-receptor or ensemble aggregation.
Future workflows must state their own comparison context and scientific gates.

## Ranking contract

`result.rank_by(name, ascending=True)` preserves its explicit boolean direction
and stable tie order. The selected score must be finite on every pose. If it is
described, descriptors and partner/receptor state IDs must match exactly across
the collection. Unit aliases canonicalize to the same representation; different
units are rejected without silently rescaling numbers. Context JSON distinguishes
booleans from numbers and retains list order.

An entirely undescribed collection remains explicitly rankable. Mixing a described
and undescribed selected score fails, as do mismatched methods, versions, components,
units, preferences, states or contexts. Equal descriptors are a necessary admission
condition, not proof of calibration or scientifically valid comparison. The caller
owns the meaning of any descriptor supplied or edited later; no immutable seal or
value-to-method certification is claimed.

Every successful ranking creates a new result and preserves the latest
`provenance['ranking_policy']` compatibility field. It also appends a versioned
`provenance['ranking_history']` entry, available as an independent snapshot through
`result.ranking_history`. Each recorded entry contains:

- `schema_version`, `evidence='recorded'`, and `origin='rank_by'` or `'backend'`;
- the selected score name, explicit direction and descriptor snapshot (or `null`);
- `input_order`: pose/state IDs, prior rank and selected numeric value;
- `output_order`: a permutation of indices into that recorded input order.

Positions disambiguate missing or repeated pose IDs within one ranking. They are
not global campaign identities. History uses scalar observations and indices,
with no coordinate copies. Its storage grows with the number of poses and ranking
decisions. New history is independently owned along with ranked metadata/context;
coordinate buffers retain the existing sharing behavior. Dictionary/JSON exports
remain detached snapshots of those coordinates as well.

When a legacy result has only a latest `ranking_policy`, the next ranking preserves
it as `evidence='legacy_policy_only'` with its original policy. Missing past score
values, ordering, method or units are not fabricated. A malformed history is rejected
at construction, reading, ranking and export rather than silently erased. This
validates record structure and finite values; it does not authenticate the history.

## Verification

`tests/test_score_semantics.py` protects admission, context/unit matching, legacy
behavior, repeated decisions, stable ties, independent evidence and non-default
unit policy. Its provider guards prohibit molecular operations and optional engine
or viewer imports on the offline path. The existing native Vina/Vinardo execution
test also checks actual descriptor context, initial order, repeated ranking and
result round trips. These are software-boundary checks, not redocking qualification.

On 2026-10-03, the local Python 3.13 gate passes 413 tests in 52.77 seconds with
the existing twelve provider warnings. Ruff lint/format, report indexes and diff
checks pass. All five notebook cells execute without errors. A one-sample legacy
export smoke retains the prior `small_mapped` payload SHA256
`920f10c557ec6e83c7f408c45550904c986cd1f8fb21e09ece835e3af81a3f7c`;
this confirms unchanged output, not a new timing comparison.
