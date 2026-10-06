#!/usr/bin/env python3
"""Fail-closed serial checks for one completed day; never author or build it."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECKS = ('extract_day_inputs', 'validate_spec', 'validate', 'check_study_links', 'run_labs')


def contract_check(root):
    digest = hashlib.sha256((root / 'PAGE_AUTHORING_CONTRACT.md').read_bytes()).hexdigest()
    path = root / 'scratch/batch-contract.sha256'
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open('x') as stream: stream.write(digest + '\n')
    except FileExistsError:
        if path.read_text().strip() != digest: return False
    return True


def report_failure(check, output, root, day):
    if re.search(r'WARN[^\n]*diagram[ -]count', output, re.I): return 'diagram-count WARN'
    if check == 'check_study_links':
        report = json.loads((root / 'scratch' / f'day-{day:03d}-study-links.json').read_text())
        if report.get('unverified') or report.get('error') or not report.get('links'): return 'unverified links or empty link report'
        for link in report['links']:
            if link.get('status') != 'pass' or str(link.get('rfc_status_note', '')).startswith('Unverified'):
                return 'unverified link or RFC status'
    if check == 'run_labs':
        report = json.loads((root / 'scratch' / f'day-{day:03d}-lab-rerun.json').read_text())
        if report.get('status') != 'PASS' or not report.get('labs'): return 'failed or SKIPPED lab'
        for lab in report['labs']:
            if lab.get('status') != 'PASS' or lab.get('exit_status') != 0 or lab.get('missing_artifacts'):
                return 'failed or SKIPPED lab tool / missing artifact'
            if len(lab.get('stages', [])) != 8 or any(s.get('status') != 'PASS' for s in lab['stages']):
                return 'failed or SKIPPED stage'
    return None


def main(argv=None, *, root=ROOT, runner=subprocess.run):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--day', type=int, required=True, choices=range(1, 181))
    parser.add_argument('--contract-hash', action='store_true', help='Pin and check canonical contract sha256')
    parser.add_argument('--skip-labs', '--no-labs', action='store_true', help='Skip lab re-runs')
    args = parser.parse_args(argv)
    checks = tuple(c for c in CHECKS if not (args.skip_labs and c == 'run_labs'))
    try:
        if args.contract_hash and not contract_check(root):
            print('FAIL: contract-hash (PAGE_AUTHORING_CONTRACT.md changed)'); return 1
        for check in checks:
            command = [sys.executable, '-B', str(root / 'scripts' / f'{check}.py'), '--day', str(args.day)]
            if check == 'check_study_links':
                report_path = root / 'scratch' / f'day-{args.day:03d}-study-links.json'
                command += ['--report', str(report_path)]
            elif check == 'run_labs':
                report_path = root / 'scratch' / f'day-{args.day:03d}-lab-rerun.json'
            # Reject stale evidence if a check exits without writing a fresh report.
            if check in ('check_study_links', 'run_labs') and report_path.exists(): report_path.unlink()
            result = runner(command, cwd=root, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print(result.stdout, end='' if result.stdout.endswith('\n') else '\n', flush=True)
            failure = report_failure(check, result.stdout, root, args.day)
            if result.returncode or failure:
                print(f'FAIL: {check} ({failure or "exit " + str(result.returncode)})'); return 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'FAIL: {locals().get("check", "contract-hash")} ({type(exc).__name__}: {exc})'); return 1
    print(f'PASS: Day {args.day:03d} batch gate'); return 0


if __name__ == '__main__': raise SystemExit(main())
