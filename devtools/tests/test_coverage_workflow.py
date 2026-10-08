"""Protect meaningful measurement and trusted, failed-test-safe report publication."""

import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


class TestCoverageWorkflow(unittest.TestCase):
    def workflow(self):
        return yaml.load(
            (ROOT / '.github/workflows/ci.yml').read_text(), Loader=yaml.BaseLoader
        )

    def test_measurement_keeps_the_existing_unfiltered_suite_and_minor_matrix(self):
        job = self.workflow()['jobs']['test']
        self.assertEqual(
            job['strategy']['matrix']['python-version'],
            ['3.11', '3.12', '3.13', '3.14'],
        )
        step = next(
            s for s in job['steps'] if s.get('name') == 'Run tests with pytest-receptor'
        )
        self.assertEqual(step['run'], 'pytest --receptor=ci')
        self.assertNotIn('continue-on-error', step)
        options = step['env']['PYTEST_ADDOPTS']
        self.assertIn("matrix.python-version == '3.14'", options)
        self.assertIn('--cov=dockingmt', options)
        self.assertIn('--cov=molsysviewer_dockingmt', options)
        self.assertIn('--cov-branch', options)
        self.assertIn('--cov-report=xml:coverage.xml', options)
        for filter_option in ('--ignore', '--deselect', ' -k ', ' -m '):
            self.assertNotIn(filter_option, options)

    def test_retained_xml_survives_test_failure_and_has_attempt_identity(self):
        job = self.workflow()['jobs']['test']
        retain = next(
            s
            for s in job['steps']
            if s.get('name') == 'Retain measured Python coverage'
        )
        self.assertIn('!cancelled()', retain['if'])
        self.assertIn("matrix.python-version == '3.14'", retain['if'])
        self.assertNotIn('success()', retain['if'])
        self.assertEqual(retain['with']['path'], 'coverage.xml')
        self.assertEqual(retain['with']['if-no-files-found'], 'error')
        self.assertIn('github.run_id', retain['with']['name'])
        self.assertIn('github.run_attempt', retain['with']['name'])
        names = [s.get('name') for s in job['steps']]
        self.assertGreater(
            names.index('Retain measured Python coverage'),
            names.index('Run tests with pytest-receptor'),
        )

    def test_publication_is_automatic_trusted_main_and_keeps_credentials_out_of_tests(
        self,
    ):
        workflow = self.workflow()
        self.assertEqual(workflow['permissions'], {'contents': 'read'})
        self.assertNotIn('permissions', workflow['jobs']['test'])
        publisher = workflow['jobs']['coverage-upload']
        self.assertEqual(publisher['needs'], 'test')
        self.assertIn('always()', publisher['if'])
        self.assertIn('!cancelled()', publisher['if'])
        self.assertIn("github.event_name != 'pull_request'", publisher['if'])
        self.assertIn("github.ref == 'refs/heads/main'", publisher['if'])
        self.assertEqual(
            publisher['permissions'], {'contents': 'read', 'id-token': 'write'}
        )
        self.assertNotIn('secrets.', str(workflow['jobs']['test']))
        self.assertNotIn('secrets.', str(publisher))

    def test_publisher_uses_only_the_retained_file_and_exact_source(self):
        publisher = self.workflow()['jobs']['coverage-upload']
        download = next(
            s
            for s in publisher['steps']
            if s.get('uses', '').startswith('actions/download-artifact@')
        )
        self.assertIn('github.run_id', download['with']['name'])
        self.assertIn('github.run_attempt', download['with']['name'])
        upload = publisher['steps'][-1]
        self.assertRegex(upload['uses'], r'^codecov/codecov-action@[a-f0-9]{40}$')
        self.assertEqual(upload['with']['use_oidc'], 'true')
        self.assertEqual(upload['with']['disable_search'], 'true')
        self.assertEqual(upload['with']['fail_ci_if_error'], 'true')
        self.assertEqual(upload['with']['files'], 'coverage-report/coverage.xml')
        self.assertEqual(upload['with']['override_commit'], '${{ github.sha }}')
        self.assertEqual(upload['with']['override_branch'], 'main')
