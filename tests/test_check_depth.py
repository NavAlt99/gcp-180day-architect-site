import contextlib
import io
import unittest
from unittest.mock import patch

from scripts import check_depth


def row(size):
    return {
        "day": 1,
        "block": "Foundations",
        "bytes": size,
        "pre": 2,
        "svg": 1,
        "external_links": 3,
        "stage_headers": 8,
        "tabletop": 0,
        "override_present": True,
    }


class CheckDepthTests(unittest.TestCase):
    def test_evaluate_uses_frozen_floor(self):
        result = check_depth.evaluate(row(265646))
        self.assertFalse(result["passes"])
        self.assertEqual(result["floor_bytes"], 265647)
        self.assertEqual(result["deficit_bytes"], 1)
        self.assertEqual(result["source_days"], [4, 10, 7])

    def test_warning_default_and_strict_failure(self):
        with patch.object(check_depth, "current_rows", return_value=[row(100)]):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(check_depth.main(["--day", "1"]), 0)
            self.assertIn("WARN Day 001 depth", output.getvalue())
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(check_depth.main(["--day", "1", "--strict"]), 1)
            self.assertIn("FAIL Day 001 depth", output.getvalue())

    def test_strict_pass(self):
        with patch.object(check_depth, "current_rows", return_value=[row(265647)]):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(check_depth.main(["--day", "1", "--strict"]), 0)
            self.assertIn("PASS Day 001 depth", output.getvalue())

    def test_missing_floor_fails_closed(self):
        fixture = row(1)
        fixture["block"] = "Unknown"
        with self.assertRaisesRegex(ValueError, "No depth floor"):
            check_depth.evaluate(fixture)


if __name__ == "__main__":
    unittest.main()
