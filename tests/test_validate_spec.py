"""In-memory failing fixtures; validator must never write curriculum output."""
import copy
import contextlib
import io
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from scripts import validate_spec as validator
from scripts.new_day_skeleton import write_skeleton

ROOT = Path(__file__).resolve().parents[1]


class ValidateSpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data, cls.legacy, cls.metadata = validator.load_spec(ROOT / 'scratch/day_data_002.py')
        cls.reference = tuple(min(values) for values in zip(*(validator.metrics(t) for t in cls.data['topics'])))

    def check(self, mutate=None, needle=None, **options):
        data = copy.deepcopy(self.data)
        if mutate: mutate(data)
        errors, warnings = validator.validate_data(2, data, metadata=self.metadata, **options)
        if needle: self.assertTrue(any(needle in e for e in errors), errors)
        else: self.assertEqual(errors, [])
        return errors, warnings

    def test_day2_passes_without_page_writes(self):
        with patch.object(Path, 'write_text', side_effect=AssertionError('validator wrote a file')):
            self.check(reference=self.reference)
            with contextlib.redirect_stdout(io.StringIO()) as stream:
                self.assertEqual(validator.main(['--day', '2']), 0)
            self.assertIn('manual review', stream.getvalue())

    def test_error_1_todo_anywhere_and_keys(self):
        self.check(lambda d: d.update(metadata={'TODO: key': ['TODO: value']}), 'TODO:')
        self.check(lambda d: d['topics'][0].update(technical='TODO: explanation'), 'topic-01 topic.technical')

    def test_error_2_coverage_keys_titles_anchors(self):
        self.check(lambda d: d['topics'].pop(), 'missing coverage topic')
        self.check(lambda d: d['topics'][0].update(key='extra'), 'extra topic')
        self.check(lambda d: d['topics'][0].update(title='Different'), 'title:')
        self.check(lambda d: d['topics'][0].update(anchors={'lab': 'wrong'}), 'anchors.lab')
        self.check(lambda d: d['topics'].append(copy.deepcopy(d['topics'][0])), 'duplicate')

    def test_error_3_lab_steps_markers_body_environment(self):
        self.check(lambda d: d['topics'][0]['lab']['steps'].pop(), 'exactly eight')
        for marker in ('Location:', 'Expected result:', 'Save:'):
            with self.subTest(marker=marker):
                self.check(lambda d: d['topics'][0]['lab']['steps'].__setitem__(0, d['topics'][0]['lab']['steps'][0].replace(marker, 'Gone:')), f'missing {marker}')
        self.check(lambda d: d['topics'][0]['lab']['steps'].__setitem__(0, '**Location:** spaceship\n\n```bash\npwd\n```\n**Expected result:** here\n**Save:** file'), 'recognised environment')
        self.check(lambda d: d['topics'][0]['lab']['steps'].__setitem__(0, '**Location:** local terminal\n\n**Expected result:** ready\n**Save:** evidence'), 'manual-step body')

    def test_error_4_diagram_boolean(self):
        self.check(lambda d: d['topics'][0]['scenario'].pop('diagram_enabled'), 'required boolean')
        self.check(lambda d: d['topics'][0]['scenario'].update(diagram_enabled='False'), 'required boolean')

    def test_error_5_fallbacks_and_conditional_routes(self):
        self.check(lambda d: d.pop('part2_intro'), 'engine fallback would insert generic prose')
        self.check(lambda d: d['topics'][0]['lab'].pop('preflight'), 'lab.preflight')
        self.check(lambda d: d['topics'][2]['scenario'].pop('facts'), 'scenario.facts')
        self.check(lambda d: d.update(arch_diagram={'type': 'flow'}), 'arch_diagram.nodes')
        data = copy.deepcopy(self.data)
        data.pop('part2_intro')
        errors, _ = validator.validate_data(2, data, legacy=True, metadata=self.metadata)
        self.assertFalse(any('fallback' in e for e in errors))

    def test_error_6_technical_structure(self):
        self.check(lambda d: d['topics'][0].update(technical='Plain explanation.'), 'subtopic list')
        for label in (*validator.LABELS, 'Concrete example:', 'Evidence limit:'):
            with self.subTest(label=label):
                self.check(lambda d: d['topics'][0].update(technical=d['topics'][0]['technical'].replace(label, 'Missing:')), f'missing {label}')

    def test_error_7_markup_and_commands(self):
        data = copy.deepcopy(self.data)
        def strip_classes(value):
            if isinstance(value, str): return value.replace('class="keyword"', 'class="other"')
            if isinstance(value, dict): return {k: strip_classes(v) for k, v in value.items()}
            if isinstance(value, list): return [strip_classes(v) for v in value]
            return value
        errors, _ = validator.validate_data(2, strip_classes(data), metadata=self.metadata)
        self.assertTrue(any('missing strong.keyword' in e for e in errors))
        self.check(lambda d: d.update(extra='<pre><code><strong class="keyword">term</strong></code></pre>'), 'keyword inside pre/code')
        self.check(lambda d: d.update(extra='<code>gcloud projects list</code>'), 'inline command')

    def test_error_8_part1_preview_only(self):
        self.check(lambda d: (d.pop('part1_html'), d['topics'][0].update(preview='Only one sentence.')), 'exactly two sentences')
        self.check(lambda d: d['topics'][0].update(technical=d['topics'][0]['technical'] + '<p>Third sentence. Fourth sentence. Fifth sentence.</p>'))
        self.assertEqual(validator.sentence_count('Address 10.240.0.1 is local. Now inspect it.'), 2)

    def test_part1_label_consistency(self):
        v2_data, _, v2_meta = validator.load_spec(ROOT / 'scratch/day_data_004.py')

        # 1. pass: v2 spec with all three labels in order passes
        errors, _ = validator.validate_data(4, copy.deepcopy(v2_data), metadata=v2_meta)
        self.assertEqual(errors, [])

        # 2. one missing label: errors for contract_version 2, warns for older specs
        bad_v2 = copy.deepcopy(v2_data)
        bad_v2['part1_html'] = bad_v2['part1_html'].replace('<strong class="side-heading">Where it sits:</strong>', '')
        errors, _ = validator.validate_data(4, bad_v2, metadata=v2_meta)
        self.assertTrue(any('Where it sits:' in e for e in errors))

        # older spec (v1) missing Where it sits warns, 0 errors
        bad_v1 = copy.deepcopy(self.data)
        bad_v1['part1_html'] = bad_v1['part1_html'].replace('<strong class="side-heading">Where it sits:</strong>', '')
        errors, warnings = validator.validate_data(2, bad_v1, metadata=self.metadata)
        self.assertEqual(errors, [])
        self.assertTrue(any('Where it sits:' in w for w in warnings))

        # 3. combined label fails for v2
        comb_v2 = copy.deepcopy(v2_data)
        comb_v2['part1_html'] = comb_v2['part1_html'].replace(
            '<strong class="side-heading">Why today:</strong>',
            '<strong class="side-heading">Why today and where it sits:</strong>'
        ).replace('<strong class="side-heading">Where it sits:</strong>', '')
        errors, _ = validator.validate_data(4, comb_v2, metadata=v2_meta)
        self.assertTrue(any('combined' in e for e in errors))

    def test_incident_caption_labels(self):
        v2_data, _, v2_meta = validator.load_spec(ROOT / 'scratch/day_data_004.py')

        # 1. engine-compiled passes
        errors, _ = validator.validate_data(4, copy.deepcopy(v2_data), metadata=v2_meta)
        self.assertEqual(errors, [])

        # 2. raw override with a bare caption fails (error for contract_version 2, warn for older specs)
        bare_svg = (
            '<figure class="diagram-figure">'
            '<svg viewBox="0 0 10 10" role="img" aria-labelledby="t d"><title id="t">T</title><desc id="d">D</desc><rect width="10" height="10"/></svg>'
            '<figcaption>Bare incident caption without required fields.</figcaption>'
            '</figure>'
        )
        bare_v2 = copy.deepcopy(v2_data)
        bare_v2['topics'][0]['scenario']['incident_svg_html'] = bare_svg
        errors, _ = validator.validate_data(4, bare_v2, metadata=v2_meta)
        self.assertTrue(any('scenario.caption' in e and 'missing' in e for e in errors), errors)

        # older spec (v1) warns, 0 errors
        bare_v1 = copy.deepcopy(self.data)
        bare_v1['topics'][2]['scenario']['incident_svg_html'] = bare_svg
        errors, warnings = validator.validate_data(2, bare_v1, metadata=self.metadata)
        self.assertEqual(errors, [])
        self.assertTrue(any('scenario.caption' in w and 'missing' in w for w in warnings), warnings)

        # 3. raw override with three fields passes
        three_fields_svg = (
            '<figure class="diagram-figure">'
            '<svg viewBox="0 0 10 10" role="img" aria-labelledby="t d"><title id="t">T</title><desc id="d">D</desc><rect width="10" height="10"/></svg>'
            '<figcaption>Figure 4.3: Supplied facts: Test facts. Architectural inference: Test inference. Expected post-fix behavior: Test expected.</figcaption>'
            '</figure>'
        )
        valid_v2 = copy.deepcopy(v2_data)
        valid_v2['topics'][0]['scenario']['incident_svg_html'] = three_fields_svg
        errors, _ = validator.validate_data(4, valid_v2, metadata=v2_meta)
        self.assertEqual(errors, [])

    def test_error_9_source_metadata(self):
        self.check(lambda d: d['topics'][0].update(reference='http://example.com'), 'https URL')
        self.check(lambda d: d['topics'][0].update(reference_label='TODO: verify doc'), 'unverified source label')
        errors, _ = validator.validate_data(2, self.data)
        self.assertTrue(any('missing source access date' in e for e in errors))
        self.check(lambda d: d.update(sources={'doc': ('Doc', 'ftp://example.com')}), 'scheme must be https')

    def test_error_10_diagrams(self):
        self.check(lambda d: d['topics'][0]['scenario'].update(svg_html='<svg></svg>'), 'diagram present with diagram_enabled False')
        for missing in ('viewBox', 'role', 'title', 'desc'):
            with self.subTest(missing=missing):
                svg = '<svg viewBox="0 0 10 10" role="img"><title id="t">T</title><desc id="d">D</desc></svg>'
                if missing in ('title', 'desc'): svg = re.sub(f'<{missing}.*?</{missing}>', '', svg)
                else: svg = re.sub(f'{missing}="[^"]*"', '', svg)
                self.check(lambda d: d.update(arch_svg_html=svg), 'SVG requires')
        self.check(lambda d: d['topics'][0].update(flow={'nodes': [{'id': 'a', 'icon': '../assets/icons/missing.svg'}], 'steps': []}), 'icon must exist locally')

    def test_incident_flag_and_technical_diagram_scope(self):
        for field, value in (('flow', {}), ('diagram', []), ('icons', []),
                             ('incident_svg_html', ''), ('svg_html', '')):
            with self.subTest(field=field):
                self.check(lambda d: d['topics'][0]['scenario'].update({field: value}), 'diagram present with diagram_enabled False')
        self.check(lambda d: d['topics'][0]['scenario'].update(diagram_enabled=True), 'requires incident diagram data')
        errors, warnings = self.check()
        self.assertFalse(errors)
        self.assertTrue(any(w.startswith('WARN topic-02 technical diagram present;') for w in warnings))
        self.assertTrue(any(w.startswith('WARN topic-03 technical diagram present;') for w in warnings))

    def test_technical_diagram_structural_failures(self):
        self.check(lambda d: d['topics'][1].update(technical=d['topics'][1]['technical'].replace('aria-labelledby=', 'ignored=')), 'IDs must resolve')
        self.check(lambda d: d['topics'][1].update(technical=re.sub(r'<figcaption>.*?</figcaption>', '', d['topics'][1]['technical'], flags=re.S)), 'non-empty figcaption')
        self.check(lambda d: d['topics'][1].update(technical=d['topics'][1]['technical'].replace('../assets/icons/generic/client.svg', '../assets/icons/missing.svg')), 'SVG icon must exist locally')
        self.check(lambda d: d['topics'][0].update(technical=d['topics'][0]['technical'] + '<figure class="diagram-container"></figure>'), 'empty diagram wrapper')
        self.check(lambda d: d['topics'][0].update(technical=d['topics'][0]['technical'] + '<h4>Technical diagram</h4>'), 'empty diagram heading')
        self.check(lambda d: d.update(arch_diagram={'title': 'Diagram', 'desc': 'Description', 'caption': 'Limit', 'nodes': []}), 'empty diagram data')

    def test_legacy_skips_only_fallback_presence(self):
        data, legacy, metadata = validator.load_spec(ROOT / 'scratch/day_data_003.py')
        self.assertTrue(legacy)
        errors, _ = validator.validate_data(3, data, legacy=legacy, metadata=metadata)
        self.assertFalse(any('fallback' in e for e in errors))
        self.assertEqual(errors, [])
        data = copy.deepcopy(data)
        data['topics'][0]['lab']['steps'][0] = data['topics'][0]['lab']['steps'][0].replace('Location:', 'Gone:')
        errors, _ = validator.validate_data(3, data, legacy=legacy, metadata=metadata)
        self.assertTrue(any('Location:' in e for e in errors))

    def test_depth_warns_without_failing_on_length(self):
        _, warnings = self.check(reference=(1000000, 1000000, 1000000, 1000000))
        self.assertTrue(warnings)
        self.assertTrue(all(w.startswith('WARN ') for w in warnings))

    def test_same_command_pattern_as_rendered_validator(self):
        source = (ROOT / 'scripts/validate.py').read_text()
        self.assertIn('re.match(r"' + validator.COMMAND_PATTERN + '"', source)

    def test_directory_fixture_uses_engine_loader(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'spec'
            data = copy.deepcopy(self.data)
            data.update(sources=self.metadata['sources'], access_date=self.metadata['access_date'])
            write_skeleton(path, data, directory=True)
            loaded, legacy, metadata = validator.load_spec(path)
            self.assertFalse(legacy)
            self.assertEqual(validator.validate_data(2, loaded, metadata=metadata)[0], [])

    def test_cli_limits_errors_and_returns_failure_without_writes(self):
        bad = copy.deepcopy(self.data)
        bad['extra'] = ['TODO: value'] * 50
        with patch.object(validator, 'load_spec', return_value=(bad, False, self.metadata)), patch.object(Path, 'write_text', side_effect=AssertionError('write')):
            with contextlib.redirect_stdout(io.StringIO()) as stream:
                self.assertEqual(validator.main(['--day', '2', '--spec', '/tmp/in-memory.py']), 1)
        lines = stream.getvalue().splitlines()
        self.assertEqual(sum(line.startswith('ERROR ') for line in lines), 30)
        self.assertEqual(sum(line.startswith('Summary:') for line in lines), 1)


if __name__ == '__main__':
    unittest.main()
