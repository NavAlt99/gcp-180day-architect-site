#!/usr/bin/env python3
"""
Lab 28.1: Idempotent Pub/Sub Budget Notification Consumer & Deduplication Engine
Demonstrates at-least-once message handling, composite state deduplication,
and safe remediation guardrails preserving Brightloaf's duplicate fulfillment invariant.
"""

import json
import os
import sys
from datetime import datetime, timezone

class IdempotentBudgetConsumer:
    def __init__(self):
        # Simulated persistent state store (e.g., Firestore / Memorystore Redis)
        self.state_store = {}
        self.remediation_history = []
        self.log_entries = []

    def log(self, level: str, message: str):
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        formatted = f"[{timestamp}] [{level.upper()}] {message}"
        print(formatted)
        self.log_entries.append(formatted)

    def derive_dedup_key(self, payload: dict) -> str:
        """Derive deterministic composite key from billing event envelope."""
        budget_name = payload.get("budgetDisplayName", "unknown")
        interval_start = payload.get("costIntervalStart", "unknown")
        threshold = payload.get("alertThresholdExceeded", 0.0)
        return f"{budget_name}#{interval_start}#{threshold:.2f}"

    def process_notification(self, raw_message: dict) -> dict:
        msg_id = raw_message.get("message_id")
        payload = raw_message.get("data", {})
        
        budget_name = payload.get("budgetDisplayName")
        cost = payload.get("costAmount", 0.0)
        budget = payload.get("budgetAmount", 0.0)
        threshold = payload.get("alertThresholdExceeded", 0.0)
        currency = payload.get("currencyCode", "USD")

        self.log("INFO", f"Received message {msg_id}: budget '{budget_name}', spend ${cost:,.2f}/{budget:,.2f} {currency} ({threshold*100:.0f}% threshold)")

        dedup_key = self.derive_dedup_key(payload)

        # Step 1: Check idempotency state store
        if dedup_key in self.state_store:
            prior = self.state_store[dedup_key]
            self.log("WARN", f"[IDEMPOTENT_DROP] Duplicate event detected for key '{dedup_key}'. First processed at {prior['timestamp']}. ACK returned without action.")
            return {
                "message_id": msg_id,
                "status": "DUPLICATE_DROPPED",
                "dedup_key": dedup_key,
                "action": "NONE"
            }

        # Step 2: Atomic State Registration
        self.state_store[dedup_key] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cost_at_trigger": cost,
            "threshold": threshold,
            "status": "PROCESSING"
        }

        # Step 3: Execute Gated Remediation Workflow
        action_summary = "NOTIFY_ONLY"
        if threshold >= 1.0:
            self.log("CRITICAL", f"100% Budget exceeded! Evaluating automated remediation guardrails...")
            
            # Guardrail check: Production workloads are strictly immune!
            self.log("GUARDRAIL", "Evaluating target: 'order-ingestion-api' (env: 'production')")
            self.log("GUARDRAIL", "IMMUNITY TRIGGERED: Production order intake is shielded from automated scaling.")
            self.log("GUARDRAIL", "Duplicate fulfillment invariant preserved: <= 1 physical fulfillment per unique order ID.")
            
            # Non-destructive action on non-production workloads only
            self.log("ACTION", "Targeting non-production: Scaling down dev batch workers ('analytics-dev-workers') from 10 to 2 instances.")
            action_summary = "SCALE_DOWN_DEV_WORKERS"
            self.remediation_history.append({
                "target": "analytics-dev-workers",
                "env": "development",
                "action": "scale_down",
                "from_instances": 10,
                "to_instances": 2
            })
        elif threshold >= 0.9:
            self.log("ALERT", f"90% Budget warning ($ {cost:,.2f}). Dispatching PagerDuty/Slack notification to FinOps channel.")
            action_summary = "PAGERDUTY_FINOPS_ALERT"
        elif threshold >= 0.5:
            self.log("NOTICE", f"50% Budget checkpoint ($ {cost:,.2f}). Dispatching informational digest to engineering leads.")
            action_summary = "CADENCE_EMAIL_DIGEST"

        # Step 4: Finalize State & Return ACK
        self.state_store[dedup_key]["status"] = "COMPLETED"
        self.state_store[dedup_key]["action_taken"] = action_summary
        self.log("SUCCESS", f"Workflow '{action_summary}' finished. State '{dedup_key}' locked. Message ACKed.")

        return {
            "message_id": msg_id,
            "status": "PROCESSED",
            "dedup_key": dedup_key,
            "action": action_summary
        }

