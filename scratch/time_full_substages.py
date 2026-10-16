import subprocess, time
from pathlib import Path
import sys
ROOT = Path(".").resolve()
sys.path.insert(0, str(ROOT))
from scripts.validate_spec import load_spec
from scripts.run_labs import extract_stage

data, _, _ = load_spec(Path("scratch/day_data_010.py"))
st8 = extract_stage(data['topics'][0]['lab']['steps'][7])

# In run_labs, commands run sequentially in the same shell (NOT in subshells)!
lines = ["set -euo pipefail"]
for i, c in enumerate(st8['commands']):
    lines.append(f'echo "=== Command {i+1} start ==="')
    lines.append(f't_start=$(date +%s%N)')
    lines.append(c)
    lines.append(f'echo "=== Command {i+1} done in $((($(date +%s%N) - t_start)/1000000)) ms ==="')

script = Path("/tmp/test_st8_full.sh")
script.write_text("\n".join(lines) + "\n")
t0 = time.time()
p = subprocess.run(["bash", str(script)], capture_output=True, text=True)
print(f"Total return code: {p.returncode}, elapsed: {round(time.time() - t0, 2)}s")
print("Stdout:")
print(p.stdout)
print("Stderr:")
print(p.stderr)
