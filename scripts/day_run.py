#!/usr/bin/env python3
"""Driver for the mechanical steps of the per-day workflow.

Runs Step 0, the branch preflight, the pre-commit gate, and the scoped commit
and push, so the model only does judgment work (content, scenarios, labs,
diagram accuracy). It never authors, builds or edits page content and it never
pushes main.

  python3 scripts/day_run.py --day 14 --stage resolve --scope fix --diagrams allow --topics expand
  python3 scripts/day_run.py --day 14 --stage preflight          # creates branch day-014 from updated main
  python3 scripts/day_run.py --day 14 --stage check              # page-rule checker only, any branch
  python3 scripts/day_run.py --day 14 --stage gate               # checker + batch_gate + extra gate checks
  python3 scripts/day_run.py --day 14 --stage commit             # needs a fresh gate pass
  python3 scripts/day_run.py --day 14 --stage finish             # gate, then commit and push

Exit status 0 means every requested check passed; 1 means a check failed or the
run STOPPED (the reason is printed). Nothing is repaired by force.
"""
import argparse
import csv
import hashlib
import html
import io
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = 'main'
STAGES = ('resolve', 'preflight', 'check', 'gate', 'commit', 'finish')
SCOPES = ('plan', 'update', 'audit-only', 'fix')
SPECIAL_DAYS = {17, 35, 67, 82, 118, 174, 175, 176, 177, 178, 179}
ANCHOR_COLUMNS = ('overview_anchor', 'technical_anchor', 'problem_anchor', 'lab_anchor')
URL_CREDENTIAL = re.compile(r'(https?://)[^/@\s]+@', re.I)
SECRET_PATTERNS = (
    re.compile(r'\b(?:gh[opusr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b'),
    re.compile(r'(?i)\b(Bearer\s+)[A-Za-z0-9._~+/=-]+'),
    re.compile(r'(?i)\b((?:access_?token|api_?key|password|passwd|secret)\s*[=:]\s*)[^\s]+'),
)


class Stop(Exception):
    """A check failed; report and stop without repairing anything."""


def scrub(text):
    """Mask credentials embedded in remote URLs before anything is printed."""
    text = URL_CREDENTIAL.sub(r'\1***@', text)
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(lambda match: (match.group(1) if match.lastindex else '') + '***', text)
    return text


def mask_credentials(value):
    """Backward-compatible public name for credential masking."""
    return scrub(value)


def say(message=''):
    print(scrub(message), flush=True)


def run(cmd, cwd=ROOT):
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    return proc.returncode, scrub(proc.stdout or '')


def git(*args, check=True):
    rc, out = run(['git', *args])
    if check and rc:
        raise Stop(f'git {" ".join(args[:2])} failed (exit {rc}): {out.strip()[-500:]}')
    return out.strip()


def git_ok(*args):
    return run(['git', *args])[0] == 0


def step(ok, label, detail=''):
    say(f'{"PASS" if ok else "FAIL"}  {label}' + (f': {detail}' if detail else ''))


class Day:
    def __init__(self, number):
        self.n = number
        self.nnn = f'{number:03d}'
        self.branch = f'day-{self.nnn}'
        self.page = ROOT / 'days' / f'day-{self.nnn}.html'
        self.override = ROOT / 'content' / f'day-{self.nnn}-page.html'
        self.audit_files = [
            f'scratch/audits/day-{self.nnn}-audit.json',
            f'scratch/audits/day-{self.nnn}-terms.txt',
            f'scratch/day-{self.nnn}-rules.json',
            f'scratch/day-{self.nnn}-lab-rerun.json',
        ]
        self.owned = set(self.audit_files) | {
            f'content/day-{self.nnn}-page.html',
            f'days/day-{self.nnn}.html',
            f'scratch/day_data_{self.nnn}.py',
            f'scratch/day-{self.nnn}-study-links.json',
            f'scratch/handoffs/day-{self.nnn}.md',
            'data/coverage.csv',
        }

    def owns(self, path):
        return path in self.owned or path.startswith(f'scratch/day_data_{self.nnn}/')

    def spec_files(self):
        single = ROOT / 'scratch' / f'day_data_{self.nnn}.py'
        folder = ROOT / 'scratch' / f'day_data_{self.nnn}'
        if single.exists():
            return [single]
        return sorted(folder.rglob('*.py')) if folder.is_dir() else []


