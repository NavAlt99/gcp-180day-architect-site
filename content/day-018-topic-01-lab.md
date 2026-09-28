**Goal:** Identify an approved lab account and project without creating a paid service. **Mode:** Google Cloud Console. You need an existing training sandbox or an account you are authorized to use. If neither is available, read the linked screens in the documentation and mark the evidence as a walkthrough, not an observation.

### Step 1 — Identify the environment

Open [Google Cloud Console](https://console.cloud.google.com/). Sign in to the approved account. Select the project picker in the top bar and read the project name and ID. Choose the approved training project if one exists. Expected: the top bar shows that project after selection. Record a redacted ID in your local note, for example `training-…-123`.

### Step 2 — Check billing ownership

Open **Navigation menu → Billing**. If you can see the billing account and linked projects, confirm that the selected project is linked to the intended lab billing account. If access is denied, record “billing visibility unavailable” and ask the account owner for the required preflight information before any billable lab. Do not infer that a project is free because its Billing page is hidden.

### Step 3 — Check the trial state

If this is your own eligible Free Trial account, inspect the trial credit and remaining time shown in Billing. Record the date and a rounded balance only. If it is an organization sandbox, record “organization sandbox; personal trial not applicable.” Do not create a new account merely to complete this exercise.

**Expected evidence:** active project, account type, billing visibility, owner and whether a trial credit is actually displayed. **Cleanup and cost:** this inspection creates no service resources. Sign out of a shared browser session; retain the redacted note. If you created a disposable project with permission, keep it only if the lab owner has approved future use; otherwise follow the owner's deletion procedure after confirming it contains no shared resources.
