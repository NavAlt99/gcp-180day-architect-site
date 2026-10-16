import tempfile
from pathlib import Path
import unittest
from scripts.extract_day_inputs import extract, section


class ExtractTests(unittest.TestCase):
    def test_roadmap_heading_fixture(self):
        text = '### Day 4 — Four\nPractice body\n### Day 5 — Five\nOther'
        self.assertEqual(section(text, 4, 3, 'roadmap'), '### Day 4 — Four\nPractice body')

    def test_brief_heading_fixture_with_nested_entry(self):
        text = '## Day 4 — Four\n~~~text\n### Day 4 — Four\nBody\n~~~\n## Day 5 — Five\nOther'
        value = section(text, 4, 2, 'brief')
        self.assertIn('### Day 4', value)
        self.assertTrue(value.endswith('~~~'))
        self.assertNotIn('Day 5', value)

    def test_missing_empty_and_duplicate_fail(self):
        for text in ('### Day 5 — Five\nOther', '### Day 4 — Four\n', '### Day 4 — Four\nA\n### Day 4 — Four\nB'):
            with self.assertRaises(ValueError): section(text, 4, 3, 'roadmap')

    def test_all_inputs_required_no_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'site'
            (root / 'data').mkdir(parents=True)
            (root.parent / 'roadmap-180-days.md').write_text('### Day 4 — Four\nPractice\n')
            (root.parent / 'gcp-architect-180-day-page-prompts.md').write_text('## Day 4 — Four\nBrief\n')
            (root / 'data/coverage.csv').write_text('day,topic_key,topic\n4,topic-01,HTTP\n')
            self.assertIn('4,topic-01,HTTP', extract(4, root))
            (root / 'data/coverage.csv').write_text('day,topic_key,topic\n')
            with self.assertRaisesRegex(ValueError, 'coverage'): extract(4, root)
            self.assertFalse((root / 'scratch').exists())
