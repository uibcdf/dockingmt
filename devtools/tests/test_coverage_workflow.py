"""Protect meaningful measurement and trusted, failed-test-safe report publication."""

import copy
import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_workflow():
    return yaml.load(
        (ROOT / '.github/workflows/ci.yml').read_text(), Loader=yaml.BaseLoader
    )


class TestCoverageWorkflow(unittest.TestCase):
    def test_measurement_keeps_the_existing_unfiltered_suite_and_minor_matrix(self):
        job = load_workflow()['jobs']['test']
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
        job = load_workflow()['jobs']['test']
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
        workflow = load_workflow()
        self.assertEqual(workflow['permissions'], {'contents': 'read'})
        self.assertNotIn('permissions', workflow['jobs']['test'])
        publisher = workflow['jobs']['coverage-upload']
        self.assertEqual(publisher['needs'], 'test')
        self.assertIn('always()', publisher['if'])
        self.assertIn('!cancelled()', publisher['if'])
        self.assertIn("github.event_name != 'pull_request'", publisher['if'])
        self.assertIn("github.ref == 'refs/heads/main'", publisher['if'])
        self.assertEqual(
            publisher['permissions'],
            {'contents': 'read', 'actions': 'read', 'id-token': 'write'},
        )
        self.assertNotIn('secrets.', str(workflow['jobs']['test']))
        self.assertNotIn('secrets.', str(publisher))

    def test_publisher_uses_only_the_retained_file_and_exact_source(self):
        publisher = load_workflow()['jobs']['coverage-upload']
        download = next(
            s
            for s in publisher['steps']
            if s.get('uses', '').startswith('actions/download-artifact@')
        )
        self.assertEqual(
            download['with']['artifact-ids'],
            '${{ steps.coverage-report.outputs.artifact-id }}',
        )
        self.assertEqual(download['with']['run-id'], '${{ github.run_id }}')
        self.assertEqual(download['with']['github-token'], '${{ github.token }}')
        self.assertEqual(download['with']['merge-multiple'], 'true')
        self.assertEqual(download['with']['path'], 'coverage-report')
        self.assertNotIn('name', download['with'])
        self.assertNotIn('pattern', download['with'])
        names = [s.get('name') for s in publisher['steps']]
        self.assertLess(
            names.index('Bind the measured Python report'),
            names.index('Download the measured Python report'),
        )
        tools = load_workflow()['jobs']['distribution']['steps']
        self.assertTrue(
            any(
                s.get('uses', '').startswith('actions/setup-node@')
                and s['with']['node-version'] == '26'
                for s in tools
            )
        )
        upload = publisher['steps'][-1]
        self.assertRegex(upload['uses'], r'^codecov/codecov-action@[a-f0-9]{40}$')
        self.assertEqual(upload['with']['use_oidc'], 'true')
        self.assertEqual(upload['with']['disable_search'], 'true')
        self.assertEqual(upload['with']['fail_ci_if_error'], 'true')
        self.assertEqual(upload['with']['files'], 'coverage-report/coverage.xml')
        self.assertEqual(upload['with']['override_commit'], '${{ github.sha }}')
        self.assertEqual(upload['with']['override_branch'], 'main')


