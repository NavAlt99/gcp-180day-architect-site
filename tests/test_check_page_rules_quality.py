"""Deterministic quality-floor checks R10-R13."""
import json
from pathlib import Path
import tempfile
import unittest

from scripts import check_page_rules as rules


def parsed(html):
    builder = rules.Builder()
    builder.feed(f'<html><body><main>{html}</main></body></html>')
    return builder.root


class QualityRuleTests(unittest.TestCase):
    def test_r10_duplicate_paragraph_fails_without_baseline(self):
        text = 'A concrete architectural paragraph explains one boundary and its evidence owner in enough detail to exceed eighty characters.'
        result = rules.check_r10(parsed(f'<p>{text}</p><p>{text}</p>'))
        self.assertEqual(result['status'], 'FAIL')

    def test_r10_unique_paragraphs_pass(self):
        result = rules.check_r10(parsed(
            '<p>This first architectural paragraph explains a unique routing boundary and its evidence owner in concrete detail.</p>'
            '<p>This second architectural paragraph instead explains a distinct application invariant and its verification evidence.</p>'))
        self.assertEqual(result['status'], 'PASS')

    def test_r11_heading_restatement_fails(self):
        root = parsed('''<article class="worked-example">
            <p><strong>Worked dossier 1: IPv4 route failure</strong></p>
            <p><strong>Worked starting point:</strong> IPv4 route failure</p>
        </article>''')
        result = rules.check_r11(root)
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn('jaccard=1.000', result['items'][0])

    def test_r11_command_output_passes(self):
        root = parsed('''<article class="worked-example">
            <p><strong>Worked dossier 1: Route ownership decision</strong></p>
            <p><strong>Worked starting point:</strong> The supplied output names no matching prefix.</p>
            <p>Run <code>ip route get 192.0.2.8</code> to preserve the command evidence.</p>
        </article>''')
        self.assertEqual(rules.check_r11(root)['status'], 'PASS')

    def test_r11_no_dossiers_is_na(self):
        result = rules.check_r11(parsed('<p>No dossier appears on this page.</p>'))
        self.assertEqual(result['status'], 'N/A')

    def test_r11_nested_dossiers_use_nearest_heading(self):
        root = parsed('''<article class="worked-example">
            <p><strong>Worked dossier 1: Outer boundary</strong></p>
            <p><strong>Worked starting point:</strong> Observation 7 identifies the outer owner.</p>
            <article class="worked-example">
              <p><strong>Worked dossier 2: Inner command</strong></p>
              <p><strong>Worked starting point:</strong> The supplied output identifies a socket.</p>
              <p><kbd>ss -ltn</kbd></p>
            </article>
        </article>''')
        result = rules.check_r11(root)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(len(result['items']), 2)
        self.assertTrue(result['items'][1].startswith('Inner command:'))

    def test_r12_dossier_counts_are_informational(self):
        def page(count):
            dossiers = ''.join(f'<p><strong>Worked dossier {i}: Case {i}</strong></p>' for i in range(1, count + 1))
            return parsed(f'<article id="topic-01-technical">{dossiers}</article>')
        result = rules.check_r12(page(9))
        self.assertEqual(result['status'], 'N/A')
        self.assertFalse(result['gated'])
        self.assertEqual(result['items'], ['topic-01-technical: 9'])

    def test_r13_removed_subtopic_fails_and_identical_passes(self):
        original = parsed('''<article id="topic-01-technical">
            <h4 id="topic-01-subtopic-1">One</h4><ul><li><strong class="side-heading">What:</strong> Detail</li></ul>
            <h4 id="topic-01-subtopic-2">Two</h4><ul><li><strong class="side-heading">What:</strong> Detail</li></ul>
        </article><article id="topic-01-lab"><li>Stage 1: One</li></article>''')
        baseline = rules.protected_snapshot(original, 'fixture.html')
        self.assertEqual(rules.check_r13(baseline, baseline)['status'], 'PASS')
        changed = parsed('''<article id="topic-01-technical">
            <h4 id="topic-01-subtopic-1">One</h4><ul><li><strong class="side-heading">What:</strong> Detail</li></ul>
        </article><article id="topic-01-lab"><li>Stage 1: One</li></article>''')
        self.assertEqual(rules.check_r13(rules.protected_snapshot(changed, 'fixture.html'), baseline)['status'], 'FAIL')

    def test_r13_dossier_count_decrease_fails_and_increase_passes(self):
        def snapshot(count):
            dossiers = ''.join(f'<p><strong>Worked dossier {i}: Case {i}</strong></p>' for i in range(1, count + 1))
            return rules.protected_snapshot(
                parsed(f'<article id="topic-01-technical">{dossiers}</article>'), 'fixture.html')

        baseline = snapshot(9)
        self.assertEqual(baseline['dossiers_per_topic'], {'topic-01-technical': 9})
        self.assertEqual(rules.check_r13(snapshot(8), baseline)['status'], 'FAIL')
        self.assertEqual(rules.check_r13(snapshot(10), baseline)['status'], 'PASS')

    def test_r10_refresh_refuses_new_or_increased_repeat(self):
        digest = '0123456789abcdef'
        repeated = {digest: {'text': 'x' * 80, 'count': 3, 'preview': 'x' * 60, 'occurrences': []}}
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'baseline.json'
            path.write_text(json.dumps({'1': {digest: {'count': 2, 'preview': 'x' * 60}}}))
            with self.assertRaisesRegex(SystemExit, 'may only shrink'):
                rules.refresh_r10_baseline(str(path), 1, repeated)


if __name__ == '__main__':
    unittest.main()
