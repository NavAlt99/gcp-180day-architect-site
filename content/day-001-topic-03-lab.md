**Goal:** Add synthetic data and a future cloud-lab safety plan to the Day 1 repository. **Mode:** local Linux shell; no cloud resource or chargeable operation.

### Step 1 — Confirm the workspace

Open the terminal used in Exercise 1 and run:

```sh
cd ~/gcp-architect-learning
pwd
git status --short
```

The path should end in `gcp-architect-learning`. Review any existing changes before continuing so they are not accidentally included in the next commit.

### Step 2 — Create synthetic order data

Run:

```sh
printf '{"order_id":"demo-001","customer":"sample-customer","amount":12.50}\n' > synthetic-order.json
python3 -m json.tool synthetic-order.json
```

Python should print a formatted JSON object with order ID `demo-001`. This verifies syntax, not business correctness. Check that the file contains no real person, customer export, address, token or password. If parsing fails, inspect its quotes and commas before proceeding.

### Step 3 — Record the safety boundary

Append a planning section to the README:

```sh
cat >> README.md <<'EOF'

## Lab safety

Data: synthetic only
Planned budget: decide before Day 18 cloud work
Billing owner: identify before enabling billing
Cleanup owner: learner
Resource inventory: no cloud resources created on Day 1
Deletion verification: list resources after each future cloud lab
Budget alert rule: an alert warns; it does not stop spending
EOF
```

Fill in a real budget and owner before any later paid lab. The Day 1 entry should remain honest: billing has not been enabled for this local exercise.

### Step 4 — Commit and verify

Run:

```sh
git add README.md synthetic-order.json
git diff --cached --stat
git -c user.name='Learner' -c user.email='learner@example.invalid' commit -m 'Record Day 1 safety plan'
git status --short
```

The staged diff should name the README and JSON fixture; the final short status should be empty. If an actual customer value appears in the diff, remove it before committing. Keep both files as evidence. No cloud cleanup is required today.
