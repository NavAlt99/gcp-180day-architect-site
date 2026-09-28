# Day 27 Exit Artifact: Billing Responsibility Matrix & Budget Thresholds

**Generated:** 2026-09-27T10:27:02.738773+00:00
**Scope:** Brightloaf Cloud Billing Account `01A2B3-4C5D6E-7F8G9H`
**Objective:** A billing responsibility matrix and correctly calculated thresholds.

---

## 1. Cloud Billing Responsibility Matrix (RACI)

Segregation of duties between corporate finance, engineering operations, and FinOps:

| Operational Activity | Corporate Finance | DevOps / Eng Leads | FinOps & Audit | Automated CI/CD |
|:---|:---|:---|:---|:---|
| **Open / Close Billing Account** | **Accountable (A)** | Informed (I) | Consulted (C) | No Access |
| **Manage Payment Profile & Credit Line** | **Responsible (R)** | No Access | Informed (I) | No Access |
| **Create & Link New Projects** | Informed (I) | **Responsible (R)** | Informed (I) | **Responsible (R)** |
| **Unlink / Migrate Projects** | **Accountable (A)** | Consulted (C) | Consulted (C) | No Access |
| **Set & Modify Monthly Budgets** | **Accountable (A)** | Consulted (C) | **Responsible (R)** | No Access |
| **Receive 50% / 90% Email Alerts** | Informed (I) | **Responsible (R)** | **Responsible (R)** | No Access |
| **Handle 100% Pub/Sub Remediation** | Informed (I) | **Responsible (R)** | Consulted (C) | **Responsible (R)** |

---

## 2. Calculated Monthly Budget Alert Thresholds

- **Baseline Allocation:** $1,000.00 USD / month
- **Target Container:** `projects/brightloaf-analytics` & `projects/brightloaf-dev-sandbox`

| Threshold (%) | Trigger Amount | Evaluation Metric | Severity | Notification Channel | Operational Response |
|:---|:---|:---|:---|:---|:---|
| **50%** | $500.00 USD | Actual Spend | Informational | Email (`eng-alerts@brightloaf.com`) | Mid-month pace review; confirm linear burn rate |
| **90%** | $900.00 USD | Actual or Forecasted | Warning | Email (`finops@brightloaf.com`, `eng-mgmt@...`) | Review unpartitioned queries and idle compute |
| **100%** | $1,000.00 USD | Actual Spend | Critical | Email + Cloud Pub/Sub Event | Automated scale-down of non-prod workloads |

---

## 3. Programmatic Pub/Sub Alert Event Schema

```json
{
  "budgetDisplayName": "brightloaf-analytics-monthly-budget",
  "costAmount": 1004.50,
  "costIntervalStart": "2026-09-01T00:00:00Z",
  "budgetAmount": 1000.00,
  "budgetAmountType": "SPECIFIED_AMOUNT",
  "alertThresholdExceeded": 1.0,
  "currencyCode": "USD"
}
```

### Invariant & Safety Compliance Attestation:
1. **Duplicate Fulfillment Invariant (&le; 1 Physical Fulfillment):** Automated cost-capping scripts triggered by Pub/Sub must strictly filter on resource tags (`env != "production"`). Production order ingestion and dispatch pipelines are shielded from automated termination.
2. **Key Avoidance:** Project linkage pipelines authenticate strictly via `roles/billing.user` with attached workload identities; zero static JSON keys are used for financial management.

**Attested by:** Brightloaf FinOps & Cloud Architecture Review Board
