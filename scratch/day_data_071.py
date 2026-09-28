"""day_data_071.py — Exhaustive architecture data specification for Day 71.

Covers Performance, Sustainability, System Design, and Conflicting Architectural Trade-offs.
Follows PAGE_AUTHORING_CONTRACT.md with deep technical mechanics, trade-off matrices,
dual-lane failure investigations, and runnable lab exercises.
"""

DAY_NUM = 71

DATA = {
    "day": 71,
    "part1_intro": (
        "Day 71 deepens the Well-Architected Framework by mastering the two remaining pillars—Performance Optimization "
        "and Sustainability—while confronting the primary intellectual challenge of enterprise architecture: managing "
        "conflicting objectives. No real-world architecture maximizes every virtue simultaneously. Reliability costs money; "
        "deep packet inspection and Zero-Trust mTLS add network latency; high-frequency batch syncing consumes carbon and "
        "egress bandwidth. Architects do not seek mythical perfection; they engineer defensible, measurable trade-offs. "
        "This session provides the mathematical formulas, regional carbon metrics, storage IOPS models, and formal Architecture "
        "Decision Record (ADR) methodologies required to defend multi-variable design decisions under strict business constraints."
    ),
    "exit_summary": (
        "Completed comprehensive Performance and Sustainability audits across the Brightloaf workload; developed a storage IOPS "
        "sizing calculator, executed a regional carbon footprint evaluation (shifting non-urgent compute to 90%+ CFE regions), "
        "and documented formal Architecture Decision Records resolving the classic tensions between cost, latency, and reliability."
    ),
    "part2_intro": (
        "The sections below provide deep technical analyses of storage thermodynamics, low-carbon grid physics, "
        "system decoupling patterns, and structured decision frameworks for resolving multi-pillar architectural conflicts."
    ),
    "arch_table_html": """<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Evaluation Lens</th>
      <th>Architectural Goal</th>
      <th>Primary Conflict / Cost</th>
      <th>Engineering Resolution Pattern</th>
      <th>Target Optimization Metric</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Performance Optimization</strong></td>
      <td>Sub-second p99 response times; high IOPS</td>
      <td>Premium network tariffs; expensive NVMe tiers</td>
      <td>Tiered caching, Hyperdisk Balanced right-sizing</td>
      <td>Disk queue depth &lt; 4; p99 latency &lt; 50 ms</td>
    </tr>
    <tr>
      <td><strong>Sustainability (GreenOps)</strong></td>
      <td>Minimize carbon emissions (Scope 2/3)</td>
      <td>Latency penalties from distant green regions</td>
      <td>Temporal job shifting; selecting &gt; 85% CFE regions</td>
      <td>Carbon-Free Energy (CFE%) &gt; 80%; idle kWh minimized</td>
    </tr>
    <tr>
      <td><strong>System Design Patterns</strong></td>
      <td>Decouple failure domains; elastic scale</td>
      <td>Eventual consistency; distributed tracing overhead</td>
      <td>Event-driven choreography; Cloud Tasks rate limiting</td>
      <td>Zero cascading failovers; bounded backpressure</td>
    </tr>
    <tr>
      <td><strong>Trade-off Governance</strong></td>
      <td>Align architecture with business priorities</td>
      <td>Subjective team disputes; architectural drift</td>
      <td>Weighted decision matrices; formal ADR registers</td>
      <td>100% architectural changes backed by versioned ADRs</td>
    </tr>
  </tbody>
</table>
</div>""",
    "arch_diagram": {
        "title": "Day 71: Multi-Variable Architectural Trade-off Balancing Flow",
        "desc": "Resolving tensions between performance, sustainability, cost, and reliability through weighted evaluation.",
        "nodes": [
            ("Constraints", "Business Drivers\\n+ SLA/SLO Requirements"),
            ("Analysis", "Storage & Carbon Profiling\\n+ IOPS & CFE% Evaluation"),
            ("Resolution", "Weighted Trade-off Matrix\\n+ Pillar Conflict Arbitration"),
            ("Artifact", "Formal ADR\\n+ Measurable Verification"),
        ],
        "caption": "Figure 71.1: Structured architectural decision flow converting conflicting business constraints into defensible ADRs."
    },
    "part3_intro": (
        "The following field cases investigate severe system breakdowns triggered by unmanaged architectural trade-offs. "
        "Each case details the real-world scenario, quantifiable impact, diagnostic trace, defensible remediation sequence, "
        "and responsive dual-lane SVG diagrams."
    ),
    "part4_intro": (
        "These hands-on exercises provide production-grade, executable configurations and verification scripts for "
        "profiling storage IOPS, evaluating regional carbon footprints, simulating token-bucket rate limiters, and "
        "generating weighted decision matrices."
    ),
    "topics": [
        {
            "key": "topic-01",
            "title": "Performance Optimization Pillar: Compute Sizing, Storage IOPS, and Network Tiers",
            "overview": (
                "Optimize performance across compute, storage, and networking layers. Model disk IOPS scaling with Hyperdisk, "
                "eliminate I/O queue bottlenecks, and evaluate Google Cloud Premium vs Standard network tiers."
            ),
            "preview": (
                "An e-commerce order processing database grinds to a halt during peak sales because the Persistent Disk volume was "
                "provisioned with insufficient capacity, capping disk IOPS at 300 and causing query queues to back up indefinitely."
            ),
            "technical": (
                "#### 1. Storage Thermodynamics: IOPS, Throughput, and Queue Depth\n\n"
                "In Google Cloud, disk performance is decoupled from physical server drives and delivered via a distributed SDN storage "
                "fabric. With standard Persistent Disk (PD), IOPS and throughput scale linearly with provisioned disk size (e.g. 30 IOPS "
                "per GB on pd-ssd up to instance limits). Provisioning a small 50GB disk for a database caps performance at 1,500 IOPS, "
                "regardless of whether the underlying VM possesses 64 vCPUs.\n\n"
                "- **Hyperdisk Generation:** Google Cloud Hyperdisk decouples storage capacity from performance. Architects provision "
                "capacity (GB), IOPS, and Throughput (MB/s) independently:\n\n"
                "```sh\n"
                "# Create Hyperdisk Balanced with customized performance\n"
                "gcloud compute disks create brightloaf-db-disk \\\n"
                "  --zone=us-central1-a \\\n"
                "  --type=hyperdisk-balanced \\\n"
                "  --size=200GB \\\n"
                "  --provisioned-iops=10000 \\\n"
                "  --provisioned-throughput=250\n"
                "```\n\n"
                "- **Queue Depth Dynamics:** When application threads issue I/O requests faster than the storage tier can acknowledge them, "
                "the operating system I/O queue depth expands. If queue depth exceeds optimal limits (typically 16 to 32 on Linux), thread "
                "wait states (`iowait`) skyrocket, freezing application worker runtimes.\n\n"
                "#### 2. Network Tiers: Premium vs Standard\n\n"
                "Google Cloud offers two global network routing tiers:\n\n"
                "  1. **Premium Tier (Default):** Ingress traffic enters Google's private global fiber backbone at the edge PoP nearest to the "
                "user (Cold Potato routing). Traffic traverses Google's private low-jitter network directly to the origin region, bypassing the "
                "congested public internet.\n"
                "  2. **Standard Tier:** Traffic is handed off to public transit ISPs as quickly as possible (Hot Potato routing). Lower cost, "
                "but subject to ISP peering congestion, variable packet loss, and higher jitter. Ideal for non-latency-critical bulk data transfers.\n\n"
                "#### 3. Memory Hierarchy and Cache Locality\n\n"
                "Optimizing compute performance requires understanding hardware memory latency tiers:\n\n"
                "- L1/L2/L3 CPU Cache: 1–10 ns\n"
                "- Main RAM (DDR5): 50–100 ns\n"
                "- Local SSD (NVMe via PCIe): 10–50 µs\n"
                "- Network Storage (Hyperdisk / PD): 500 µs – 2 ms\n"
                "- Cross-Region Network Hop: 30 – 120 ms\n\n"
                "Application architectures that eliminate remote database round-trips via in-memory caching (Memorystore Redis) achieve "
                "a 1,000x reduction in request latency.\n\n"
                "#### 4. Kernel Tuning and TCP Socket Buffers\n\n"
                "High-throughput networking on Compute Engine VMs requires tuning Linux kernel network stack parameters (`sysctl`). Default "
                "TCP buffer limits (`rmem_max`, `wmem_max`) throttle single-connection TCP window sizes on high-bandwidth cross-region links "
                "(Bandwidth-Delay Product limitation).\n\n"
                "#### 5. Architectural Trade-offs: Storage Performance Primitives\n\n"
                "| Storage Primitive | Max Read IOPS | Max Throughput | Latency (p99) | Persistence / Durability | Relative Cost |\n"
                "|---|---|---|---|---|---|\n"
                "| **Local SSD (NVMe)** | Up to 2,400,000 | Up to 9,600 MB/s | Sub-millisecond (< 50 µs) | Ephemeral (wiped on VM stop) | Moderate (per GB/hr) |\n"
                "| **Hyperdisk Extreme** | Up to 500,000 | Up to 10,000 MB/s | Sub-millisecond (200 µs) | Durable (Regional / Zonal) | Highest |\n"
                "| **Hyperdisk Balanced** | Up to 160,000 | Up to 2,400 MB/s | Low (< 1 ms) | Durable (Flexible sizing) | Moderate |\n"
                "| **Persistent Disk SSD** | Up to 100,000 | Up to 1,200 MB/s | Low (1–2 ms) | Durable (Capacity-bound) | Standard |\n"
                "| **Standard PD (HDD)** | Up to 7,500 | Up to 1,200 MB/s | High (10–25 ms) | Durable (Sequential only) | Lowest |\n"
            ),
            "questions": [
                "Why does provisioning a small Persistent Disk volume starve database performance even on high-vCPU VMs?",
                "What is the difference between Hot Potato routing (Standard Tier) and Cold Potato routing (Premium Tier)?",
                "How does I/O queue depth saturation trigger cascading thread exhaustion in application runtimes?",
                "Under what architectural scenario is Local SSD preferred over durable network storage?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/performance-optimization",
            "reference_label": "Google Cloud Architecture Center: Performance Optimization Pillar",
            "scenario": {
                "scenario": (
                    "During an unannounced flash sale, Brightloaf's primary order fulfillment database on Compute Engine began "
                    "experiencing severe query timeouts. Application API response times degraded from 140ms to 9.2 seconds. While the VM's "
                    "16 vCPUs showed only 28% CPU utilization, Linux `vmstat` reported `wa` (iowait) at 68%. The database disk had been "
                    "provisioned as a standard 100GB `pd-balanced` volume, which capped disk IOPS at 600. The sudden flood of 2,400 write "
                    "transactions per second overwhelmed the disk controller, causing Linux kernel I/O queue depth to explode past 140, "
                    "blocking all database worker threads."
                ),
                "impact": (
                    "P1 operational disruption. Over 6,200 warehouse picking and packing dispatches were delayed by 90 minutes. Delivery "
                    "trucks missed departure windows. SLA penalty fees assessed by retail partners totaled $84,000. Customer cancellation "
                    "rate surged to 16%."
                ),
                "constraints": (
                    "Resolve the storage I/O bottleneck with zero database downtime; ensure storage performance scales independently of "
                    "disk capacity; maintain sub-20ms database write latencies under 5,000 transactions/second."
                ),
                "diagnostic_steps": [
                    "Step 1: Check VM metrics in Cloud Monitoring; observe disk write IOPS flatlined at exactly 600 while I/O queue depth climbed continuously.",
                    "Step 2: SSH into the database instance and run `iostat -xz 1`; identify `%util` at 100% and `await` exceeding 850ms on `/dev/sdb`.",
                    "Step 3: Review disk provisioning configuration; confirm the disk is a 100GB `pd-balanced` volume without custom IOPS provisioning.",
                    "Step 4: Correlate with application thread dumps; observe 180 worker threads stuck in `BLOCKED` state waiting on PostgreSQL WAL write flushes."
                ],
                "root": (
                    "Capacity-coupled storage provisioning capped disk IOPS at 600. High-frequency transactional writes saturated disk I/O, "
                    "exhausting kernel queue depth and blocking database commit operations."
                ),
                "remediation_steps": [
                    "Step 1: Dynamically modify the disk type and performance online: upgrade disk to `hyperdisk-balanced` with 12,000 provisioned IOPS and 300 MB/s throughput using online volume modification.",
                    "Step 2: Move the PostgreSQL Write-Ahead Log (WAL) directory to a dedicated, high-IOPS storage volume to isolate write-heavy sequential logging from random table reads.",
                    "Step 3: Tune PostgreSQL memory configuration parameters (`shared_buffers = 16GB`, `work_mem = 64MB`, `wal_buffers = 16MB`) to optimize in-memory caching and reduce disk sync frequency.",
                    "Step 4: Establish Cloud Monitoring alerting on disk queue depth (`disk/queue_depth > 10` for 2 minutes) to detect I/O saturation before latency spills over to customer APIs."
                ],
                "verify": (
                    "Execute a synthetic transactional benchmark simulating 4,000 writes/second. Verify in Cloud Monitoring that disk IOPS "
                    "surges to 4,200 without saturation, I/O queue depth remains below 4, and p99 transaction write latency stays under 12ms."
                ),
                "residual": (
                    "Hyperdisk Balanced volumes have provisioned billing rates based on configured IOPS and throughput regardless of actual "
                    "consumption; capacity sizing must be audited quarterly to prevent over-paying for idle IOPS headroom."
                ),
                "diagram": (
                    "100GB disk caps IOPS at 600",
                    "I/O queue depth explodes (>140)",
                    "DB freezes, 9.2s latency, $84k loss",
                    "Upgrade to Hyperdisk 12k IOPS online",
                    "Queue depth < 4, latency drops to 12ms"
                ),
                "facts": "100GB pd-balanced disk capped at 600 IOPS; iowait was 68%; I/O queue depth exceeded 140; 6,200 dispatches delayed.",
                "inference": "Capacity-bound storage provisioning creates hidden performance ceilings; decoupling IOPS via Hyperdisk eliminates I/O bottlenecks.",
                "expected": "Hyperdisk Balanced delivers 12,000 IOPS on demand, maintaining sub-15ms transaction write latency under load."
            },
            "lab": {
                "name": "Storage IOPS Modeling and Disk Sizing Benchmarking",
                "file": "day-071-performance-sizing.md",
                "goal": "Model storage IOPS requirements, write a Hyperdisk provisioning script, and benchmark disk queue depth dynamics.",
                "expected": "A complete storage sizing document, a Hyperdisk creation command specification, and an executable Python I/O modeling script.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 70 operational metrics and Day 68 technical requirements",
                "preflight": "Review Google Cloud Hyperdisk documentation and pricing tiers.",
                "steps": [
                    "Draft the storage performance requirements in `day-071-performance-sizing.md`: peak transaction rate = 4,000 writes/sec, average write size = 8 KB, target latency < 15ms.",
                    "Calculate throughput: `4,000 writes/sec * 8 KB = 32,000 KB/s = 31.25 MB/s`. With read traffic (3:1 read-to-write ratio), total IOPS needed = 16,000 IOPS, total throughput = 125 MB/s.",
                    "Define the Hyperdisk Balanced creation command:\n\n```sh\n# Provision Hyperdisk Balanced with decoupled IOPS and throughput\ngcloud compute disks create brightloaf-highperf-data \\\n  --zone=us-central1-a \\\n  --type=hyperdisk-balanced \\\n  --size=250GB \\\n  --provisioned-iops=16000 \\\n  --provisioned-throughput=200\n```",
                    "Develop an executable Python script to model queue depth and disk latency (`io_model.py`):\n\n```python\n# io_model.py\n\ndef model_io_latency(arrival_rate: float, service_capacity_iops: float):\n    # M/M/1 queuing model approximation for I/O queue depth\n    rho = arrival_rate / service_capacity_iops\n    if rho >= 1.0:\n        return float('inf'), float('inf'), rho\n    # Average queue length L = rho / (1 - rho)\n    queue_length = rho / (1.0 - rho)\n    # Average response time W = 1 / (mu - lambda) in seconds\n    response_time_ms = (1.0 / (service_capacity_iops - arrival_rate)) * 1000.0\n    return queue_length, response_time_ms, rho\n\n# Test Old Config: 550 IOPS arrival against 600 IOPS capacity\nq_old, lat_old, util_old = model_io_latency(550, 600)\n# Test Hyperdisk Config: 4000 IOPS arrival against 16000 IOPS capacity\nq_new, lat_new, util_new = model_io_latency(4000, 16000)\n\nprint(f\"Old PD: Utilization={util_old*100:.1f}%, Queue={q_old:.1f}, Latency={lat_old:.2f} ms\")\nprint(f\"Hyperdisk: Utilization={util_new*100:.1f}%, Queue={q_new:.2f}, Latency={lat_new:.2f} ms\")\nassert lat_new < 1.0, \"Hyperdisk latency calculation failed!\"\nprint(\"Storage Performance Modeling Verified Successfully.\")\n```",
                    "Execute the Python storage modeling test:\n\n```sh\npython3 io_model.py\n```"
                ],
                "verification": (
                    "Run automated storage sizing test:\n\n```sh\npython3 -c \"import io_model; print('Storage Model Test Passed')\"\n```\n\nConfirm output displays `Storage Model Test Passed` and verifies latency under 1ms."
                ),
                "trouble": (
                    "If queue depth calculation returns infinity, verify that arrival rate does not exceed provisioned IOPS capacity."
                ),
                "cleanup": "No remote cloud resources created; retain scripts and configuration files in local repository.",
                "accept": "A validated storage sizing calculation, Hyperdisk provisioning command, and working Python queue depth model."
            }
        },
        {
            "key": "topic-02",
            "title": "Sustainability Pillar: Low-Carbon Regions, Carbon-Free Energy, and GreenOps",
            "overview": (
                "Implement environmental sustainability (GreenOps) on Google Cloud. Select low-carbon regions using Carbon-Free Energy "
                "(CFE%) metrics, execute temporal workload shifting, and eliminate zombie compute wattage."
            ),
            "preview": (
                "An organization schedules heavy nightly batch analytics in a high-carbon region powered by coal energy, producing 4.8x "
                "more carbon emissions than if scheduled in a nearby hydro/nuclear-powered low-carbon region."
            ),
            "technical": (
                "#### 1. GreenOps and the Physics of Datacenter Decarbonization\n\n"
                "Cloud computing consumes vast amounts of electrical energy. Google Cloud operates datacenters globally, but the electrical "
                "grids supplying those datacenters vary drastically in their energy sources:\n\n"
                "- **Carbon-Free Energy (CFE%):** The percentage of time a specific Google Cloud region is powered by carbon-free energy "
                "(solar, wind, hydro, nuclear) on an hourly matched basis.\n"
                "- **Grid Carbon Intensity:** The average grams of CO2 equivalent emitted per kilowatt-hour of electricity generated on "
                "that local regional grid (gCO2eq/kWh).\n\n"
                "For example:\n\n"
                "- `europe-north1` (Hamina, Finland): **97% CFE** (low carbon; hydro & nuclear)\n"
                "- `us-central1` (Council Bluffs, Iowa): **89% CFE** (wind-rich)\n"
                "- `asia-south1` (Mumbai, India): **18% CFE** (fossil-heavy coal grid)\n\n"
                "#### 2. Architectural Strategies for Carbon Reduction\n\n"
                "Architects achieve direct emission reductions through three primary engineering levers:\n\n"
                "  1. **Spatial Workload Placement (Region Selection):** For non-latency-sensitive workloads (machine learning training, "
                "nightly BigQuery batch analytics, video transcode pipelines), select regions designated with the 'Low CO2' badge in the Google "
                "Cloud Console (`europe-north1`, `us-west1`, `northamerica-northeast1`).\n"
                "  2. **Temporal Workload Shifting:** Shifting batch processing to hours of peak renewable generation (e.g. running daytime "
                "analytics when regional solar farms produce surplus grid energy).\n"
                "  3. **Elastic Wattage Elimination:** An idle VM running at 5% CPU consumes over 50% of its peak power draw due to baseline "
                "motherboard, RAM refresh, and cooling overhead. Aggressive serverless scale-to-zero (Cloud Run) and ephemeral compute (Dataproc Serverless) "
                "physically turns off Silicon when work is complete.\n\n"
                "#### 3. Google Cloud Carbon Footprint Tool and BigQuery Export\n\n"
                "Google Cloud provides monthly reporting of greenhouse gas emissions associated with cloud usage via the **Carbon Footprint Tool**. "
                "Data is calculated according to the Greenhouse Gas Protocol (GHG Protocol Scope 2: market-based and location-based emissions). "
                "Billing administrators export carbon metrics to BigQuery for automated executive ESG compliance reporting.\n\n"
                "#### 4. The Latency-Carbon Trade-off\n\n"
                "While batch workloads can easily run in Finland or Oregon, real-time user-facing APIs cannot arbitrarily move across continents "
                "without violating latency SLOs. Architects resolve this tension by splitting the workload topology: user-facing presentation "
                "tiers reside close to users, while asynchronous backends and data pipelines reside in high-CFE green regions.\n\n"
                "#### 5. Architectural Trade-offs: Regional Carbon Efficiency\n\n"
                "| Google Cloud Region | CFE Score (%) | Grid Carbon Intensity | Average Network RTT to US East | Primary Energy Source | Recommended Workload |\n"
                "|---|---|---|---|---|---|\n"
                "| **us-west1 (Oregon)** | **92% CFE** | 85 gCO2eq/kWh | ~65 ms | Hydroelectric & Wind | Ideal US Green Tier for ML & Analytics |\n"
                "| **europe-north1 (Finland)** | **97% CFE** | 42 gCO2eq/kWh | ~105 ms | Hydro, Wind & Nuclear | European Green Tier; Global Batch |\n"
                "| **us-central1 (Iowa)** | **89% CFE** | 120 gCO2eq/kWh | ~30 ms | High Wind Capacity | General Purpose US Core Compute |\n"
                "| **us-east4 (N. Virginia)** | **46% CFE** | 340 gCO2eq/kWh | < 5 ms | Mixed Natural Gas & Coal | Latency-critical US East Ingress Only |\n"
                "| **asia-east1 (Taiwan)** | **17% CFE** | 510 gCO2eq/kWh | ~180 ms | High Fossil Fuel Mix | Strictly Regional APAC Ingress |\n"
            ),
            "questions": [
                "What is the difference between hourly-matched Carbon-Free Energy (CFE%) and annual unbundled renewable energy credits?",
                "Why does an idle VM consume more than 50% of its peak electrical power?",
                "How do architects resolve the conflict between choosing a low-carbon region and meeting user latency SLOs?",
                "What metrics are tracked under Scope 2 market-based versus location-based carbon accounting?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/sustainability",
            "reference_label": "Google Cloud Architecture Center: Sustainability pillar",
            "scenario": {
                "scenario": (
                    "Brightloaf's enterprise data team executes a massive daily sales reconciliation and supply-chain forecasting pipeline "
                    "running 12 hours every night across a 40-node Compute Engine Dataproc cluster in `us-east4` (Northern Virginia). "
                    "During an annual corporate sustainability audit, the Chief Sustainability Officer discovered that the data engineering "
                    "pipeline generated 42.8 metric tons of CO2 equivalent annually. Northern Virginia's regional grid had a CFE score of only "
                    "46%, powered heavily by fossil fuels. The company risked failing its board-mandated Net-Zero carbon reduction targets, "
                    "jeopardizing ESG-linked corporate financing lines."
                ),
                "impact": (
                    "ESG compliance failure and regulatory audit citation. Carbon emissions from cloud infrastructure were 3.8x higher than "
                    "necessary. Threat of losing a $15 million sustainability-linked credit facility due to failure to meet Scope 2 reduction targets."
                ),
                "constraints": (
                    "Reduce batch data pipeline carbon emissions by at least 65% within 60 days; do not increase compute infrastructure costs; "
                    "maintain existing 06:00 UTC morning delivery deadlines for executive business reports."
                ),
                "diagnostic_steps": [
                    "Step 1: Open Google Cloud Carbon Footprint dashboard; filter emissions by project and service; identify Dataproc in `us-east4` accounts for 74% of total departmental emissions.",
                    "Step 2: Review regional CFE ratings; observe `us-east4` is 46% CFE, while `us-west1` (Oregon) is 92% CFE and `europe-north1` is 97% CFE.",
                    "Step 3: Check network transfer latency and egress costs between primary storage in `us-central1` and compute in `us-west1`; confirm cross-region transfer completes in 18 minutes without violating report delivery deadlines.",
                    "Step 4: Audit cluster utilization; discover the Dataproc cluster remained running idle for 12 hours during the day after batch completion."
                ],
                "root": (
                    "Workloads were deployed by default to `us-east4` without considering carbon intensity. Failure to use ephemeral "
                    "serverless processing allowed idle VMs to consume power 24/7 on a fossil-heavy grid."
                ),
                "remediation_steps": [
                    "Step 1: Migrate the batch processing pipeline to `us-west1` (Oregon, 92% CFE), immediately cutting grid carbon intensity from 340 gCO2eq/kWh to 85 gCO2eq/kWh.",
                    "Step 2: Replace the permanent 24/7 Dataproc cluster with Dataproc Serverless, ensuring compute resources provision on demand and scale to zero instantly upon job completion.",
                    "Step 3: Establish a Cloud Scheduler trigger initiating the batch run at 01:00 Pacific Time, aligning execution with regional wind energy surges.",
                    "Step 4: Implement organizational policies restricting batch compute deployments to Google Cloud regions with CFE scores exceeding 80%."
                ],
                "verify": (
                    "Monitor the Carbon Footprint BigQuery export following the migration. Verify that monthly carbon emissions for the analytics "
                    "pipeline drop from 3.56 metric tons to 0.88 metric tons CO2eq (a 75.2% reduction) with zero impact on morning report delivery."
                ),
                "residual": (
                    "Cross-region data transfer between `us-central1` storage and `us-west1` compute incurs cross-region network egress costs; "
                    "data transfers must be scheduled in compressed columnar formats (Parquet) to minimize network bytes."
                ),
                "diagram": (
                    "24/7 Dataproc in us-east4 (46% CFE)",
                    "Fossil grid, idle VMs draw power",
                    "42.8 tons CO2/yr, ESG target failed",
                    "Move to us-west1 (92% CFE) + Serverless",
                    "75% carbon cut, scale-to-zero efficiency"
                ),
                "facts": "Dataproc batch ran in us-east4 (46% CFE); emitted 42.8 tons CO2/yr; idle cluster drew power for 12 hours daily.",
                "inference": "Non-urgent batch compute should be spatially and temporally shifted to high-CFE regions and ephemeral runtimes.",
                "expected": "Migrating to us-west1 Dataproc Serverless cuts emissions by 75% while scaling compute to zero upon completion."
            },
            "lab": {
                "name": "Regional Carbon Footprint Evaluation and Workload Placement Model",
                "file": "day-071-sustainability-model.md",
                "goal": "Build an environmental carbon accounting model in Python to evaluate emissions across GCP regions and automate green placement.",
                "expected": "A complete sustainability policy document, a region evaluation matrix, and an executable Python carbon calculation script.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 70 cost modeling and Day 68 technical requirements",
                "preflight": "Review Google Cloud Region Carbon Information dataset and GHG Protocol Scope 2 guidance.",
                "steps": [
                    "Draft the GreenOps regional placement strategy in `day-071-sustainability-model.md`.",
                    "Define the regional carbon comparison dataset in Python (`carbon_calc.py`):\n\n```python\n# carbon_calc.py\n\nREGIONS = {\n    'us-east4': {'name': 'Northern Virginia', 'cfe': 0.46, 'intensity_g_kwh': 340},\n    'us-central1': {'name': 'Iowa', 'cfe': 0.89, 'intensity_g_kwh': 120},\n    'us-west1': {'name': 'Oregon', 'cfe': 0.92, 'intensity_g_kwh': 85},\n    'europe-north1': {'name': 'Finland', 'cfe': 0.97, 'intensity_g_kwh': 42}\n}\n\ndef calculate_annual_emissions(kwh_per_run: float, runs_per_year: int, region_key: str):\n    reg = REGIONS[region_key]\n    total_kwh = kwh_per_run * runs_per_year\n    emissions_kg_co2 = (total_kwh * reg['intensity_g_kwh']) / 1000.0\n    emissions_tons = emissions_kg_co2 / 1000.0\n    return total_kwh, emissions_tons\n\n# Scenario: 40-node batch job consuming 350 kWh per run, 365 runs/year\nkwh_run = 350.0\nruns = 365\n\nkwh, tons_east = calculate_annual_emissions(kwh_run, runs, 'us-east4')\n_, tons_oregon = calculate_annual_emissions(kwh_run, runs, 'us-west1')\n_, tons_finland = calculate_annual_emissions(kwh_run, runs, 'europe-north1')\n\nsavings_tons = tons_east - tons_oregon\npct_reduction = (savings_tons / tons_east) * 100\n\nprint(f\"Annual Energy Consumption: {kwh:,.0f} kWh\")\nprint(f\"us-east4 (Virginia) Emissions: {tons_east:.2f} metric tons CO2eq\")\nprint(f\"us-west1 (Oregon) Emissions: {tons_oregon:.2f} metric tons CO2eq\")\nprint(f\"europe-north1 (Finland) Emissions: {tons_finland:.2f} metric tons CO2eq\")\nprint(f\"Net Reduction (Oregon vs Virginia): {savings_tons:.2f} tons ({pct_reduction:.1f}% reduction)\")\nassert pct_reduction > 70.0, \"Carbon reduction calculation error!\"\nprint(\"Carbon Model Verified Successfully.\")\n```",
                    "Execute the Python carbon footprint model:\n\n```sh\npython3 carbon_calc.py\n```",
                    "Create a gcloud policy definition template restricting batch clusters to green regions:\n\n```sh\ncat << 'EOF' > green-region-policy.json\n{\n  \"constraint\": \"constraints/gcp.resourceLocations\",\n  \"listPolicy\": {\n    \"allowedValues\": [\n      \"in:us-west1-locations\",\n      \"in:europe-north1-locations\"\n    ]\n  }\n}\nEOF\n```"
                ],
                "verification": (
                    "Run automated sustainability calculation verification:\n\n```sh\npython3 -c \"import carbon_calc; print('Carbon Footprint Model Validated')\"\n```\n\nConfirm output shows net carbon reduction exceeding 70%."
                ),
                "trouble": (
                    "If policy constraint deployment fails, verify Access Context Manager organization policy editing privileges."
                ),
                "cleanup": "No remote cloud resources created; retain JSON policies and calculation scripts in local repository.",
                "accept": "A verified GreenOps mathematical model, carbon comparison matrix, and regional constraint policy manifest."
            }
        },
        {
            "key": "topic-03",
            "title": "System Design as Cross-Cutting Guidance: Decoupling, Backpressure, and Idempotency",
            "overview": (
                "Apply core distributed system patterns across all Well-Architected pillars. Implement event-driven decoupling, "
                "token-bucket rate limiting for backpressure, and idempotent request handling."
            ),
            "preview": (
                "A third-party payment gateway suffers a 2-minute outage; callers retry immediately, generating a synchronous "
                "thread cascade that crashes the entire e-commerce checkout tier."
            ),
            "technical": (
                "#### 1. Synchronous vs Asynchronous Boundary Dynamics\n\n"
                "System design is the cross-cutting discipline that binds all Well-Architected lenses together. A foundational rule of "
                "cloud resilience is: **never allow a synchronous dependency to cross an external or multi-tenant boundary**.\n\n"
                "- In a synchronous model (`Client -> Web -> Order API -> Payment Gateway -> DB`), the latency and availability of the entire "
                "chain is bounded by the slowest, least reliable dependency (`Availability = A_web * A_order * A_pay * A_db`). A momentary hiccup "
                "in the payment gateway ties up client threads in the web tier, causing thread exhaustion.\n"
                "- In an asynchronous decoupled model (`Client -> Web -> Pub/Sub / Cloud Tasks -> Worker Pool -> Payment Gateway`), the "
                "ingress tier accepts the order immediately, persists it to durable queue storage, and returns an HTTP 202 Accepted status with "
                "a correlation tracking ID. Downstream workers process tasks asynchronously, buffering load surges safely.\n\n"
                "#### 2. Backpressure and Token Bucket Rate Limiting\n\n"
                "When downstream capacity is bounded (e.g. legacy ERP systems that crash beyond 200 RPS), upstream systems must enforce "
                "**Backpressure**. Cloud Tasks provides native rate-limiting controls:\n\n"
                "```sh\n"
                "# Create Cloud Tasks queue with strict concurrency and rate limits\n"
                "gcloud tasks queues create order-processing-queue \\\n"
                "  --max-dispatches-per-second=150 \\\n"
                "  --max-concurrent-dispatches=50 \\\n"
                "  --max-attempts=10 \\\n"
                "  --min-backoff=2s \\\n"
                "  --max-backoff=60s\n"
                "```\n\n"
                "If the queue depth grows, callers receive backpressure signals rather than overwhelming the downstream service.\n\n"
                "#### 3. Idempotency Keys and the Day 64 Invariant\n\n"
                "In decoupled and asynchronous architectures, network retries guarantee at-least-once delivery. Without idempotency, retries "
                "cause duplicate charges, duplicate inventory allocations, and double shipments, violating the core **Day 64 single-fulfillment invariant**.\n\n"
                "Every state-changing mutation must require an **Idempotency Key** (a client-generated UUID attached to the HTTP request header "
                "`Idempotency-Key: 7b2a8f9c-...`). The server checks an atomic distributed cache (Memorystore Redis `SET key value NX EX 86400`):\n\n"
                "  1. If the key is new: execute the transaction and cache the response.\n"
                "  2. If the key exists: return the previously cached response immediately without re-executing business logic.\n\n"
                "#### 4. Orchestration vs Choreography\n\n"
                "Distributed workflows choose between:\n\n"
                "- **Choreography (Pub/Sub + Eventarc):** Services emit domain events; downstream services react autonomously. Loose coupling, "
                "high scalability, but difficult to visualize end-to-end workflow state.\n"
                "- **Orchestration (Cloud Workflows):** A centralized state machine coordinates steps, manages retries, handles branching logic, "
                "and monitors timeouts. Ideal for complex multi-step sagas (order -> inventory -> payment -> shipment).\n\n"
                "#### 5. Architectural Trade-offs: Decoupling & Orchestration Patterns\n\n"
                "| Pattern Primitive | Coupling Level | Delivery Guarantee | State Visibility | Concurrency Control | Best Suited For |\n"
                "|---|---|---|---|---|---|\n"
                "| **Direct Synchronous (REST/gRPC)** | High (Tight) | At-most-once (or caller retry) | Immediate (Call stack) | None (Caller overwhelms target) | Low-latency read queries, UI data fetching |\n"
                "| **Cloud Tasks Queue** | Low (Loose) | At-least-once (Configurable) | High (Queue depth & metrics) | Built-in Token Bucket Rate Limiting | Dispatching work to rate-limited third-party APIs |\n"
                "| **Cloud Pub/Sub Messaging** | Lowest (Decoupled) | At-least-once (or EOD) | Moderate (Subscription lag) | Horizontal subscriber autoscaling | High-throughput broadcast events, analytics streaming |\n"
                "| **Cloud Workflows Engine** | Moderate (Orchestrated) | Exactly-once state transitions | Highest (Visual execution graph) | Programmatic concurrency branches | Complex transactional sagas, order fulfillment |\n"
            ),
            "questions": [
                "How does converting a synchronous payment call into an asynchronous queue protect the frontend web tier?",
                "Why is an idempotency key required whenever network retries are introduced into a payment flow?",
                "What is the difference between workflow orchestration (Cloud Workflows) and event choreography (Pub/Sub)?",
                "How does Cloud Tasks token bucket rate limiting prevent downstream ERP database collapse?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework/system-design",
            "reference_label": "Google Cloud Architecture Center: System design pillar",
            "scenario": {
                "scenario": (
                    "Brightloaf's checkout system processed orders by making a direct, synchronous HTTP call from the web application "
                    "to a legacy third-party fraud detection API. During an international promotional campaign, the fraud detection vendor "
                    "experienced a database brownout, causing response times to balloon from 200ms to 45 seconds per request. Because the "
                    "call was synchronous and lacked a circuit breaker or timeout ceiling, 250 incoming customer requests per second occupied "
                    "every available thread in the web application container pool. Within 90 seconds, all frontend Compute Engine instances "
                    "exhausted their thread pools and failed their Load Balancer health checks, taking down the entire website."
                ),
                "impact": (
                    "P1 total system outage lasting 48 minutes. Zero orders processed across all retail channels. Over 18,000 active shopping "
                    "carts abandoned. Lost sales estimated at $220,000. Customer trust damaged by browser gateway timeout screens."
                ),
                "constraints": (
                    "Decouple the checkout transaction from third-party API availability; enforce strict backpressure; preserve the Day 64 "
                    "single-fulfillment invariant under all retry scenarios."
                ),
                "diagnostic_steps": [
                    "Step 1: Inspect Load Balancer backend service metrics; observe 100% of compute instances marked UNHEALTHY simultaneously.",
                    "Step 2: Review web application thread dumps; identify 500+ threads in `WAITING` state on `SocketInputStream.socketRead0()` to external fraud vendor IP.",
                    "Step 3: Audit client timeout configurations; discover HTTP client timeout was set to 60 seconds with unlimited retries.",
                    "Step 4: Check architecture documentation; confirm zero asynchronous queuing or backpressure buffers between web tier and external vendor."
                ],
                "root": (
                    "Synchronous coupling to an external third-party service without timeouts, circuit breakers, or asynchronous queuing "
                    "caused a downstream brownout to propagate upstream, starving application threads and collapsing ingress compute."
                ),
                "remediation_steps": [
                    "Step 1: Immediately configure strict client-side HTTP timeouts (socket timeout = 2.5s) with a circuit breaker tripping after 5 consecutive timeouts.",
                    "Step 2: Decouple the fraud check: publish order events to Cloud Tasks (`order-processing-queue`) configured with rate limiting (150 dispatches/sec).",
                    "Step 3: Implement Redis-backed idempotency tokens (`Idempotency-Key` header) across all order processing endpoints, enforcing the Day 64 single-fulfillment invariant.",
                    "Step 4: Return an immediate HTTP 202 Accepted response to the customer upon queue commit, polling or streaming status updates via WebSockets."
                ],
                "verify": (
                    "Inject a simulated 30-second delay into the fraud detection mock endpoint. Verify that the frontend web tier continues "
                    "serving checkouts in under 180ms, tasks queue safely in Cloud Tasks, and zero duplicate order fulfillments occur."
                ),
                "residual": (
                    "Asynchronous order acceptance requires robust frontend polling or push notifications to inform customers of delayed "
                    "payment authorizations or fraud rejections."
                ),
                "diagram": (
                    "Sync call to slow fraud API",
                    "500 threads blocked on I/O",
                    "All VMs fail health checks (504)",
                    "Decouple via Cloud Tasks + Idempotency",
                    "202 Accepted, rate-limited execution"
                ),
                "facts": "Synchronous fraud API took 45s; web thread pools exhausted; all VMs failed health checks; site down for 48 minutes.",
                "inference": "Synchronous dependencies across network boundaries cause cascading thread starvation; asynchronous queues isolate failure domains.",
                "expected": "Cloud Tasks buffers traffic surges and rate-limits downstream calls, keeping frontend web APIs responsive."
            },
            "lab": {
                "name": "Asynchronous Decoupling and Token-Bucket Rate Limiter Simulation",
                "file": "day-071-system-design.md",
                "goal": "Build an executable Python token-bucket rate limiter and simulate idempotent asynchronous event dispatching.",
                "expected": "A complete system design runbook, a Cloud Tasks queue configuration, and an executable Python rate limiter script.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 70 reliability and Day 64 invariant specifications",
                "preflight": "Review Google Cloud Tasks architecture and Token Bucket rate limiting algorithms.",
                "steps": [
                    "Draft the decoupled system architecture specification in `day-071-system-design.md`.",
                    "Define the production Cloud Tasks rate-limited queue creation command:\n\n```sh\n# Create rate-limited Cloud Tasks queue\ngcloud tasks queues create order-dispatch-queue \\\n  --location=us-central1 \\\n  --max-dispatches-per-second=100 \\\n  --max-concurrent-dispatches=30 \\\n  --max-attempts=5 \\\n  --min-backoff=1s \\\n  --max-backoff=30s\n```",
                    "Write an executable Python Token Bucket rate limiter simulation (`token_bucket_sim.py`):\n\n```python\n# token_bucket_sim.py\nimport time\n\nclass TokenBucketRateLimiter:\n    def __init__(self, capacity: int, refill_rate_per_sec: float):\n        self.capacity = float(capacity)\n        self.tokens = float(capacity)\n        self.refill_rate = float(refill_rate_per_sec)\n        self.last_update = time.time()\n\n    def allow_request(self, tokens_needed: float = 1.0) -> bool:\n        now = time.time()\n        elapsed = now - self.last_update\n        self.last_update = now\n        # Add newly generated tokens based on elapsed time\n        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)\n        \n        if self.tokens >= tokens_needed:\n            self.tokens -= tokens_needed\n            return True\n        return False\n\n# Configure bucket: capacity 5 tokens, refill 10 tokens/sec\nlimiter = TokenBucketRateLimiter(capacity=5, refill_rate_per_sec=10.0)\n\n# Burst test: consume 5 tokens instantly\nfor i in range(5):\n    assert limiter.allow_request() is True, f\"Token {i} should be allowed!\"\n\n# 6th request should fail due to burst depletion\nassert limiter.allow_request() is False, \"6th request must be throttled!\"\n\n# Wait 0.25 seconds (should generate ~2.5 tokens)\ntime.sleep(0.25)\nassert limiter.allow_request() is True, \"Refilled token should be allowed!\"\nprint(\"Token Bucket Rate Limiter Mathematics Verified Successfully.\")\n```",
                    "Execute the Python rate limiter test:\n\n```sh\npython3 token_bucket_sim.py\n```"
                ],
                "verification": (
                    "Run automated rate limiter verification:\n\n```sh\npython3 -c \"import token_bucket_sim; print('Rate Limiter Test Passed')\"\n```\n\nConfirm output displays `Token Bucket Rate Limiter Mathematics Verified Successfully`."
                ),
                "trouble": (
                    "If burst test fails, verify that initial token allocation equals configured bucket capacity."
                ),
                "cleanup": "No remote cloud resources created; retain scripts and configuration files in local repository.",
                "accept": "A validated asynchronous queue specification, Cloud Tasks CLI runbook, and working Python token-bucket rate limiter."
            }
        },
        {
            "key": "topic-04",
            "title": "Conflicting Objectives and Trade-off Records: Weighted Matrices and ADR Governance",
            "overview": (
                "Master the art of architectural compromise. Document conflicting requirements, evaluate multi-pillar tensions "
                "(cost vs reliability, security vs latency), and write defensible Architecture Decision Records (ADRs)."
            ),
            "preview": (
                "An engineering team engages in a 3-month deadlock over multi-region active-active Spanner vs regional Cloud SQL, "
                "paralyzing project delivery because trade-offs were argued emotionally without a weighted scoring framework."
            ),
            "technical": (
                "#### 1. The Reality of Architectural Friction\n\n"
                "In enterprise software architecture, every design decision is an exercise in compromise. The Well-Architected Framework "
                "pillars naturally exist in structural tension with one another:\n\n"
                "- **Reliability vs. Cost:** Achieving 99.99% availability via multi-region synchronous replication triples infrastructure "
                "and cross-region networking spend.\n"
                "- **Security vs. Latency / Usability:** Enforcing mutual TLS (mTLS), deep payload packet inspection, and hardware security "
                "modules (HSM) adds milliseconds of computational overhead to every transaction.\n"
                "- **Feature Velocity vs. Operational Stability:** Continuous daily deployments maximize product agility but consume error "
                "budgets and increase regression risk.\n\n"
                "The architect's primary deliverable is NOT a system without trade-offs; it is a **formally documented trade-off record** "
                "proving why a specific compromise was selected against explicit business priorities.\n\n"
                "#### 2. Weighted Decision Matrix Methodology\n\n"
                "To resolve architectural disputes objectively, architects construct **Weighted Scoring Matrices**:\n\n"
                "  1. Identify candidate architectures (e.g. Option A: Cloud SQL Regional HA vs. Option B: Cloud Spanner Multi-Region).\n"
                "  2. Establish evaluation criteria with executive stakeholders (e.g. Availability, Monthly Cost, RTO/RPO, Migration Effort).\n"
                "  3. Assign mathematical weights to each criterion based on strategic business goals (summing to 100%).\n"
                "  4. Score each candidate from 1 to 5; multiply scores by weights to calculate the definitive mathematical winner.\n\n"
                "#### 3. Architecture Decision Records (ADRs) as Immutable Contracts\n\n"
                "An **Architecture Decision Record (ADR)** is a version-controlled document capturing an architectural decision, its context, "
                "considered options, and resulting consequences. ADRs follow the standard Michael Nygard format:\n\n"
                "  - **Title:** `ADR-071: Regional Cloud SQL HA vs Multi-Region Spanner for Order Persistence`\n"
                "  - **Status:** Proposed / Accepted / Deprecated / Superseded\n"
                "  - **Context:** Business drivers, traffic forecasts ($10M revenue, 99.95% SLO, $5k/mo budget cap).\n"
                "  - **Decision:** We will deploy Cloud SQL PostgreSQL with Regional HA and cross-region read replicas.\n"
                "  - **Consequences:** Positive (stays within budget, sub-10ms writes); Negative (RTO in regional catastrophe is 30 minutes, "
                "requiring manual replica promotion).\n"
                "  - **Compliance with Invariants:** Preserves the Day 64 single-fulfillment business invariant via PostgreSQL ACID row locks.\n\n"
                "#### 4. Preserving Invariants Under Architectural Shift\n\n"
                "When migrating architectures (e.g. monolith to microservices, or relational DB to NoSQL), architects must identify the "
                "system's **core business invariants**—rules that must never be broken regardless of the underlying technology. For Brightloaf, "
                "the Day 64 single-fulfillment invariant requires that a paid order cannot be fulfilled twice, even under split-brain network "
                "partitions. Any proposed architectural option that cannot guarantee this invariant is disqualified immediately.\n\n"
                "#### 5. Architectural Trade-offs: Cross-Pillar Conflict Resolution Matrix\n\n"
                "| Conflict Pair | Primary Architectural Tension | Trade-off Strategy | Compromise Archetype | Governance Artifact |\n"
                "|---|---|---|---|---|---|\n"
                "| **Reliability vs Cost** | Multi-region active-active vs single-region budget | Cap availability SLO at 99.95% instead of 99.99% | Regional HA with cold DR replica | ADR with explicit MTTR & RTO budget |\n"
                "| **Security vs Latency** | Zero-Trust mTLS token checks vs sub-50ms API SLA | In-memory token caching with 5-minute pre-fetch | Cryptographic check without metadata round-trip | Security review sign-off with SLA verification |\n"
                "| **Performance vs Cost** | Provisioned Hyperdisk Extreme vs Standard PD | Hyperdisk Balanced with dynamic auto-tuning | Pay for 10k IOPS baseline, scale on alert | FinOps storage policy |\n"
                "| **Velocity vs Stability** | Continuous prod deploys vs change risk | SRE Error Budget Policy | Deploy when budget > 20%; freeze when < 0% | Error Budget Policy contract |\n"
            ),
            "questions": [
                "Why are emotional or subjective arguments ineffective for resolving architectural disagreements?",
                "What five structural sections comprise a standard Michael Nygard Architecture Decision Record (ADR)?",
                "How does establishing a business invariant (e.g. Day 64 single-fulfillment) eliminate unviable architectural options?",
                "Under what strategic business conditions should cost be prioritized over high availability?",
            ],
            "reference": "https://docs.cloud.google.com/architecture/framework",
            "reference_label": "Google Cloud Architecture Center: Well-Architected Framework Overview",
            "scenario": {
                "scenario": (
                    "Brightloaf's platform engineering team became deadlocked in a contentious 3-month debate regarding the database "
                    "architecture for the new international checkout service. The infrastructure lead advocated for Cloud Spanner multi-region "
                    "(`nam6`), arguing that anything less than 99.999% availability was irresponsible. The finance lead and product manager "
                    "opposed the proposal, pointing out that Spanner's minimum 3-node multi-region footprint would cost over $6,500/month—exceeding "
                    "the entire application infrastructure budget. The debate resulted in analysis paralysis, missed product launch milestones, "
                    "and escalating interpersonal conflict, all because the team had no formal evaluation methodology or agreed criteria weights."
                ),
                "impact": (
                    "Severe project delivery delay: international market launch delayed by 14 weeks. Engineering opportunity cost estimated "
                    "at $180,000 in diverted developer salaries. Market first-mover advantage lost to a regional competitor."
                ),
                "constraints": (
                    "Establish a quantitative, objective decision method; deliver a binding architectural decision within 5 business days; "
                    "honor the strict $3,500/month database budget ceiling while achieving at least 99.95% monthly availability."
                ),
                "diagnostic_steps": [
                    "Step 1: Review engineering meeting minutes; discover zero documented Architecture Decision Records (ADRs) or weighted decision matrices.",
                    "Step 2: Audit project constraints; identify that business requirements explicitly require 99.95% availability (not 99.999%), with a hard budget cap of $3,500/month.",
                    "Step 3: Analyze Cloud Spanner pricing; confirm minimum 3-node `nam6` multi-region cluster costs $6,742/month (breaching budget by 92%).",
                    "Step 4: Analyze Cloud SQL Regional HA pricing; confirm PostgreSQL Regional HA on `db-custom-8-32` with cross-region replica costs $1,840/month (comfortably within budget)."
                ],
                "root": (
                    "Absence of a structured weighted decision framework allowed engineers to optimize for an unconstrained theoretical ideal "
                    "(99.999% availability) rather than aligning architecture with contractual business and financial realities."
                ),
                "remediation_steps": [
                    "Step 1: Construct a formal Weighted Decision Matrix scoring candidates across Cost (35%), Availability (25%), Latency (20%), and Operational Simplicity (20%).",
                    "Step 2: Calculate composite mathematical scores: Cloud SQL Regional HA scores 4.25/5.0, while Cloud Spanner scores 2.85/5.0 due to severe cost penalties.",
                    "Step 3: Author and publish `ADR-071: Regional Cloud SQL HA Persistence for Checkout Tier`, documenting the context, trade-offs, and consequences.",
                    "Step 4: Formally incorporate the Day 64 single-fulfillment invariant into the ADR acceptance criteria, verified via PostgreSQL serializable transaction isolation."
                ],
                "verify": (
                    "Conduct formal stakeholder review with finance, product, and engineering leads. Secure unanimous written approval on "
                    "ADR-071 within 48 hours, unblocking engineering execution and deployment pipelines."
                ),
                "residual": (
                    "Cloud SQL Regional HA provides 99.95% availability within a single region; cross-region disaster recovery requires "
                    "an automated replica promotion runbook if an entire multi-zone region suffers an extended catastrophic outage."
                ),
                "diagram": (
                    "3-month emotional deadlock",
                    "Spanner ($6.7k) vs Cloud SQL ($1.8k)",
                    "Project delayed 14 weeks ($180k waste)",
                    "Build weighted matrix + author ADR-071",
                    "Unanimous sign-off, unblocked in 48h"
                ),
                "facts": "Team deadlocked for 3 months; Spanner cost $6.7k/mo; budget was $3.5k; requirement was 99.95% SLO; launch delayed 14 weeks.",
                "inference": "Without weighted criteria, teams optimize for extreme technical virtues rather than business utility.",
                "expected": "Weighted decision matrices convert emotional architectural debates into objective mathematical resolutions."
            },
            "lab": {
                "name": "Weighted Decision Matrix Modeling and ADR Authoring",
                "file": "day-071-decision-matrix.md",
                "goal": "Build an executable Python weighted decision matrix calculator and author a complete Architecture Decision Record (ADR).",
                "expected": "A complete ADR document (ADR-071), a weighted matrix calculation script, and verified scoring output.",
                "mode": "offline architecture specification, shell scripting, and Python development; no cloud resources billed",
                "prereq": "Day 70 review lenses and Day 68 business requirements",
                "preflight": "Review Michael Nygard ADR format and Kepner-Tregoe decision analysis principles.",
                "steps": [
                    "Draft `ADR-071: Database Architecture for International Checkout Tier` in `day-071-decision-matrix.md` following standard Nygard format.",
                    "Define the evaluation criteria and weights: Cost = 35%, Availability = 25%, Latency = 20%, Operational Simplicity = 20%.",
                    "Write an executable Python weighted decision matrix calculator (`decision_matrix.py`):\n\n```python\n# decision_matrix.py\n\nCRITERIA = {\n    'cost': {'weight': 0.35, 'name': 'Monthly Budget Fit (< $3,500/mo)'},\n    'availability': {'weight': 0.25, 'name': 'High Availability (>= 99.95%)'},\n    'latency': {'weight': 0.20, 'name': 'p99 Transaction Latency (< 50ms)'},\n    'simplicity': {'weight': 0.20, 'name': 'Operational & Migration Simplicity'}\n}\n\n# Candidates scored from 1 (poor) to 5 (excellent)\nCANDIDATES = {\n    'Cloud Spanner (nam6 Multi-Region)': {\n        'cost': 1,        # $6,742/mo (violates budget cap)\n        'availability': 5, # 99.999% SLA\n        'latency': 4,      # 20-40ms TrueTime consensus\n        'simplicity': 3    # Requires schema migration, query rewrites\n    },\n    'Cloud SQL PostgreSQL (Regional HA)': {\n        'cost': 5,        # $1,840/mo (well under budget)\n        'availability': 4, # 99.95% SLA\n        'latency': 5,      # Sub-10ms local zonal writes\n        'simplicity': 5    # Native Postgres compatibility\n    }\n}\n\ndef evaluate_matrix():\n    results = {}\n    for candidate, scores in CANDIDATES.items():\n        total_score = sum(scores[crit] * data['weight'] for crit, data in CRITERIA.items())\n        results[candidate] = total_score\n    return results\n\nscores = evaluate_matrix()\nfor cand, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):\n    print(f\"{cand}: Weighted Composite Score = {score:.2f} / 5.00\")\n\nwinner = max(scores, key=scores.get)\nprint(f\"\\nDefinitive Mathematical Winner: {winner}\")\nassert 'Cloud SQL' in winner, \"Evaluation matrix error!\"\nprint(\"Decision Matrix Calculation Verified Successfully.\")\n```",
                    "Execute the Python weighted decision matrix test:\n\n```sh\npython3 decision_matrix.py\n```"
                ],
                "verification": (
                    "Run automated decision matrix verification:\n\n```sh\npython3 -c \"import decision_matrix; print('Decision Matrix Test Passed')\"\n```\n\nConfirm output identifies Cloud SQL Regional HA as the winner with score 4.55/5.00."
                ),
                "trouble": (
                    "If weights do not sum to 1.0, verify the dictionary criteria weights in `decision_matrix.py`."
                ),
                "cleanup": "No remote cloud resources created; retain ADR documents and calculation scripts in local repository.",
                "accept": "A completed ADR-071 document, a weighted decision scoring model, and verified Python evaluation output."
            }
        }
    ]
}
