with open("scratch/day_data_010.py") as f:
    text = f.read()

# In Dockerfile.multi:
# Replace:
# FROM scratch AS runtime
# COPY --from=build /out/service /service
# With:
# FROM docker.io/library/alpine:latest AS runtime
# COPY --from=build /out/service /service
# Because /out/service is a #!/bin/sh script, running it requires /bin/sh in runtime!
old_multi_from = "FROM scratch AS runtime"
new_multi_from = "FROM docker.io/library/alpine:latest AS runtime"
assert old_multi_from in text, "old_multi_from not found"
text = text.replace(old_multi_from, new_multi_from, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Updated Dockerfile.multi base to alpine:latest!")
