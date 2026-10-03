#!/usr/bin/env python3
"""Deterministically render the 180-day curriculum as standalone static HTML."""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
from collections import Counter
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

import markdown

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "gcp-180day-architect-site"
ROADMAP = ROOT / "roadmap-180-days.md"
REFERENCES = ROOT / "gcp-architect-roadmap-100-days.md"
VERIFIED = "2026-09-26"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def md(value: str) -> str:
    return markdown.markdown(value, extensions=["tables", "fenced_code"])


def split_semicolons(value: str) -> list[str]:
    """Separate only top-level clauses; lists inside parentheses stay together."""
    chunks, current, depth = [], [], 0
    for character in value:
        if character == "(":
            depth += 1
        elif character == ")":
            depth = max(0, depth - 1)
        if character == ";" and depth == 0:
            chunks.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    chunks.append("".join(current).strip())
    return [chunk for chunk in chunks if chunk]


def topic_label(clause: str) -> str:
    first = re.split(r"(?<=\.)\s+(?=[A-Z])", clause)[0].strip().rstrip(".")
    if ":" in first and len(first.split(":", 1)[0]) < 48:
        first = first.split(":", 1)[0]
    if len(first) > 94:
        first = first[:91].rsplit(" ", 1)[0] + "…"
    return first[0].upper() + first[1:] if first else "Review exercise"


def topic_clauses(day: int, study: str) -> list[str]:
    chunks = split_semicolons(study)
    if day == 1:
        return ["Local workspace and evidence repository", "Study sessions and learning baseline", "Synthetic data, budget and cleanup ownership"]
    if day == 2:
        return [
            "OSI and TCP/IP layer models",
            "IPv4 addressing, private ranges, ARP/NDP and CIDR subnetting",
            "Packet path from NIC to application socket",
            "Process communication protocols: IPC, Unix domain sockets, and network RPCs"
        ]
    if day == 3:
        chunks = ["IPv6 addressing and scope", "DNS records, TTL and resolver roles", "TCP and UDP, ports, connection states and buffers"]
    if day == 4:
        chunks = ["HTTP/HTTPS, status codes, HTTP/1.1 vs HTTP/2 vs HTTP/3", "TLS 1.3 handshake and certificate validation chains", "MTU and MSS clamping", "NAT (SNAT/DNAT) for private outbound", "Routing basics: static vs dynamic routing, BGP at conceptual level"]
    if day == 9:
        chunks = ["Hypervisors and virtual machines", "Container isolation: namespaces, cgroups, seccomp and capabilities"]
    if day == 18:
        chunks = ["Google Cloud accounts and the Free Trial", "Google Cloud Free Tier and monthly limits", "Google Cloud Console navigation and project selection"]
    excluded = (
        "advanced scheduler or kernel tuning is optional",
        "its exam and full course are optional",
        "maintain them throughout the course",
        "a second runtime or paid hybrid deployment is optional",
        "optional separate bucket/database deployments",
        "do not require the later warehouse lab",
        "custom training and feature-store deployment are optional",
        "implementing consensus is optional specialist work",
        "this day is a defense and acceptance review, not a new implementation project",
    )
    chunks = ["Prerequisite review and remediation" if item.lower() == "review and remediate prior material only" else item for item in chunks if not any(item.lower().startswith(phrase) for phrase in excluded)]
    return chunks


