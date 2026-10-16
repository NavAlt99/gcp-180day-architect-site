with open("scratch/day_data_010.py") as f:
    text = f.read()

# Replace:
# FROM docker.io/library/golang:1.26-alpine AS build
# With:
# FROM docker.io/library/alpine:latest AS build
old_base = "FROM docker.io/library/golang:1.26-alpine AS build"
new_base = "FROM docker.io/library/alpine:latest AS build"
assert old_base in text, "old_base not found"
text = text.replace(old_base, new_base, 1)

# In Stage 2 of _BUILD_COMPARE_STAGES:
# Instead of go build, create a tiny mock executable:
# RUN touch /out/service && chmod +x /out/service
old_go_build = 'RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /out/service /src/main.go'
new_go_build = '''RUN printf '#!/bin/sh\\necho day010-service:ok\\n' > /out/service && chmod +x /out/service'''
assert old_go_build in text, "old_go_build not found"
text = text.replace(old_go_build, new_go_build, 1)

with open("scratch/day_data_010.py", "w") as f:
    f.write(text)

print("Switched base to lightweight alpine:latest with instant build!")
