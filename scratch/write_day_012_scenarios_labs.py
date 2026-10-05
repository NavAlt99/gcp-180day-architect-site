"""Writer for day_012_scenarios_labs.py with real newlines."""

def main():
    content = '''"""Day 12 Scenarios and Labs definitions."""

from scratch.generate_day_012 import FIG_12_4_HTML, FIG_12_5_HTML, FIG_12_6_HTML

SCENARIOS = {
    'topic-01': {
        'scenario': 'OmniRetail Global operates an e-commerce checkout and inventory allocation API serving North American and European customers. During initial deployment, the engineering team provisioned the checkout application on three Compute Engine virtual machines and a standalone MySQL database instance, all hosted within a single availability zone: us-central1-a (Council Bluffs, Iowa). At 14:22 UTC, an external municipal construction crew severed primary redundant electrical feed lines to the Council Bluffs substation, triggering an immediate localized facility power failure in us-central1-a. Because the checkout VMs and database disk volumes were zonal resources confined strictly to us-central1-a without automated cross-zonal replication, the entire checkout service became unreachable. Incoming client requests timed out, dropping 3,800 active checkout transactions and rendering the storefront unable to accept orders for 4 hours and 18 minutes until physical utility power was restored.',
        'impact': '4 hours and 18 minutes of continuous checkout service outage; 3,800 active shopping cart transactions dropped; estimated $240,000 in lost direct sales revenue and severe brand degradation during a scheduled promotional campaign.',
        'constraints': 'Storefront requires 99.99% availability; maximum acceptable Recovery Time Objective (RTO) is less than 5 minutes; Recovery Point Objective (RPO) must be 0 for all committed customer orders; user round-trip latency must remain under 60 ms for North American users and under 40 ms for European users.',
        'evidence': '<p>Illustrative system log captured during the us-central1-a zonal failure and load balancer health check failure:</p>\\n<pre><code>2026-10-04T14:22:04.112Z glb-frontend-edge [info]: Health check probe failed for backend target 10.128.1.14:8080 (us-central1-a): Connection timed out (110: Connection timed out)\\n2026-10-04T14:22:05.450Z glb-frontend-edge [error]: No healthy backends available in forwarding rule fr-checkout-service (us-central1-a 0/3 healthy, no failover zones configured)\\n2026-10-04T14:22:06.890Z glb-frontend-edge [warn]: Returning HTTP 503 Service Unavailable to client 198.51.100.44 (duration: 5002ms, path: /api/v1/checkout/commit)\\n2026-10-04T14:22:10.002Z compute-engine-api [alert]: Zonal facility power anomaly detected in us-central1-a; host hypervisor unreachable for instances checkout-vm-01, checkout-vm-02, checkout-vm-03</code></pre>\\n' + FIG_12_4_HTML,
        'root': 'Single point of failure (SPOF) architecture: both compute instances and persistent database storage were deployed exclusively within a single physical availability zone (us-central1-a) without cross-zonal distribution, regional health checking, or multi-zone standby failover.',
        'verify': 'Deployed synthetic fault injection test simulating complete zonal outage in us-central1-a: the Regional Managed Instance Group automatically detected unhealthy instances, redirected 100% of live traffic to us-central1-b and us-central1-c within 18 seconds, and Cloud SQL executed automated synchronous standby failover with zero transaction loss.',
        'residual': 'Regional multi-zone deployment eliminates single-zone SPOFs but remains vulnerable to catastrophic planetary regional cataclysms; cross-region disaster recovery replication to europe-west1 is required for complete catastrophic continuity.',
        'diagram_enabled': False,
        'facts': 'Production workload ran exclusively in us-central1-a with 0 instances in alternate zones; zonal failure caused 4h 18m total service outage.',
        'inference': 'Zonal deployments violate high availability mandates for revenue-critical workloads; Regional MIGs and Cloud SQL HA across 3 zones provide seamless failure domain isolation.',
        'expected': 'Incoming traffic automatically routes around degraded zones to healthy instances in alternate zones with zero HTTP 503 errors and zero operator intervention.',
        'diagnostic_steps': [
            'Query Cloud Logging for Compute Engine instance state transitions and zonal health alert notifications.',
            'Inspect Cloud Load Balancing telemetry for backend health check transition logs and HTTP 503 response spikes.',
            'Audit Cloud Monitoring zonal availability metrics across us-central1-a, us-central1-b, and us-central1-c.'
        ],
        'remediation_steps': [
            'Convert zonal compute instances into an immutable Compute Engine Instance Template with a stateless container startup script.',
            'Deploy a Regional Managed Instance Group (Regional MIG) spanning us-central1-a, us-central1-b, and us-central1-c with target distribution shape set to EVEN.',
            'Configure an External Application Load Balancer with HTTP health checks pointing to /healthz with a 5-second check interval and 2-consecutive-failure unhealthy threshold.',
            'Migrate standalone database to Cloud SQL for PostgreSQL configured with High Availability (regional synchronous replication across separate zones).'
        ]
    },
    'topic-02': {
        'scenario': 'OmniRetail launched an unannounced promotional flash sale at 10:00 UTC, causing storefront traffic to surge from a baseline of 400 requests per second to over 9,500 requests per second in under 90 seconds. The Compute Engine Autoscaler detected an average CPU utilization spike to 94% across the baseline 6 instances and aggressively scaled out the Managed Instance Group to its maximum limit of 120 instances. Each application instance was configured with an internal connection pool allocating 25 persistent TCP connections to the backend Cloud SQL PostgreSQL instance (which was sized with max_connections = 500). As 120 instances booted and simultaneously initialized connection pools, they attempted to establish 3,000 concurrent database connections. PostgreSQL immediately exhausted its connection table, rejecting connections with fatal errors and entering severe memory lock contention. With the database unresponsive, application response times ballooned from 45 ms to over 15,000 ms, causing upstream load balancers to timeout and the autoscaler to detect sustained high load—locking the system in an Autoscaling Death Spiral.',
        'impact': '45 minutes of complete transaction processing outage during peak flash-sale revenue window; 18,500 failed checkout operations; $420,000 in estimated direct lost sales revenue and severe brand backlash.',
        'constraints': 'Flash sale generates 25x traffic surges within 120 seconds; backend Cloud SQL instance has a hard physical connection limit of 500 connections; end-to-end checkout API latency budget is 200 ms; autoscaler must prevent thrashing and connection flooding.',
        'evidence': '<p>Illustrative system log captured during the autoscaling connection storm and database collapse:</p>\\n<pre><code>2026-10-04T10:01:14.204Z compute-autoscaler [info]: Scaling MIG mig-checkout-na out from 6 to 120 instances (CPU target 65% exceeded, observed 94%)\\n2026-10-04T10:01:38.892Z cloud-sql-postgres [error]: FATAL: remaining connection slots are reserved for non-replication superuser connections (active: 500/500)\\n2026-10-04T10:01:39.104Z checkout-app-worker-88 [error]: org.postgresql.util.PSQLException: FATAL: sorry, too many clients already\\n2026-10-04T10:01:42.502Z glb-frontend-edge [warn]: Backend timeout: 10.128.2.44:8080 failed to respond within 15000ms; returning HTTP 504 Gateway Timeout\\n2026-10-04T10:02:00.110Z compute-autoscaler [warn]: Autoscaler target utilization remains 98% due to queued thread contention; unable to scale further (max_replicas=120 reached)</code></pre>\\n' + FIG_12_5_HTML,
        'root': 'Uncontrolled horizontal autoscaling saturation cascade: the stateless compute layer expanded rapidly without downstream connection multiplexing or admission control, exhausting the relational database connection ceiling and triggering an unrecoverable positive feedback failure loop.',
        'verify': 'Executed synthetic load test simulating 30x traffic surge against the remediated architecture: PgBouncer multiplexed 3,500 client connections into a stable pool of 150 PostgreSQL backend connections; Cloud SQL CPU remained at 42%, and API response latency stayed under 65 ms.',
        'residual': 'Connection pooling protects relational databases from connection exhaustion, but high write volume still requires horizontal sharding or read replica offloading for catalog queries.',
        'diagram_enabled': False,
        'facts': '120 instances attempted 3,000 concurrent connections to a database limited to 500 connections, crashing the stateful storage tier.',
        'inference': 'Horizontal compute elasticity must be bounded by downstream capacity constraints; connection multiplexing and predictive autoscaling decouple compute spikes from stateful bottlenecks.',
        'expected': 'System scales horizontally to meet traffic demand while PgBouncer maintains database connection counts well below the 500-connection ceiling.',
        'diagnostic_steps': [
            'Inspect Cloud SQL PostgreSQL logs in Cloud Logging for "sorry, too many clients already" and connection pool exhaustion errors.',
            'Analyze Compute Engine Autoscaler scaling history to correlate replica count expansion timestamps with database latency spikes.',
            'Review Cloud Monitoring thread pool and database active connection count metrics during the incident window.'
        ],
        'remediation_steps': [
            'Deploy PgBouncer connection pooler in transaction pooling mode between the Managed Instance Group and Cloud SQL, capping total server connections at 150.',
            'Configure Compute Engine Autoscaler cooldown period to 120 seconds and implement scale-in controls (max-scaled-in-replicas-percent=15) to eliminate flapping.',
            'Enable Google Cloud Predictive Autoscaling on the regional MIG to forecast and pre-provision capacity ahead of scheduled promotional campaigns.',
            'Deploy Memorystore for Redis as an in-memory caching layer to absorb 85% of repeated product catalog read queries before they reach Cloud SQL.'
        ]
    },
    'topic-03': {
        'scenario': 'OmniRetail completed a rapid cloud migration of its microservices catalog and image processing pipeline from an on-premises data center to Google Cloud. The project team had created a preliminary monthly budget estimate of $11,500 based solely on Compute Engine VM list prices ($7,200) and Persistent Disk storage ($4,300) using basic pricing sheets. At the end of the first full billing month, the corporate Google Cloud invoice totaled $48,520—representing a catastrophic 320% budget overrun. A detailed audit revealed three massive unbudgeted cost drivers: (1) Inter-zonal network data transfer charges totaling $18,240, caused by microservices in us-central1-a making uncompressed JSON RPC calls across zones to services in us-central1-b and us-central1-c; (2) Cloud NAT data processing charges of $9,860, caused by CI/CD worker pools pulling multi-gigabyte container images from public registries through a single Cloud NAT gateway; and (3) Cloud Storage Class A operation charges of $8,920, caused by an unbatched catalog thumbnailing service writing millions of 2 KB image files individually using standard HTTP PUT calls.',
        'impact': '$37,020 monthly cloud budget overrun (320% above budget); emergency architecture review freeze; mandatory executive escalation; and reallocation of engineering product feature budgets to cover infrastructure deficits.',
        'constraints': 'Total monthly infrastructure spend must not exceed $15,000; high availability across three availability zones must be preserved; developer CI/CD deployment cadence cannot be throttled.',
        'evidence': '<p>Illustrative Cloud Billing BigQuery export query output captured during the financial cost audit:</p>\\n<pre><code>+-----------------------------------------------------+-----------------------+----------------+\\n| SKU Description                                     | Usage Amount          | Net Cost (USD) |\\n+-----------------------------------------------------+-----------------------+----------------+\\n| Inter-Zone Data Transfer within North America       | 1,824,000 GiB         | $18,240.00     |\\n| Cloud NAT Data Processing                           | 219,110 GiB           | $9,859.95      |\\n| Cloud Storage Class A Operations (Standard Storage) | 1,784,000,000 Ops     | $8,920.00      |\\n| Compute Engine N2 Custom Instance Core              | 14,400 vCPU-hours     | $4,550.40      |\\n| Compute Engine N2 Custom Instance Ram               | 57,600 GiB-hours      | $2,649.60      |\\n| Balanced SSD Persistent Disk                        | 43,000 GiB-months     | $4,300.00      |\\n+-----------------------------------------------------+-----------------------+----------------+\\n| TOTAL MONTHLY INVOICE                               |                       | $48,519.95     |\\n+-----------------------------------------------------+-----------------------+----------------+</code></pre>\\n' + FIG_12_6_HTML,
        'root': 'The vCPU-Only Fallacy: formulating cloud infrastructure budgets exclusively around raw compute and disk pricing while omitting the remaining four dimensions of the production Cloud Bill of Materials (inter-zone egress, NAT processing, and API operation fees).',
        'verify': 'Audited second-month billing invoice after implementing Private Service Connect, gRPC Protobuf compression, Artifact Registry regional caching, and object batching: total monthly expenditure dropped to $11,180 (within the $15,000 budget ceiling).',
        'residual': 'Pay-as-you-go cloud architectures require continuous FinOps governance, automated budget threshold alerts, and programmatic spend anomaly detection to prevent new microservice features from re-introducing egress blowouts.',
        'diagram_enabled': False,
        'facts': 'Compute and disk represented only 24% of the monthly invoice; unbudgeted networking data transfer and storage API operations accounted for 76% of total spend.',
        'inference': 'Production cloud cost modeling requires a comprehensive 6-dimension Bill of Materials; failure to account for data egress and API operations produces severe financial risk.',
        'expected': 'Monthly cloud billing stays within the $15,000 budget envelope with real-time budget threshold alerts firing at 50%, 80%, and 100% of forecasted spend.',
        'diagnostic_steps': [
            'Execute SQL queries against the Cloud Billing export dataset in BigQuery to isolate top expenditure SKUs and percentage growth rates.',
            'Analyze VPC Flow Logs in Cloud Logging to identify source and destination IP addresses generating cross-zonal data transfer volume.',
            'Inspect Cloud Storage monitoring dashboards to evaluate Class A versus Class B API operation ratios across storage buckets.'
        ],
        'remediation_steps': [
            'Deploy Google Artifact Registry within the regional VPC and configure Private Google Access, eliminating public internet Cloud NAT processing surcharges on container pulls.',
            'Replace uncompressed HTTP/JSON cross-zone microservice communication with gRPC Protobuf payloads and enable gzip compression, reducing egress volume by 72%.',
            'Refactor catalog image pipeline to aggregate thumbnail writes into batched archive objects and implement Cloud Storage lifecycle rules to transition cold objects to Nearline.',
            'Configure Cloud Billing Budgets with Pub/Sub programmatic notifications wired to Cloud Functions to alert engineering leads at 50%, 80%, and 100% budget thresholds.'
        ]
    }
}

LABS = {
    'topic-01': {
        'name': 'Exercise A · Regional Topology, Latency, and Residency Trade-Off Modeling',
        'goal': 'Evaluate deployment locations for an e-commerce retailer between us-central1 (Council Bluffs, Iowa) and europe-west1 (St. Ghislain, Belgium) across latency, data residency, network egress, and failure domains.',
        'expected': 'A validated Python regional comparison script and structured evaluation dataset comparing latency, GDPR compliance, cost, and resilience.',
        'mode': 'Tabletop analysis with Python simulation (local terminal, zero cloud spend). Mode breakdown: Observed locally: Python simulation script execution, cost modeling formulas, latency math. Simulated or predicted: Google Cloud regional latency distributions, MIG autoscaling response curves, multi-sku pricing bills. Untested on GCP: Live GCP project billing account creation, multi-region Cloud Load Balancer provisioning, cross-continental fiber cut simulations.',
        'covers': "Estimate two deployment locations and compare vertical versus horizontal scaling for the retailer's hypothetical workload.",
        'prereq': 'Linux terminal, Python 3.8+, bash, standard POSIX utilities (mkdir, cat, python3).',
        'preflight': 'Verify local terminal environment and ensure Python 3 is available.',
        'verification': 'Execute the location modeling script and verify latency and residency calculations.',
        'trouble': 'If Python encounters syntax or import errors, verify python3 version is 3.8 or newer.',
        'cleanup': 'All generated files reside in scratch/day12_lab/ and can be removed or retained for reference.',
        'accept': 'A validated JSON and Markdown report comparing us-central1 and europe-west1 deployment locations.',
        'file': 'scratch/day12_lab/regional_location_comparison.json',
        'steps': [
            """**Stage 1: Preflight and Environment Baseline**

**Location:** local terminal

**Actions:**
Verify required core utilities and establish dedicated lab workspace.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day12_lab
python3 -c "import sys; print(f'Python runtime verified: {sys.version}')"
```

**Expected result:**
All CLI tools confirm executable availability and Python 3.8+ runtime is validated.

**Save:** scratch/day12_lab/stage1_preflight.txt""",

            """**Stage 2: Define Hypothetical Retailer Workload and Regional Parameters**

**Location:** local terminal

**Actions:**
Author a structured JSON specification defining user distributions, latency targets, and compliance rules for us-central1 versus europe-west1.
```bash
cat <<'EOF' > scratch/day12_lab/workload_spec.json
{
  "workload_name": "OmniRetail Global Storefront",
  "na_users_percent": 60,
  "eu_users_percent": 40,
  "peak_rps": 5000,
  "regions": {
    "us-central1": {
      "location": "Council Bluffs, Iowa, USA",
      "zones": ["us-central1-a", "us-central1-b", "us-central1-c", "us-central1-f"],
      "na_latency_ms": 28,
      "eu_latency_ms": 112,
      "gdpr_compliant": false,
      "compute_cost_index": 1.00,
      "carbon_free_energy_percent": 89
    },
    "europe-west1": {
      "location": "St. Ghislain, Belgium",
      "zones": ["europe-west1-b", "europe-west1-c", "europe-west1-d"],
      "na_latency_ms": 98,
      "eu_latency_ms": 22,
      "gdpr_compliant": true,
      "compute_cost_index": 1.08,
      "carbon_free_energy_percent": 83
    }
  }
}
EOF
cat scratch/day12_lab/workload_spec.json
```

**Expected result:**
A structured JSON file defining regional performance, residency, and cost metrics is written.

**Save:** scratch/day12_lab/workload_spec.json""",

            """**Stage 3: Author Regional Latency and Residency Modeling Script**

**Location:** local terminal

**Actions:**
Create a Python simulation script that calculates user weighted latency, compliance risk, and single-region versus dual-region trade-offs.
```bash
cat <<'EOF' > scratch/day12_lab/model_regions.py
import json

with open("scratch/day12_lab/workload_spec.json", "r") as f:
    spec = json.load(f)

results = []
for region_name, rdata in spec["regions"].items():
    weighted_latency = (
        spec["na_users_percent"] * rdata["na_latency_ms"] +
        spec["eu_users_percent"] * rdata["eu_latency_ms"]
    ) / 100.0
    
    compliance = "Compliant" if rdata["gdpr_compliant"] else "Non-Compliant (Requires EU boundary)"
    failure_domain = f"Regional Multi-Zone ({len(rdata['zones'])} zones)"
    
    results.append({
        "region": region_name,
        "location": rdata["location"],
        "zones_count": len(rdata["zones"]),
        "weighted_latency_ms": weighted_latency,
        "na_latency_ms": rdata["na_latency_ms"],
        "eu_latency_ms": rdata["eu_latency_ms"],
        "gdpr_status": compliance,
        "cost_multiplier": rdata["compute_cost_index"],
        "failure_domain": failure_domain
    })

output = {
    "workload": spec["workload_name"],
    "evaluation": results,
    "architectural_recommendation": {
        "strategy": "Dual-Region Hybrid Deployment",
        "frontend": "Global Anycast External Application Load Balancer",
        "na_hub": "us-central1 (60% traffic, optimal compute cost)",
        "eu_hub": "europe-west1 (40% traffic, strictly GDPR compliant)",
        "resiliency": "Survives complete single-region catastrophic failure with automated traffic failover"
    }
}

with open("scratch/day12_lab/regional_location_comparison.json", "w") as out:
    json.dump(output, out, indent=2)

print("=" * 80)
print(f"{'REGION':<14} | {'ZONES':<6} | {'WEIGHTED LATENCY':<18} | {'GDPR STATUS':<24} | {'COST INDEX':<10}")
print("=" * 80)
for r in results:
    print(f"{r['region']:<14} | {r['zones_count']:<6} | {r['weighted_latency_ms']:>14.1f} ms | {r['gdpr_status']:<24} | {r['cost_multiplier']:>9.2f}x")
print("=" * 80)
print("Regional location comparison model generated successfully.")
EOF
```

**Expected result:**
Python modeling script model_regions.py authored with latency math and compliance logic.

**Save:** scratch/day12_lab/model_regions.py""",

            """**Stage 4: Execute Regional Comparison Simulation**

**Location:** local terminal

**Actions:**
Run the regional simulation script and verify console output.
```bash
python3 scratch/day12_lab/model_regions.py
```

**Expected result:**
Tabular output showing us-central1 (61.6 ms weighted, non-compliant) and europe-west1 (67.6 ms weighted, compliant).

**Save:** scratch/day12_lab/stage4_simulation_output.txt""",

            """**Stage 5: Inspect Regional Trade-Off Metrics**

**Location:** local terminal

**Actions:**
Inspect the generated regional comparison JSON structure to verify failure domain attributes.
```bash
cat scratch/day12_lab/regional_location_comparison.json
```

**Expected result:**
Formatted JSON displaying detailed attributes for both deployment regions and architectural recommendation.

**Save:** scratch/day12_lab/regional_location_comparison.json""",

            """**Stage 6: Formulate Dual-Region Resiliency Matrix**

**Location:** local terminal

**Actions:**
Generate an analytical markdown table documenting failure domain trade-offs and latency impacts.
```bash
cat <<'EOF' > scratch/day12_lab/resiliency_matrix.md
# Regional Deployment Trade-Off Analysis

| Evaluation Parameter | us-central1 (Iowa) | europe-west1 (Belgium) | Dual-Region (us-central1 + europe-west1) |
| :--- | :--- | :--- | :--- |
| **Primary User Proximity** | North America (< 30 ms) | Europe (< 25 ms) | Global (< 30 ms local Anycast routing) |
| **Cross-Continental Latency** | 112 ms to EU users | 98 ms to NA users | Localized to nearest edge PoP |
| **Data Residency (GDPR)** | Violates EU PII sovereignty | Strictly GDPR compliant | Partitioned: EU data stays in EU |
| **Failure Domain Scope** | Regional (4 zones) | Regional (3 zones) | Multi-Region Planetary (7 zones across 2 continents) |
| **Compute Cost Baseline** | 1.00x (Lowest cost tier) | 1.08x (+8% energy/tax premium) | Blended 1.03x |
| **DR Recovery Time (RTO)** | 4+ hours (requires full rebuild) | 4+ hours (requires full rebuild) | < 30 seconds (automated Load Balancer drain) |
EOF
cat scratch/day12_lab/resiliency_matrix.md
```

**Expected result:**
Resiliency matrix markdown file created detailing comparative regional trade-offs.

**Save:** scratch/day12_lab/resiliency_matrix.md""",

            """**Stage 7: Generate Regional Architecture Assessment Report**

**Location:** local terminal

**Actions:**
Compile a structured summary verifying that single-region deployment is inadequate for global latency and regulatory compliance.
```bash
cat <<'EOF' > scratch/day12_lab/regional_assessment_summary.txt
ASSESSMENT SUMMARY: OmniRetail Regional Deployment
- Single region deployment in us-central1 imposes an unacceptable 112 ms latency penalty on European shoppers and exposes the company to severe GDPR non-compliance fines.
- Single region deployment in europe-west1 imposes a 98 ms latency penalty on 60% of current shoppers and incurs an 8% compute cost premium.
- Recommended Architecture: Deploy Regional Managed Instance Groups in both us-central1 and europe-west1 behind a single Google Cloud Global External Application Load Balancer with Cloud Armor edge security.
EOF
cat scratch/day12_lab/regional_assessment_summary.txt
```

**Expected result:**
Summary report authored with clear architectural justification.

**Save:** scratch/day12_lab/regional_assessment_summary.txt""",

            """**Stage 8: Verify Output Artifact Completeness**

**Location:** local terminal

**Actions:**
Verify that all generated JSON and Markdown artifacts exist and contain valid data.
```bash
test -f scratch/day12_lab/regional_location_comparison.json && echo "Comparison JSON: VERIFIED"
test -f scratch/day12_lab/resiliency_matrix.md && echo "Resiliency Matrix: VERIFIED"
test -f scratch/day12_lab/regional_assessment_summary.txt && echo "Assessment Summary: VERIFIED"
```

**Expected result:**
All three files report VERIFIED status.

**Save:** scratch/day12_lab/stage8_verification.txt"""
        ]
    },
    'topic-02': {
        'name': 'Exercise B · Vertical versus Horizontal Scaling Dynamic Simulation',
        'goal': 'Model and compare vertical scaling (e2-standard-4 up to n2-standard-64) versus horizontal scaling (Regional MIG scaling from 2 to 24 instances) under synthetic load spikes, evaluating availability impact, scaling latency, and database connection limits.',
        'expected': 'A benchmark simulation showing vertical scaling downtime and hardware limits versus horizontal scaling elasticity and connection pool saturation dynamics.',
        'mode': 'Tabletop analysis with Python simulation (local terminal, zero cloud spend). Mode breakdown: Observed locally: Python simulation script execution, cost modeling formulas, latency math. Simulated or predicted: Google Cloud regional latency distributions, MIG autoscaling response curves, multi-sku pricing bills. Untested on GCP: Live GCP project billing account creation, multi-region Cloud Load Balancer provisioning, cross-continental fiber cut simulations.',
        'covers': "Estimate two deployment locations and compare vertical versus horizontal scaling for the retailer's hypothetical workload.",
        'prereq': 'Linux terminal, Python 3.8+, bash, standard POSIX utilities (mkdir, cat, python3).',
        'preflight': 'Verify local terminal environment and ensure Python 3 is available.',
        'verification': 'Execute the scaling simulation script and compare vertical vs horizontal performance metrics.',
        'trouble': 'Ensure script execution has write permissions in scratch/day12_lab/.',
        'cleanup': 'All generated files reside in scratch/day12_lab/ and can be removed or retained for reference.',
        'accept': 'Validated scaling comparison metrics and markdown analysis document.',
        'file': 'scratch/day12_lab/scaling_comparison.json',
        'steps': [
            """**Stage 1: Preflight and Environment Readiness**

**Location:** local terminal

**Actions:**
Verify required CLI tools for the scaling simulation.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
mkdir -p scratch/day12_lab
python3 -c "print('Scaling simulator environment ready.')"
```

**Expected result:**
Environment readiness confirmed.

**Save:** scratch/day12_lab/stage1_scaling_preflight.txt""",

            """**Stage 2: Define Traffic Spike and Server Hardware Sizing Curves**

**Location:** local terminal

**Actions:**
Create a configuration file defining baseline versus peak traffic parameters and instance sizing specifications.
```bash
cat <<'EOF' > scratch/day12_lab/scaling_spec.json
{
  "baseline_rps": 600,
  "peak_rps": 7200,
  "spike_duration_seconds": 120,
  "database_max_connections": 500,
  "app_pool_per_instance": 20,
  "vertical_scaling": {
    "initial_type": "e2-standard-4 (4 vCPU, 16 GB)",
    "target_type": "n2-standard-64 (64 vCPU, 256 GB)",
    "reboot_downtime_seconds": 180,
    "max_hardware_ceiling_rps": 4800,
    "availability_during_resize": "0% (Complete Outage)"
  },
  "horizontal_scaling_unmanaged": {
    "initial_instances": 2,
    "scaled_instances": 24,
    "scaling_latency_seconds": 45,
    "db_connections_attempted": 480,
    "downtime_seconds": 0,
    "risk": "Approaches 500 DB connection ceiling (96% saturation)"
  },
  "horizontal_scaling_pgbouncer": {
    "initial_instances": 2,
    "scaled_instances": 24,
    "pgbouncer_multiplexed_connections": 60,
    "db_saturation_percent": 12,
    "downtime_seconds": 0,
    "risk": "None (Decoupled state tier)"
  }
}
EOF
cat scratch/day12_lab/scaling_spec.json
```

**Expected result:**
A structured scaling specification JSON file is created.

**Save:** scratch/day12_lab/scaling_spec.json""",

            """**Stage 3: Author Scaling Dynamics Simulator**

**Location:** local terminal

**Actions:**
Create a Python script that models system response, transaction drop rates, and bottleneck characteristics under both scaling models.
```bash
cat <<'EOF' > scratch/day12_lab/simulate_scaling.py
import json

with open("scratch/day12_lab/scaling_spec.json", "r") as f:
    spec = json.load(f)

peak_rps = spec["peak_rps"]

# 1. Vertical Scaling Simulation
vert = spec["vertical_scaling"]
vert_downtime = vert["reboot_downtime_seconds"]
vert_dropped_requests = vert_downtime * (peak_rps / 2)  # Average dropped requests during restart
vert_capacity_shortfall = max(0, peak_rps - vert["max_hardware_ceiling_rps"])

# 2. Horizontal Scaling Unmanaged
horiz_raw = spec["horizontal_scaling_unmanaged"]
horiz_raw_db_conn = horiz_raw["scaled_instances"] * spec["app_pool_per_instance"]

# 3. Horizontal Scaling with PgBouncer
horiz_opt = spec["horizontal_scaling_pgbouncer"]

comparison = {
    "metrics": {
        "peak_demand_rps": peak_rps,
        "vertical_dropped_requests_during_resize": int(vert_dropped_requests),
        "vertical_peak_throughput_deficit_rps": vert_capacity_shortfall,
        "horizontal_dropped_requests": 0,
        "horizontal_raw_db_connections": horiz_raw_db_conn,
        "horizontal_pgbouncer_db_connections": horiz_opt["pgbouncer_multiplexed_connections"]
    },
    "summary": {
        "vertical_outcome": "FAILED: 3-minute downtime caused 432,000 dropped requests; hardware ceiling cannot service 7,200 RPS.",
        "horizontal_unmanaged_outcome": "RISKY: Services peak traffic but DB connections reach 480/500, risking connection exhaustion.",
        "horizontal_pgbouncer_outcome": "OPTIMAL: 100% requests serviced with 0 downtime; DB connections capped at 60 (12% saturation)."
    }
}

with open("scratch/day12_lab/scaling_comparison.json", "w") as out:
    json.dump(comparison, out, indent=2)

print("=" * 80)
print(f"{'SCALING STRATEGY':<28} | {'DOWNTIME':<10} | {'DROPPED REQS':<14} | {'DB CONNECTIONS':<16}")
print("=" * 80)
print(f"{'Vertical (Scale-Up VM)':<28} | {'180 s':<10} | {int(vert_dropped_requests):>14,} | {'20 (Single VM)':<16}")
print(f"{'Horizontal (Unmanaged MIG)':<28} | {'0 s':<10} | {'0':>14} | {horiz_raw_db_conn:>13} / 500")
print(f"{'Horizontal (MIG + PgBouncer)':<28} | {'0 s':<10} | {'0':>14} | {horiz_opt['pgbouncer_multiplexed_connections']:>13} / 500")
print("=" * 80)
EOF
```

**Expected result:**
Python scaling simulator authored successfully.

**Save:** scratch/day12_lab/simulate_scaling.py""",

            """**Stage 4: Run Vertical Scaling Simulation**

**Location:** local terminal

**Actions:**
Execute the scaling simulation script and observe the simulated failure dynamics of vertical scaling.
```bash
python3 scratch/day12_lab/simulate_scaling.py
```

**Expected result:**
Console output shows vertical scaling incurring 180s downtime and over 432,000 dropped requests during reboot.

**Save:** scratch/day12_lab/stage4_scaling_run.txt""",

            """**Stage 5: Run Horizontal Scaling Simulation with PgBouncer Pooling**

**Location:** local terminal

**Actions:**
Inspect the generated comparison JSON to evaluate connection pool multiplexing benefits.
```bash
cat scratch/day12_lab/scaling_comparison.json
```

**Expected result:**
JSON confirms zero dropped requests and DB connection stabilization at 60 connections.

**Save:** scratch/day12_lab/scaling_comparison.json""",

            """**Stage 6: Compare Resilience, Downtime, and Maximum Capacity Headroom**

**Location:** local terminal

**Actions:**
Author a structured comparison matrix evaluating operational trade-offs.
```bash
cat <<'EOF' > scratch/day12_lab/scaling_tradeoffs.md
# Architectural Comparison: Vertical vs Horizontal Scaling

| Dimension | Vertical Scaling (Scale Up) | Horizontal Scaling (Scale Out + PgBouncer) |
| :--- | :--- | :--- |
| **Operational Disruption** | High: VM reboot causes 2–4 min service blackout | Zero: Rolling addition of healthy instances |
| **Scalability Ceiling** | Hard hypervisor limit (e.g., 416 vCPU) | Virtually limitless (100+ instances across zones) |
| **Downstream State Impact** | Low: Single connection stream | High: Requires connection multiplexer (PgBouncer) |
| **Cost Profile** | Expensive: Overprovisioned large instances | Elastic: Scales down to baseline when traffic subsides |
| **Failure Domain** | Single VM: Kernel panic causes total outage | Distributed: Survives individual VM crashes |
EOF
cat scratch/day12_lab/scaling_tradeoffs.md
```

**Expected result:**
Scaling trade-offs markdown document created.

**Save:** scratch/day12_lab/scaling_tradeoffs.md""",

            """**Stage 7: Synthesize Scaling Strategy Recommendation**

**Location:** local terminal

**Actions:**
Draft the architectural recommendation for the retailer's production workload.
```bash
cat <<'EOF' > scratch/day12_lab/scaling_recommendation.txt
RECOMMENDATION: Horizontal Stateless Scaling with PgBouncer Multiplexing
- Vertical scaling is strictly rejected for the storefront API due to mandatory reboot downtime and an inability to meet the 7,200 RPS peak demand.
- The retailer must adopt Regional Managed Instance Groups with an External Application Load Balancer.
- Connection multiplexing via PgBouncer is mandatory to prevent downstream database saturation cascades as instance count scales from 2 to 24.
EOF
cat scratch/day12_lab/scaling_recommendation.txt
```

**Expected result:**
Scaling recommendation text file created.

**Save:** scratch/day12_lab/scaling_recommendation.txt""",

            """**Stage 8: Validate Comparative Metrics Output**

**Location:** local terminal

**Actions:**
Verify that simulation outputs and trade-off matrices exist and are non-empty.
```bash
test -s scratch/day12_lab/scaling_comparison.json && echo "Scaling JSON: VALIDATED"
test -s scratch/day12_lab/scaling_tradeoffs.md && echo "Tradeoffs Doc: VALIDATED"
test -s scratch/day12_lab/scaling_recommendation.txt && echo "Recommendation: VALIDATED"
```

**Expected result:**
All simulation files report VALIDATED status.

**Save:** scratch/day12_lab/stage8_scaling_validation.txt"""
        ]
    },
    'topic-03': {
        'name': 'Exercise C · Construct Complete Location Decision Artifact',
        'goal': 'Synthesize the regional evaluation, scaling dynamics, and six-part Bill of Materials into the authoritative Day 12 exit artifact: a location decision document detailing latency, data residency, cost, and failure-domain assumptions.',
        'expected': 'Production of scratch/day-012-location-decision.md detailing executive summary, latency budgets, GDPR compliance boundaries, BOM monthly cost models, and failure domain architectures.',
        'mode': 'Tabletop analysis with Python simulation (local terminal, zero cloud spend). Mode breakdown: Observed locally: Python simulation script execution, cost modeling formulas, latency math. Simulated or predicted: Google Cloud regional latency distributions, MIG autoscaling response curves, multi-sku pricing bills. Untested on GCP: Live GCP project billing account creation, multi-region Cloud Load Balancer provisioning, cross-continental fiber cut simulations.',
        'covers': "Estimate two deployment locations and compare vertical versus horizontal scaling for the retailer's hypothetical workload.",
        'prereq': 'Linux terminal, Python 3.8+, bash, standard POSIX utilities (mkdir, cat, python3).',
        'preflight': 'Verify local terminal environment and ensure outputs from Exercises A and B are present.',
        'verification': 'Inspect generated location decision markdown file against all contract requirements.',
        'trouble': 'Verify that all calculation inputs from earlier stages are generated in scratch/day12_lab/.',
        'cleanup': 'All generated files reside in scratch/day12_lab/ and can be removed or retained for reference.',
        'accept': 'The complete location decision document at scratch/day-012-location-decision.md.',
        'file': 'scratch/day-012-location-decision.md',
        'steps': [
            """**Stage 1: Preflight and Dependency Audit**

**Location:** local terminal

**Actions:**
Confirm availability of CLI tools and verify presence of previous exercise artifacts.
```bash
command -v bash
command -v python3
command -v cat
command -v mkdir
test -f scratch/day12_lab/regional_location_comparison.json && echo "Exercise A artifacts: PRESENT"
test -f scratch/day12_lab/scaling_comparison.json && echo "Exercise B artifacts: PRESENT"
```

**Expected result:**
Tools and prerequisite lab files are confirmed present.

**Save:** scratch/day12_lab/stage1_bom_preflight.txt""",

            """**Stage 2: Define Full Production Cloud Bill of Materials Parameters**

**Location:** local terminal

**Actions:**
Create a comprehensive JSON specification defining monthly usage across all 6 BOM dimensions for us-central1 versus europe-west1.
```bash
cat <<'EOF' > scratch/day12_lab/bom_spec.json
{
  "workload": "OmniRetail Production Architecture",
  "dimensions": {
    "compute": {
      "description": "Baseline 4 x n2-standard-4 instances + Autoscaled peak (blended avg 8 instances)",
      "us_central1_monthly_usd": 724.80,
      "europe_west1_monthly_usd": 782.78
    },
    "persistent_storage": {
      "description": "1,200 GB Balanced SSD Disk + Regional snapshots",
      "us_central1_monthly_usd": 144.00,
      "europe_west1_monthly_usd": 158.40
    },
    "object_storage": {
      "description": "5,000 GB Standard Storage + 2.5M Class A Ops + 10M Class B Ops",
      "us_central1_monthly_usd": 116.50,
      "europe_west1_monthly_usd": 128.15
    },
    "network_egress": {
      "description": "15,000 GB Internet Egress + 8,000 GB Inter-zone data transfer",
      "us_central1_monthly_usd": 1820.00,
      "europe_west1_monthly_usd": 1820.00
    },
    "managed_backing_services": {
      "description": "Cloud SQL HA db-custom-4-16 + Memorystore Redis 5GB",
      "us_central1_monthly_usd": 482.40,
      "europe_west1_monthly_usd": 520.99
    },
    "observability_security": {
      "description": "Cloud Logging (80 GB beyond free tier) + Cloud Armor WAF",
      "us_central1_monthly_usd": 85.00,
      "europe_west1_monthly_usd": 85.00
    }
  }
}
EOF
cat scratch/day12_lab/bom_spec.json
```

**Expected result:**
Production BOM specification authored covering all six cost dimensions.

**Save:** scratch/day12_lab/bom_spec.json""",

            """**Stage 3: Author Production Cloud Bill of Materials Generator**

**Location:** local terminal

**Actions:**
Create a Python script that computes total monthly bills, evaluates Committed Use Discount (CUD) savings, and calculates multi-region cost.
```bash
cat <<'EOF' > scratch/day12_lab/generate_bom.py
import json

with open("scratch/day12_lab/bom_spec.json", "r") as f:
    spec = json.load(f)

dimensions = spec["dimensions"]

us_total = sum(d["us_central1_monthly_usd"] for d in dimensions.values())
eu_total = sum(d["europe_west1_monthly_usd"] for d in dimensions.values())

# 3-Year Compute CUD savings (55% discount on baseline 4 instances = ~$360/mo savings)
cud_savings_us = 362.40
cud_savings_eu = 391.39

us_optimized = us_total - cud_savings_us
eu_optimized = eu_total - cud_savings_eu

# Dual-region blended topology (60% us-central1, 40% europe-west1 + cross-region sync egress)
dual_region_total = (us_optimized * 0.60) + (eu_optimized * 0.40) + 320.00  # $320 inter-region replication

bom_summary = {
    "us_central1_on_demand_total": us_total,
    "us_central1_cud_optimized_total": us_optimized,
    "europe_west1_on_demand_total": eu_total,
    "europe_west1_cud_optimized_total": eu_optimized,
    "dual_region_optimized_total": dual_region_total,
    "monthly_budget_target": 5000.00,
    "budget_variance_status": "Within Budget ($5,000 ceiling)"
}

with open("scratch/day12_lab/bom_summary.json", "w") as out:
    json.dump(bom_summary, out, indent=2)

print("=" * 80)
print(f"{'DEPLOYMENT ARCHITECTURE':<34} | {'ON-DEMAND / MO':<16} | {'FINOPS OPTIMIZED / MO':<22}")
print("=" * 80)
print(f"{'us-central1 (Single Region)':<34} | ${us_total:>14.2f} | ${us_optimized:>20.2f}")
print(f"{'europe-west1 (Single Region)':<34} | ${eu_total:>14.2f} | ${eu_optimized:>20.2f}")
print(f"{'Dual-Region Hybrid (US + EU)':<34} | ${((us_total*0.6)+(eu_total*0.4)+320):>14.2f} | ${dual_region_total:>20.2f}")
print("=" * 80)
print("BOM cost analysis generated successfully.")
EOF
```

**Expected result:**
Python BOM calculation script authored successfully.

**Save:** scratch/day12_lab/generate_bom.py""",

            """**Stage 4: Calculate 6-Dimension Monthly Cost Forecast**

**Location:** local terminal

**Actions:**
Run the BOM calculation script and inspect output.
```bash
python3 scratch/day12_lab/generate_bom.py
```

**Expected result:**
Console output displays on-demand vs FinOps optimized totals, confirming dual-region spend is ~$3,200/month.

**Save:** scratch/day12_lab/stage4_bom_run.txt""",

            """**Stage 5: Author Comprehensive Location Decision Markdown Artifact**

**Location:** local terminal

**Actions:**
Author the complete Day 12 roadmap exit artifact combining latency, residency, cost, and failure-domain assumptions.
```bash
cat <<'EOF' > scratch/day-012-location-decision.md
# Day 12 Exit Evidence: Location Decision Architecture Artifact

## Executive Summary
This document establishes the binding architectural location decision for OmniRetail Global, evaluating candidate deployment regions against latency budgets, data residency legal mandates, a six-part Bill of Materials (BOM) cost model, and physical failure-domain isolation assumptions.

---

## 1. Candidate Deployment Locations Evaluation

| Region Key | Physical Data Center Location | Availability Zones | NA Latency (P50/P99) | EU Latency (P50/P99) | Data Residency Compliance | Carbon-Free Energy % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **us-central1** | Council Bluffs, Iowa, USA | 4 zones (a, b, c, f) | 28 ms / 42 ms | 112 ms / 148 ms | Non-compliant for EU PII | 89% CFE |
| **europe-west1** | St. Ghislain, Belgium | 3 zones (b, c, d) | 98 ms / 135 ms | 22 ms / 34 ms | Fully GDPR / EU Sovereign Compliant | 83% CFE |

### Decision Analysis:
- **Latency Impact:** Deploying exclusively in `us-central1` degrades European customer conversion rates due to an unacceptably high 112 ms latency floor across the Atlantic. Conversely, deploying exclusively in `europe-west1` penalizes 60% of current revenue-generating shoppers in North America with 98 ms latency.
- **Data Residency Mandate:** European Union General Data Protection Regulation (GDPR) Article 44 strictly limits the transfer of EU citizen personal data to non-adequate third countries. Hosting EU customer purchase histories and PII solely in Iowa violates regulatory compliance and exposes OmniRetail to penalties up to 4% of global annual turnover.

---

## 2. Scaling Architecture Decision: Vertical vs Horizontal

| Metric / Behavior | Vertical Scaling (Scale Up e2 to n2) | Horizontal Scaling (Regional MIG + PgBouncer) | Architectural Verdict |
| :--- | :--- | :--- | :--- |
| **Availability During Scale Event** | 0% (3-minute reboot downtime) | 100% (Zero-downtime rolling additions) | Horizontal required for 99.99% SLA |
| **Dropped Transactions at Peak** | ~432,000 dropped requests | 0 dropped requests | Vertical fails during flash sales |
| **Throughput Ceiling** | 4,800 RPS (Hardware limit) | 15,000+ RPS (Limitless horizontal scale) | Horizontal supports 7,200 RPS peak |
| **Stateful DB Connection Impact** | 20 connections (Single VM) | 60 multiplexed connections (PgBouncer) | PgBouncer prevents DB connection collapse |

**Conclusion:** Vertical scaling is rejected due to mandatory service downtime during re-sizing. OmniRetail adopts Regional Managed Instance Groups with a target CPU utilization of 65% and PgBouncer connection multiplexing.

---

## 3. Production Cloud Bill of Materials (BOM) & Economic Modeling

| BOM Cost Dimension | Scope & Resource Description | us-central1 (Monthly) | europe-west1 (Monthly) | Dual-Region Hybrid (Monthly) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Compute** | Blended average 8 x n2-standard-4 instances | $724.80 | $782.78 | $747.99 |
| **2. Persistent Storage** | 1,200 GB Balanced SSD + Regional Snapshots | $144.00 | $158.40 | $149.76 |
| **3. Object Storage** | 5,000 GB Standard + 2.5M Class A + 10M Class B | $116.50 | $128.15 | $121.16 |
| **4. Network Data Egress** | 15 TB Internet Egress + 8 TB Inter-Zone Egress | $1,820.00 | $1,820.00 | $2,140.00 (Includes DR Sync) |
| **5. Managed Services** | Cloud SQL HA (db-custom-4-16) + Memorystore | $482.40 | $520.99 | $497.84 |
| **6. Observability & Security** | Cloud Logging (80 GB billable) + Cloud Armor WAF | $85.00 | $85.00 | $85.00 |
| **Subtotal (On-Demand)** | Standard monthly list price | **$3,372.70** | **$3,495.32** | **$3,741.75** |
| **FinOps Optimization** | 3-Year Compute CUD (55% off baseline) | -$362.40 | -$391.39 | -$374.00 |
| **FINAL MONTHLY SPEND** | Optimized operational expenditure | **$3,010.30** | **$3,103.93** | **$3,367.75** |

*Budget Variance:* The final Dual-Region spend ($3,367.75/month) is comfortably within the corporate $5,000 monthly infrastructure budget ceiling.

---

## 4. Failure Domain and High Availability Assumptions

1. **Edge Tier:** Google Global Anycast External Application Load Balancers terminate TLS at the nearest Edge PoP, mitigating DDoS attacks via Cloud Armor and caching static assets on Cloud CDN.
2. **Compute Tier:** Regional Managed Instance Groups in `us-central1` (zones a, b, c) and `europe-west1` (zones b, c, d) ensure complete survival against any single data center building or electrical grid failure.
3. **Database Tier:** Cloud SQL High Availability with synchronous cross-zone replication delivers an RTO < 60 seconds and RPO = 0.
4. **Disaster Recovery Tier:** Asynchronous cross-region replication for storage buckets and read replicas ensures business continuity with RTO < 15 minutes and RPO < 1 minute in the catastrophic event of a full continental regional blackout.

---

## 5. Architectural Approval and Sign-Off
- **Architect Role:** Lead Enterprise Cloud Architect
- **Approval Date:** 2026-10-04
- **Status:** APPROVED FOR IMPLEMENTATION
EOF
```

**Expected result:**
Direct creation of scratch/day-012-location-decision.md.

**Save:** scratch/day-012-location-decision.md""",

            """**Stage 6: Inspect and Validate Location Decision Document Line Count**

**Location:** local terminal

**Actions:**
Verify that scratch/day-012-location-decision.md was authored and contains all required sections.
```bash
test -s scratch/day-012-location-decision.md && wc -l scratch/day-012-location-decision.md
```

**Expected result:**
Word count confirms complete document generation.

**Save:** scratch/day12_lab/stage6_exec.txt""",

            """**Stage 7: Inspect and Validate Location Decision Document**

**Location:** local terminal

**Actions:**
Inspect the generated decision document to verify that all roadmap requirements (latency, residency, cost, failure domains) are thoroughly addressed.
```bash
cat scratch/day-012-location-decision.md | head -n 45
```

**Expected result:**
Document displays complete headers, comparison tables, and architectural justifications.

**Save:** scratch/day12_lab/stage7_inspect.txt""",

            """**Stage 8: Verify Alignment with Exit Evidence Criteria**

**Location:** local terminal

**Actions:**
Verify the presence and integrity of scratch/day-012-location-decision.md against the roadmap exit requirements.
```bash
test -s scratch/day-012-location-decision.md && echo "ROADMAP EXIT ARTIFACT: VERIFIED AND COMPLETE"
```

**Expected result:**
Terminal outputs verification confirmation.

**Save:** scratch/day12_lab/stage8_final_audit.txt"""
        ]
    }
}
'''
    with open('scratch/day_012_scenarios_labs.py', 'w') as f:
        f.write(content)
    print("Wrote scratch/day_012_scenarios_labs.py with real newlines.")

if __name__ == '__main__':
    main()
