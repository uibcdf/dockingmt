"""Exercise actual shared controls against DockingMT declaration regressions."""

import hashlib
import io
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import unittest
from pathlib import Path

import yaml
from setuptools import find_namespace_packages

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'devtools'))
from check_dependency_routes import SDK_SHA, load_sdk  # noqa: E402

PLAN = 'devtools/conda-build/release_plan.example.toml'
RESOURCES = 'devtools/conda-build/resources.toml'


class TestDistributionContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.routes = load_sdk()
        cls.noarch = load_sdk('noarch_conda')
        cls.publication = load_sdk('conda_release_contract')
        cls.installed = load_sdk('installed_noarch')

    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='dockingmt-controls-')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for name in (
            'pyproject.toml',
            '.github',
            'devtools/conda-build',
            'devtools/conda-envs',
            'devtools/dependency_routes.toml',
            'dockingmt',
            'molsysviewer_dockingmt',
        ):
            source, target = ROOT / name, self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(
                    source, target, ignore=shutil.ignore_patterns('__pycache__')
                )
            else:
                shutil.copy2(source, target)
        self.plan, self.inventory = self.noarch.inspect_recipe(
            self.root, PLAN, RESOURCES
        )

    def mutate(self, path, old, new):
        p = self.root / path
        self.assertIn(old, p.read_text())
        p.write_text(p.read_text().replace(old, new))

    def payload(self):
        entries = {
            p: b'# synthetic administrative payload\n'
            for p in self.inventory['required_paths']
        }
        entries[self.inventory['version_file']] = b'__version__ = "0.0.0"\n'
        entries['info/index.json'] = json.dumps(
            {
                'name': 'dockingmt',
                'version': '0.0.0',
                'build': 'py_0',
                'build_number': 0,
                'subdir': 'noarch',
                'depends': self.inventory['expected_run'],
            }
        ).encode()
        entries['info/link.json'] = b'{"noarch": {"type": "python"}}'
        entries['site-packages/dockingmt-0.0.0.dist-info/METADATA'] = (
            b'Name: dockingmt\nVersion: 0.0.0\n'
        )
        return entries

    def validate(self, entries):
        path = self.root / 'dockingmt-0.0.0-py_0.tar.bz2'
        with tarfile.open(path, 'w:bz2') as archive:
            for name, content in entries.items():
                member = tarfile.TarInfo(name)
                member.size = len(content)
                archive.addfile(member, io.BytesIO(content))
        return self.noarch.inspect_artifact(path, self.plan, self.inventory)

    def test_complete_core_addon_and_generated_version_inventory(self):
        expected = {
            'site-packages/' + str(p.relative_to(self.root))
            for package in ('dockingmt', 'molsysviewer_dockingmt')
            for p in (self.root / package).rglob('*')
            if p.is_file()
        }
        expected.add(self.inventory['version_file'])
        self.assertEqual(set(self.inventory['required_paths']), expected)
        self.validate(self.payload())

    def test_missing_addon_typing_and_core_files_fail(self):
        for p in (
            'molsysviewer_dockingmt/addon.py',
            'dockingmt/py.typed',
            'dockingmt/__init__.py',
        ):
            entries = self.payload()
            del entries['site-packages/' + p]
            with self.subTest(path=p), self.assertRaises(ValueError):
                self.validate(entries)

    def test_stale_embedded_and_distribution_versions_fail(self):
        for p in (
            self.inventory['version_file'],
            'site-packages/dockingmt-0.0.0.dist-info/METADATA',
        ):
            entries = self.payload()
            entries[p] = entries[p].replace(b'0.0.0', b'0.0.1')
            with self.subTest(path=p), self.assertRaises(ValueError):
                self.validate(entries)

    def test_missing_source_resource_and_wrong_generated_target_fail(self):
        (self.root / 'dockingmt/py.typed').unlink()
        with self.assertRaises(ValueError):
            self.noarch.inspect_resources(self.root, RESOURCES)
        (self.root / 'dockingmt/py.typed').touch()
        self.mutate(
            'pyproject.toml',
            'file = "dockingmt/_version.py"',
            'file = "dockingmt/wrong.py"',
        )
        with self.assertRaises(ValueError):
            self.noarch.inspect_resources(self.root, RESOURCES)

    def test_missing_recipe_dependency_and_weaker_python_floor_fail(self):
        p = self.root / 'devtools/conda-build/meta.yaml'
        original = p.read_text()
        for text in (
            original.replace('    - numpy\n', ''),
            original.replace('python >=3.11,<3.15', 'python >=3.10,<3.15'),
        ):
            p.write_text(text)
            with self.assertRaises(ValueError):
                self.noarch.inspect_recipe(self.root, PLAN, RESOURCES)

    def test_optional_features_stay_outside_core_runtime(self):
        project = tomllib.loads((self.root / 'pyproject.toml').read_text())['project']
        self.assertEqual(project['optional-dependencies']['vina'], ['vina'])
        self.assertEqual(project['optional-dependencies']['viewer'], ['molsysviewer'])
        self.assertEqual(
            set(self.inventory['expected_run']),
            {
                'python>=3.11,<3.15',
                'argdigest',
                'depdigest',
                'molsysmt',
                'numpy',
                'pyunitwizard',
                'smonitor',
            },
        )
        self.assertEqual(
            self.installed.test_dependencies(self.plan, self.inventory)[-3:],
            ['vina==1.2.7', 'rdkit==2026.03.1', 'openmm==8.6.1'],
        )

    def test_namespace_discovery_excludes_sdk_and_tests(self):
        (self.root / '.molsyssuite/sdk/devtools').mkdir(parents=True)
        packages = find_namespace_packages(
            where=str(self.root), include=['dockingmt*', 'molsysviewer_dockingmt*']
        )
        self.assertIn('molsysviewer_dockingmt', packages)
        self.assertTrue(
            all(
                p.split('.')[0] in {'dockingmt', 'molsysviewer_dockingmt'}
                for p in packages
            )
        )

    def test_offline_routes_and_publication_controls_do_not_claim_installation(self):
        def absent(name):
            raise AssertionError('Declaration-only must not read installed science')

        result = self.routes.audit(self.root, distribution_for=absent)
        self.assertEqual(len(result['routes']), 9)
        self.assertEqual(len(result['contexts']), 4)
        self.assertEqual(result['qualification'], 'declared-only')
        self.assertTrue(result['installed_check_required'])
        self.assertNotIn('installed_sources', result)
        self.assertEqual(self.publication.workflow_findings(self.root), [])

    def test_new_runtime_route_and_changed_workflow_fail(self):
        p = self.root / 'devtools/conda-envs/unreviewed.yaml'
        p.write_text('dependencies: [python]\n')
        with self.assertRaises(ValueError):
            self.routes.audit(self.root)
        p.unlink()
        p = self.root / '.github/workflows/ci.yml'
        p.write_text(p.read_text() + '\n# altered route\n')
        with self.assertRaises(ValueError):
            self.routes.audit(self.root)

    def test_changed_public_floor_and_missing_non_source_dependency_fail(self):
        p = self.root / 'pyproject.toml'
        original = p.read_text()
        self.mutate('pyproject.toml', '"depdigest",', '"depdigest>=999",')
        with self.assertRaises(ValueError):
            self.routes.audit(self.root)
        p.write_text(original)
        self.mutate('devtools/conda-envs/test_env.yaml', '  - numpy\n', '')
        with self.assertRaises(ValueError):
            self.routes.audit(self.root)

    def check_source_bindings(self):
        inventory = tomllib.loads(
            (self.root / 'devtools/dependency_routes.toml').read_text()
        )
        sources = {s['id']: s for s in inventory['source_routes']}
        for workflow, key in (('ci.yml', 'test'), ('full-matrix.yml', 'full-test')):
            job = yaml.safe_load(
                (self.root / '.github/workflows' / workflow).read_text()
            )['jobs'][key]
            clones = [
                s
                for s in job['steps']
                if s.get('with', {}).get('repository')
                in {'uibcdf/argdigest', 'uibcdf/molsysmt', 'uibcdf/molsysviewer'}
            ]
            for context in inventory['contexts']:
                condition = (
                    "matrix.python-version == '3.14'"
                    if context['python_minor'] == '3.14'
                    else "matrix.python-version != '3.14'"
                )
                observed = {
                    s['with']['repository'].split('/')[1]: s['with']['ref']
                    for s in clones
                    if s['if'] == condition
                }
                expected = {
                    sources[id]['name']: sources[id]['commit']
                    for id in context['sources']
                }
                self.assertEqual(observed, expected)
                self.assertEqual(context['overlays'], [])
                self.assertTrue(
                    all(
                        sources[id]['install'] == 'pip-no-deps-directory'
                        for id in context['sources']
                    )
                )
        self.assertNotEqual(
            sources['viewer-base']['commit'], sources['viewer-py314']['commit']
        )
        self.assertEqual(sources['viewer-base']['role'], 'integration')

    def test_directory_context_bindings_preserve_lane_specific_sources(self):
        self.check_source_bindings()

    def test_pin_drift_is_detected_even_after_refreshing_the_workflow_hash(self):
        p = self.root / '.github/workflows/ci.yml'
        original = p.read_text()
        p.write_text(
            original.replace('1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e', 'b' * 40)
        )
        digest = hashlib.sha256(original.encode()).hexdigest()
        self.mutate(
            'devtools/dependency_routes.toml',
            digest,
            hashlib.sha256(p.read_bytes()).hexdigest(),
        )
        # The shared parser intentionally does not interpret arbitrary shell routes.
        with self.assertRaises(AssertionError):
            self.check_source_bindings()

    def test_installed_preflight_precedes_unchanged_scientific_steps(self):
        for workflow, key in (('ci.yml', 'test'), ('full-matrix.yml', 'full-test')):
            steps = yaml.safe_load(
                (self.root / '.github/workflows' / workflow).read_text()
            )['jobs'][key]['steps']
            names = {s.get('name'): i for i, s in enumerate(steps)}
            check = names['Check dependency routes and installed clone context']
            self.assertLess(names['Install dockingmt'], check)
            self.assertLess(check, names['Run tests with pytest-receptor'])
            install = steps[names['Install compatible scientific sibling sources']][
                'run'
            ]
            self.assertIn('--no-deps', install)
            self.assertNotIn('git+', install)
            self.assertEqual(
                steps[names['Run tests with pytest-receptor']]['run'],
                'pytest --receptor=ci',
            )
            self.assertEqual(
                steps[names['Check out immutable dependency SDK']]['with']['ref'],
                SDK_SHA,
            )

    def test_example_requires_all_fourteen_candidate_jobs(self):
        jobs = self.plan['gate_jobs']
        self.assertEqual(sum(len(v) for v in jobs.values()), 14)
        for minor in ('3.11', '3.12', '3.13', '3.14'):
            for workflow, prefix in (
                ('ci.yml', 'Test'),
                ('full-matrix.yml', 'Full test'),
            ):
                self.assertIn(
                    'Run tests with pytest-receptor',
                    jobs['.github/workflows/' + workflow][
                        prefix + ' on ubuntu-latest, Python ' + minor
                    ],
                )
        for minor in ('3.13', '3.14'):
            self.assertIn(
                'Run tests with pytest-receptor',
                jobs['.github/workflows/full-matrix.yml'][
                    'Full test on macos-15, Python ' + minor
                ],
            )
        self.assertFalse((ROOT / 'devtools/conda-build/release_plan.toml').exists())

    def test_all_eight_installed_cells_require_science_and_final_provenance(self):
        gate = self.inventory['installed_gate']
        self.assertEqual(gate['platforms'], ['linux-64', 'osx-arm64'])
        self.assertEqual(gate['python_versions'], ['3.11', '3.12', '3.13', '3.14'])
        self.assertEqual(
            gate['required_steps'],
            [
                'Install exact artifact',
                'Validate installed files',
                'Run installed tests',
                'Recheck dependency provenance after installed tests',
            ],
        )
        self.assertEqual(self.inventory['installed_tests']['paths'], ['tests'])
        self.assertEqual(set(gate['platforms']), set(self.plan['test_platforms']))
        self.assertEqual(
            set(gate['python_versions']), set(self.plan['python_versions'])
        )

    def test_wrappers_pin_sdk_and_keep_qualification_separate_from_producer(self):
        for name in (
            'build_and_upload_conda_packages.yaml',
            'promote_conda_package.yaml',
            'test_installed_conda_package.yaml',
            'conda_publication_governance.yaml',
        ):
            data = yaml.safe_load((self.root / '.github/workflows' / name).read_text())
            self.assertTrue(
                all(
                    j['uses'].endswith('@2d32048457c6d37093ae509f5626d00a5cda121b')
                    for j in data['jobs'].values()
                )
            )
            if name.startswith('promote'):
                values = data['jobs']['promote']['with']
                for key in ('candidate_sha', 'qualification_sha', 'sha256'):
                    self.assertEqual(values[key], '${{ inputs.' + key + ' }}')

    def test_installed_selection_excludes_source_pythonpath_for_addon_imports(self):
        fixture = self.root / 'receiving-fixture'
        prefix = self.root / 'installed-prefix'
        tests = fixture / 'tests'
        tests.mkdir(parents=True)
        prefix.mkdir()
        (fixture / 'pyproject.toml').write_text(
            '[tool.pytest.ini_options]\npythonpath = ["."]\n'
        )
        for directory, value in ((fixture, 'source'), (prefix, 'installed')):
            (directory / 'candidate.py').write_text("value = '" + value + "'\n")
            (directory / 'addon.py').write_text("value = '" + value + "'\n")
        (tests / 'test_origin.py').write_text(
            "def test_origin():\n    import addon\n    assert addon.value == 'installed'\n"
        )
        sdk = Path(self.installed.__file__).resolve().parents[2]
        command = "import json,sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); from devtools.scripts.installed_noarch import run_tests; sys.prefix=sys.argv[2]; sys.path.insert(0,sys.prefix); __import__('candidate'); raise SystemExit(run_tests(Path(sys.argv[3]),json.loads(sys.argv[4])))"
        for args, expected in (
            ([], 1),
            (self.inventory['installed_tests']['pytest_args'], 0),
        ):
            data = {
                'import_name': 'candidate',
                'installed_tests': {'paths': ['tests'], 'pytest_args': args},
            }
            result = subprocess.run(
                [
                    sys.executable,
                    '-P',
                    '-c',
                    command,
                    str(sdk),
                    str(prefix),
                    str(fixture),
                    json.dumps(data),
                ],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_adapter_declared_cli_is_owner_anchored_outside_the_clone(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / 'devtools/check_dependency_routes.py'),
                '--declared-only',
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['qualification'], 'declared-only')


if __name__ == '__main__':
    unittest.main()
