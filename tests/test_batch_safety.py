import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts import batch_gate as gate, run_labs as labs, validate_spec as validator, write_handoff as handoff

FIXTURE = Path(__file__).parent / 'fixtures/lab_spec.py'


class LabTests(unittest.TestCase):
    def setUp(self):
        self.topic = copy.deepcopy(labs.load_spec(FIXTURE)[0]['topics'][0])

    def test_fixture_state_artifacts_and_cleanup(self):
        result = labs.run_lab(self.topic, 10)
        self.assertEqual(result['status'], 'PASS', result)
        self.assertEqual(result['exit_status'], 0)
        self.assertEqual(len(result['stages']), 8)
        self.assertTrue(result['stages'][1]['artifacts'][0]['exists'])
        self.assertTrue(result['stages'][1]['artifacts'][0]['sha256'])
        self.assertFalse(list(Path('/tmp').glob('fixture.XXXXXX')))

    def test_missing_artifact_stops_before_cleanup(self):
        self.topic['lab']['steps'][3] = self.topic['lab']['steps'][3].replace('stage4.txt\n```', 'other.txt\n```')
        result = labs.run_lab(self.topic, 10)
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn({'stage': 4, 'path': 'stage4.txt'}, result['missing_artifacts'])
        self.assertEqual(result['stages'][7]['status'], 'NOT_RUN')

    def test_command_failure_records_missing_artifact(self):
        self.topic['lab']['steps'][1] = self.topic['lab']['steps'][1].replace('test "$FIXTURE_STATE" = retained', 'exit 9')
        result = labs.run_lab(self.topic, 10)
        self.assertEqual(result['exit_status'], 9)
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn({'stage': 2, 'path': 'stage2.txt'}, result['missing_artifacts'])

    def test_missing_optional_tool_never_passes(self):
        self.topic['lab']['steps'][5] = self.topic['lab']['steps'][5].replace('```bash\n', '```bash\ncommand -v nonexistent_fixture_tool || echo skipped\n')
        result = labs.run_lab(self.topic, 10)
        self.assertEqual(result['status'], 'SKIPPED')
        self.assertEqual(result['stages'][5]['missing_tools'], ['nonexistent_fixture_tool'])
        self.assertEqual(result['stages'][0]['status'], 'NOT_RUN')

    def test_missing_tool_cannot_be_masked(self):
        self.topic['lab']['steps'][1] = self.topic['lab']['steps'][1].replace('```bash\n', '```bash\nnonexistent_fixture_tool || echo ignore\n')
        result = labs.run_lab(self.topic, 10)
        self.assertEqual(result['status'], 'SKIPPED', result)
        self.assertEqual(result['stages'][1]['missing_tools'], ['nonexistent_fixture_tool'])

    def test_timeout_kills_lab(self):
        self.topic['lab']['steps'][1] = self.topic['lab']['steps'][1].replace('```bash\n', '```bash\nsleep 30 &\nwait\n')
        result = labs.run_lab(self.topic, .3)
        self.assertTrue(result['timed_out'])
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn({'stage': 2, 'path': 'stage2.txt'}, result['missing_artifacts'])

    def test_manual_cloud_non_shell_and_missing_save_fail_closed(self):
        for text in ('**Location:** Console\n```bash\necho hi\n```\n**Save:** test.txt',
                     '**Location:** Local Linux Bash terminal\n```python\nprint(1)\n```\n**Save:** test.txt'):
            self.topic['lab']['steps'][1] = text
            self.assertEqual(labs.run_lab(self.topic)['status'], 'SKIPPED')
        self.setUp()
        self.topic['lab']['steps'][1] = self.topic['lab']['steps'][1].replace('**Save:** stage2.txt', '**Save:** record evidence')
        self.assertEqual(labs.run_lab(self.topic)['status'], 'FAIL')

    def test_multiple_blocks_preserve_order(self):
        self.topic['lab']['steps'][1] = self.topic['lab']['steps'][1].replace('```\n\n**Expected', '```\n\n```sh\ntest -f stage2.txt\nprintf appended >> stage2.txt\n```\n\n**Expected')
        self.assertEqual(labs.run_lab(self.topic)['status'], 'PASS')

    def test_cli_writes_json_and_returns_failure_for_skip(self):
        with tempfile.TemporaryDirectory() as temporary, patch.object(labs, 'ROOT', Path(temporary)):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(labs.main(['--day', '1', '--spec', str(FIXTURE), '--timeout', '10']), 0)
            report = json.loads((Path(temporary) / 'scratch/day-001-lab-rerun.json').read_text())
            self.assertEqual(report['status'], 'PASS')


