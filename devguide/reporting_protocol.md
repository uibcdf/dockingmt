# Reporting protocol

This repository implements the common issue-backed lifecycle defined by
`uibcdf/molsyssuite` in its `devguide/reporting_protocol.md`.

## Identity and ownership

Component-local work uses `uibcdf/dockingmt#<number>`. Suite-wide rules and coordinated
changes use `uibcdf/molsyssuite`. Open the owning issue before creating a queued record.
Every queued document has an issue, although an incoming issue may await triage without
a document.

## Local paths

- `pending_bugs/`: open defects;
- `pending_proposals/`: open proposals;
- `archive/`: all resolved, withdrawn and superseded records.

Every report starts from `templates/report.md`. The issue holds public state; the
document holds analysis, measurements, alternatives and refuted paths.

## Closing

Set a closed status and date, name a durable test in `guard` or policy in `normative`,
move the record to `archive/`, regenerate indexes and close the issue with the outcome
and archived path. Archive, never delete. Append corrections to archived records rather
than rewriting their history.

## Offline checks

```bash
python devtools/devguide_index.py
python devtools/devguide_index.py --check
python -m pytest tests/test_reporting_protocol.py
```
