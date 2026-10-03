"""Check timing attribution and cleanup with a deterministic native stand-in."""

import importlib
import json
import sys
from types import SimpleNamespace

import pytest
import pyunitwizard as puw

from devtools.profile_workflow import _sample, _summarize
from dockingmt import BoxRegion, DockingProblem, VinaBackend, VinaProtocol
from dockingmt._private.smonitor import CapabilityMismatchError


@pytest.fixture
def timed_native(monkeypatch, tmp_path):
    from depdigest.core import checker

    available = checker.is_installed
    monkeypatch.setattr(
        checker,
        'is_installed',
        lambda name: True if name == 'vina' else available(name),
    )
    engine = importlib.import_module('dockingmt.engines.vina')
    clock = SimpleNamespace(now=0.0, calls=0, fail=False, paths=[])

    def read_clock():
        clock.calls += 1
        return clock.now

    class Native:
        def __init__(self, **kwargs):
            clock.now += 2

        def set_receptor(self, rigid_pdbqt_filename):
            clock.paths.append(rigid_pdbqt_filename)

        def set_ligand_from_file(self, path):
            clock.paths.append(path)

        def compute_vina_maps(self, **kwargs):
            clock.now += 3

        def dock(self, **kwargs):
            clock.now += 5
            if clock.fail:
                raise RuntimeError('native failure')

        def poses(self, **kwargs):
            clock.now += 7
            return []

        def energies(self, **kwargs):
            return []

        def info(self):
            return {'weights': [-0.035579], 'box_spacing': 0.375}

    monkeypatch.setitem(
        sys.modules, 'vina', SimpleNamespace(Vina=Native, __version__='test')
    )
    # Patch only the adapter's time reference; do not change SMonitor/provider clocks.
    monkeypatch.setattr(engine, 'time', SimpleNamespace(perf_counter=read_clock))
    receptor = tmp_path / 'receptor.pdbqt'
    partner = tmp_path / 'partner.pdbqt'
    receptor.write_text(
        'ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00     0.000 N\n'
    )
    partner.write_text('ROOT\nATOM placeholder ligand\nENDROOT\n')
    problem = DockingProblem(
        receptor=receptor,
        partner=partner,
        search_domain=BoxRegion(
            center=puw.quantity([0, 0, 0], 'angstrom'),
            size=puw.quantity([10, 10, 10], 'angstrom'),
        ),
    )
    return clock, problem


def test_phase_timings_attribute_native_cost_and_include_cleanup(timed_native):
    from pathlib import Path

    clock, problem = timed_native
    result = VinaBackend().dock(problem, VinaProtocol(collect_timings=True))
    timings = result.provenance['timings']
    assert timings['phases'] == {
        'validation': 0,
        'search_domain_projection': 0,
        'preparation': 0,
        'backend_import': 0,
        'input_projection': 0,
        'engine_setup': 2,
        'affinity_maps': 3,
        'native_docking': 5,
        'result_normalization': 7,
        'cleanup': 0,
    }
    assert timings['total'] == 17
    assert result.provenance['elapsed_seconds'] == 5
    assert clock.paths and all(not Path(path).exists() for path in clock.paths)


def test_disabled_profiling_only_reads_existing_native_clock(timed_native):
    clock, problem = timed_native
    result = VinaBackend().dock(problem)
    assert clock.calls == 2
    assert result.provenance['elapsed_seconds'] == 5
    assert 'timings' not in result.provenance


@pytest.mark.parametrize('enabled', [False, True])
def test_profiling_preserves_native_failure_and_cleanup(timed_native, enabled):
    from pathlib import Path

    clock, problem = timed_native
    clock.fail = True
    with pytest.raises(RuntimeError, match='native failure'):
        VinaBackend().dock(problem, VinaProtocol(collect_timings=enabled))
    assert clock.paths and all(not Path(path).exists() for path in clock.paths)


def test_report_keeps_phase_and_outer_measurements_separate_and_detects_mismatch():
    samples = []
    for enabled, elapsed in ((False, 20), (True, 21), (True, 25), (False, 22)):
        samples.append(
            {
                'collect_timings': enabled,
                'measurements': {'dock_call': elapsed, 'result_export': 1},
                'adapter_timings': {'phases': {'native_docking': 5, 'affinity_maps': 3}}
                if enabled
                else None,
                'scientific_sha256': 'same',
                'input_identity': {'source_sha256': 'same'},
                'environment': {'python': 'same'},
                'source_revision': {'code_sha256': 'same'},
                'profiler_sha256': 'same',
            }
        )
    report = _summarize(samples)
    assert report['scientific_outputs_match']
    assert report['input_identities_match']
    assert report['execution_contexts_match']
    assert report['measurement_medians']['enabled']['dock_call'] == 23
    assert report['measurement_medians']['disabled']['dock_call'] == 21
    assert report['dock_call_median_difference'] == 2
    assert report['adapter_phase_medians'] == {'native_docking': 5, 'affinity_maps': 3}
    samples[-1]['scientific_sha256'] = 'changed'
    samples[-1]['input_identity']['source_sha256'] = 'changed'
    samples[-1]['environment']['python'] = 'changed'
    report = _summarize(samples)
    assert not report['scientific_outputs_match']
    assert not report['input_identities_match']
    assert not report['execution_contexts_match']


def test_report_rejects_unpaired_samples():
    with pytest.raises(ValueError, match='Equal nonempty'):
        _summarize([])


@pytest.mark.parametrize('field', ['constraints', 'search_guidance'])
def test_captured_profile_preserves_unsupported_intent(timed_native, tmp_path, field):
    clock, problem = timed_native
    result = VinaBackend().dock(
        problem, VinaProtocol(seed=42, cpu=1, capture_backend_inputs=True)
    )
    record = result.to_dict()
    record['problem_info'][field] = [{'unsupported': 'intent'}]
    manifest = tmp_path / 'captured.json'
    manifest.write_text(json.dumps(record))
    paths_before = list(clock.paths)
    with pytest.raises(CapabilityMismatchError) as caught:
        _sample(True, manifest)
    assert caught.value.extra['capability'] == field
    assert clock.paths == paths_before


@pytest.mark.parametrize('role', ['receptor', 'partner'])
def test_captured_profile_rejects_tampered_bytes(timed_native, tmp_path, role):
    clock, problem = timed_native
    result = VinaBackend().dock(
        problem, VinaProtocol(seed=42, cpu=1, capture_backend_inputs=True)
    )
    record = result.to_dict()
    record['provenance']['backend_artifacts'][role]['content_base64'] = 'dGFtcGVyZWQ='
    manifest = tmp_path / 'captured.json'
    manifest.write_text(json.dumps(record))
    paths_before = list(clock.paths)
    with pytest.raises(ValueError, match='SHA-256'):
        _sample(True, manifest)
    assert clock.paths == paths_before
