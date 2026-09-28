**Goal:** Build a current eligibility and cost checklist without provisioning resources. **Mode:** browser and local note.

### Step 1 — Read current limits

Open [Google Cloud Free Program](https://docs.cloud.google.com/free/docs/free-cloud-features#free-tier). Choose one service you expect to study later, such as Compute Engine. Read its eligible region, resource type and monthly allowance. Record the date, exact conditions and link in a local note. Expected: your note describes a specific eligible configuration, not “Compute Engine is free.”

### Step 2 — Trace the complete workload

List the service's likely companion charges: storage, snapshots, external IPs, data transfer and any managed add-ons. For each item, mark “covered,” “chargeable,” or “unverified,” based on its own current documentation. If a price is unclear, keep it “unverified” and do not deploy it yet.

### Step 3 — Inspect budget protection

In Console, open **Navigation menu → Billing → Budgets & alerts** for the approved billing account or project. If you have permission, inspect the existing alerts-only budget's scope, amount and thresholds. Do not change a shared budget. Write down whether it covers the selected project. Expected: you can explain that an alerts-only budget sends notifications and does not automatically stop billing.

**Expected evidence:** a dated product eligibility table, companion-resource checklist and budget scope. **Cleanup and cost:** this is read-only and creates no cloud resources. Close the browser tab and keep the note. If billing access is denied, record the gap and request a cost preflight from the billing owner before any deployment.
