# Let's inspect the exact commands extracted from steps[7]
import sys
from pathlib import Path
ROOT = Path(".").resolve()
sys.path.insert(0, str(ROOT))
from scripts.validate_spec import load_spec
from scripts.run_labs import extract_stage

data, _, _ = load_spec("scratch/day_data_010.py")
step8_info = extract_stage(data['topics'][0]['lab']['steps'][7])
print("Step 8 artifacts required:", step8_info['artifacts'])
print("Step 8 commands count:", len(step8_info['commands']))
for idx, cmd in enumerate(step8_info['commands']):
    print(f"--- Command {idx+1} (first 200 chars) ---")
    print(cmd[:200])
