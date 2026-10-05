import re
import ast

with open('scratch/day_data_013.py') as f:
    text = f.read()

data_dict = ast.literal_eval(text.split('DATA = ')[1].rstrip())

for t in data_dict['topics']:
    for s_idx, step in enumerate(t['lab']['steps']):
        blocks = re.findall(r'```bash\n(.*?)```', step, re.DOTALL)
        for b in blocks:
            py_files = re.findall(r"cat <<'EOF' > (\S+\.py)\n(.*?)\nEOF", b, re.DOTALL)
            for py_name, py_code in py_files:
                try:
                    compile(py_code, py_name, 'exec')
                    print(f'Topic {t["key"]} Stage {s_idx+1} {py_name}: VALID')
                except SyntaxError as e:
                    print(f'Topic {t["key"]} Stage {s_idx+1} {py_name}: SYNTAX ERROR at line {e.lineno}: {e.msg}')
                    lines = py_code.splitlines()
                    for ln in range(max(0, e.lineno-3), min(len(lines), e.lineno+2)):
                        print(f'  {ln+1}: {lines[ln]}')
