**Goal:** Navigate the Console and, if authorized, configure a project-scoped budget alert. **Mode:** Google Cloud Console; no billable service is deployed. You need an approved sandbox and billing permission to create the optional alert.

### Step 1 — Tour the project context

Open [Google Cloud Console](https://console.cloud.google.com/). Use the top-bar project picker to select the approved lab project. Open **Navigation menu** and find **IAM & Admin → Manage resources**. Check the project ID in the list against the top bar. Expected: both identify the same project. If the project is missing, stop and check account access; do not create a replacement.

### Step 2 — Try a pinned product

Use the navigation menu or search to open **Cloud Storage → Buckets**. Pin Cloud Storage if the Console offers that control. Return to the Console home screen and use the pin to reopen Buckets. Expected: the shortcut opens the service, while the selected project stays visible in the top bar. Do not create a bucket.

### Step 3 — Configure an alert if allowed

Open **Navigation menu → Billing → Budgets & alerts → Create budget**. Choose an **alerts-only** budget and give it a distinctive lab name. Scope it to the approved project, choose a small monthly amount approved by the billing owner, review the threshold notifications and select **Finish**. Expected: the budget appears in the list with the chosen scope. Google states that alerts-only budgets do not automatically cap spending. If permission is missing or a shared budget already covers the project, record the existing setup and skip creation.

### Step 4 — Verify and clean up

Reopen the budget to verify the project scope, threshold recipients and amount. Record a redacted summary, then delete this exercise's budget only if it was disposable and the billing owner approves; leave shared alerts in place. Recheck **Budgets & alerts** to confirm the intended state. No service resource was created, so there is no workload to delete or charge from this lab. Save the project-selection and budget-preflight notes for Day 19.
