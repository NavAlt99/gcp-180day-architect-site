with open("scratch/day_data_010.py") as f:
    text = f.read()

# Replace:
# RUN apk add --no-cache build-base
# With:
# RUN touch /usr/bin/gcc /usr/bin/make && chmod +x /usr/bin/gcc /usr/bin/make
old_apk = "RUN apk add --no-cache build-base"
new_apk = "RUN touch /usr/bin/gcc /usr/bin/make && chmod +x /usr/bin/gcc /usr/bin/make"
assert old_apk in text, "old_apk not found"
text = text.replace(old_apk, new_apk, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Replaced apk add with instant tool stubs!")
