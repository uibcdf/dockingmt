"""Current CI and frozen scientific receivers retain distinct source contracts."""

import tomllib
from pathlib import Path

import pytest
import yaml
from packaging.requirements import Requirement
from packaging.version import Version

ROOT = Path(__file__).resolve().parents[2]
CURRENT = {
    'argdigest': '07126411f108ee1ff607e9c9a0816109b2c9253e',
    'molsysmt': 'efbe67e1c6042078144bce1db24aa80bb565dbd2',
    'molsysviewer': '1187fc187247aa2d20d01791856a541d50562bcb',
}
FROZEN = {
    'argdigest': '3d1ec53c374098016452abab74706e9d80df5462',
    'molsysmt': '00abb958fb93649131d5ce5fe5e12e90cf4900e9',
    'molsysviewer': '78ede79e2e345593db5bfe80d246d3f6c70bd005',
}


def inventory():
    data = tomllib.loads((ROOT / 'devtools/dependency_routes.toml').read_text())
    return data, {row['id']: row for row in data['source_routes']}


@pytest.mark.parametrize('minor', ['3.11', '3.12', '3.13', '3.14'])
def test_current_ci_selects_the_received_source_cohort(minor):
    data, routes = inventory()
    context = next(row for row in data['contexts'] if row['name'] == 'ci-' + minor)
    observed = {
        routes[key]['name']: routes[key]['commit'] for key in context['sources']
    }
    assert observed == CURRENT
    assert context['overlays'] == []


@pytest.mark.parametrize(
    'workflow,job_name', [('ci.yml', 'test'), ('full-matrix.yml', 'full-test')]
)
def test_ordinary_workflows_bind_current_sources_for_both_minor_branches(
    workflow, job_name
):
    job = yaml.safe_load((ROOT / '.github/workflows' / workflow).read_text())['jobs'][
        job_name
    ]
    for condition in [
        "matrix.python-version == '3.14'",
        "matrix.python-version != '3.14'",
    ]:
        observed = {
            step['with']['repository'].split('/')[1]: step['with']['ref']
            for step in job['steps']
            if step.get('if') == condition
            and step.get('with', {}).get('repository')
            in {'uibcdf/' + name for name in CURRENT}
        }
        assert observed == CURRENT
    assert job['strategy']['matrix']['python-version'] == [
        '3.11',
        '3.12',
        '3.13',
        '3.14',
    ]


def test_frozen_e4_context_and_actual_checkout_bindings_stay_historical():
    data, routes = inventory()
    context = next(row for row in data['contexts'] if row['name'] == 'e4-3.14')
    assert {
        routes[key]['name']: routes[key]['commit'] for key in context['sources']
    } == FROZEN
    assert context['environment'] == 'devtools/conda-envs/e4_env.yaml'
    assert context['overlays'] == []
    job = yaml.safe_load(
        (ROOT / '.github/workflows/qualify-3ptb-interactions.yml').read_text()
    )['jobs']['receive']
    observed = {
        step['with']['repository'].split('/')[1]: step['with']['ref']
        for step in job['steps']
        if step.get('with', {}).get('repository')
        in {'uibcdf/' + name for name in FROZEN}
    }
    assert observed == FROZEN
    preflight = next(
        step['run']
        for step in job['steps']
        if step.get('name')
        == 'Verify existing source routes and installed bounds before computation'
    )
    for key in context['sources']:
        assert '--source-root ' + key + '=' in preflight
    assert all(
        key
        not in next(row for row in data['contexts'] if row['name'] == 'ci-3.14')[
            'sources'
        ]
        for key in context['sources']
    )


@pytest.mark.parametrize(
    'name,minimum',
    [
        ('h5py', '3.11.0'),
        ('pandas', '2.2.2'),
        ('jinja2', '3.1.2'),
        ('networkx', '3.3'),
        ('tqdm', '4.65.0'),
        ('matplotlib', '3.8.4'),
    ],
)
def test_current_bootstrap_declares_the_received_provider_requirements(name, minimum):
    environment = yaml.safe_load(
        (ROOT / 'devtools/conda-envs/test_env.yaml').read_text()
    )
    requirements = {
        req.name.lower(): req
        for item in environment['dependencies']
        if isinstance(item, str)
        for req in [Requirement(item)]
    }
    assert name in requirements
    specifier = requirements[name].specifier
    assert Version(minimum) in specifier
    assert any(
        item.operator in ('>=', '>') and Version(item.version) >= Version(minimum)
        for item in specifier
    )


def test_fixed_source_candidate_stays_on_its_original_checkout_sources():
    document = yaml.safe_load(
        (ROOT / '.github/workflows/qualify-source-0.1.0.yml').read_text()
    )
    checkouts = [
        step['with']
        for job in document['jobs'].values()
        for step in job['steps']
        if step.get('with', {}).get('repository')
        in {'uibcdf/' + name for name in FROZEN}
    ]
    assert {
        item['repository'].split('/')[1]: item['ref'] for item in checkouts
    } == FROZEN