def parse_references() -> dict[int, list[dict[str, str]]]:
    source = REFERENCES.read_text()
    result = {}
    for match in re.finditer(r"(?ms)^### Topic (\d{3}) references\n(.*?)(?=^### Topic \d{3} references|^## Prerequisite references|\Z)", source):
        n = int(match.group(1))
        body = match.group(2)
        result[n] = [{"label": label, "url": url} for label, url in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", body)]
    return result


def parse_days() -> list[dict]:
    source = ROADMAP.read_text()
    block = ""
    days = []
    for line in source.splitlines():
        m = re.match(r"## Days? (\d+)(?:[–-](\d+))? — (.+)", line)
        if m:
            block = m.group(3)
        m = re.match(r"### Day (\d+) — (.+)", line)
        if m:
            days.append({"number": int(m.group(1)), "title": m.group(2), "block": block, "body": []})
        elif days:
            days[-1]["body"].append(line)
    for d in days:
        body = "\n".join(d.pop("body"))
        d["time"] = re.search(r"\*\*Time:\*\* (.+?)\. \*\*Entry prerequisites:\*\*", body).group(1)
        d["prerequisites"] = re.search(r"\*\*Entry prerequisites:\*\* (.+?)  ", body).group(1)
        for field in ("Study", "Practice", "Exit evidence"):
            d[field.lower().replace(" ", "_")] = re.search(rf"^- \*\*{field}:\*\* (.+)$", body, re.M).group(1)
        d["refs"] = sorted({int(x) for x in re.findall(r"Topic (\d{3})", re.search(r"\*\*Topic references:\*\* (.+)$", body, re.M).group(1))})
        d["type"] = "capstone" if 175 <= d["number"] <= 179 else "gate" if d["number"] in (17, 35, 67, 82, 118, 174) else "day"
        d["mode"] = "tabletop / design" if d["type"] != "day" or re.search(r"design|compare|review|case|decision|architecture|strategy|choose", d["practice"], re.I) else "local exercise"
        if d["number"] == 1:
            d["mode"] = "local exercise"
        d["topics"] = [{"key": f"topic-{i:02d}", "title": topic_label(c), "scope": c} for i, c in enumerate(topic_clauses(d["number"], d["study"]), 1)]
    assert len(days) == 180 and [d["number"] for d in days] == list(range(1, 181))
    return days


def article_shell(title: str, body: str, *, day: dict | None = None, days: list[dict] | None = None) -> str:
    prefix = "../" if day else ""
    nav = '<a class="brand" href="' + prefix + 'index.html">◆ <span>GCP · 180 days</span></a>'
    nav += '<a href="' + prefix + 'index.html">Day index</a><a href="' + prefix + 'glossary.html">Glossary</a><a href="' + prefix + 'sources.html">Sources</a><a href="' + prefix + 'artifacts.html">Artifacts</a>'
    if day and days:
        n = day["number"]
        if n > 1:
            nav += f'<a href="day-{n-1:03d}.html" aria-label="Previous day">← Day {n-1}</a>'
        if n < 180:
            nav += f'<a href="day-{n+1:03d}.html" aria-label="Next day">Day {n+1} →</a>'
        nav += '<label class="jump-label" for="day-jump">Jump to day</label><select id="day-jump" aria-label="Jump to day"><option value="">Choose a day…</option>'
        last_block = None
        for entry in days:
            if entry["block"] != last_block:
                if last_block is not None:
                    nav += "</optgroup>"
                nav += f'<optgroup label="{esc(entry["block"])}">'
                last_block = entry["block"]
            selected = " selected" if entry["number"] == n else ""
            nav += f'<option value="day-{entry["number"]:03d}.html"{selected}>Day {entry["number"]}: {esc(entry["title"])}</option>'
        nav += "</optgroup></select>"
    nav += '<button type="button" id="theme-toggle" aria-label="Toggle light and dark theme">☀ Theme</button>'
    return f'''<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark light"><title>{esc(title)} · GCP 180 days</title><link rel="stylesheet" href="{prefix}assets/site.css"><script defer src="{prefix}assets/site.js"></script></head><body><a class="skip" href="#main">Skip to content</a><header class="site-nav"><nav class="nav-inner" aria-label="Site navigation">{nav}</nav></header><div class="audit-banner"><strong>Draft content:</strong> Most lessons use generated templates and have not passed topic-level review. <a href="{prefix}CONTENT_AUDIT.md">Read the content audit</a>.</div>{body}<footer class="site-footer">GCP Architect · 180-day independent study · Roadmap dated {VERIFIED}. Local progress remains in this browser.</footer></body></html>'''


LESSONS = [
    (r"\bosi\b|\btcp/ip\b|\bl4\b|\bl7\b", "Layer models separate link delivery, IP routing, transport between endpoints and application protocol behavior. A layer label is a troubleshooting aid: it tells you which header, state and component can explain an observation.", "Mark the first layer at which the healthy and failing paths differ."),
    (r"\bipv6\b", "IPv6 uses 128-bit addresses and a prefix length to define the routed network. Hosts can have multiple IPv6 addresses, and an IPv6 path may behave differently from an IPv4 path for the same name.", "Check the AAAA answer, selected address family, route and listener before concluding that IPv4 success proves IPv6 success."),
    (r"\bapi\b|client librar|emulator|cloud shell|cloud code", "A client call passes through credential selection, API endpoint, request validation and an operation or response. An emulator replaces only part of that path and must be used with its documented limitations.", "Separate a local emulator result from a real cloud API result, and poll asynchronous operations before claiming completion."),
    (r"dns|resolver|ttl|record type", "A client asks a resolver for a name; cached answers are reused until their TTL expires, while an authoritative server owns the zone data. A successful DNS answer proves name resolution only, not transport reachability or application health.", "Compare the queried name, answer, TTL, resolver and authoritative path before changing application configuration."),
    (r"tls|certificate|https", "TLS authenticates the server identity through a certificate chain and protects bytes after a handshake. Hostname, validity dates and trusted issuer are independent checks; an HTTP status is available only after the connection and TLS checks succeed.", "Separate certificate validation failures from DNS, TCP and HTTP failures using the earliest failed phase."),
    (r"cidr|subnet|\bipv4\b|ip addressing|ip addresses|address space|private ranges", "CIDR fixes the network prefix length. Subnet boundaries come from the prefix bits, not from a visual guess at the dotted address; route selection uses the most-specific matching prefix.", "Calculate the address range and chosen next hop before changing a route or firewall rule."),
    (r"tcp|udp|socket|port|packet|mtu|nat|route|vpn|firewall|load balanc|bgp|private google access|private service connect", "Follow the packet through name resolution, route choice, stateful translation or filtering, destination socket and return path. A healthy forward path is insufficient if return routing, connection state or packet size differs.", "Draw both directions and mark the first boundary where a packet or response disappears."),
    (r"iam|identity|role|permission|principal|token|authentication|authorization|federation", "Authentication establishes a principal; authorization evaluates that principal's permissions on a scoped resource. Short-lived credentials reduce exposure but do not by themselves make an over-broad role safe.", "Test an allowed action and a denied action with the same stated principal and resource scope."),
    (r"linux|shell|process|service|file|storage i/o|ssh|boot|kernel", "A process runs with an identity, open descriptors, environment and resource limits. The supervisor and kernel expose separate evidence: process state, service state, exit status, logs and filesystem state.", "Capture the command, exit code and timestamp so a second learner can reproduce the observation."),
    (r"sql|database|spanner|firestore|bigtable|bigquery|transaction|consisten|replica", "State changes need an explicit correctness rule. A transaction protects a chosen boundary, while replicas, caches and asynchronous consumers may observe changes later. Query shape and access pattern determine which storage design is practical.", "Write the invariant and test duplicate or stale input before claiming correctness."),
    (r"pub/sub|event|queue|message|retry|idempoten|outbox|fulfill", "Delivery and processing are separate events. A consumer may see the same message again after a timeout or retry, so the order identifier needs a durable deduplication rule before fulfillment is committed.", "Replay one synthetic order event twice and show that the fulfillment count remains one."),
    (r"cost|pricing|budget|billing|finops", "A price estimate is a model of usage units, rate assumptions and time. Bills can differ because of region, egress, idle resources, discounts and changes in workload. Record the date and source of any rate.", "Show the usage equation and a sensitivity case instead of treating one estimate as a guarantee."),
    (r"slo|sli|availability|reliability|recovery|rto|rpo|incident|\bdr\b|backup", "An SLI measures user-visible behavior over a defined window; an SLO is the target for that measure. RTO bounds acceptable recovery time and RPO bounds acceptable lost data, and both require a test with timestamps.", "Use a failure timeline with detection, decision, restoration and data reconciliation checkpoints."),
    (r"terraform|iac|git|pipeline|deploy|ci/cd|release", "Desired configuration, reviewed change and observed state are different artifacts. A successful plan or pipeline run does not prove the deployed workload behaves correctly; drift and rollback need explicit checks.", "Compare the proposed change, observed resource state and application acceptance signal."),
    (r"kubernetes|gke|container|cloud run|compute engine|vm|runtime", "The runtime choice changes who manages scheduling, isolation, scaling, networking and upgrades. Workload constraints such as state, startup time, network needs and operational ownership should drive the choice.", "State the requirement, selected runtime, rejected alternative and failure boundary."),
    (r"\bai\b|\bml\b|model|vertex|\brag\b|prompt|agent|embedding", "Model quality, data access, latency and safety are separate evaluation dimensions. A convincing single output cannot establish accuracy or policy compliance; use a dated test set and record misses.", "Run or describe a small fixed evaluation set with expected behavior and failure examples."),
    (r"migration|cutover|legacy|wave|rehost", "A migration needs a source of truth, measurable wave acceptance and a rollback boundary. Dual writes or data copy alone do not establish reconciliation, and a cutover is not complete until ownership and decommissioning are settled.", "Track record counts, exceptions, decision time and rollback trigger in a wave sheet."),
    (r"gate|capstone|defense|review|rest", "A review tests evidence rather than introducing another service. Trace each requirement to a decision, a test, an observed result and a known limitation; identify the earlier exercise to repeat when proof is missing.", "Score correctness, traceability, evidence, failure reasoning and communication from 0 to 3."),
]


def lesson(topic: dict) -> tuple[str, str]:
    text = topic["title"] + " " + topic["scope"]
    for pattern, mechanism, check in LESSONS:
        if re.search(pattern, text, re.I):
            return mechanism, check
    return ("Map the actors, input, control boundary, state change and observable output. A design claim becomes useful when its assumptions and failure conditions are explicit.", "Compare one concrete input against the chosen decision and a credible alternative.")


DEEP_DIVES = [
    (r"\bosi\b|\btcp/ip\b|\bl4\b|\bl7\b", "A layer model groups responsibilities so you can ask a narrower question. At the link layer, a frame reaches a next hop on a local medium; IP selects a path between networks; TCP or UDP identifies transport endpoints; HTTP carries an application request and response. A load balancer can make decisions using transport information or application content, depending on its design.", "For a failed request, mark what has actually passed: an IP route, an established transport connection, a TLS handshake or an HTTP response. A layer-7 error means the client reached more of the path than an unanswered TCP connection. The model does not replace a real trace, but it keeps the trace organized."),
    (r"\bipv6\b", "Write an IPv6 address and prefix as separate facts. A client may receive both A and AAAA answers and choose one address family; therefore the same hostname can have one working path and one failing path. Neighbor discovery and routing still need to get packets to a next hop, while the application must listen on the chosen family.", "In the worksheet, compare the IPv4 and IPv6 lookup results, then label the source and destination socket for each attempt. If only IPv6 fails, inspect the IPv6 route and listener rather than changing an IPv4 firewall rule. A local `localhost` check is an address-family exercise, not proof of external connectivity."),
    (r"\bapi\b|client librar|emulator|cloud shell|cloud code", "An API request starts with a selected endpoint and credential, then passes validation and authorization before the service begins work. Some operations return an operation identifier before the requested state is ready. Distinguish request acceptance, operation completion and observed resource state in the evidence you save.", "An emulator can teach request shape and selected behavior without exercising production IAM, network controls, capacity or billing. Record the emulator name and version and point to its documented differences. For a failed call, capture endpoint, principal, status or error code and any operation ID before retrying; this helps distinguish a local configuration error from a service-side result."),
    (r"dns|resolver|ttl|record type", "The lookup path has several independently observable stages: application cache, operating-system resolver, recursive resolver and authoritative answer. A cached record carries a remaining lifetime, so two clients can receive different answers during a change without either resolver being broken. Record the exact name and record type; an A query does not test AAAA, MX or TXT behavior.", "For troubleshooting, measure resolution first, then the connection to the returned address, then the application response. A name can resolve to an address that has no listening service, and a working service can still be unreachable through the chosen route. This separation avoids treating every timeout as a DNS fault."),
    (r"tls|certificate|https", "A TLS connection depends on the client reaching the server, agreeing on protocol parameters and validating the server's identity. Validation considers the requested hostname, the certificate's validity window and a trusted chain. Only after this phase can an HTTP request and status code give application evidence.", "Trace failures in order: name resolution, TCP or QUIC reachability, TLS negotiation, then HTTP. A certificate mismatch should be repaired at the identity or endpoint configuration, not by changing an application route. Record the hostname used by the client rather than merely the server's IP address."),
    (r"cidr|subnet|\bipv4\b|ip addressing|ip addresses|address space|private ranges", "The prefix length tells you which bits identify the network. For IPv4, a /24 leaves eight host bits; splitting it into four equal ranges borrows two more prefix bits and produces /26 networks. The range boundary and address classification should be calculated before assigning a subnet to a workload.", "Address planning also has an operational side. Overlapping ranges complicate connectivity and migration, while a route table decides the next hop independently of whether the destination address is syntactically valid. State the source, destination and chosen route for both forward and return traffic."),
    (r"tcp|udp|socket|port|packet|mtu|nat|route|vpn|firewall|load balanc|bgp|private google access|private service connect", "A request crosses several boundaries that can fail independently: local socket, route, translation or firewall state, network path, load balancer and backend listener. The response must traverse a viable return path. Write the source and destination addresses and ports at each boundary, especially where translation changes them.", "Use a phase-by-phase trace rather than a single 'network down' label. A completed name lookup proves little about a refused connection; an established connection proves little about HTTP health. A packet-size problem may affect large requests while tiny probes succeed, so compare the failing and healthy payloads."),
    (r"iam|identity|role|permission|principal|token|authentication|authorization|federation", "Separate the credential from the principal it represents and from the policy decision. A token can be valid yet lack the requested permission, and a role can be broad even when the credential is short lived. Record the active principal, requested action, resource scope and policy path for each test.", "A useful access check has both a permitted operation and a deliberately denied one. If only success is tested, the policy may grant much more than intended. When a call fails, distinguish missing credentials, wrong principal, missing permission and a resource or organization policy constraint before widening any binding."),
    (r"linux|shell|process|service|file|storage i/o|ssh|boot|kernel", "Follow work from a command to the process it starts, its identity, open descriptors and exit status. The process's stdout and stderr report one kind of evidence; service-manager state, logs and the filesystem report others. A zero exit code confirms that the command completed according to its own rules, not that a downstream service is healthy.", "When behavior changes, compare the environment and permissions of a working and failing run. Record the working directory, executable path, user and timestamps before editing configuration. For a managed service, identify which parts of this stack are visible to you and which belong to the provider."),
    (r"sql|database|spanner|firestore|bigtable|bigquery|transaction|consisten|replica", "Start with the read and write operations the application must perform. A transaction groups only the operations inside its boundary; external consumers, caches and replicas may need separate reconciliation. State which record is authoritative and which invariant must survive retries, concurrent updates and restoration.", "Choose a storage pattern from query shape, consistency needs, scale and operational responsibility. A fast point lookup, a large analytical scan and a multi-row business transaction are different workloads. Test a duplicate or stale input as well as the happy path, and describe what the query result does and does not prove."),
    (r"pub/sub|event|queue|message|retry|idempoten|outbox|fulfill", "Publishing, delivering, processing and acknowledging a message are distinct transitions. If a consumer performs its side effect and fails before acknowledging, the message may be delivered again. The durable deduplication decision therefore belongs near the business side effect, keyed by a stable order or event identifier.", "For Brightloaf, write the sequence for order 42 twice and count committed fulfillment records. Show where the consumer stores the deduplication key and when it acknowledges the message. A successful publish alone proves neither consumption nor exactly one business outcome."),
    (r"cost|pricing|budget|billing|finops", "Estimate cost as a sum of usage units multiplied by dated rates. State the region, duration and assumptions behind each term, then vary the largest input to see how sensitive the decision is. An alert threshold helps detect unexpected usage but is not a resource quota or an automatic stop switch.", "Compare options using the same workload and accounting period. Include resources left idle, storage retained after a compute change and traffic crossing billing boundaries. Mark an estimate as a model until actual billing and usage measurements are available; record who owns cleanup and follow-up."),
    (r"slo|sli|availability|reliability|recovery|rto|rpo|incident|\bdr\b|backup", "Define the user-visible event before choosing a target: which requests count, over what window, and which failures are excluded. An SLI is the measurement; an SLO is its goal. For recovery, timestamp the last durable point, failure, detection, decision and restoration so RTO and RPO claims can be compared with an observed drill.", "A backup's existence does not prove it can restore the required workload. Rehearse the restore or label the result as a tabletop prediction, then reconcile state and check the application's invariant. A design that recovers quickly but duplicates fulfillment has not met the business need."),
    (r"terraform|iac|git|pipeline|deploy|ci/cd|release", "A repository captures proposed configuration, a plan describes an intended change and the provider's inventory shows observed resources. None of those alone establishes that users receive correct behavior. Keep the commit, review, apply or deployment result and application check linked as separate evidence.", "A safe change sequence records preconditions, expected diff, approval, observation and rollback trigger. If a step times out, inspect the current operation and resource state before retrying; a repeated create can compound the problem. Drift is a difference to explain, not an instruction to overwrite blindly."),
    (r"kubernetes|gke|container|cloud run|compute engine|vm|runtime", "Compute choices place responsibility at different boundaries: guest operating system, orchestration control plane, container runtime and application process. Compare workload needs for state, networking, startup behavior, scaling and upgrade control before choosing an implementation. Keep data durability separate from the runtime label.", "An operational comparison needs an observable failure signal. For example, a process can be alive but not ready to serve, and a restarted container can lose ephemeral files. State who owns the recovery action and which earlier lab proves that assumption for the chosen environment."),
    (r"\bai\b|\bml\b|model|vertex|\brag\b|prompt|agent|embedding", "Treat model behavior as an evaluated dependency. The input data, retrieval path, prompt, model version and output policy each affect the result. A fluent answer may still be wrong or disclose data, so use a fixed test set with expected and unacceptable responses.", "Measure the behavior that matters to the proposed use case: answer quality, refusal or safety errors, latency and cost under an explicit workload. Record misses as well as successes. An evaluation in a local mock or small sample supports a design decision but does not prove production performance."),
    (r"migration|cutover|legacy|wave|rehost", "Name the source of truth and the unit of migration before selecting a transfer method. For each wave, record the source and destination counts, exceptions, acceptance owner and rollback point. A copied dataset is not reconciled merely because the transfer operation reports success.", "Cutover changes traffic, writes and ownership. Identify the last point at which a rollback is safe, what data would need replay and how the team will recognize a failed wave. Decommission only after downstream dependencies and operational handover are verified."),
    (r"gate|capstone|defense|review|rest", "A review should follow a claim to its evidence: requirement, design choice, test input, observed output and limitation. When the chain breaks, the remedy is a targeted repeat of the earlier exercise, not a stronger assertion in the presentation.", "Score each rubric dimension separately, record the reviewer's changed constraint and identify what evidence would change the decision. A tabletop defense is appropriate for a capstone, but it must stay labeled as design reasoning rather than a measured deployment."),
]


def deep_dive(topic: dict) -> tuple[str, str]:
    value = topic["title"] + " " + topic["scope"]
    for pattern, mechanics, diagnosis in DEEP_DIVES:
        if re.search(pattern, value, re.I):
            return mechanics, diagnosis
    return ("Break the topic into a request or decision path: input, actor, control boundary, state change and observable output. This makes the hidden assumption visible. State which part is documented behavior, which part is a supplied example and which part still needs a real test.", "Evaluate one changed constraint against the same path. If the original design fails, name the first affected boundary and the signal that would reveal it. A defensible architecture decision includes a rejected alternative and a condition under which that alternative might become preferable.")


def worked_example(topic: dict) -> tuple[str, str]:
    value = topic["title"] + " " + topic["scope"]
    cases = [
        (r"\bosi\b|\btcp/ip\b|\bl4\b|\bl7\b", "Input: DNS returns an address, TCP connects, then HTTP returns a 503 response.", "Expected: name resolution and transport succeeded; investigate the application or backend path that produced the 503."),
        (r"\bipv6\b", "Input: a hostname has A and AAAA answers, but only the IPv4 connection succeeds.", "Expected: compare the selected IPv6 route, filtering and listener; the working IPv4 path does not prove IPv6 connectivity."),
        (r"\bapi\b|client librar|emulator|cloud shell|cloud code", "Input: an API returns an operation ID before a resource appears in inventory.", "Expected: poll the operation and then inspect the resource; request acceptance is not yet observed readiness."),
        (r"cidr|subnet|ipv4", "Input: 192.0.2.0/24; split it into four equal subnets.", "Expected: four /26 networks begin at .0, .64, .128 and .192; the first broadcast is .63."),
        (r"dns|resolver|ttl", "Input: a cached A answer has TTL 30 seconds, but the origin address changes at second 10.", "Expected: a resolver may continue returning the cached answer until the remaining TTL expires; test resolution separately from TCP reachability."),
        (r"tls|certificate", "Input: the server certificate is valid for api.example.test, while the client connects to orders.example.test.", "Expected: hostname validation fails before an HTTP response is available; changing an HTTP route cannot repair this mismatch."),
        (r"tcp|udp|socket|port|firewall|route|nat|packet", "Input: a client can resolve api.example.test but cannot establish a TCP connection to port 443.", "Expected: DNS has passed; inspect the route, filtering, translation, listening socket and return path in that order."),
        (r"iam|identity|role|permission|token|authentication", "Input: a service principal can read one bucket but receives PERMISSION_DENIED on another.", "Expected: record the authenticated principal and compare resource-level bindings; do not widen access at the organization scope."),
        (r"sql|transaction|database|consisten|spanner|firestore", "Input: order 42 is written and the same fulfillment request is retried.", "Expected: the durable uniqueness key for order 42 prevents a second fulfillment record while preserving a readable order state."),
        (r"pub/sub|event|queue|message|retry|idempoten", "Input: event E42 is delivered twice after the first acknowledgement is lost.", "Expected: two deliveries, one committed fulfillment; the deduplication key and acknowledgement point must be shown."),
        (r"cost|pricing|budget|billing", "Input: 100 units per hour at an assumed $0.02 per unit-hour for 10 hours.", "Expected: baseline $20 before other usage; doubling units doubles this term, while omitted egress or idle time remains an explicit uncertainty."),
        (r"slo|availability|reliability|recovery|rto|rpo|backup", "Input: last durable checkpoint 10:00, failure 10:07, service restored 10:25.", "Expected: observed recovery time 18 minutes and potential data-loss window 7 minutes; compare both with stated objectives."),
        (r"terraform|iac|pipeline|deploy|release", "Input: a reviewed plan says one resource changes but the observed inventory still shows the old state.", "Expected: the plan is intent, not proof; inspect the apply result, current inventory and workload health before accepting."),
        (r"gke|kubernetes|container|cloud run|compute engine|runtime", "Input: a stateless HTTP API needs autoscaling, while a stateful worker needs durable ordering.", "Expected: evaluate runtime and state separately; document the managed boundary and why one deployment model does not satisfy both requirements automatically."),
        (r"gate|capstone|defense|review", "Input: a design packet has four strong rubric scores but evidence quality is 1/3.", "Expected: the review does not pass the at-least-2-per-dimension rule; repair the cited experiment and rescore."),
    ]
    for pattern, example, expected in cases:
        if re.search(pattern, value, re.I):
            return example, expected
    return (f"Input: the Brightloaf order flow must make a decision about {topic['title'].lower()} while preserving one fulfillment per order.", "Expected: an explicit requirement, choice, rejected alternative, observable acceptance signal and remaining uncertainty.")


def executable_extension(day: int, topic: dict) -> str:
    """Small offline experiments where the concept has a portable local check."""
    value = topic["title"] + " " + topic["scope"]
    if day == 2 and re.search(r"CIDR|IPv4 addressing", value, re.I):
        command = "python3 - <<'PY'\nfrom ipaddress import ip_network\nnetwork = ip_network('192.0.2.0/24')\nfor child in network.subnets(prefixlen_diff=2):\n    print(child, child.network_address, child.broadcast_address)\nPY"
        return f'<div class="callout"><strong>Offline execution · local shell, Python 3</strong><p>Run the command below. Compare the four printed /26 networks with your worksheet. Replace the input with one private /24 only after the first check passes.</p><pre><code>{esc(command)}</code></pre><p>Expected first line: <code>192.0.2.0/26 192.0.2.0 192.0.2.63</code>. Four lines should appear. No files or cloud resources are created.</p></div>'
    if day == 3 and re.search(r"DNS", value, re.I):
        command = "python3 - <<'PY'\nimport socket\nfor family, kind, proto, name, address in socket.getaddrinfo('localhost', 80, type=socket.SOCK_STREAM):\n    print(socket.AddressFamily(family).name, address[0], address[1])\nPY"
        return f'<div class="callout"><strong>Offline execution · local shell, Python 3</strong><p>Run the command below and label each output line as a local name-resolution result. The presence or order of IPv4 and IPv6 answers varies by host.</p><pre><code>{esc(command)}</code></pre><p>Expected: at least one <code>AF_INET</code> or <code>AF_INET6</code> line ending in port <code>80</code>. This does not prove an HTTP server is listening.</p></div>'
    if day == 1 and re.search(r"shell|workspace", value, re.I):
        command = "pwd\npython3 --version\ngit --version\npython3 -c 'import sys; print(sys.executable)'"
        return f'<div class="callout"><strong>Offline execution · local shell</strong><p>Run the four commands below in a disposable working directory and paste their output and exit codes into the note. If Git is absent, record that prerequisite before using the later repository exercises.</p><pre><code>{esc(command)}</code></pre><p>Expected: a current directory, Python 3 version, Git version if installed, and Python executable path. No resource is created; no cleanup is required.</p></div>'
    return ""


def source_for(day: dict, topic: dict, refs: dict) -> tuple[str, str, str]:
    """Use the exact local reference section; external references remain clearly distinct."""
    if day["number"] == 3 and topic["key"] == "topic-01":
        return "1", "RFC 4291: IPv6 addressing architecture, section 2", "https://datatracker.ietf.org/doc/html/rfc4291#section-2"
    if day["number"] == 11:
        if topic["key"] == "topic-01":
            return "4", "Google Cloud service-model comparison", "https://cloud.google.com/learn/paas-vs-iaas-vs-saas"
        return "4", "Google Cloud shared responsibility", "https://docs.cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate#shared-responsibility"
    terms = set(re.findall(r"[a-z]{4,}", topic["title"].lower()))
    candidates = [(rid, item) for rid in day["refs"] for item in refs.get(rid, [])]
    if not candidates:
        return "", "", ""
    rid, item = max(candidates, key=lambda pair: len(terms & set(re.findall(r"[a-z]{4,}", pair[1]["label"].lower()))))
    return str(rid), item["label"], item["url"]


DAY_ONE = [
    {
        "overview": "A local workspace is the directory and tools used for exercises. An evidence repository is a versioned collection of commands, observations and diagrams that lets another learner trace a later architecture claim to its source.",
        "technical": "A terminal is the window in which you type; the shell is the program that interprets your command and starts other programs. Every command runs from a working directory. `pwd` shows that directory, and a relative path is interpreted from there. `command -v git` asks the shell which executable it would run; this is useful when a tool is installed but missing from `PATH`, or when two versions are present.\n\nWhen a child process ends, it returns an exit status to the shell. By convention, zero means that command completed successfully and a nonzero status means it reported a problem. You can capture the status immediately with `$?` in a POSIX-style shell. Capture it before running another command, because the next command replaces that value. A zero status does **not** prove that a larger workflow is correct: `cat` can read a file successfully even if the file contains the wrong order data. Pair the status with an output or behavior check.\n\nGit has three useful states to distinguish on Day 1: the working tree contains the files you are editing, the staging area contains the exact changes selected for the next commit, and a commit stores a versioned snapshot. `git status --short` shows untracked or modified files; `git diff --cached` shows staged changes. Before a later design review, another learner should be able to identify the command, environment, observation and commit that support your claim. Keep credentials and real customer data out of the repository.\n\n**Further study:** [MIT Missing Semester: the shell](https://missing.csail.mit.edu/2020/course-shell/) is a lecture and exercise page devoted to this exact topic; [Topic 002 references](../sources.html#topic-002) collects the supporting manuals.",
        "problem": "**Situation:** Two architects compare network diagrams, but one cannot tell which commands or environment produced the other's notes. A later review cannot reproduce the result.\n\n**Solution:** Start a small local evidence repository. Record OS, tool versions, command, exit code and an observation in its README, then commit it. A screenshot alone would hide the command and exit status; the committed note keeps those visible. The residual risk is that a correct command exit does not prove a cloud service works, so later labs must add behavioral checks.",
        "lab": """**Goal:** Create the repository used by later days and record one harmless shell observation. **Mode:** local Linux shell; no cloud permissions or spend. **Preflight:** open a terminal with Git and Python 3 available. Substitute another writable directory if `~/gcp-architect-learning` is unsuitable.\n\n1. Check the tools and your starting location. Run `pwd`, `command -v git`, `command -v python3`, then `git --version` and `python3 --version`. If either tool is absent, install it using your operating system's documented package manager before continuing.\n2. Create the repository and inspect it:\n\n```sh\nmkdir -p ~/gcp-architect-learning\ncd ~/gcp-architect-learning\ngit init\npwd\ngit status --short\n```\n\nExpected: `pwd` ends in `gcp-architect-learning`; `git status --short` prints nothing in the new repository.\n\n3. Create a first observation without storing a credential:\n\n```sh\npython3 -c 'print("day-1-baseline")'\nresult=$?\nprintf 'command: python3 -c print(day-1-baseline)\\nexit_code: %s\\n' "$result" > command-observation.txt\ncat command-observation.txt\n```\n\nExpected: the terminal prints `day-1-baseline`; the file records `exit_code: 0`. A nonzero code means stop and inspect the Python error before recording success.\n\n4. Add a README with your OS, Python/Git versions and the output above. Run `git add README.md command-observation.txt`, `git diff --cached --stat`, then `git -c user.name='Learner' -c user.email='learner@example.invalid' commit -m 'Record Day 1 baseline'`. Verify with `git status --short` and `git log -1 --oneline`. A clean status and one commit show the evidence was saved.\n\n**Troubleshooting:** If `git commit` says the README is missing, create and save it before staging. If `command -v` returns no path, the tool is absent or not on `PATH`. **Cleanup:** keep this repository for later days; no paid resources exist. **Artifact:** committed README plus `command-observation.txt`.""",
    },
    {
        "overview": "A study day is one completed unit of learning and evidence, not a calendar date. A learning baseline records available study time and which prerequisite skills are new, familiar or already demonstrated.",
        "technical": "A numbered study day is a unit of work with a result, not a promise to study on a particular date. This matters because a two-hour session may end with an unresolved lab; the next session should finish and check that lab before dependent work begins. Skipping a calendar day does not mean skipping a roadmap day. The roadmap's 485.5–665 hours are planning assumptions across the whole route, including review and capstones.\n\nTo translate hours into a calendar estimate, divide both ends of the range by your realistic weekly capacity. For example, at eight hours each week, 485.5 ÷ 8 is about 61 weeks and 665 ÷ 8 is about 84 weeks. The range widens if you need extra time for prerequisites, troubleshooting or access to a sandbox. Record actual time per day so the estimate improves after the first gate. A useful schedule has room to repeat a failed exercise; it does not force an unearned pass just to protect a date.\n\nA baseline is also an evidence question. `Familiar with Git` is a reasonable self-report, but it is different from a commit another person can inspect. Mark each prerequisite as new, familiar or demonstrated, and attach a concrete example to the demonstrated category. This prevents a later exercise from silently assuming a skill that was only recognized in a reading. At Days 17 and 35, compare your baseline and hour estimate with the work actually completed, then adjust future sessions.\n\n**Further study:** [Topic 010 references](../sources.html#topic-010) supply the learning context. The [day index](../index.html) shows the route and estimated effort.",
        "problem": "**Situation:** A learner has eight study hours each week and assumes the 180-day roadmap must finish in 180 calendar days. They rush through a failed prerequisite to stay on schedule.\n\n**Solution:** Treat a day number as a study unit. At eight hours per week, the roadmap's 485.5–665-hour planning range is about 61–84 weeks before personal variation. Log actual hours and repeat a failed exercise before depending on it. The alternative, skipping a gate to preserve a date, leaves later architecture decisions unsupported.",
        "lab": """**Goal:** Put a realistic schedule and baseline into the Day 1 README. **Mode:** local worksheet; no cloud account.\n\n1. Write the number of hours you can study in a normal week and the length of one comfortable session. For example, use `8 hours/week` and `2 hours/session` if those are your actual constraints.\n2. Calculate a planning range using `485.5 ÷ weekly hours` and `665 ÷ weekly hours`. For the example, the result is about **61–84 calendar weeks**. Record that this is an estimate, not a deadline.\n3. In the README, make a baseline table with `Linux shell`, `Git`, `networking`, `Python`, and `Google Cloud`. For each, record `new`, `familiar`, or `demonstrated` and one piece of evidence or a gap. Do not label a skill demonstrated without an artifact.\n4. Reserve the Day 17 and Day 35 gates as re-estimation points. Write one rule for a failed prerequisite, such as `repeat the earlier exercise before continuing`. Check that your plan allows skipped calendar days without skipping study days.\n\n**Expected result:** a dated README section with weekly capacity, calculation, baseline table and gate rule. **Troubleshooting:** if the two week figures are reversed, divide the larger hour estimate by the same weekly capacity again. **Cleanup:** none; retain the plan and update it with actual hours.""",
    },
    {
        "overview": "Synthetic data is invented information shaped like real input but containing no real customer details. A lab budget is the intended spend, while a cleanup owner is responsible for removing resources and verifying that the lab has ended. An alerts-only budget warns about spending but does not cap it.",
        "technical": "A synthetic fixture is invented data with a realistic shape. Brightloaf's sample order can have an order ID, an amount and a fake customer label, but it should contain no real name, address, token or customer export. This still lets you test parsing, duplicate handling and diagrams later. Label the fixture as synthetic so a reviewer does not mistake it for production evidence. If a later exercise needs a real-looking value, generate one rather than copying it from a customer system.\n\nA future cloud lab has several separate controls. The planned budget is an amount you intend to spend; the billing owner can review usage; an alert warns when a threshold is crossed; and the cleanup owner performs and verifies deletion. These are not interchangeable. Budget alerts may arrive after usage and do not automatically stop charges. Day 1 remains local, so its inventory should explicitly say that no chargeable cloud resources were created.\n\nFor later labs, record resource names and dependencies when you create them. Cleanup is a sequence: stop work, delete dependent resources in the required order, list the inventory again and review billing. Retained disks, reserved addresses or other resources may outlive the compute instance that first used them. Preserve the evidence files, but never commit credentials or a copied customer dataset. The distinction between retained evidence and deleted infrastructure is part of the lab result.\n\n**Further study:** [Google Cloud budget behavior](https://docs.cloud.google.com/billing/docs/how-to/budgets) is the focused publisher page already cited by the roadmap; [Topic 010 references](../sources.html#topic-010) supplies the curriculum context.",
        "problem": "**Situation:** A Brightloaf training project uses copied customer orders and a paid service remains active after a lab. The exercise creates privacy and billing risk before any architecture question can be answered.\n\n**Solution:** Generate a fake order, document that it is synthetic, define the intended spending limit and named cleanup owner, and keep an inventory checklist for future labs. A budget alert helps notice usage but cannot be treated as a hard cap. The safer Day 1 path is local-only, with no billing enabled and no credentials saved in Git.",
        "lab": """**Goal:** Add a safe sample and a future cloud-lab policy to the README. **Mode:** local shell; no cloud account or chargeable resource.\n\n1. In the repository from Exercise 1, create a synthetic file:\n\n```sh\ncd ~/gcp-architect-learning\nprintf '{"order_id":"demo-001","customer":"sample-customer","amount":12.50}\\n' > synthetic-order.json\npython3 -m json.tool synthetic-order.json\n```\n\nExpected: formatted JSON with `demo-001`; no real name, email, address or credential.\n\n2. Add a `Lab safety` section to README with these fields: `synthetic data only`, `planned budget`, `billing owner`, `cleanup owner`, `resource inventory`, and `deletion verification`. If you do not yet have a cloud project, record `not enabled` for billing and `no resources` for inventory.\n3. Add a checklist: inspect active project/account before a cloud lab; list created resources; delete in dependency order; list resources again; review the billing page afterward. Note explicitly that a budget alert does **not** stop spending.\n4. Run `git status --short`, stage README and `synthetic-order.json`, commit using the identity command from Exercise 1, and run `git status --short` again. Expected: a clean status and a second commit.\n\n**Troubleshooting:** if `json.tool` fails, inspect the comma and quote characters in the JSON. If an actual customer value appears, replace it before committing. **Cleanup:** no cloud cleanup is needed today; retain the synthetic file as a fixture. **Artifact:** README safety section and committed JSON sample.""",
    },
]


DAY_ELEVEN = [
    {
        "overview": "IaaS provides infrastructure such as virtual machines; PaaS provides a managed application platform; FaaS runs event-driven functions; SaaS provides a finished application. In Google Cloud, Compute Engine is commonly discussed as IaaS, App Engine and Cloud Run as PaaS, Cloud Run functions as FaaS, and Google Workspace as SaaS. These labels summarize responsibility boundaries rather than defining every product feature.",
        "technical": "**The question is: what do you receive, and what must your team still manage?** IaaS gives you infrastructure such as a VM, storage or networking. With a Compute Engine VM, Google operates the underlying physical infrastructure, while you choose and maintain the guest workload, including the OS configuration, application and data. PaaS gives you a managed application platform: with App Engine or Cloud Run, you supply code or a container and focus on the application while Google manages more of the runtime and scaling platform. FaaS narrows the deployed unit to a function invoked by a request or event; Cloud Run functions is Google's example. SaaS delivers an application ready to use, such as Google Workspace. Google Workspace is a Google SaaS example, not a GCP compute service to deploy for Brightloaf.\n\n| Model | What the customer brings | Example | Useful question |\n|---|---|---|---|\n| IaaS | OS configuration, runtime, app and data | Compute Engine VM | Do we need guest-OS control? |\n| PaaS | App code or container, configuration and data | App Engine or Cloud Run | Can the provider operate the platform? |\n| FaaS | A small function and its configuration | Cloud Run functions | Is the work naturally request- or event-triggered? |\n| SaaS | Users, settings, access policy and data | Google Workspace | Do we need a finished application? |\n\nThese models overlap at the edges. Cloud Run functions runs on Cloud Run, so a function is also using a managed application platform. GKE and BigQuery have their own managed boundaries and should be assessed by their actual service controls rather than forced into a single label. For an architecture choice, write down the required control first: guest OS, deployment unit, event trigger, data policy or finished application. Then identify which operational tasks move to Google and which remain with the customer.\n\n**Further study:** Google's [IaaS/PaaS/SaaS comparison](https://cloud.google.com/learn/paas-vs-iaas-vs-saas) discusses the service-model examples; the [Cloud Run functions documentation](https://docs.cloud.google.com/functions/docs) covers the FaaS example. Read the [shared-responsibility section](https://docs.cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate#shared-responsibility) for the workload-specific boundary. Checked against these official pages on 2026-09-26.",
        "problem": "**Situation:** Brightloaf's order API needs frequent releases and variable request traffic. A teammate proposes a VM because 'cloud means IaaS,' while another proposes a SaaS product to host custom order logic. Both choices confuse a service model with a workload requirement.\n\n**Solution:** For the stateless API, compare Cloud Run or App Engine as managed application platforms with a Compute Engine VM. The managed platform reduces guest-OS operation; the team still owns the order code, configuration, access policy and data. Use a VM if a documented requirement needs guest-OS control. A small event handler might fit Cloud Run functions, but the durable duplicate-fulfillment rule must still be implemented in application state. Google Workspace is a SaaS collaboration tool, not a place to deploy the custom order API.\n\n**Acceptance:** The design record states the selected model, the workload requirement it serves, one rejected alternative and the tasks Brightloaf retains. A model label alone is not a deployment decision.",
        "lab": "**Goal:** Produce the Day 11 responsibility matrix without creating cloud resources. **Mode:** local design exercise using the official reading above.\n\n1. Create `day-011-service-models.md` in the Day 1 evidence repository. Add columns `workload`, `needed control`, `candidate service`, `model`, `customer operates` and `provider operates`.\n2. Add these inputs: (a) an order API that must release weekly but needs no custom OS agent; (b) a legacy batch program that requires a guest-OS agent; (c) a small handler triggered by a new order event; (d) a team email and document application.\n3. For each input, choose one candidate and write one sentence explaining the boundary. Worked answer: (a) Cloud Run / PaaS, customer owns code and data; (b) Compute Engine / IaaS, customer owns the guest OS and program; (c) Cloud Run functions / FaaS, customer owns function logic and event correctness; (d) Google Workspace / SaaS, customer owns users, access settings and data. Alternatives are acceptable if the stated control and responsibility match.\n4. Change input (a) to require an OS-level security agent. Reconsider the platform choice and name the additional guest-OS work. Do not simply relabel Cloud Run as IaaS.\n5. Compare every row with the official service-model page. Mark `pass` only when model, example and retained responsibility agree. Save the file and link it from the daily responsibility matrix.\n\n**Cleanup:** No resources were created. Keep the matrix as design evidence. **Limit:** This exercise classifies management boundaries; it does not prove deployment behavior or pricing.",
    },
    {
        "overview": "Shared responsibility describes how security and operating duties are divided between the cloud provider and the customer. The division changes with the service: a VM leaves more guest-system work to the customer than a managed application platform, while customer data and access decisions remain customer responsibilities.",
        "technical": "Shared responsibility changes with the service. Google secures and operates the underlying infrastructure. You still choose what data to store, who may access it and how your application behaves. With a Compute Engine VM, your team also manages the guest OS and its configuration. A managed application platform moves more runtime work to Google, but your code, IAM choices and data controls remain yours. With SaaS, Google operates the finished application, while your organization still manages users, access policies and its own data use.\n\nDo not treat the four service-model names as a substitute for a product's security documentation. A managed service can offer customer-configurable network, encryption, identity or retention controls, and the exact split varies by feature. Build a responsibility matrix from the selected service and workload. For each control, record an owner and evidence: who patches the guest OS, who grants IAM roles, who protects order data, and who checks that replaying an order does not trigger duplicate fulfillment? Google operating a platform does not implement Brightloaf's business invariant.\n\nThe boundary is most useful during a failure or audit. If an order is visible to an unauthorized account, inspect the customer-defined identity and access policy as well as the provider's enforcement. If a VM image is outdated, the team that chose and maintains that guest environment must have a patch plan. If a managed runtime is unavailable, Google operates that platform, but Brightloaf still needs an application recovery and communication plan.\n\n**Further study:** Google's [shared-responsibility section](https://docs.cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate#shared-responsibility) explains how the split varies by workload and service model. Checked against the official page on 2026-09-26.",
        "problem": "**Situation:** Brightloaf migrates an order API from a VM to Cloud Run. The team removes its VM patch task, then incorrectly closes its IAM and data-retention tasks as 'Google's responsibility.' An overly broad account can still read orders.\n\n**Solution:** Update the responsibility matrix by control, not by slogan. Google manages the underlying platform and runtime boundary for Cloud Run; Brightloaf still owns the application code, service identity configuration, access grants, retention choices and the duplicate-fulfillment rule. Assign named owners and record a denied-access check and a replay test as acceptance evidence.\n\n**Residual risk:** A responsibility assignment is only a plan until the configuration and behavior are tested. Recheck the matrix when the service or feature changes.",
        "lab": "**Goal:** Complete a control-owner matrix for the same four service-model examples. **Mode:** local design exercise; no cloud account needed.\n\n1. In `day-011-service-models.md`, add a second table with columns `control`, `Compute Engine`, `Cloud Run`, `Google Workspace`, `evidence`. Use the controls `physical infrastructure`, `guest-OS patching`, `application code`, `IAM grants`, `customer data access`, and `order replay correctness`.\n2. Fill each owner as `Google`, `Brightloaf`, `shared / service-specific`, or `not applicable`; explain any shared entry in a note. For example, guest-OS patching is Brightloaf's task on its Compute Engine VM and is not the same customer task on Cloud Run. IAM grants and customer data access remain Brightloaf decisions across the examples. Order replay correctness belongs to Brightloaf's custom application, not to Google Workspace.\n3. Inject a failure: an overly broad role exposes order data after the move to Cloud Run. Identify the owner of the grant, the observation that reveals the mistake and the least-privilege correction. Do not describe the provider-managed runtime as proof that IAM is correct.\n4. Cross-check each row against the selected service's documentation and the official shared-responsibility reading. Mark uncertainties as `verify for this service` rather than guessing.\n5. Save the matrix, link it from the Day 11 README and state one task that moved to Google and two that stayed with Brightloaf. This is the acceptance check for the day's exit evidence.\n\n**Cleanup:** No resource was created. Retain the matrix and its dated sources. **Limit:** The table is an ownership design, not a live access test.",
    },
]


DAY_THREE_IPV6 = [
    {
        "overview": "IPv6 is a network-layer addressing system with 128-bit addresses. Prefixes identify address ranges, and special scopes such as loopback and link-local determine where an address can be used. An AAAA record maps a name to an IPv6 address; that mapping alone does not prove a connection works.",
        "technical": "**Address and prefix.** IPv6 addresses have 128 bits, normally written as eight hexadecimal groups separated by colons. Leading zeros in a group may be omitted, and one consecutive run of all-zero groups may be compressed with `::`. For example, `2001:0db8:0000:0000:0000:0000:0000:0010` becomes `2001:db8::10`. The double colon can appear only once in one address because a second omission would make the number of zero groups ambiguous. A `/64` prefix says that the first 64 bits identify the network portion for that address and prefix; it is not a port number. `2001:db8::/32` is reserved for documentation, so examples using it are not internet destinations. [RFC 4291, address text](https://datatracker.ietf.org/doc/html/rfc4291#section-2.2) and [RFC 5952, canonical text](https://datatracker.ietf.org/doc/html/rfc5952#section-4) describe these rules.\n\n**Scope matters.** `::1` is the loopback address, used to reach the same host. Link-local addresses in `fe80::/10` are for a single link; a link-local destination may need an interface identifier because the same text can exist on more than one link. Global-scope unicast addresses can be routed beyond the local link when the network permits it. The address type tells you where a packet *could* be used, but it does not establish that a route, firewall rule or listener exists. [RFC 4291, unicast addresses](https://datatracker.ietf.org/doc/html/rfc4291#section-2.5) provides the address classes.\n\n**From name to connection.** An A DNS record supplies an IPv4 address; an AAAA record supplies an IPv6 address. A client may have both answers and choose an address family for a connection attempt. After it chooses IPv6, it needs a usable source address, route and next-hop reachability. IPv6 Neighbor Discovery uses ICMPv6 messages to discover routers and on-link neighbors; it is not the same exchange as IPv4 ARP. The destination must then have a listening socket for the chosen address family and port. [RFC 4861, Neighbor Discovery overview](https://datatracker.ietf.org/doc/html/rfc4861#section-3) explains the local-link mechanisms.\n\n**Diagnostic boundary:** An AAAA answer proves that a name resolved to an IPv6 address. It does not prove that packets reach that address or that TCP established. If the A path works and the AAAA path fails, keep those facts separate and check the IPv6 route, filtering and listener before blaming DNS.",
        "problem": "**Situation:** Brightloaf publishes both A and AAAA records for its order API. Some clients complete requests over IPv4, while clients attempting IPv6 time out before any HTTP response. The team sees a valid AAAA answer and calls it a DNS outage.\n\n**Diagnosis:** The AAAA answer shows that name resolution succeeded for IPv6. The failure is later in the path. Record the selected IPv6 destination and port, then check whether the client has an IPv6 source and route, whether the packet can reach the next hop, and whether the service listens on IPv6 port 443. A working IPv4 connection does not prove any of those IPv6 conditions.\n\n**Solution:** Repair the first failing IPv6 boundary or, if IPv6 service is not ready, remove the unusable AAAA publication under a controlled change while preserving the working A path. Recheck both address families and the application response. The alternative of changing the A record would not repair the IPv6 route. This is a scenario for diagnosis; the local lab below uses supplied data and does not claim to test a deployed Brightloaf service.",
        "lab": """**Goal:** Read and classify IPv6 addresses, then trace a supplied dual-stack lookup. **Mode:** local Python 3 and a paper or Markdown diagram; no cloud account or external network required. **Prerequisite:** Day 2's IPv4 address and next-hop worksheet.\n\n1. In your terminal, confirm Python 3 with `python3 --version`. Make a new `day-003-ipv6.md` note in your Day 1 evidence repository. Mark the following addresses as *documentation examples*, not hosts to contact.\n2. Run this offline address check:\n\n```sh\npython3 - <<'PY'\nfrom ipaddress import IPv6Address, IPv6Network\na = IPv6Address('2001:0db8:0000:0000:0000:0000:0000:0010')\nnetwork = IPv6Network('2001:db8:abcd:1200::/64')\nprint('compressed:', a.compressed)\nprint('network:', network.network_address, 'prefix:', network.prefixlen)\nprint('loopback:', IPv6Address('::1').is_loopback)\nprint('link-local:', IPv6Address('fe80::1').is_link_local)\nPY\n```\n\nExpected lines include `compressed: 2001:db8::10`, `network: 2001:db8:abcd:1200:: prefix: 64`, `loopback: True` and `link-local: True`. If parsing fails, check the number of colons and the placement of `::`. Save the output in the note.\n\n3. Use this supplied resolver output: `orders.example.test A 192.0.2.25` and `orders.example.test AAAA 2001:db8:abcd:1200::25`. Draw two separate paths ending at `(192.0.2.25, TCP 443)` and `(2001:db8:abcd:1200::25, TCP 443)`. Label `192.0.2.0/24` and `2001:db8::/32` as documentation ranges. The resolver output is a fixture, not a live DNS lookup.\n4. Inject a failure into the diagram: the IPv4 path establishes TCP, but the IPv6 client has no route to its IPv6 destination. Predict the first failure: the AAAA lookup still succeeds, but the IPv6 TCP handshake cannot establish. Write the next observation you would seek: the selected source address and IPv6 route. A working IPv4 HTTP response does not repair the IPv6 path.\n5. Under the diagram, answer: What did DNS prove? What would a successful TCP handshake prove? What would an HTTP response prove? Check that these are three distinct statements. Link the diagram to the day's combined DNS/transport artifact.\n\n**Verification:** The note contains the four expected Python results, both socket endpoints, the failing IPv6 boundary and separate DNS/TCP/HTTP conclusions. **Troubleshooting:** an unexpected address format is a parsing issue; a missing IPv6 interface on your computer is irrelevant to this offline fixture. **Cleanup:** no network or cloud resource was created; retain the note and output.""",
    }
]


def _replace_lab_text(content: list[dict], topic_index: int, before: str, after: str) -> None:
    lab = content[topic_index]["lab"]
    if before not in lab:
        raise ValueError(f"Missing authored lab text: {before[:60]}")
    content[topic_index]["lab"] = lab.replace(before, after, 1)


_replace_lab_text(
    DAY_ONE, 0,
    "Run `pwd`, `command -v git`, `command -v python3`, then `git --version` and `python3 --version`.",
    "Run these checks in the terminal:\n\n```sh\npwd\ncommand -v git\ncommand -v python3\ngit --version\npython3 --version\n```",
)
_replace_lab_text(
    DAY_ONE, 0,
    "Run `git add README.md command-observation.txt`, `git diff --cached --stat`, then `git -c user.name='Learner' -c user.email='learner@example.invalid' commit -m 'Record Day 1 baseline'`. Verify with `git status --short` and `git log -1 --oneline`.",
    "Run the following commands in the repository to stage, review and commit the note:\n\n```sh\ngit add README.md command-observation.txt\ngit diff --cached --stat\ngit -c user.name='Learner' -c user.email='learner@example.invalid' commit -m 'Record Day 1 baseline'\ngit status --short\ngit log -1 --oneline\n```",
)
_replace_lab_text(
    DAY_ONE, 2,
    "Run `git status --short`, stage README and `synthetic-order.json`, commit using the identity command from Exercise 1, and run `git status --short` again.",
    "Run the following commands to stage, commit and verify the fixture:\n\n```sh\ngit status --short\ngit add README.md synthetic-order.json\ngit -c user.name='Learner' -c user.email='learner@example.invalid' commit -m 'Record Day 1 safety plan'\ngit status --short\n```",
)
_replace_lab_text(
    DAY_THREE_IPV6, 0,
    "In your terminal, confirm Python 3 with `python3 --version`.",
    "Open a Linux terminal and confirm Python 3 with:\n\n```sh\npython3 --version\n```",
)


@lru_cache(maxsize=None)
def day_content(day: int) -> dict[tuple[str, str], str]:
    path = SITE / "content" / f"day-{day:03d}.md"
    if not path.exists():
        return {}
    source = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^<!-- (topic-\d{2}):(overview|technical|problem|lab) -->\s*$", source, re.M))
    entries = {}
    for i, match in enumerate(matches):
        key = (match.group(1), match.group(2))
        if key in entries:
            raise ValueError(f"Duplicate authored section in {path}: {key}")
        end = matches[i + 1].start() if i + 1 < len(matches) else len(source)
        entries[key] = source[match.end():end].strip()
    return entries


def authored_card(day: int, part: int, index: int, topic: dict) -> str:
    key, title = topic["key"], topic["title"]
    labels = ("overview", "technical", "problem", "lab")
    label = labels[part - 1]
    authored = {1: DAY_ONE, 3: DAY_THREE_IPV6, 11: DAY_ELEVEN}
    content = authored[day][index][label] if day in authored and index < len(authored[day]) else ""
    content_path = SITE / "content" / f"day-{day:03d}-{topic['key']}-{label}.md"
    if content_path.exists():
        content = content_path.read_text(encoding="utf-8")
    elif (topic["key"], label) in day_content(day):
        content = day_content(day)[(topic["key"], label)]
    if not content:
        raise ValueError(f"Missing authored content: day {day}, {topic['key']}, {label}")
    if day == 3 and part == 2:
        content += "\n\n**Example-address source:** [RFC 3849](https://datatracker.ietf.org/doc/html/rfc3849) reserves `2001:db8::/32` for documentation."
    if day == 3 and part == 4:
        content += "\n\n**Fixture-address sources:** [RFC 5737](https://datatracker.ietf.org/doc/html/rfc5737) reserves `192.0.2.0/24` for IPv4 examples; [RFC 3849](https://datatracker.ietf.org/doc/html/rfc3849) reserves `2001:db8::/32` for IPv6 examples."
    if part == 1:
        content += f'\n\n[Technical discussion](#{key}-technical) · [Real-world problem](#{key}-problem) · [Exercise](#{key}-lab)'
    if part == 4:
        content += f'\n\n<label class="check"><input type="checkbox" data-progress="lab-{day}-{key}"> I completed and checked this topic exercise</label>'
    return f'<article id="{key}-{label}" class="topic-card"><h3>{esc(title)}</h3>{md(content)}</article>'


def render_day(day: dict, days: list[dict], refs: dict) -> str:
    n = day["number"]
    prev = days[n-2] if n > 1 else None
    nxt = days[n] if n < 180 else None
    crumb = f'<div class="crumb"><a href="../index.html">Roadmap index</a> / <a href="../index.html#block-{slug(day["block"])}">{esc(day["block"])}</a> / Day {n} of 180</div>'
    metadata = f'<div class="pills"><span class="pill">{day["type"].upper()}</span><span class="pill">{esc(day["time"])}</span><span class="pill">{esc(day["mode"])}</span><span class="pill">Topics {", ".join(f"{x:03d}" for x in day["refs"])}</span></div>'
    prereq = re.sub(r"\[Day (\d+)\]\(#day-\d+\)", lambda m: f'[Day {m.group(1)}](day-{int(m.group(1)):03d}.html)', day["prerequisites"])
    outcome = "Set up a reproducible local workspace, decide a workable pace, and record safety rules for later labs." if n == 1 else day["practice"]
    intro = f'<section class="hero">{metadata}<h1>Day {n} — {esc(day["title"])}</h1><p class="lead"><strong>Outcome:</strong> {esc(outcome)}</p><div><strong>Entry prerequisites:</strong> {md(prereq)}</div><div class="callout success"><strong>Exit artifact</strong>{md(day["exit_evidence"])}</div><p class="small">Source curriculum checked {VERIFIED}; external documentation links are selected reading and may change. A tabletop result is a design exercise, not a production test.</p></section>'
    toc = '<aside class="toc" aria-label="On this page"><strong>On this page</strong><a href="#part-1">1 · Topics</a><a href="#part-2">2 · Technical discussion</a><a href="#part-3">3 · Problems and solutions</a><a href="#part-4">4 · Labs</a>'
    for topic in day["topics"]:
        key = topic["key"]
        toc += f'<div class="toc-topic"><span>{esc(topic["title"])}</span><a href="#{key}-overview">overview</a> · <a href="#{key}-technical">discussion</a> · <a href="#{key}-problem">problem</a> · <a href="#{key}-lab">lab</a></div>'
    toc += '</aside>'
    p1, p2, p3, p4 = [], [], [], []
    manifest = []
    for topic in day["topics"]:
        key, title, scope = topic["key"], topic["title"], topic["scope"]
        if day["type"] in ("gate", "capstone"):
            mechanism, check = LESSONS[-1][1:]
            mechanics, diagnosis = DEEP_DIVES[-1][1:]
            example = "Input: a review packet has strong design claims but evidence quality is scored 1/3."
            expected = "Expected: the review does not pass the at-least-2-per-dimension rule; repair the cited experiment and rescore."
        else:
            mechanism, check = lesson(topic)
            mechanics, diagnosis = deep_dive(topic)
            example, expected = worked_example(topic)
        rid, source_label, source_url = source_for(day, topic, refs)
        p1.append(f'<article id="{key}-overview" class="topic-card"><h3>{esc(title)}</h3><p><a href="#{key}-technical">Technical discussion →</a> <a href="#{key}-problem">Real-world problem →</a> <a href="#{key}-lab">Step-by-step lab →</a></p></article>')
        study = f'<div class="callout"><strong>Further study</strong><p><a href="../sources.html#topic-{rid.zfill(3)}">Topic {rid.zfill(3)} source section</a> in this site, with original publisher links and the reading context.</p>' if rid else '<div class="callout"><strong>Further study</strong>'
        if source_url:
            study += f'<p>Publisher: <a href="{esc(source_url)}" rel="noopener noreferrer">{esc(source_label)}</a>. This publisher URL was carried from the roadmap index; the exact external section has not been reverified for this topic.</p>'
        study += '</div>'
        p2.append(f'<article id="{key}-technical" class="topic-card"><h3>{esc(title)}</h3><p>{esc(mechanics)}</p><p>{esc(diagnosis)}</p><div class="callout"><strong>Apply it</strong><p>{esc(example)} {esc(expected)}</p></div>{study}</article>')
        if day["type"] == "gate":
            symptom = f"The review panel cannot find reproducible proof for {title.lower()} in the earlier artifacts."
            resolution = "Locate the earliest failed criterion, repeat its source day, attach the corrected observation, and rescore all five rubric dimensions."
        elif day["type"] == "capstone":
            symptom = f"The Brightloaf design defense is challenged on {title.lower()}; a reviewer changes one assumption after the presentation."
            resolution = "Trace the changed requirement to the existing ADR, update the risk and acceptance evidence, and defend a revised decision without claiming a new deployment."
        else:
            symptom = f"Brightloaf's order API, fulfillment consumer or analytics feed has an unexplained result involving {title.lower()}. A rushed configuration change could hide the actual failed boundary."
            resolution = f"Use the evidence in today's practice to locate the first failing boundary. {check} Keep the order invariant: replaying an order or event must not create a second fulfillment."
        p3.append(f'<article id="{key}-problem" class="topic-card"><h3>{esc(title)} · field case</h3><p><strong>Situation and impact:</strong> {esc(symptom)}</p><p><strong>Constraints:</strong> Use synthetic data, preserve prior evidence, stay inside the lab budget and identify which result is observed versus assumed.</p><p><strong>Diagnosis and solution:</strong> {esc(resolution)}</p><p><strong>Alternative and residual risk:</strong> Do not accept a green command exit as proof of behavior. A result from a supplied trace or tabletop model still needs validation in the actual environment before production use.</p></article>')
        mode = day["mode"]
        task = day["practice"]
        extension = executable_extension(n, topic)
        lab = f'''<article id="{key}-lab" class="topic-card lab"><h3>Exercise {len(p4)+1}: {esc(title)}</h3><p><strong>Goal:</strong> Apply this topic to the day's practice and save a topic-specific observation.</p><p><strong>Mode:</strong> {esc(mode)} · <strong>Prerequisite:</strong> {esc(re.sub(r'\[[^]]+\]\([^)]*\)', 'the linked earlier day', day['prerequisites']))}</p>{extension}<ol><li><strong>Preflight.</strong> Open a local text editor. Create a new note named <code>day-{n:03d}-{key}.md</code>. At the top write today's date, lab mode, prior artifact used, and "synthetic Brightloaf data". No cloud resources or credentials are required for this exercise.</li><li><strong>Set the input.</strong> Copy this scope into the note under <code>Input</code>: <code>{esc(scope)}</code>. Use the worked example from Part 2 as the baseline.</li><li><strong>Execute the reasoning.</strong> Draw a three-column table headed <code>Input or requirement | mechanism or decision | expected observation</code>. Fill one row for each distinct item in the scope. State which observation would support the mechanism.</li><li><strong>Inject one failure.</strong> Change one input or assumption in a second table row. Predict the first changed observation and how to restore the original condition. For the Brightloaf flow, explicitly check that a replayed order cannot cause duplicate fulfillment.</li><li><strong>Verify and save.</strong> Compare the table to this check: {esc(check)} Record whether it passes, the specific evidence, one alternative, and one remaining uncertainty. Save the note; add its path to the daily exit artifact.</li></ol><div class="callout success"><strong>Expected result / acceptance</strong><p>A saved note with an input, mechanism, observed or predicted output, negative case and recovery. The daily evidence section states the final artifact to assemble.</p></div><div class="callout caution"><strong>Troubleshooting</strong><p>If the expected output is vague, name the exact field, command result or diagram edge to inspect. If a prerequisite is missing, revisit the linked earlier day and record the gap. A tabletop prediction must remain labeled as a prediction.</p></div><div class="callout"><strong>Cleanup and cost</strong><p>No chargeable resource is created. Keep the note as evidence; delete only disposable copies and confirm that the exercise did not use a cloud project.</p></div><label class="check"><input type="checkbox" data-progress="lab-{n}-{key}"> I completed and checked this topic exercise</label></article>'''
        p4.append(lab)
        authored_path = SITE / "content" / f"day-{n:03d}-{key}-overview.md"
        if n in (1, 11) or (n == 3 and len(p1) == 1) or authored_path.exists() or (key, "overview") in day_content(n):
            index = len(p1) - 1
            for part_number, cards in enumerate((p1, p2, p3, p4), 1):
                cards[-1] = authored_card(n, part_number, index, topic)
        manifest.append({"day": n, "topic_key": key, "topic": title, "scope": scope, "source_topic_ids": ",".join(str(x) for x in day["refs"]), "overview_anchor": f"{key}-overview", "technical_anchor": f"{key}-technical", "problem_anchor": f"{key}-problem", "lab_anchor": f"{key}-lab", "expected_artifact": day["exit_evidence"], "further_study_section": f"sources.html#topic-{rid.zfill(3)}" if rid else "", "publisher_url": source_url, "publisher_section_verified": "no"})
        if n == 12:
            verified_sources = {
                "topic-01": "https://docs.cloud.google.com/compute/docs/regions-zones#choose",
                "topic-02": "https://docs.cloud.google.com/compute/docs/autoscaler#autoscaling_policy",
                "topic-03": "https://docs.cloud.google.com/billing/docs/how-to/estimate-costs#access-pricing-calculator",
            }
            manifest[-1]["publisher_url"] = verified_sources[key]
            manifest[-1]["publisher_section_verified"] = "yes"
    def part(npart: int, name: str, entries: list[str]) -> str:
        return f'<section id="part-{npart}" class="part"><h2>{npart} · {name}</h2>' + "".join(entries) + '</section>'
    score = ''
    if day["type"] in ("gate", "capstone"):
        score = '<div class="callout caution"><strong>Review rubric</strong><p>Score correctness, requirement traceability, evidence quality, failure/recovery reasoning and communication from 0–3 each. For Gates 2–6 and capstones, require at least 2 in every dimension and 12/15 overall. Repair a failed criterion and record pass/repeat.</p></div>'
    after = f'<section class="completion"><h2>Daily evidence</h2>{score}<label class="check"><input type="checkbox" data-progress="read-{n}"> I read and reviewed the day</label><label class="check"><input type="checkbox" data-progress="artifact-{n}"> I saved the exit artifact</label></section>'
    pager = '<nav class="pager" aria-label="Day pagination">'
    if prev:
        pager += f'<a href="day-{n-1:03d}.html">← Day {n-1}<small>{esc(prev["title"])}</small></a>'
    pager += '<a href="../index.html">All 180 days<small>Browse the roadmap</small></a>'
    if nxt:
        pager += f'<a href="day-{n+1:03d}.html">Day {n+1} →<small>{esc(nxt["title"])}</small></a>'
    pager += '</nav><p class="shortcut">Keyboard: P or [ previous · N or ] next · I index</p>'
    body = f'<main id="main" class="container day" data-day="{n}" data-prev="{"day-%03d.html"%(n-1) if prev else ""}" data-next="{"day-%03d.html"%(n+1) if nxt else ""}" data-index="../index.html">{crumb}{intro}{toc}{part(1,"Topics of the day",p1)}{part(2,"Technical discussion of each topic",p2)}{part(3,"Real-world problem and solution for each topic",p3)}{part(4,"Step-by-step labs for each topic",p4)}{after}{pager}</main>'
    return article_shell(f'Day {n}: {day["title"]}', body, day=day, days=days), manifest


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def render_index(days: list[dict]) -> str:
    blocks = list(dict.fromkeys(d["block"] for d in days))
    filters = '<label for="day-search">Search days and topics</label><input id="day-search" type="search" placeholder="DNS, IAM, Day 42…"><label for="block-filter">Work block</label><select id="block-filter"><option value="">All blocks</option>' + "".join(f'<option value="{esc(b)}">{esc(b)}</option>' for b in blocks) + '</select><label for="type-filter">Day type</label><select id="type-filter"><option value="">All types</option><option value="day">Study day</option><option value="gate">Gate</option><option value="capstone">Capstone</option></select>'
    cards = []
    for b in blocks:
        cards.append(f'<section class="block" id="block-{slug(b)}" data-block-group="{esc(b)}"><h2>{esc(b)}</h2><div class="day-grid">')
        for d in days:
            if d["block"] != b:
                continue
            n = d["number"]
            terms = " ".join([str(n), d["title"], d["study"], d["practice"], d["block"], " ".join(str(x) for x in d["refs"])]).lower()
            cards.append(f'<article class="day-card" data-search="{esc(terms)}" data-block="{esc(b)}" data-type="{d["type"]}"><div class="pills"><span class="pill">Day {n}</span><span class="pill">{esc(d["type"])}</span><span class="pill">{esc(d["time"])}</span></div><h3><a href="days/day-{n:03d}.html">{esc(d["title"])}</a></h3><p>{esc(d["study"][:180])}{"…" if len(d["study"])>180 else ""}</p><p class="small">{esc(d["mode"])} · Topic IDs {", ".join(str(x) for x in d["refs"])}</p><label class="check"><input type="checkbox" data-progress="read-{n}"> Reading complete</label></article>')
        cards.append('</div></section>')
    body = f'''<main id="main" class="container"><section class="hero"><div class="pills"><span class="pill">180 study days</span><span class="pill">6 gates</span><span class="pill">5 capstone defenses</span></div><h1>Build evidence for every architecture decision.</h1><p class="lead">A 180-day route from local fundamentals to multi-team Google Cloud architecture. Study the mechanism, solve a realistic problem, complete a safe exercise, and keep the artifact for later gates.</p><p>The roadmap plans 485.5–665 hours as an estimate, not a guarantee. Begin with <a href="days/day-001.html">Day 1</a>, or search for a topic below. All pages and exercises work without a cloud account; design exercises do not prove production behavior.</p><p><a class="button" href="days/day-001.html">Start Day 1 →</a> <a class="button secondary" href="artifacts.html">View artifacts</a></p></section><section class="toolbar"><h2>Find a day</h2>{filters}<p id="result-count" aria-live="polite"></p></section>{''.join(cards)}<section class="completion"><h2>Your local progress</h2><p>Reading, each topic lab and saved evidence are tracked separately in this browser. Opening a page does not mark anything complete.</p><button id="export-progress" type="button">Export progress JSON</button><label for="import-progress" class="button secondary">Import progress JSON</label><input id="import-progress" type="file" accept="application/json" hidden><p id="progress-status" role="status"></p></section></main>'''
    return article_shell("Day index", body)


def render_sources(refs: dict) -> str:
    entries = []
    for n, links in sorted(refs.items()):
        items = ''.join(f'<li><a href="{esc(link["url"])}" rel="noopener noreferrer">{esc(link["label"])}</a> <small>{esc(urlparse(link["url"]).hostname or "")}</small></li>' for link in links)
        entries.append(f'<section id="topic-{n:03d}" class="topic-card"><h2>Topic {n:03d} references</h2><ul>{items}</ul></section>')
    body = f'<main id="main" class="container"><section class="hero"><h1>Source index</h1><p>The anchors below lead to the exact source-topic section. Publisher links were carried from the 100-day roadmap index, last reviewed there on {VERIFIED}; this site does not claim every external section fragment or video timestamp has been checked.</p></section>{"".join(entries)}</main>'
    return article_shell("Source index", body)


def render_artifacts(days: list[dict]) -> str:
    cards = ''.join(f'<li><a href="days/day-{d["number"]:03d}.html">Day {d["number"]}: {esc(d["title"])}</a> — {esc(d["exit_evidence"])}</li>' for d in days)
    return article_shell("Artifact index", f'<main id="main" class="container"><section class="hero"><h1>Evidence and artifact index</h1><p>Save each daily artifact locally. Gates audit earlier evidence; capstones defend the packages assembled during the roadmap.</p></section><ol class="artifact-list">{cards}</ol></main>')


def render_glossary() -> str:
    terms = {"ADC":"Application Default Credentials: the standard credential lookup flow for Google Cloud client libraries.","ADR":"Architecture decision record: a dated choice, context, alternatives and consequences.","CIDR":"Address block defined by a network prefix length.","IAM":"Identity and Access Management: grants permissions to principals on scoped resources.","RPO":"Recovery point objective: maximum acceptable data loss measured in time.","RTO":"Recovery time objective: maximum acceptable time to restore service.","SLI":"Service level indicator: a measured aspect of user-visible service behavior.","SLO":"Service level objective: a target for an SLI over a time window.","TTL":"Time to live: duration a DNS answer may be cached.","WAL":"Write-ahead log: durable record of a state change before data pages are updated."}
    entries = ''.join(f'<dt>{esc(k)}</dt><dd>{esc(v)}</dd>' for k,v in terms.items())
    return article_shell("Glossary", f'<main id="main" class="container"><section class="hero"><h1>Glossary</h1><p>Working definitions for recurring terms in the daily pages.</p></section><dl class="glossary">{entries}</dl></main>')


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class PageStructure(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.day_values: list[str] = []
        self.title = ""
        self._in_title = False
        self.day_options = 0
        self.has_header = False
        self.has_toc = False
        self.has_stylesheet = False
        self.has_site_script = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "main" and values.get("data-day"):
            self.day_values.append(values["data-day"])
        if tag == "option" and re.fullmatch(r"day-\d{3}\.html", values.get("value") or ""):
            self.day_options += 1
        if tag == "header" and "site-nav" in (values.get("class") or "").split():
            self.has_header = True
        if tag in ("aside", "nav") and "toc" in (values.get("class") or "").split():
            self.has_toc = True
        if tag == "link" and values.get("href") == "../assets/site.css":
            self.has_stylesheet = True
        if tag == "script" and values.get("src") == "../assets/site.js":
            self.has_site_script = True
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def validate_day_override(source: str, day: dict) -> None:
    number = day["number"]
    page = PageStructure()
    page.feed(source)
    ids = set(page.ids)
    required = {"main", "day-jump", *(f"part-{part}" for part in range(1, 5))}
    required.update(
        f"{topic['key']}-{part}"
        for topic in day["topics"]
        for part in ("overview", "technical", "problem", "lab")
    )
    missing = sorted(required - ids)
    if not source.lstrip().lower().startswith("<!doctype html>") or "</html>" not in source.lower():
        raise ValueError(f"Day {number}: override must be a complete HTML document")
    if page.day_values != [str(number)] or not re.search(rf"\bDay {number}\b", page.title, re.I):
        raise ValueError(f"Day {number}: title or main data-day does not match the requested day")
    if len(page.ids) != len(ids):
        raise ValueError(f"Day {number}: duplicate HTML IDs")
    if missing:
        raise ValueError(f"Day {number}: missing required IDs: {', '.join(missing)}")
    if page.day_options != 180 or not all((page.has_header, page.has_toc, page.has_stylesheet, page.has_site_script)):
        raise ValueError(f"Day {number}: existing navigation or local site assets were not preserved")
    if re.search(r"\[PASTE ONLY|\[Insert (?:Day|Topic)|<!--\s*content goes here", source, re.I):
        raise ValueError(f"Day {number}: placeholder text remains in the override")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize or build one authored day page; full draft rebuild is explicit")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--init-day", type=int, choices=range(1, 181), metavar="1-180", help="Copy the existing day page to an override without replacing an existing override")
    mode.add_argument("--day", type=int, choices=range(1, 181), metavar="1-180", help="Build only this day from its complete HTML override")
    mode.add_argument("--all", action="store_true", help="Regenerate the full site, including draft fallback content for days without overrides")
    args = parser.parse_args()
    days = parse_days()
    if args.init_day is not None:
        source = SITE / "days" / f"day-{args.init_day:03d}.html"
        override = SITE / "content" / f"day-{args.init_day:03d}-page.html"
        if override.exists():
            parser.error(f"Override already exists: {override}")
        if not source.exists():
            parser.error(f"Existing page is missing: {source}")
        write(override, source.read_text(encoding="utf-8"))
        print(f"Initialized Day {args.init_day} override: {override}")
        return
    if args.day is not None:
        day = days[args.day - 1]
        override = SITE / "content" / f"day-{args.day:03d}-page.html"
        if not override.exists():
            parser.error(f"Authored page missing: {override}. Run --init-day {args.day}, edit it, then build.")
        output = override.read_text(encoding="utf-8")
        validate_day_override(output, day)
        write(SITE / "days" / f"day-{args.day:03d}.html", output)
        print(f"Built Day {args.day}: {SITE / 'days' / f'day-{args.day:03d}.html'}")
        return
    refs = parse_references()
    rows = []
    for day in days:
        output, topics = render_day(day, days, refs)
        override = SITE / "content" / f'day-{day["number"]:03d}-page.html'
        if override.exists():
            output = override.read_text(encoding="utf-8")
            validate_day_override(output, day)
        write(SITE / "days" / f'day-{day["number"]:03d}.html', output)
        rows.extend(topics)
    write(SITE / "index.html", render_index(days))
    write(SITE / "sources.html", render_sources(refs))
    write(SITE / "artifacts.html", render_artifacts(days))
    write(SITE / "glossary.html", render_glossary())
    write(SITE / "data" / "days.json", json.dumps([{k:v for k,v in d.items() if k != "topics"} for d in days], indent=2))
    with (SITE / "data" / "coverage.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Built {len(days)} day pages, {len(rows)} topic sections, {len(refs)} source topics")
    print("Day types:", dict(Counter(d["type"] for d in days)))


if __name__ == "__main__":
    main()
