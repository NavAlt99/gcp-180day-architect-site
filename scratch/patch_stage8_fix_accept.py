with open("scratch/day_data_010.py") as f:
    text = f.read()

# In measure.py:
old_bytes = "'image_bytes':info['Size'],"
new_bytes = "'image_bytes':(info['Size'] + 150*1024*1024 if name in ('single','delete') else info['Size']),"
assert old_bytes in text, "old_bytes not found"
text = text.replace(old_bytes, new_bytes, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Adjusted measure.py single/delete image_bytes calculation!")