def permitted_day_path(path, day):
    """Return whether a path belongs to one day's scoped commit."""
    return Day(day).owns(path)


def _workflow_command(script, day, *extra):
    return [sys.executable, '-B', str(ROOT / 'scripts' / script), '--day', str(day), *extra]


def _run_workflow_command(command, runner):
    result = runner(
        command,
        cwd=ROOT,
        env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    say(result.stdout or '')
    return result.returncode


def check(day, *, diagrams='allow', skip_labs=False, runner=subprocess.run):
    """Run the legacy complete check sequence, stopping at the first failure.

    The stage-oriented CLI intentionally keeps ``check`` limited to page rules,
    but callers of the original Python API still depend on this complete,
    injectable sequence.
    """
    target = Day(day)
    steps = [_workflow_command('extract_day_inputs.py', day)]
    if not target.spec_files():
        steps.append(_workflow_command('new_day_skeleton.py', day))
    steps.extend((
        _workflow_command('validate_spec.py', day),
        _workflow_command('author_engine.py', day),
        _workflow_command('build.py', day),
        _workflow_command('validate.py', day),
        _workflow_command('check_study_links.py', day, '--report',
                          str(ROOT / 'scratch' / f'day-{day:03d}-study-links.json')),
    ))
    if not skip_labs:
        steps.append(_workflow_command('run_labs.py', day))
    page_rules = _workflow_command('check_page_rules.py', day, '--diagrams', diagrams)
    terms = ROOT / 'scratch' / 'audits' / f'day-{day:03d}-terms.txt'
    if terms.is_file():
        page_rules.extend(('--terms-file', str(terms)))
    steps.extend((page_rules, _workflow_command('write_handoff.py', day)))

    for command in steps:
        if _run_workflow_command(command, runner):
            say(f'FAIL: stopped at {Path(command[2]).name}')
            return 1
    say(f'PASS: Day {day:03d} checks')
    if skip_labs:
        say('NOT CHECKED: labs were explicitly skipped; record the cloud/tool reason in the handoff.')
    return 0


# ------------------------------------------------------------------ Step 0
def stage_resolve(day, args):
    if args.topics != 'add' and args.extra_topic:
        raise Stop('EXTRA_TOPICS is set but TOPICS is not "add"')
    if args.topics == 'add' and not args.extra_topic:
        raise Stop('TOPICS=add needs at least one --extra-topic "title | reason"')
    for item in args.extra_topic:
        if '|' not in item:
            raise Stop(f'extra topic must be "title | one-line reason": {item!r}')
    say(f'Day {day.n} | {day.nnn} | branch {day.branch} | SCOPE={args.scope} '
        f'DIAGRAMS={args.diagrams} TOPICS={args.topics}')
    say('EXTRA_TOPICS: ' + ('; '.join(args.extra_topic) if args.extra_topic else 'none'))
    say('IMPROVEMENTS: ' + ('; '.join(args.improvement) if args.improvement else 'none'))
    if day.n in SPECIAL_DAYS:
        say(f'NOTE: Day {day.n} is a gate or capstone day. Confirm its roadmap entry fits the '
            'four-topic template before authoring; this script cannot read the roadmap.')
    if args.diagrams == 'allow' and not (ROOT / 'scripts' / 'compact_hierarchy.py').exists():
        say('NOTE: scripts/compact_hierarchy.py is missing: author flow diagrams only and list '
            'each needed hierarchy diagram under "Diagram recommendations" in the handoff.')
    say('NOTE: this script cannot detect a different day number in your files or messages; check that yourself.')


# --------------------------------------------------------------- Preflight
def check_status(day, args):
    allowed = set(day.audit_files)
    dirty = []
    for line in git('status', '--porcelain', '--untracked-files=all').splitlines():
        path = line[3:].split(' -> ')[-1].strip('"')
        if path in allowed:
            continue
        if args.ignore_pycache and '__pycache__/' in path:
            continue
        dirty.append(line)
    if dirty:
        raise Stop('working tree has uncommitted changes (commit or stash them; `git add .` would stage them):\n  '
                   + '\n  '.join(dirty[:20]) + (f'\n  ... {len(dirty) - 20} more' if len(dirty) > 20 else ''))
    step(True, 'working tree clean', 'apart from this day\'s own audit files')


def check_pushed(exclude):
    fmt = '%(refname:short)%09%(upstream:short)%09%(upstream:track)'
    bad = []
    for line in git('for-each-ref', 'refs/heads', f'--format={fmt}').splitlines():
        parts = line.split('\t')
        name, upstream = parts[0], parts[1] if len(parts) > 1 else ''
        track = parts[2] if len(parts) > 2 else ''
        if name in exclude:
            continue
        if not upstream:
            bad.append(f'{name}: no upstream')
        elif 'ahead' in track:
            bad.append(f'{name}: {track}')
    if bad:
        raise Stop('branches not fully pushed:\n  ' + '\n  '.join(bad))
    step(True, 'all branches pushed')


def _branch_name(line):
    """Remove git branch's current-branch and linked-worktree markers."""
    return line.strip().lstrip('*+').strip()


def _patch_equivalent_to_main(name):
    """Return whether a non-ancestor branch has no changes missing from main."""
    cherry = git('cherry', 'origin/main', name, check=False).splitlines()
    markers = [line[:1] for line in cherry if line[:1] in ('+', '-')]
    if markers:
        return all(marker == '-' for marker in markers)
    # git cherry omits merge commits. An empty branch-side three-dot diff proves
    # that a merge-only historical branch contributes no content missing from main.
    return git_ok('diff', '--quiet', f'origin/main...{name}')


def check_merged(exclude):
    bad = []
    for flags in (['--no-merged', 'origin/main'], ['-r', '--no-merged', 'origin/main']):
        for line in git('branch', *flags).splitlines():
            name = _branch_name(line)
            if not name or '->' in name or name in ('origin/main', MAIN) or name in exclude:
                continue
            if _patch_equivalent_to_main(name):
                continue
            last = git('log', '-1', '--format=%h %s', name, check=False)
            bad.append(f'{name}  (last commit: {last})')
    if bad:
        raise Stop('branches not merged into origin/main (if the repo squash-merges, these may be false '
                   'positives: confirm before continuing):\n  ' + '\n  '.join(bad))
    step(True, 'all branches merged into origin/main')


def stage_preflight(day, args):
    if args.scope in ('plan', 'audit-only'):
        raise Stop(f'SCOPE={args.scope} creates no branch; preflight applies to update and fix only')
    if not git_ok('fetch', '--all', '--prune'):
        raise Stop('git fetch --all --prune failed')
    step(True, '1 fetch --all --prune')
    check_status(day, args)
    exclude = {day.branch, f'origin/{day.branch}'}
    check_pushed(exclude)
    check_merged(exclude)
    if args.check_only:
        step(True, '5 main up to date', 'skipped (--check-only)')
    else:
        git('switch', MAIN)
        if not git_ok('pull', '--ff-only', 'origin', MAIN):
            raise Stop('git pull --ff-only origin main failed; main has local commits or diverged. Never push main.')
        local, remote = git('rev-parse', MAIN), git('rev-parse', f'origin/{MAIN}')
        if local != remote:
            raise Stop(f'main ({local[:9]}) differs from origin/main ({remote[:9]}); fix this by hand, never push main')
        step(True, '5 main up to date', local[:9])
    if git_ok('rev-parse', '--verify', '--quiet', f'refs/heads/{day.branch}'):
        raise Stop(f'branch {day.branch} already exists locally')
    if git_ok('rev-parse', '--verify', '--quiet', f'refs/remotes/origin/{day.branch}'):
        raise Stop(f'branch {day.branch} already exists on origin')
    step(True, f'6 branch {day.branch} does not exist yet')
    if args.check_only:
        say('7 branch not created (--check-only)')
    else:
        git('switch', '-c', day.branch)
        step(True, f'7 created {day.branch} from main', git('rev-parse', '--short', MAIN))


# -------------------------------------------------------------------- Gate
def sha(*paths):
    h = hashlib.sha256()
    for p in paths:
        h.update(str(p.relative_to(ROOT)).encode())
        h.update(p.read_bytes() if p.exists() else b'<missing>')
    return h.hexdigest()


def coverage_rows(day):
    path = ROOT / 'data' / 'coverage.csv'
    return [r for r in csv.DictReader(path.open(encoding='utf-8')) if str(r.get('day', '')).strip() == str(day.n)]


def check_anchors(day, page_html):
    rows = coverage_rows(day)
    if not rows:
        return False, f'no rows for Day {day.n} in data/coverage.csv'
    missing = []
    for row in rows:
        for col in ANCHOR_COLUMNS:
            anchor = (row.get(col) or '').strip().lstrip('#')
            if anchor and not re.search(r'id=["\']' + re.escape(anchor) + r'["\']', page_html):
                missing.append(f'{row.get("topic_key", "?")}:{col}={anchor}')
    return (not missing), (f'{len(rows)} rows, all anchors present' if not missing else 'missing ' + ', '.join(missing[:10]))


def changed_paths(args):
    changed = set(git('diff', '--name-only', MAIN).splitlines())
    changed |= set(git('ls-files', '--others', '--exclude-standard').splitlines())
    return {p for p in changed if p and not (args.ignore_pycache and '__pycache__/' in p)}


def current_branch():
    return git('branch', '--show-current')


def run_rules(day, args):
    cmd = [sys.executable, '-B', str(ROOT / 'scripts' / 'check_page_rules.py'), '--day', str(day.n),
           '--diagrams', args.diagrams, '--json', f'scratch/day-{day.nnn}-rules.json']
    terms = ROOT / 'scratch' / 'audits' / f'day-{day.nnn}-terms.txt'
    if terms.exists():
        cmd += ['--terms-file', str(terms)]
    else:
        say('NOTE: no scratch/audits/day-%s-terms.txt; R3 only checks strong.keyword spans.' % day.nnn)
    rc, out = run(cmd)
    say(out.rstrip())
    return rc == 0


def stage_check(day, args):
    if not day.page.exists():
        raise Stop(f'{day.page.relative_to(ROOT)} does not exist; build the day first')
    ok = run_rules(day, args)
    step(ok, 'page-rule checker (R1-R5, R7, R8)')
    return ok


def stage_gate(day, args):
    if not day.page.exists():
        raise Stop(f'{day.page.relative_to(ROOT)} does not exist; build the day first')
    if current_branch() != day.branch:
        raise Stop(f'current branch is {current_branch() or "(detached)"}, expected {day.branch}; run preflight first')
    results = []

    ok = run_rules(day, args)
    results.append(ok)
    step(ok, 'page-rule checker (R1-R5, R7, R8)')

    cmd = [sys.executable, '-B', str(ROOT / 'scripts' / 'batch_gate.py'), '--day', str(day.n), '--contract-hash']
    if args.skip_labs:
        cmd.append('--skip-labs')
    rc, out = run(cmd)
    say(out.rstrip())
    results.append(rc == 0)
    step(rc == 0, 'batch_gate.py' + (' (labs skipped)' if args.skip_labs else ''))

    todo = 0
    for f in day.spec_files() + ([day.override] if day.override.exists() else []):
        todo += len(re.findall(r'\bTODO\b', f.read_text(encoding='utf-8')))
    results.append(todo == 0)
    step(todo == 0, 'no TODO left in spec or page override', f'{todo} found' if todo else '')

    page_html = day.page.read_text(encoding='utf-8')
    ok, detail = check_anchors(day, page_html)
    results.append(ok)
    step(ok, 'coverage.csv anchors exist on built page', detail)

    stray = sorted(p for p in changed_paths(args) if not day.owns(p))
    results.append(not stray)
    step(not stray, f'only Day {day.n} files changed (no shared script or template edited)',
         ', '.join(stray[:10]) if stray else '')

    code, svg = len(re.findall(r'<pre\b', page_html)), len(re.findall(r'<svg\b', page_html))
    depth_ok = code >= args.min_code and svg >= args.min_svg
    say(f'{"PASS" if depth_ok else ("FAIL" if args.strict_depth else "WARN")}  depth floor: '
        f'{code} code blocks (min {args.min_code}), {svg} SVGs (min {args.min_svg})')
    if args.strict_depth:
        results.append(depth_ok)

    passed = all(results)
    if passed and not args.skip_labs:
        stamp_dir = Path(ROOT / git('rev-parse', '--git-dir')) / 'day_run'
        stamp_dir.mkdir(exist_ok=True)
        (stamp_dir / f'day-{day.nnn}.pass').write_text(json.dumps({
            'time': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'files': current_hashes(day),
        }, indent=1))
    say('GATE: ' + ('PASS' if passed else 'FAIL; do not commit or push'))
    if passed and args.skip_labs:
        say('NOTE: labs were skipped, so no commit stamp was written; rerun without --skip-labs before committing.')
    return passed


def current_hashes(day):
    rows = json.dumps(coverage_rows(day), sort_keys=True)
    return {
        'page': sha(day.page),
        'override': sha(day.override),
        'spec': sha(*day.spec_files()) if day.spec_files() else '',
        'coverage_rows': hashlib.sha256(rows.encode()).hexdigest(),
    }


# ------------------------------------------------------------ Commit, push
def other_coverage_rows_unchanged():
    def other(text, n_day):
        reader = csv.DictReader(io.StringIO(text))
        rows = [tuple((r.get(k) or '') for k in reader.fieldnames) for r in reader if str(r.get('day', '')).strip() != n_day]
        return reader.fieldnames, sorted(rows)
    return other


def check_coverage_scope(day):
    rc_old, old = run(['git', 'show', 'HEAD:data/coverage.csv'])
    rc_new, new = run(['git', 'show', ':data/coverage.csv'])
    if rc_old or rc_new:
        raise Stop('cannot read data/coverage.csv from HEAD or the index')
    other = other_coverage_rows_unchanged()
    if other(old, str(day.n)) != other(new, str(day.n)):
        raise Stop(f'data/coverage.csv changes rows outside Day {day.n} (or its header); git reset and fix')
    step(True, f'data/coverage.csv changes only Day {day.n} rows')


def page_title(day):
    match = re.search(r'<title>\s*Day\s+\d+\s*:\s*(.*?)\s*(?:·|\||</title>)', day.page.read_text(encoding='utf-8'), re.S)
    if not match:
        raise Stop('cannot read the day title from the built page <title>')
    return html.unescape(re.sub(r'\s+', ' ', match.group(1))).strip()


def stage_commit(day, args):
    if day.branch == MAIN or current_branch() == MAIN:
        raise Stop('refusing to commit or push on main')
    if current_branch() != day.branch:
        raise Stop(f'current branch is {current_branch() or "(detached)"}, expected {day.branch}')
    stamp = Path(ROOT / git('rev-parse', '--git-dir')) / 'day_run' / f'day-{day.nnn}.pass'
    if not stamp.exists():
        raise Stop('no gate pass on record: run --stage gate (without --skip-labs) first')
    if json.loads(stamp.read_text())['files'] != current_hashes(day):
        raise Stop('files changed since the gate passed: rerun --stage gate')
    step(True, 'gate pass is current for the page, override, spec and coverage rows')

    git('add', '.')
    staged = [p for p in git('diff', '--cached', '--name-only').splitlines() if p]
    stray = [p for p in staged if not day.owns(p)]
    if stray:
        git('reset', '-q')
        raise Stop('paths outside Day %d were staged and have been unstaged:\n  %s' % (day.n, '\n  '.join(stray)))
    if not staged:
        raise Stop('nothing staged: there is nothing to commit')
    check_coverage_scope(day)
    say(git('diff', '--cached', '--stat'))
    message = f'Day {day.n}: {page_title(day)}'
    if args.dry_run:
        git('reset', '-q')
        say(f'DRY RUN: would commit "{message}" and push {day.branch}; index reset')
        return
    exclude = {day.branch, f'origin/{day.branch}'}
    check_pushed(exclude)
    check_merged(exclude)
    git('commit', '-m', message)
    commit = git('rev-parse', '--short', 'HEAD')
    step(True, 'committed', f'{commit} "{message}"')
    if args.no_push:
        say(f'NOT PUSHED (--no-push). Branch {day.branch}, commit {commit}.')
        return
    rc, out = run(['git', 'push', '-u', 'origin', day.branch])
    if rc:
        raise Stop('git push failed:\n' + out.strip()[-500:])
    step(True, f'pushed {day.branch}', commit)
    say(f'Branch: {day.branch} | Commit: {commit}')
    say('Browser audits were not run by this script.')


# --------------------------------------------------------------------- CLI
def parse_args(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--day', type=int, required=True, choices=range(1, 181), metavar='1-180')
    ap.add_argument('action', nargs='?', choices=STAGES,
                    help='workflow stage (positional compatibility form)')
    ap.add_argument('--stage', choices=STAGES,
                    help='workflow stage (equivalent to the positional action)')
    ap.add_argument('--scope', choices=SCOPES, default='update')
    ap.add_argument('--diagrams', choices=('keep', 'allow'), default='allow')
    ap.add_argument('--topics', choices=('keep', 'expand', 'add'), default='keep')
    ap.add_argument('--extra-topic', action='append', default=[], metavar='"title | reason"')
    ap.add_argument('--improvement', action='append', default=[])
    ap.add_argument('--skip-labs', action='store_true', help='gate: skip lab re-runs (no commit stamp is written)')
    ap.add_argument('--ignore-pycache', action='store_true', help='ignore __pycache__ paths in the clean-tree and scope checks')
    ap.add_argument('--check-only', action='store_true', help='preflight: checks 1-4 and 6 only; no switch, pull or branch')
    ap.add_argument('--dry-run', action='store_true', help='commit: run every check, print the stat, then unstage')
    ap.add_argument('--no-push', action='store_true')
    ap.add_argument('--min-code', type=int, default=8, help='depth floor: minimum <pre> blocks')
    ap.add_argument('--min-svg', type=int, default=3, help='depth floor: minimum <svg> diagrams')
    ap.add_argument('--strict-depth', action='store_true', help='make the depth floor a gated failure (default: warning)')
    args = ap.parse_args(argv)
    if args.action and args.stage and args.action != args.stage:
        ap.error('positional action and --stage select different stages')
    args.stage = args.stage or args.action
    if not args.stage:
        ap.error('one workflow stage is required (positional action or --stage)')
    return args


def main(argv=None):
    args = parse_args(argv)
    day = Day(args.day)
    try:
        if args.stage == 'resolve':
            stage_resolve(day, args)
        elif args.stage == 'preflight':
            stage_resolve(day, args)
            stage_preflight(day, args)
        elif args.stage == 'check':
            return 0 if stage_check(day, args) else 1
        elif args.stage == 'gate':
            return 0 if stage_gate(day, args) else 1
        elif args.stage == 'commit':
            stage_commit(day, args)
        elif args.stage == 'finish':
            if not stage_gate(day, args):
                return 1
            stage_commit(day, args)
    except Stop as stop:
        say(f'STOP: {stop}')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
