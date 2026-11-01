import json
from pathlib import Path
import tempfile
import unittest

from scripts import site_metrics


class SiteMetricsTests(unittest.TestCase):
    def test_measure_day_counts_requested_fields(self):
        html = '''<html><body>
        <a href="https://example.test/a">A</a><a href="local.html">Local</a>
        <strong>Stage 1: Preflight</strong><h4>Stage 2: Prepare</h4>
        <pre>one</pre><pre>two</pre><svg></svg>
        <p>Tabletop check; another tabletop decision.</p>
        </body></html>'''
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            page = root / "day.html"
            override = root / "override.html"
            page.write_text(html, encoding="utf-8")
            override.write_text("override", encoding="utf-8")
            row = site_metrics.measure_day(7, page, override, "Fixture block")
        self.assertEqual(row, {
            "day": 7,
            "block": "Fixture block",
            "bytes": len(html.encode()),
            "pre": 2,
            "svg": 1,
            "external_links": 1,
            "stage_headers": 2,
            "tabletop": 2,
            "override_present": True,
        })

    def test_payload_and_markdown_are_deterministic(self):
        rows = [{"day": 1, "block": "Fixture", "bytes": 10, "pre": 0, "svg": 0,
                 "external_links": 1, "stage_headers": 7, "tabletop": 1,
                 "override_present": False}]
        data = site_metrics.payload(rows)
        self.assertEqual(data["summary"], {
            "days": 1, "zero_pre": 1, "zero_svg": 1,
            "stage_headers_below_8": 1, "overrides_present": 0,
        })
        self.assertIn("| 1 | Fixture | 10 | 0 | 0 | 1 | 7 | 1 | no |", site_metrics.markdown(data))
        self.assertEqual(json.loads(json.dumps(data)), data)


if __name__ == "__main__":
    unittest.main()
