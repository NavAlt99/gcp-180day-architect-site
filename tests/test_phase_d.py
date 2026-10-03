"""Compact flows and directory specs: fixtures only, no durable-page migration."""
import copy
import hashlib
import json
from pathlib import Path
from pprint import pformat
import tempfile
import unittest
from bs4 import BeautifulSoup

from scripts.author_engine import (load_day_module, render_sophisticated_flow_svg,
                                   render_topology_svg, render_incident_svg)
from scripts.compact_flow import render_compact_flow
from scripts.new_day_skeleton import skeleton, write_skeleton

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def flow():
    return {'title': 'Complete sequence', 'caption': 'Supplied illustrative flow; not observed.',
            'nodes': [{'id': 'start', 'label': 'Receive and inspect the entire incoming request without losing any label words',
                       'detail': 'Full request information retained for evaluation', 'icon': '../assets/icons/generic/client.svg'},
                      {'id': 'finish', 'label': 'Deliver response', 'detail': 'Save evidence', 'icon': '../assets/icons/generic/server.svg'}],
            'steps': [{'from': 'start', 'to': 'finish', 'label': 'validate and deliver'}]}


class PhaseDTests(unittest.TestCase):
    def test_directory_day2_identical_semantic_hash(self):
        data = load_day_module(ROOT / 'scratch/day_data_002.py')
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / 'day_data_002'
            directory.mkdir()
            meta = {k: v for k, v in data.items() if k != 'topics'}
            (directory / 'meta.py').write_text('DATA = ' + pformat(meta))
            for i, topic in enumerate(data['topics'], 1):
                (directory / f'topic_{i:02d}.py').write_text('TOPIC = ' + pformat(topic))
            self.assertEqual(digest(load_day_module(directory)), digest(data))

    def test_directory_skeleton_identical_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'spec'
            data = skeleton(2)
            write_skeleton(path, data, directory=True)
            self.assertEqual(digest(data), digest(load_day_module(path)))
            with self.assertRaises(FileExistsError):
                write_skeleton(path, data, directory=True)

    def test_missing_directory_topic_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)
            (path / 'meta.py').write_text('DATA = {}')
            (path / 'topic_02.py').write_text('TOPIC = {}')
            with self.assertRaisesRegex(ValueError, 'contiguous'):
                load_day_module(path)

    def test_compact_accessibility_icons_labels_and_unique_ids(self):
        data = flow()
        html = render_compact_flow('fixture-a', data) + render_compact_flow('fixture-b', data)
        soup = BeautifulSoup(html, 'html.parser')
        ids = [el['id'] for el in soup.select('[id]')]
        self.assertEqual(len(ids), len(set(ids)))
        for svg in soup.select('svg'):
            for target in svg['aria-labelledby'].split():
                self.assertIsNotNone(soup.find(id=target))
            self.assertEqual(len(svg.select('image')), len(data['nodes']))
            for image in svg.select('image'):
                icon = (ROOT / 'days' / image['href']).resolve()
                self.assertTrue(icon.is_relative_to(ROOT / 'assets/icons'))
                self.assertTrue(icon.is_file())
            node = svg.select_one('[data-node="start"]')
            self.assertEqual(' '.join(t.text for t in node.select('text')[:4]), '1. ' + data['nodes'][0]['label'])
        self.assertEqual(len(soup.select('figcaption')), 2)
        self.assertEqual(len(soup.select('.flow-transitions li')), 2)

    def test_too_long_label_fails_without_truncation(self):
        data = flow(); data['nodes'][0]['label'] = 'unbounded ' * 10000
        with self.assertRaisesRegex(ValueError, 'cannot fit'):
            render_compact_flow('fixture-long', data)

    def test_bad_icons_ids_and_step_order_fail(self):
        for change in ('icon', 'id', 'step'):
            with self.subTest(change=change):
                data = flow()
                if change == 'icon': data['nodes'][0]['icon'] = 'https://example.com/icon.svg'
                if change == 'id': data['nodes'][1]['id'] = 'start'
                if change == 'step': data['steps'][0]['to'] = 'missing'
                with self.assertRaises(ValueError): render_compact_flow('bad', data)

    def test_existing_renderer_compact_routes_and_raw_precedence(self):
        data = flow()
        for renderer in (render_sophisticated_flow_svg, render_topology_svg):
            self.assertIn('Complete sequence', renderer(2, data))
        topic = {'scenario': {'diagram_enabled': True, 'flow': data}}
        self.assertIn('Complete sequence', render_incident_svg(2, 1, topic))
        topic['scenario']['incident_svg_html'] = '<svg>RAW ESCAPE</svg>'
        self.assertIn('RAW ESCAPE', render_incident_svg(2, 1, topic))
        self.assertNotIn('Complete sequence', render_incident_svg(2, 1, topic))


if __name__ == '__main__':
    unittest.main()
