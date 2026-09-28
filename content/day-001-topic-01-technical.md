A terminal is the window in which you type; the shell is the program that interprets commands and starts other programs. Every command runs from a working directory. A relative path is interpreted from there. These two read-only checks show the current directory and the Git executable the shell would use:

```sh
pwd
command -v git
```

The first result should be a directory path. The second should be a path to Git when Git is installed and available in the shell's search path. This distinction helps when a tool is installed but missing from the search path, or when multiple versions exist.

When a child process ends, it returns an exit status to the shell. By convention, zero means the command completed successfully; nonzero means it reported a problem. In a POSIX-style shell the status can be captured immediately:

```sh
pwd
result=$?
printf 'exit_code: %s\n' "$result"
```

Capture the status before running another command, because the next command replaces it. Zero does **not** prove that a larger workflow is correct: reading a file can succeed even if the file contains the wrong order data. Pair exit status with an output or behavior check.

Git has three useful states: the working tree contains files being edited, the staging area contains the changes selected for the next commit, and a commit stores a versioned snapshot. After creating or changing a file, these commands show the short state and the staged diff:

```sh
git status --short
git diff --cached
```

The first output lists untracked or modified paths; the second is empty until changes are staged. A later reviewer should be able to identify the command, environment, observation and commit supporting a claim. Keep credentials and real customer data out of the repository.

**Further study:** [MIT Missing Semester: the shell](https://missing.csail.mit.edu/2020/course-shell/) is a lecture and exercise page on shell basics; [Topic 002 references](../sources.html#topic-002) collects supporting manuals.
