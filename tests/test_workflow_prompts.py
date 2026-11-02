"""Durable checks for the complete day and batch workflow prompts."""
import hashlib
from pathlib import Path
import unittest

from scripts import check_page_rules as rules


ROOT = Path(__file__).resolve().parents[1]


def parsed(html):
    builder = rules.Builder()
    builder.feed(html)
    return builder.root


class PageRuleFiveTests(unittest.TestCase):
    def test_shared_stylesheet_without_inline_width_passes(self):
        root = parsed('<link rel="stylesheet" href="../assets/site.css"><article id="topic-01-technical"></article>')
        result = rules.check_r5(root)
        self.assertEqual(result['status'], 'PASS')
        self.assertTrue(result['gated'])

    def test_missing_shared_stylesheet_or_inline_width_fails(self):
        for html in ('<article id="topic-01-technical"></article>',
                     '<link rel="stylesheet" href="../assets/site.css"><style>.topic-card p{max-width:82ch}</style>',
                     '<link rel="stylesheet" href="../assets/site.css"><article id="topic-01-technical" style="width:90%"></article>'):
            with self.subTest(html=html):
                self.assertEqual(rules.check_r5(parsed(html))['status'], 'FAIL')


class WorkflowPromptTests(unittest.TestCase):
    def test_complete_worker_prompt_and_batch_reference(self):
        worker = (ROOT / 'DAY_WORKFLOW_PROMPT.md').read_text()
        batch = (ROOT / 'BATCH_UPDATE_PROMPT.md').read_text()
        for required in (
            'SCOPE=                 (plan | update | audit-only | fix)',
            '### R1 — linked subtopics', '### R9 — deterministic checker',
            '### SCOPE=plan', '### SCOPE=audit-only', '### SCOPE=fix', '### SCOPE=update',
            '### DIAGRAMS=keep', '### DIAGRAMS=allow',
            '### TOPICS=keep', '### TOPICS=expand', '### TOPICS=add',
            '## Branch preflight', '## Work', '## Gate before commit',
            '## Commit and push', '## Finish'):
            self.assertIn(required, worker)
        self.assertIn('entire DAY_WORKFLOW_PROMPT.md', batch)

    def test_contract_pin_matches(self):
        digest = hashlib.sha256((ROOT / 'PAGE_AUTHORING_CONTRACT.md').read_bytes()).hexdigest()
        self.assertEqual((ROOT / 'scratch/batch-contract.sha256').read_text().strip(), digest)


if __name__ == '__main__':
    unittest.main()
