import contextlib
import io
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

from scripts import day_run


class DayRunTests(unittest.TestCase):
    def test_masks_remote_userinfo_and_common_tokens(self):
        text = (
            "https://user:token@example.test/repo "
            "github_pat_abcdefghijklmnopqrstuvwxyz123456 "
            "Authorization: Bearer abc.def.ghi access_token=visible"
        )
        masked = day_run.mask_credentials(text)
        self.assertNotIn("user:token", masked)
        self.assertNotIn("github_pat_", masked)
        self.assertNotIn("abc.def.ghi", masked)
        self.assertNotIn("visible", masked)
        self.assertGreaterEqual(masked.count("***"), 4)

    def test_permitted_commit_scope_is_day_specific(self):
        allowed = (
            "scratch/day_data_007.py", "content/day-007-page.html",
            "days/day-007.html", "scratch/day-007-rules.json",
            "scratch/audits/day-007-terms.txt", "scratch/handoffs/day-007.md",
            "data/coverage.csv",
        )
        self.assertTrue(all(day_run.permitted_day_path(path, 7) for path in allowed))
        self.assertFalse(day_run.permitted_day_path("days/day-008.html", 7))
        self.assertFalse(day_run.permitted_day_path("scripts/build.py", 7))

    def test_check_order_stops_on_first_failure_and_masks_output(self):
        seen = []

        def runner(cmd, **kwargs):
            name = Path(cmd[2]).name
            seen.append(name)
            code = 1 if name == "validate_spec.py" else 0
            return subprocess.CompletedProcess(cmd, code, "access_token=visible\n")

        with patch.object(Path, "exists", return_value=True), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            status = day_run.check(7, runner=runner)
        self.assertEqual(status, 1)
        self.assertEqual(seen, ["extract_day_inputs.py", "validate_spec.py"])
        self.assertNotIn("visible", output.getvalue())

    def test_check_runs_page_rules_before_handoff(self):
        seen = []

        def runner(cmd, **kwargs):
            seen.append(Path(cmd[2]).name)
            return subprocess.CompletedProcess(cmd, 0, "")

        with patch.object(Path, "exists", return_value=True), \
             patch.object(Path, "is_file", return_value=True), \
             contextlib.redirect_stdout(io.StringIO()):
            status = day_run.check(7, runner=runner)
        self.assertEqual(status, 0)
        self.assertEqual(seen, [
            "extract_day_inputs.py", "validate_spec.py", "author_engine.py",
            "build.py", "validate.py", "check_study_links.py", "run_labs.py",
            "check_page_rules.py", "write_handoff.py",
        ])

    def test_prompt_day_contains_only_six_switches(self):
        prompt = (day_run.ROOT / "PROMPT_DAY.md").read_text().splitlines()
        self.assertLess(len(prompt), 40)
        self.assertEqual(
            [line.split("=", 1)[0] for line in prompt],
            ["DAY", "SCOPE", "DIAGRAMS", "TOPICS", "EXTRA_TOPICS", "IMPROVEMENTS"],
        )


if __name__ == "__main__":
    unittest.main()