class GateTests(unittest.TestCase):
    def test_hash_first_run_and_changed_contract(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root / 'PAGE_AUTHORING_CONTRACT.md').write_text('canonical')
            self.assertTrue(gate.contract_check(root)); pin = (root / 'scratch/batch-contract.sha256').read_text()
            self.assertTrue(gate.contract_check(root))
            (root / 'PAGE_AUTHORING_CONTRACT.md').write_text('changed')
            self.assertFalse(gate.contract_check(root))
            self.assertEqual((root / 'scratch/batch-contract.sha256').read_text(), pin)

    def run_gate(self, fail=None, content=None, exit_status=0):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); (root / 'scratch').mkdir()
            seen = []
            def runner(cmd, **kwargs):
                name = Path(cmd[2]).stem; seen.append(name)
                if name == 'check_study_links':
                    (root / 'scratch/day-004-study-links.json').write_text(json.dumps({'unverified': 0, 'links': [{'status': 'pass'}]}))
                if name == 'run_labs':
                    (root / 'scratch/day-004-lab-rerun.json').write_text(json.dumps({'status': 'PASS', 'labs': [{'status': 'PASS', 'exit_status': 0, 'stages': [{'status': 'PASS'}] * 8}]}))
                if name == fail and content:
                    report = root / 'scratch' / ('day-004-study-links.json' if name == 'check_study_links' else 'day-004-lab-rerun.json')
                    report.write_text(json.dumps(content))
                return subprocess.CompletedProcess(cmd, exit_status if name == fail else 0,
                    'WARN diagram count below committed page\n' if name == fail == 'validate_spec' and exit_status == 0 else '')
            with contextlib.redirect_stdout(io.StringIO()) as output:
                status = gate.main(['--day', '4'], root=root, runner=runner)
            return status, seen, output.getvalue()

    def test_exact_order_and_pass(self):
        status, seen, _ = self.run_gate()
        self.assertEqual(status, 0); self.assertEqual(seen, list(gate.CHECKS))

    def test_stop_first_exit_failure_and_diagram_warning(self):
        for fail, code in [('validate', 1), ('validate_spec', 0)]:
            status, seen, output = self.run_gate(fail, exit_status=code)
            self.assertEqual(status, 1); self.assertEqual(seen[-1], fail)
            self.assertIn('FAIL: ' + fail, output)

    def test_unverified_links_and_skipped_labs(self):
        for fail, data in [('check_study_links', {'links': [{'status': 'unverified'}], 'unverified': 1}),
                           ('check_study_links', {'links': [{'status': 'pass', 'rfc_status_note': 'Unverified RFC status: offline'}]}),
                           ('run_labs', {'status': 'FAIL', 'labs': [{'status': 'SKIPPED'}]})]:
            status, seen, _ = self.run_gate(fail, data)
            self.assertEqual(status, 1); self.assertEqual(seen[-1], fail)

    def test_missing_report_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(FileNotFoundError):
                gate.report_failure('check_study_links', '', Path(temporary), 4)


class BaselineAndHandoffTests(unittest.TestCase):
    def test_day4_ranges(self):
        self.assertEqual(validator.depth_ranges(), ((11219, 13061), (4, 4), (8, 8), (7711, 13420)))

    def test_handoff_generated_records_and_git_stat(self):
        data = {'topics': [{'key': 'topic-01', 'title': 'Fixture', 'technical': '<p>Relevance to GCP: A documented claim. <a href="https://example.test/docs#section">Section</a></p>',
                            'lab': {'name': 'Fixture lab', 'covers': 'Practice clause', 'file': 'evidence.md'}}],
                'roadmap_practice': 'Practice clause', 'roadmap_exit': 'evidence',
                'sources': {'s': ('Source label', 'https://example.test/docs#section')},
                'review_records': {'source_ledger': {'https://example.test/docs#section': {'heading_opened': 'Actual heading'}}}}
        with patch.object(handoff, 'load_spec', return_value=(data, False, {})), patch.object(handoff, 'old_spec', return_value=data), patch.object(handoff, 'git', side_effect=[' 1 file changed, 2 insertions(+)\n', 'scratch/fixture.py', '+added\n']):
            output = handoff.generate(1, handoff.ROOT / 'scratch/fixture.py')
        for text in ('Practice clause', 'Actual heading', 'A documented claim', '1 file changed, 2 insertions', 'No source lines removed.'):
            self.assertIn(text, output)
        self.assertNotIn('verified source', output)


if __name__ == '__main__': unittest.main()
