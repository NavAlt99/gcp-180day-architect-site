import re
import unittest

from bs4 import BeautifulSoup

from scripts import build, check_page_rules


HTML = '''<!doctype html><html><body>
<section id="part-1"><article id="topic-01-overview" class="topic-card">
<h3>Fixture topic</h3><p>Existing overview prose.</p></article></section>
<section id="part-2"><article id="topic-01-technical" class="topic-card technical">
<h3>Fixture technical title</h3><h4>Existing mechanism</h4>
<p><strong class="side-heading">What it is in general:</strong> Existing explanation with <strong class="keyword">fixture term</strong>.</p>
<p>Use `fixture.txt` safely:</p><p>Checks:\n- preserve the first fact\n- preserve the second fact</p>
</article></section></body></html>'''


class BuildRuleGenerationTests(unittest.TestCase):
    def test_rules_are_generated_from_page_markup_and_idempotent(self):
        output = build.apply_page_rules(HTML, 1)
        self.assertEqual(build.apply_page_rules(output, 1), output)
        parser = check_page_rules.Builder()
        parser.feed(output)
        root = parser.root
        ids = {node.attrs['id'] for node in check_page_rules.nodes(root)
               if isinstance(node, check_page_rules.Node) and 'id' in node.attrs}
        for result in (
            check_page_rules.check_r1(root, ids),
            check_page_rules.check_r2(root),
            check_page_rules.check_r3(root, []),
            check_page_rules.check_r7(output),
        ):
            self.assertEqual(result['status'], 'PASS', result)

    def test_existing_words_are_preserved_outside_generated_r1_navigation(self):
        output = build.apply_page_rules(HTML, 1)
        before = BeautifulSoup(HTML, 'html.parser')
        after = BeautifulSoup(output, 'html.parser')
        for generated in list(after.select('[data-generated-rule="R1"],[data-generated-rule="R1-preserved-anchor"]')):
            generated.decompose()
        words = lambda soup: re.findall(r'\w+', soup.get_text(' ', strip=True).replace('`', '').casefold())
        self.assertEqual(words(before), words(after))

    def test_build_paths_follow_the_active_checkout(self):
        self.assertEqual(build.SITE, build.Path(build.__file__).resolve().parents[1])
        self.assertEqual(build.ROADMAP, build.SITE.parent / 'roadmap-180-days.md')


if __name__ == '__main__':
    unittest.main()
