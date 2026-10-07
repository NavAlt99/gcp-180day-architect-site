"""Phase B/C safety checks; no page output is written by this suite."""
import copy
import csv
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts import author_engine as engine
from scripts.new_day_skeleton import skeleton
from scratch.day_helpers import case

ROOT = Path(__file__).resolve().parents[1]


class AuthoringFollowupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.complete = engine.load_day_module(ROOT / 'scratch/day_data_002.py')

    def assert_rejected(self, data, field, topic=True):
        key = data['topics'][0]['key']
        with patch.object(Path, 'write_text') as write:
            with self.assertRaises(ValueError) as caught:
                engine.compile_day_page(2, data)
            self.assertIn(field, str(caught.exception))
            if topic:
                self.assertIn(key, str(caught.exception))
            write.assert_not_called()

    def test_lab_todo(self):
        data = copy.deepcopy(self.complete)
        data['topics'][0]['lab']['goal'] = 'TODO: goal'
        self.assert_rejected(data, 'lab.goal')

    def test_case_default_evidence_label(self):
        data = copy.deepcopy(self.complete)
        data['topics'][0]['scenario'] = case('symptom', 'impact', 'constraints', 'records',
                                            'root', [], [], 'verify', 'residual')
        self.assert_rejected(data, 'scenario.evidence')

    def test_all_topic_content_fields(self):
        for field in ('overview', 'preview', 'technical', 'questions', 'reference', 'reference_label'):
            with self.subTest(field=field):
                data = copy.deepcopy(self.complete)
                data['topics'][0][field] = ['TODO: question'] if field == 'questions' else 'TODO: fill'
                self.assert_rejected(data, field)

    def test_all_scenario_fields(self):
        fields = ('scenario', 'impact', 'constraints', 'facts', 'inference', 'expected',
                  'evidence', 'evidence_label', 'root', 'verify', 'residual',
                  'diagnostic_steps', 'remediation_steps')
        for field in fields:
            with self.subTest(field=field):
                data = copy.deepcopy(self.complete)
                data['topics'][0]['scenario'][field] = 'TODO: fill'
                self.assert_rejected(data, f'scenario.{field}')

    def test_day_content_and_source_metadata(self):
        for field in ('part1_html', 'part1_intro', 'part2_intro', 'part3_intro', 'part4_intro',
                      'exit_summary', 'completion_html', 'sources', 'access_date'):
            with self.subTest(field=field):
                data = copy.deepcopy(self.complete)
                data[field] = {'verified': ('label', 'TODO: URL')} if field == 'sources' else 'TODO: fill'
                self.assert_rejected(data, field, topic=False)

    def test_complete_day2_passes(self):
        engine.validate_spec_todos(self.complete)
        for topic in self.complete['topics']:
            engine.resolve_lab(topic['lab'], self.complete.get('lab_defaults'))

    def test_missing_default_names_topic(self):
        data = copy.deepcopy(self.complete)
        del data['topics'][0]['lab']['mode']
        self.assert_rejected(data, 'lab.mode')

    def test_skeleton_anchors_and_slots_day2(self):
        data = skeleton(2)
        with (ROOT / 'data/coverage.csv').open(newline='') as stream:
            rows = [r for r in csv.DictReader(stream) if int(r['day']) == 2]
        self.assertEqual(len(data['topics']), len(rows))
        for topic, row in zip(data['topics'], rows):
            self.assertEqual(topic['key'], row['topic_key'])
            for part in ('overview', 'technical', 'problem', 'lab'):
                self.assertEqual(topic['anchors'][part], row[f'{part}_anchor'])
            self.assertEqual(topic['reference'], 'TODO: verify ' + row['publisher_url'])
            self.assertEqual(topic['lab']['file'], f"day-002-{topic['key']}.md")
            self.assertEqual(len(topic['lab']['steps']), 8)
        self.assert_rejected(data, 'overview')

    def test_skeleton_registry_and_overwrite_refusal(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / 'fixture.py'
            command = [sys.executable, str(ROOT / 'scripts/new_day_skeleton.py'), '--day', '2', '--output', str(dest)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = dest.read_bytes()
            module = runpy.run_path(str(dest))
            self.assertEqual(module['SOURCES'], skeleton(2)['sources'])
            self.assertEqual(module['ACCESS_DATE'], 'TODO: access date')
            self.assertEqual(module['DATA']['sources'], module['SOURCES'])
            self.assertEqual(module['DATA']['access_date'], module['ACCESS_DATE'])
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(second.returncode, 2)
    def test_render_incident_svg_wrapping(self):
        # 1. override with its own figure: returned unwrapped
        override_fig = '<figure class="custom-fig"><svg></svg><figcaption>text</figcaption></figure>'
        topic_with_fig = {'scenario': {'incident_svg_html': override_fig}}
        out = engine.render_incident_svg(1, 1, topic_with_fig)
        self.assertEqual(out, override_fig)

        # 2. override without one: wrapped in diagram-container
        override_no_fig = '<svg viewBox="0 0 10 10"></svg>'
        topic_no_fig = {'scenario': {'incident_svg_html': override_no_fig}}
        out = engine.render_incident_svg(1, 1, topic_no_fig)
        self.assertEqual(out, f'<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto">{override_no_fig}</div></figure>')

        # 3. engine-compiled: generates dual-lane figure without nested figures
        topic_compiled = {
            'title': 'Test Incident',
            'scenario': {
                'diagram_enabled': True,
                'diagram': ('Trigger', 'Root cause', 'Impact', 'Control', 'Outcome'),
                'facts': 'Supplied facts: test.',
                'inference': 'Architectural inference: test.',
                'expected': 'Expected post-fix behavior: test.'
            }
        }
        out = engine.render_incident_svg(1, 1, topic_compiled)
        self.assertTrue(out.startswith('<figure class="diagram-container">'))
        self.assertEqual(out.count('<figure'), 1)
        self.assertEqual(out.count('</figure>'), 1)


if __name__ == '__main__':
    unittest.main()