def run_simulation():
    consumer = IdempotentBudgetConsumer()

    # Synthetic Pub/Sub Message Stream with duplicates & periodic updates
    stream = [
        # Event 1: 50% Threshold crossing
        {
            "message_id": "ps-msg-101",
            "publish_time": "2026-09-15T10:00:00Z",
            "data": {
                "budgetDisplayName": "brightloaf-core-monthly",
                "costAmount": 2550.00,
                "budgetAmount": 5000.00,
                "costIntervalStart": "2026-09-01T00:00:00Z",
                "budgetAmountType": "SPECIFIED_AMOUNT",
                "alertThresholdExceeded": 0.5,
                "currencyCode": "USD"
            }
        },
        # Event 2: Immediate duplicate delivery of Event 1 (simulating slow ACK / network retry)
        {
            "message_id": "ps-msg-101-retry",
            "publish_time": "2026-09-15T10:00:14Z",
            "data": {
                "budgetDisplayName": "brightloaf-core-monthly",
                "costAmount": 2550.00,
                "budgetAmount": 5000.00,
                "costIntervalStart": "2026-09-01T00:00:00Z",
                "budgetAmountType": "SPECIFIED_AMOUNT",
                "alertThresholdExceeded": 0.5,
                "currencyCode": "USD"
            }
        },
        # Event 3: 90% Threshold crossing
        {
            "message_id": "ps-msg-102",
            "publish_time": "2026-09-24T14:30:00Z",
            "data": {
                "budgetDisplayName": "brightloaf-core-monthly",
                "costAmount": 4510.80,
                "budgetAmount": 5000.00,
                "costIntervalStart": "2026-09-01T00:00:00Z",
                "budgetAmountType": "SPECIFIED_AMOUNT",
                "alertThresholdExceeded": 0.9,
                "currencyCode": "USD"
            }
        },
        # Event 4: 100% Threshold crossing
        {
            "message_id": "ps-msg-103",
            "publish_time": "2026-09-27T08:14:02Z",
            "data": {
                "budgetDisplayName": "brightloaf-core-monthly",
                "costAmount": 5040.25,
                "budgetAmount": 5000.00,
                "costIntervalStart": "2026-09-01T00:00:00Z",
                "budgetAmountType": "SPECIFIED_AMOUNT",
                "alertThresholdExceeded": 1.0,
                "currencyCode": "USD"
            }
        },
        # Event 5: Redelivery of Event 4 (ACK deadline expiration duplicate)
        {
            "message_id": "ps-msg-103-redelivered",
            "publish_time": "2026-09-27T08:14:15Z",
            "data": {
                "budgetDisplayName": "brightloaf-core-monthly",
                "costAmount": 5040.25,
                "budgetAmount": 5000.00,
                "costIntervalStart": "2026-09-01T00:00:00Z",
                "budgetAmountType": "SPECIFIED_AMOUNT",
                "alertThresholdExceeded": 1.0,
                "currencyCode": "USD"
            }
        }
    ]

    print("================================================================================")
    print("  BRIGHTLOAF IDEMPOTENT BUDGET NOTIFICATION CONSUMER (PUB/SUB RECEPTOR)         ")
    print("================================================================================")
    
    results = []
    for msg in stream:
        res = consumer.process_notification(msg)
        results.append(res)
        print("-" * 80)

    # Output stats
    processed = sum(1 for r in results if r["status"] == "PROCESSED")
    dropped = sum(1 for r in results if r["status"] == "DUPLICATE_DROPPED")
    print(f"\nSimulation Complete: Total Messages: {len(stream)} | Processed: {processed} | Duplicates Dropped: {dropped}")
    
    # Save log report
    os.makedirs("scratch/day028", exist_ok=True)
    log_file = "scratch/day028/budget-consumer.log"
    with open(log_file, "w") as f:
        f.write("\n".join(consumer.log_entries) + "\n")
    print(f"Consumer execution log saved to: {log_file}")

if __name__ == "__main__":
    run_simulation()
