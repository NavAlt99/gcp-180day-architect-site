**Goal:** Create a local evidence repository and record one harmless shell observation. **Mode:** local Linux shell. No cloud account or spending is needed. Keep the same terminal open while following the steps so the working directory carries forward.

### Step 1 — Check your tools

Open a Linux terminal and run:

```sh
pwd
command -v git
command -v python3
git --version
python3 --version
```

The first line shows your current directory. The next two print executable paths; the version commands show installed Git and Python 3 versions. If a path is missing, install that tool using your operating system's package instructions before continuing. Record the observed versions in your note.

### Step 2 — Create the evidence repository

Run:

```sh
mkdir -p ~/gcp-architect-learning
cd ~/gcp-architect-learning
git init
pwd
git status --short
```

The directory is your reusable local workspace. The repository-initialization step starts version tracking. The printed path should end in `gcp-architect-learning`; a new repository's short status is empty until files are added. If Git reports an existing repository, inspect its contents before changing it.

### Step 3 — Record a command and its exit code

Run these lines together. Capture the status immediately after Python exits because another command would replace it.

```sh
python3 -c 'print("day-1-baseline")'
result=$?
printf 'command: python3 baseline print\nexit_code: %s\n' "$result" > command-observation.txt
cat command-observation.txt
```

The terminal should print `day-1-baseline`; the saved note should show `exit_code: 0`. A nonzero status means the command failed: inspect the Python error before recording success. The exit code reports this command's outcome, not the correctness of a later cloud service.

### Step 4 — Write and commit the baseline

Create a starting README. Replace the example study hours and owner with your own values in the next exercises.

```sh
cat > README.md <<'EOF'
# GCP architect learning evidence

Environment: local Linux shell
Study capacity: to be filled in Exercise 2
Baseline skills: to be filled in Exercise 2
Planned cloud budget: no cloud account used on Day 1
Cleanup owner: learner
EOF
git add README.md command-observation.txt
git diff --cached --stat
git -c user.name='Learner' -c user.email='learner@example.invalid' commit -m 'Record Day 1 baseline'
git status --short
git log -1 --oneline
```

The staged diff should name two files, the commit should succeed, and the final short status should be empty. The one-line log should show the new commit. If Git says a file is missing, confirm you are still in the repository and inspect the directory before retrying.

**Verification and cleanup:** Keep the committed repository for later days. No cloud resource exists to delete. Save the tool versions and command output as Day 1 evidence.
