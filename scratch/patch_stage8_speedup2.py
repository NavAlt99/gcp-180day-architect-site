with open("scratch/day_data_010.py") as f:
    text = f.read()

# Replace:
# dd if=/dev/urandom of=/build/cache.bin bs=1048576 count=32 && i=0; while [ "$i" -lt 2000 ]; do touch "/build/header-$i"; i=$((i+1)); done
# With:
# dd if=/dev/zero of=/build/cache.bin bs=1048576 count=32 && python3 -c 'import pathlib; [pathlib.Path(f"/build/header-{i}").touch() for i in range(2000)]'
old_loop = 'dd if=/dev/urandom of=/build/cache.bin bs=1048576 count=32 && i=0; while [ "$i" -lt 2000 ]; do touch "/build/header-$i"; i=$((i+1)); done'
new_loop = 'dd if=/dev/zero of=/build/cache.bin bs=1048576 count=32 && python3 -c \'import pathlib; [pathlib.Path(f"/build/header-{i}").touch() for i in range(2000)]\''
assert old_loop in text, "old_loop not found"
text = text.replace(old_loop, new_loop, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Fast file creation patched!")
