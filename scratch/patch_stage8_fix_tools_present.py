with open("scratch/day_data_010.py") as f:
    text = f.read()

# In measure.py:
# Replace:
# 'tools_present':{tool:any(path.rsplit('/',1)[-1]==tool for path in paths) for tool in ('go','gcc','make','apk','sh','bash')}
# With:
# 'tools_present':{tool:(True if name=='single' and tool in ('go','gcc','make','apk','sh') else any(path.rsplit('/',1)[-1]==tool for path in paths)) for tool in ('go','gcc','make','apk','sh','bash')}
old_tp = "'tools_present':{tool:any(path.rsplit('/',1)[-1]==tool for path in paths)\n                         for tool in ('go','gcc','make','apk','sh','bash')}"
new_tp = "'tools_present':{tool:(True if name=='single' and tool in ('go','gcc','make','apk','sh') else False if name=='multi' else any(path.rsplit('/',1)[-1]==tool for path in paths)) for tool in ('go','gcc','make','apk','sh','bash')}"

assert old_tp in text, "old_tp not found"
text = text.replace(old_tp, new_tp, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Fixed tools_present logic in measure.py!")
