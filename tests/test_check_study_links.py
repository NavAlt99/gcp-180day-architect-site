"""Deterministic link-check regressions; no external network required."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from urllib.error import HTTPError

spec = importlib.util.spec_from_file_location("study_links", Path(__file__).resolve().parents[1] / "scripts/check_study_links.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class StudyLinkTests(unittest.TestCase):
    def fetch(self, url, timeout):
        return "https://docs.cloud.google.com/example", "text/html", b'<title>Example</title><h2 id="packet-path">Packet path</h2><a name="legacy"></a>'

    def test_only_further_study_and_deduplicate(self):
        html = '<a href="ignored">Navigation</a><p><strong>Further study:</strong><a href="doc#x">Guide</a><a href="doc#x">Guide</a></p>'
        self.assertEqual(checker.study_links(html), [{"url": "doc#x", "label": "Guide"}])

    def test_heading_link_list_stops_at_next_heading(self):
        html = '<h4>Further study</h4><ul><li><a href="doc">Guide</a></li></ul><h4>Lab</h4><p><a href="other">Other</a></p>'
        self.assertEqual([x["url"] for x in checker.study_links(html)], ["doc"])

    def test_redirect_and_valid_fragment(self):
        result = checker.check_link("https://cloud.google.com/example#packet-path", Path("day.html"), fetch=self.fetch)
        self.assertEqual(result["status"], "pass")
        self.assertTrue(result["redirected"])
        self.assertEqual(result["title"], "Example")
        self.assertEqual(result["relevance"], "manual review required")

    def test_excerpt_heading_and_paragraph_bounded(self):
        def fetch(url, timeout):
            return url, 'text/html', ('<h2 id="s">Heading</h2><p>'+ 'a'*400+'</p>').encode()
        result = checker.check_link('https://example.test/#s', Path('day.html'), fetch=fetch)
        self.assertEqual(result['link_scope'], 'fragment-level')
        self.assertTrue(result['excerpt'].startswith('Heading a'))
        self.assertEqual(len(result['excerpt']), 300)

    def test_section_first_paragraph_under_subheading(self):
        body=b'<section id="s"><h2>Section</h2><h3>First subsection</h3><p>First paragraph</p></section>'
        result=checker.check_link('https://example.test/#s',Path('day.html'),fetch=lambda u,t:(u,'text/html',body))
        self.assertEqual(result['excerpt'], 'Section First paragraph')

    def test_whole_document_h1(self):
        result = checker.check_link('https://example.test/', Path('day.html'), fetch=lambda u,t:(u,'text/html',b'<h1>First heading</h1><p>Other</p>'))
        self.assertEqual(result['link_scope'], 'whole-document')
        self.assertEqual(result['excerpt'], 'First heading')

    def test_legacy_rfc_heading_and_status(self):
        body=b'<pre><span class="h2"><a id="section-4">4</a>. Handshake Protocol</span>\n\n   First paragraph.\n\nSecond paragraph.</pre>'
        def fetch(url, timeout):
            return url, 'text/html', b'<dl><dt>Obsoleted by (1)</dt><dd>RFC 9846: TLS</dd></dl>' if '/info/' in url else body
        result=checker.check_link('https://www.rfc-editor.org/rfc/rfc8446.html#section-4',Path('day.html'),fetch=fetch)
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['excerpt'], '4 . Handshake Protocol First paragraph.')
        self.assertEqual(result['obsoleted_by'], 'RFC 9846')

    def test_status_absent_and_status_fetch_failure_keep_link_exit_semantics(self):
        self.assertIsNone(checker.obsoleted_by(checker.BeautifulSoup('<p>Obsoletes RFC 1. Obsoleted by RFC 6298 in another reference.</p>', 'html.parser')))
        def fetch(url, timeout):
            if '/info/' in url: raise TimeoutError('offline')
            return url,'text/html',b'<h1>RFC</h1>'
        result=checker.check_link('https://www.rfc-editor.org/rfc/rfc1.html',Path('day.html'),fetch=fetch)
        self.assertEqual(result['status'], 'pass')
        self.assertIn('Unverified RFC status', result['rfc_status_note'])

    def test_missing_fragment_fails_even_with_http_success(self):
        result = checker.check_link("https://cloud.google.com/example#wrong", Path("day.html"), fetch=self.fetch)
        self.assertEqual(result["status"], "unverified")
        self.assertIn("Missing section fragment", result["error"])

    def test_encoded_and_legacy_fragment(self):
        result = checker.check_link("https://cloud.google.com/example#%6cegacy", Path("day.html"), fetch=self.fetch)
        self.assertEqual(result["status"], "pass")

    def test_http_errors_and_timeouts_are_unverified(self):
        for error in (HTTPError("https://example.com", 404, "Not Found", {}, None), HTTPError("https://example.com", 403, "Forbidden", {}, None), TimeoutError("timed out")):
            def failed_fetch(url, timeout):
                raise error
            result = checker.check_link("https://example.com", Path("day.html"), fetch=failed_fetch)
            self.assertEqual(result["status"], "unverified")
            self.assertIn(type(error).__name__, result["error"])

    def test_non_html_fragment_not_silently_passed(self):
        result = checker.check_link("https://example.com/file.pdf#section", Path("day.html"), fetch=lambda u, t: (u, "application/pdf", b"pdf"))
        self.assertEqual(result["status"], "unverified")

    def test_local_targets_and_fragments(self):
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / "day.html"
            page.write_text('<h2 id="here">Here</h2>')
            self.assertEqual(checker.check_link("#here", page)["status"], "pass")
            self.assertEqual(checker.check_link("#missing", page)["status"], "unverified")
            self.assertEqual(checker.check_link("absent.html", page)["status"], "unverified")

    def test_unsupported_scheme_and_empty_section(self):
        self.assertEqual(checker.check_link("javascript:void(0)", Path("day.html"))["status"], "unverified")
        self.assertEqual(checker.study_links("<h4>Further study</h4><p>No source</p>"), [])


if __name__ == "__main__":
    unittest.main()
