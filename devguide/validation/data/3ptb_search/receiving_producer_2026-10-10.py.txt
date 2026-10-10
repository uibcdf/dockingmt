"""Receive immutable 3PTB searches and re-evaluate saved geometry without Vina.

Keep the original reporting failure visible. Correct only the optional-map
handling in the case-specific receiver; retain the registered RMSD criterion.
"""

from __future__ import annotations

import argparse
import gzip
import json
from copy import deepcopy
from pathlib import Path

import molsysmt as msm
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_3ptb_admission import ROOT, SOURCE_SHA, producer_identity, sha
from devtools.qualify_3ptb_search import OUTPUT as SEARCHES
from devtools.qualify_3ptb_search import baseline, evaluate, summarize, utc
from devtools.qualify_181l_receptor import save

OUTPUT = SEARCHES.with_name('evaluation_2026-10-10.json.gz')


def qualify(pdb, *, search_sha256, output):
    """Evaluate every returned saved pose; never execute preparation or searches."""
    output = Path(output)
    if output.exists():
        raise FileExistsError('Use a new receiving output; retain original evidence')
    payload = SEARCHES.read_bytes()
    if sha(payload) != search_sha256:
        raise ValueError('Search archive differs from the declared original producer')
    searches = json.loads(gzip.decompress(payload))
    original, registration = baseline()
    assert searches['status'] == 'population_attempted'
    assert searches['execution_registration'] == registration
    assert len(searches['runs']) == len(original['population']) == 24
    for relative, expected in searches['original_producer'][
        'consumer_source_sha256'
    ].items():
        if relative not in ('devtools/qualify_3ptb_search.py', 'dockingmt/_version.py'):
            assert sha((ROOT / relative).read_bytes()) == expected, relative
    if sha(Path(pdb).read_bytes()) != SOURCE_SHA:
        raise ValueError('Reference differs from the registered original PDB')
    source = msm.convert(Path(pdb), to_form='molsysmt.MolSys', get_missing_bonds=False)
    reference = msm.extract(source, selection="group_name=='BEN'", structure_indices=0)
    assert msm.get(reference, n_atoms=True) == 9
    identity = producer_identity()
    identity['consumer_driver_sha256'] = sha(Path(__file__).read_bytes())
    identity['consumer_source_sha256']['devtools/evaluate_3ptb_saved.py'] = identity[
        'consumer_driver_sha256'
    ]
    identity['consumer_source_sha256']['devtools/qualify_3ptb_search.py'] = sha(
        (ROOT / 'devtools/qualify_3ptb_search.py').read_bytes()
    )
    record = {
        'schema': 'dockingmt.3ptb_saved_evaluation@1',
        'created_utc': utc(),
        'search_archive_sha256': search_sha256,
        'receiving_producer': identity,
        'registered_criterion_changed': False,
        'new_searches_executed': 0,
        'fixed_evaluations_executed': 0,
        'original_execution_summary': searches['summary'],
        'runs': [],
    }
    for frozen, run in zip(original['population'], searches['runs'], strict=True):
        assert {k: run[k] for k in frozen if k != 'status'} == {
            k: frozen[k] for k in frozen if k != 'status'
        }
        received = {
            k: deepcopy(v)
            for k, v in run.items()
            if k not in ('result', 'evaluation', 'error')
        }
        received['original_status'] = run['status']
        received['original_error'] = run.get('error')
        if 'result' in run:
            result = dmt.DockingResult.from_dict(run['result'])
            dmt.verify_captured_inputs(result.provenance['backend_artifacts'])
            for role in ('receptor', 'partner'):
                assert (
                    result.provenance['backend_artifacts'][role]['sha256']
                    == frozen[f'{role}_pdbqt_sha256']
                )
            actual = result.provenance['backend_box']
            assert {k: actual[k] for k in frozen['backend_box']} == frozen[
                'backend_box'
            ]
            box = dmt.BoxRegion(
                puw.quantity(frozen['backend_box']['center'], 'angstrom'),
                puw.quantity(frozen['backend_box']['size'], 'angstrom'),
            )
            received['evaluation'] = evaluate(
                result, reference, box, original, run['arm']
            )
            received['status'] = 'evaluated'
        record['runs'].append(received)
    # Reuse scientific counters with raw results supplied only for denominators.
    counted = [
        dict(received, **({'result': run['result']} if 'result' in run else {}))
        for received, run in zip(record['runs'], searches['runs'], strict=True)
    ]
    record['summary'] = summarize(counted)
    record['finished_utc'] = utc()
    save(record, output)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdb', type=Path)
    parser.add_argument('--search-sha256', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    record = qualify(args.pdb, search_sha256=args.search_sha256, output=args.output)
    print(json.dumps(record['summary']))


if __name__ == '__main__':
    main()
