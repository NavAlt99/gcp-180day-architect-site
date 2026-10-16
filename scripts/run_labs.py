#!/usr/bin/env python3
"""Rerun local shell lab stages from a durable spec in disposable workspaces.

This executes authored commands, not a security sandbox. Cloud/manual stages and
non-shell blocks fail closed as SKIPPED. Save paths must be explicit file paths.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.validate_spec import load_spec, soup


def extract_stage(text):
    doc = soup(text)
    blocks = doc.select('pre code')
    commands, unsupported = [], []
    for block in blocks:
        languages = [c.removeprefix('language-') for c in block.get('class', []) if c.startswith('language-')]
        if languages and languages[0] not in ('bash', 'sh', 'shell'):
            unsupported.append(languages[0])
        else:
            commands.append(block.get_text())
    metadata_doc = soup(str(doc))
    for pre in metadata_doc.select('pre'): pre.decompose()
    plain = metadata_doc.get_text(' ', strip=True)
    save = re.search(r'Save:\s*(.*)', plain)
    save_text = save.group(1) if save else ''
    # All explicit filenames, including paths in prose or comma-separated lists.
    paths = re.findall(r'(?:\$\{?LAB_DIR\}?/|\./)?[\w./-]+\.[\w.-]+', save_text)
    if re.fullmatch(r'[\w${}/.-]+', save_text.strip()):
        paths = [save_text.strip()]
    paths = list(dict.fromkeys(p.rstrip('.,;') for p in paths))
    location = re.search(r'Location:\s*([^\n]+)', plain)
    local = bool(location and re.match(r'local(?: [\w/-]+){0,4} terminal\b', location.group(1), re.I))
    tools = list(dict.fromkeys(re.findall(r'\bcommand\s+-v\s+([\w.+-]+)', '\n'.join(commands))))
    return {'commands': commands, 'artifacts': paths, 'save': save_text,
            'tools': tools, 'unsupported': unsupported, 'local': local}


def run_lab(topic, timeout=60):
    stages = [extract_stage(s) for s in topic.get('lab', {}).get('steps', [])]
    result = {'topic': topic.get('key'), 'name': topic.get('lab', {}).get('name'),
              'status': 'FAIL', 'exit_status': None, 'missing_artifacts': [], 'stages': []}
    if len(stages) != 8:
        result['error'] = 'Expected exactly eight stages'
        return result
    for i, stage in enumerate(stages, 1):
        missing_tools = [t for t in dict.fromkeys(stage['tools'] + (['bash', 'python3'] if i == 1 else [])) if shutil.which(t) is None]
        reason = ('missing tool(s): ' + ', '.join(missing_tools) if missing_tools else
                  'manual/cloud stage or unsupported code block' if not stage['local'] or not stage['commands'] or stage['unsupported'] else '')
        result['stages'].append({'stage': i, 'status': 'SKIPPED' if reason else 'NOT_RUN',
                                 'missing_tools': missing_tools, 'reason': reason,
                                 'artifacts': [], 'missing_artifacts': []})
    if any(s['status'] == 'SKIPPED' for s in result['stages']):
        result['status'] = 'SKIPPED'
        return result
    with tempfile.TemporaryDirectory(prefix='curriculum-lab-') as temporary:
        work = Path(temporary)
        manifest = work / 'manifest.json'
        events = work / 'events.jsonl'
        manifest.write_text(json.dumps(stages))
        # Shim absolute mktemp templates into this lab's owned temp directory.
        # Bash state (cd, variables, background PIDs) persists across all stages.
        shim = work / 'bin'; shim.mkdir()
        mktemp = shutil.which('mktemp')
        if mktemp:
            (shim / 'mktemp').write_text('#!/usr/bin/env python3\nimport os,sys\na=[os.path.join(os.environ["LAB_RUN_ROOT"],os.path.basename(x)) if x.startswith("/tmp/") else x for x in sys.argv[1:]]\nos.execv(' + repr(mktemp) + ',[' + repr(mktemp) + ']+a)\n')
            (shim / 'mktemp').chmod(0o755)
        helper = work / 'record.py'
        helper.write_text('''import hashlib,json,os,pathlib,sys
root=pathlib.Path(os.environ['LAB_RUN_ROOT']).resolve()
stage=int(sys.argv[1]); event=sys.argv[2]
data=json.loads((root/'manifest.json').read_text())[stage-1]
record={'stage':stage,'event':event,'artifacts':[],'missing_artifacts':[]}
if event in ('finish','abort'):
 for name in data['artifacts']:
  name=os.path.expandvars(name)
  path=pathlib.Path(name).resolve()
  ok=path.is_relative_to(root) and path.is_file()
  record['artifacts'].append({'path':name,'exists':ok,'sha256':hashlib.sha256(path.read_bytes()).hexdigest() if ok else None})
  if not ok: record['missing_artifacts'].append(name)
 if not data['artifacts']: record['missing_artifacts'].append('(no explicit Save path)')
with (root/'events.jsonl').open('a') as stream: stream.write(json.dumps(record)+'\\n')
if record['missing_artifacts']: sys.exit(1)
''')
        record = shlex.quote(sys.executable) + ' ' + shlex.quote(str(helper))
        guard = '''guard_lab_tool() {
  local cmd="$1" tool
  if [[ "$cmd" =~ ^[[:space:]]*([a-zA-Z0-9_./+-]+)([[:space:]]|$) ]]; then
    tool="${BASH_REMATCH[1]}"
    case "$tool" in if|then|else|elif|fi|for|while|until|do|done|case|esac|in|function) return ;; esac
    if ! builtin type -t -- "$tool" >/dev/null 2>&1; then
      printf 'SKIPPED_TOOL stage=%s tool=%s\\n' "$LAB_STAGE" "$tool" >&2
      exit 125
    fi
  fi
}
trap 'guard_lab_tool "$BASH_COMMAND"' DEBUG
'''
        lines = ['set -euo pipefail', 'LAB_STAGE=0', guard, f"trap 'rc=$?; if [ \"$LAB_STAGE\" -gt 0 ]; then {record} \"$LAB_STAGE\" abort || :; fi; exit \"$rc\"' EXIT"]
        for i, stage in enumerate(stages, 1):
            lines += [f'LAB_STAGE={i}', f'{record} {i} start', *stage['commands'], f'{record} {i} finish', 'LAB_STAGE=0']
        script = work / 'run.sh'; script.write_text('\n'.join(lines) + '\n')
        env = {**os.environ, 'LAB_RUN_ROOT': temporary, 'HOME': temporary,
               'TMPDIR': temporary, 'PATH': str(shim) + os.pathsep + os.environ.get('PATH', '')}
        proc = subprocess.Popen(['bash', str(script)], cwd=work, env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
        timed_out = False
        timeout_cwd = work
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            try: timeout_cwd = Path(f'/proc/{proc.pid}/cwd').resolve(strict=True)
            except OSError: pass
            os.killpg(proc.pid, signal.SIGKILL)
            stdout, stderr = proc.communicate()
        finally:
            # Remove background servers even if the shell exited unexpectedly.
            try: os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError: pass
        result.update(exit_status=proc.returncode, timed_out=timed_out, stdout=stdout, stderr=stderr)
        for line in events.read_text().splitlines() if events.exists() else []:
            event = json.loads(line); stage = result['stages'][event['stage'] - 1]
            if event['event'] == 'start':
                stage['status'] = 'FAIL'
            else:
                stage.update(status='FAIL' if event['event'] == 'abort' or event['missing_artifacts'] else 'PASS',
                             artifacts=event['artifacts'], missing_artifacts=event['missing_artifacts'])
                result['missing_artifacts'] += [{'stage': event['stage'], 'path': p} for p in event['missing_artifacts']]
        if timed_out:
            for i, stage in enumerate(result['stages']):
                if stage['status'] == 'FAIL' and not stage['artifacts']:
                    for name in stages[i]['artifacts']:
                        resolved = timeout_cwd / name
                        ok = resolved.resolve().is_relative_to(work) and resolved.is_file()
                        stage['artifacts'].append({'path': name, 'exists': ok})
                        if not ok: stage['missing_artifacts'].append(name)
                    if not stages[i]['artifacts']: stage['missing_artifacts'].append('(no explicit Save path)')
                    result['missing_artifacts'] += [{'stage': i + 1, 'path': name} for name in stage['missing_artifacts']]
        if proc.returncode in (125, 127):
            for stage in result['stages']:
                if stage['status'] == 'FAIL':
                    stage.update(status='SKIPPED', reason='tool unavailable during execution; see stderr')
                    stage['missing_tools'] += re.findall(r'SKIPPED_TOOL stage=' + str(stage['stage']) + r' tool=(\S+)', stderr)
        if proc.returncode:
            # Retain small diagnostic logs before removing the owned workspace.
            result['diagnostic_logs'] = {}
            for log in work.rglob('*.log'):
                if log.is_file() and not log.is_symlink():
                    with log.open('rb') as stream:
                        stream.seek(max(0, log.stat().st_size - 4000))
                        result['diagnostic_logs'][str(log.relative_to(work))] = stream.read().decode(errors='replace')
        result['status'] = ('SKIPPED' if any(s['status'] == 'SKIPPED' for s in result['stages']) else
                            'PASS' if proc.returncode == 0 and all(s['status'] == 'PASS' for s in result['stages']) else 'FAIL')
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--day', type=int, required=True, choices=range(1, 181))
    parser.add_argument('--spec', type=Path)
    parser.add_argument('--timeout', type=float, default=60, help='Seconds per lab')
    args = parser.parse_args(argv)
    if args.timeout <= 0: parser.error('--timeout must be positive')
    directory = ROOT / 'scratch' / f'day_data_{args.day:03d}'
    path = args.spec or (directory if directory.is_dir() else directory.with_suffix('.py'))
    report = {'day': args.day, 'spec': str(path), 'labs': [], 'status': 'FAIL'}
    try:
        data, _, _ = load_spec(path)
        report['labs'] = [run_lab(t, args.timeout) for t in data.get('topics', [])]
        if report['labs'] and all(l['status'] == 'PASS' for l in report['labs']): report['status'] = 'PASS'
    except Exception as exc:
        report['error'] = f'{type(exc).__name__}: {exc}'
    output = ROOT / 'scratch' / f'day-{args.day:03d}-lab-rerun.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    for lab in report['labs']:
        print(f"{lab['status']}: {lab['topic']} exit={lab['exit_status']} missing={lab['missing_artifacts']}")
        for stage in lab['stages']:
            print(f"  Stage {stage['stage']}: {stage['status']} {stage['reason']}")
    print(f"{report['status']}: labs; report={output}")
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
