import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_shared_governance_surfaces_are_present():
    for filename in (
        'MOLSYSSUITE_GUIDE.md',
        'SMONITOR_GUIDE.md',
        'DEPDIGEST_GUIDE.md',
        'ARGDIGEST_GUIDE.md',
        'PYUNITWIZARD_GUIDE.md',
        'GH_RUN_RECEPTOR_GUIDE.md',
    ):
        assert (ROOT / filename).is_file()

    policy = ROOT / '.github/workflows/molsyssuite-policy.yml'
    assert policy.is_file()
    assert (
        'uibcdf/molsyssuite/.github/workflows/'
        'check-python-repository.yaml@policy-v1.4.6'
    ) in policy.read_text(encoding='utf-8')


def test_ci_covers_supported_lanes_and_common_quality_gates():
    workflow = (ROOT / '.github/workflows/ci.yml').read_text(encoding='utf-8')
    assert 'python-version: ["3.11", "3.12", "3.13"]' in workflow
    assert 'repository: uibcdf/argdigest' in workflow
    assert 'ref: "4fdbf19d386bbf476455d35c9988bf00624873e1"' in workflow
    assert 'repository: uibcdf/molsysmt' in workflow
    assert 'ref: "284038cfc39074e077814f7524417e8cb53af209"' in workflow
    assert 'repository: uibcdf/molsysviewer' in workflow
    assert 'ref: "2c022507265c744d532f39df345322074f80a2a3"' in workflow
    assert '.molsyssuite/argdigest' in workflow
    assert '.molsyssuite/molsysmt' in workflow
    assert '.molsyssuite/molsysviewer' in workflow
    assert 'ruff check .' in workflow
    assert 'ruff format --check .' in workflow
    assert 'pytest --receptor=ci' in workflow


def test_project_declares_the_suite_python_support_range():
    project = tomllib.loads((ROOT / 'pyproject.toml').read_text(encoding='utf-8'))[
        'project'
    ]
    assert project['requires-python'] == '>=3.11,<3.14'


def test_readme_routes_contributors_to_suite_governance():
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    assert 'MOLSYSSUITE_GUIDE.md' in readme
    assert 'MolSysSuite: Scientific Component' in readme
