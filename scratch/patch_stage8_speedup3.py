with open("scratch/day_data_010.py") as f:
    text = f.read()

# Replace:
# python3 -c 'import pathlib; [pathlib.Path(f"/build/header-{i}").touch() for i in range(2000)]'
# With:
# awk 'BEGIN { for (i=0; i<2000; i++) print "/build/header-" i }' | xargs touch
old_py = "python3 -c 'import pathlib; [pathlib.Path(f\"/build/header-{i}\").touch() for i in range(2000)]'"
new_awk = "awk 'BEGIN { for (i=0; i<2000; i++) print \"/build/header-\" i }' | xargs touch"
assert old_py in text, "old_py not found"
text = text.replace(old_py, new_awk, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Replaced with instant awk | xargs touch!")