class TestCoverageBinding(unittest.TestCase):
    """Execute the actual publisher script; official actions own API pagination/download."""

    def setUp(self):
        self.evidence = json.loads(
            (
                ROOT / 'devtools/tests/data/coverage_partial_rerun_20261105.json'
            ).read_text()
        )

    def binding(self, evidence=None):
        step = next(
            s
            for s in load_workflow()['jobs']['coverage-upload']['steps']
            if s.get('id') == 'coverage-report'
        )
        self.assertRegex(step['uses'], r'^actions/github-script@[a-f0-9]{40}$')
        self.assertEqual(
            step['env']['COVERAGE_PUBLISHER_ATTEMPT'], '${{ github.run_attempt }}'
        )
        self.assertNotIn('${{', step['with']['script'])
        payload = {
            **(evidence or self.evidence),
            'script': step['with']['script'],
        }
        harness = r"""
const fs = require('node:fs');
const data = JSON.parse(fs.readFileSync(0, 'utf8'));
const calls = [], outputs = {}, messages = [];
process.env.COVERAGE_PUBLISHER_ATTEMPT = String(data.publisher_attempt);
const github = {
  rest: {actions: {listJobsForWorkflowRun: 'jobs', listWorkflowRunArtifacts: 'artifacts'}},
  async paginate(route, parameters) {calls.push({route, parameters}); return data[route];}
};
const core = {info: value => messages.push(value), setOutput: (key, value) => outputs[key] = value};
const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
(async () => {
  try {
    await new AsyncFunction('github', 'context', 'core', data.script)(github, data.context, core);
    process.stdout.write(JSON.stringify({outputs, calls, messages}));
  } catch (error) {
    process.stdout.write(JSON.stringify({error: error.message, outputs, calls}));
  }
})();
"""
        node = shutil.which('node')
        self.assertIsNotNone(node, 'The administrative workflow declares Node 26')
        result = subprocess.run(
            [node, '-e', harness],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=15,
            env={**os.environ, 'NODE_OPTIONS': ''},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_partial_rerun_uses_original_artifact_despite_relabelled_job_attempt(self):
        received = self.binding()
        self.assertNotIn('error', received)
        self.assertEqual(
            received['outputs'],
            {'artifact-id': '13431816891', 'producer-attempt': '1'},
        )
        for call in received['calls']:
            self.assertEqual(call['parameters']['run_id'], 42059033330)
            self.assertEqual(call['parameters']['per_page'], 100)
            self.assertEqual(call['parameters']['owner'], 'uibcdf')
            self.assertEqual(call['parameters']['repo'], 'dockingmt')
        self.assertEqual(received['calls'][0]['parameters']['filter'], 'latest')
        message = json.loads(received['messages'][0])
        self.assertEqual(message['producer_attempt'], 1)
        self.assertEqual(message['publisher_attempt'], 2)

    def new_producer(self):
        evidence = copy.deepcopy(self.evidence)
        steps = evidence['jobs'][0]['steps']
        steps[0].update(
            started_at='2026-11-05T16:07:00Z', completed_at='2026-11-05T16:10:00Z'
        )
        steps[1].update(
            started_at='2026-11-05T16:10:00Z', completed_at='2026-11-05T16:10:10Z'
        )
        return evidence

    def test_full_rerun_uses_new_measurement_with_old_artifact_still_present(self):
        evidence = self.new_producer()
        new = copy.deepcopy(evidence['artifacts'][0])
        new.update(
            id=13431816892,
            name='dockingmt-python-coverage-42059033330-2',
            created_at='2026-11-05T16:10:05Z',
        )
        evidence['artifacts'].append(new)
        received = self.binding(evidence)
        self.assertEqual(
            received.get('outputs'),
            {'artifact-id': '13431816892', 'producer-attempt': '2'},
        )

    def test_failed_tests_still_publish_their_successfully_retained_measurement(self):
        evidence = copy.deepcopy(self.evidence)
        evidence['jobs'][0]['conclusion'] = 'failure'
        evidence['jobs'][0]['steps'][0]['conclusion'] = 'failure'
        self.assertEqual(self.binding(evidence)['outputs']['producer-attempt'], '1')

    def test_new_measurement_without_artifact_does_not_fall_back_to_old_coverage(self):
        received = self.binding(self.new_producer())
        self.assertIn('error', received)
        self.assertEqual(received['outputs'], {})

    def test_uncertain_or_unrelated_evidence_is_rejected(self):
        for damage in (
            'missing_job',
            'duplicate_job',
            'wrong_job_run',
            'wrong_job_source',
            'active_job',
            'missing_tests',
            'skipped_tests',
            'failed_retention',
            'missing_retention',
            'duplicate_retention',
            'bad_timing',
            'no_artifact',
            'duplicate_artifact',
            'expired',
            'wrong_artifact_run',
            'wrong_artifact_source',
            'bad_attempt',
            'future_attempt',
            'bad_artifact_id',
            'missing_created_at',
            'reversed_steps',
        ):
            with self.subTest(damage=damage):
                evidence = copy.deepcopy(self.evidence)
                job, artifact = evidence['jobs'][0], evidence['artifacts'][0]
                if damage == 'missing_job':
                    evidence['jobs'] = []
                elif damage == 'duplicate_job':
                    evidence['jobs'].append(copy.deepcopy(job))
                elif damage == 'wrong_job_run':
                    job['run_id'] += 1
                elif damage == 'wrong_job_source':
                    job['head_sha'] = '0' * 40
                elif damage == 'active_job':
                    job['status'] = 'in_progress'
                elif damage == 'missing_tests':
                    job['steps'].pop(0)
                elif damage == 'skipped_tests':
                    job['steps'][0]['conclusion'] = 'skipped'
                elif damage == 'failed_retention':
                    job['steps'][1]['conclusion'] = 'failure'
                elif damage == 'missing_retention':
                    job['steps'].pop()
                elif damage == 'duplicate_retention':
                    job['steps'].append(copy.deepcopy(job['steps'][1]))
                elif damage == 'bad_timing':
                    job['steps'][1]['completed_at'] = None
                elif damage == 'no_artifact':
                    evidence['artifacts'] = []
                elif damage == 'duplicate_artifact':
                    evidence['artifacts'].append(copy.deepcopy(artifact))
                elif damage == 'expired':
                    artifact['expired'] = True
                elif damage == 'wrong_artifact_run':
                    artifact['workflow_run']['id'] += 1
                elif damage == 'wrong_artifact_source':
                    artifact['workflow_run']['head_sha'] = '0' * 40
                elif damage == 'bad_attempt':
                    artifact['name'] += '-alias'
                elif damage == 'future_attempt':
                    artifact['name'] = 'dockingmt-python-coverage-42059033330-3'
                elif damage == 'bad_artifact_id':
                    artifact['id'] = 0
                elif damage == 'missing_created_at':
                    artifact.pop('created_at')
                else:
                    job['steps'][1]['number'] = 16
                received = self.binding(evidence)
                self.assertIn('error', received)
                self.assertEqual(received['outputs'], {})
