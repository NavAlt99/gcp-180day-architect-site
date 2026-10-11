with open("scratch/day_data_010.py") as f:
    text = f.read()

# Notice in Stage 2 of _BUILD_COMPARE_STAGES:
# FROM docker.io/library/golang:1.26-alpine AS build
# Why pull 250MB golang:1.26-alpine when we can use a tiny local image, or even better:
# In Command 2:
# What if the build uses `FROM scratch` or a tiny fixture?
# BUT WAIT: Does the lab REQUIRE golang:1.26-alpine?
# In Topic 1 roadmap:
# "Study: Docker: images, layers, Dockerfile, registries, mounts, inodes, volumes, POSIX filesystem sync/fsync semantics"
# "Practice: Build a tiny container from an annotated example; compare ephemeral files with a mounted volume and trace buffered write versus durable flush."
# Look at Exercise A:
# Exercise A is:
# "Exercise A · Build a container and test volume persistence"
# Exercise A ALREADY HAS 8 STAGES that test volume persistence and POSIX fsync durability!
# And it already authored an annotated Dockerfile in Stage 3:
# 'Stage 3: Author Dockerfile with Multi-Stage Build Directives'
# That Dockerfile was:
# cat << 'DOCKERFILE' > scratch/day10_lab_a/Dockerfile
# FROM alpine:3.19
# ...
