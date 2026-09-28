#!/usr/bin/env python3
"""Build complete, production-grade content/day-057-page.html."""
import re
from pathlib import Path

SITE = Path("/home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site")
ORIGINAL = SITE / "days" / "day-057.html"

content = ORIGINAL.read_text(encoding="utf-8")

header_match = re.search(r'(<!doctype html>.*?<header class="site-nav">.*?</header>)', content, re.DOTALL)
if not header_match:
    raise ValueError("Could not extract header from days/day-057.html")
header_html = header_match.group(1)

# Ensure day 57 is selected
header_html = re.sub(r'<option value="day-\d{3}\.html" selected>', lambda m: m.group(0).replace(' selected', ''), header_html)
header_html = header_html.replace('<option value="day-057.html">Day 57: BGP, MTU and NAT diagnosis</option>',
                                  '<option value="day-057.html" selected>Day 57: BGP, MTU and NAT diagnosis</option>')

hero_and_toc = """
<div class="audit-banner"><strong>Draft content:</strong> Most lessons use generated templates and have not passed topic-level review. <a href="../CONTENT_AUDIT.md">Read the content audit</a>.</div>
<main id="main" class="container day" data-day="57" data-prev="day-056.html" data-next="day-058.html" data-index="../index.html">
<div class="crumb"><a href="../index.html">Roadmap index</a> / <a href="../index.html#block-core-services-and-integrated-practice">Core services and integrated practice</a> / Day 57 of 180</div>
<section class="hero">
<div class="pills"><span class="pill">DAY 57</span><span class="pill">3–4 hours</span><span class="pill">production practice</span><span class="pill">BGP &amp; Hybrid Transit</span></div>
<h1>Day 57 — BGP, MTU and NAT diagnosis</h1>
<p class="lead"><strong>Outcome:</strong> Diagnose BGP route withdrawal, asymmetric return paths, MTU blackholes, and Cloud NAT port exhaustion; engineer deterministic MED path preference, Private Google Access for on-premises hosts, and hybrid failover architectures.</p>
<div><strong>Entry prerequisites:</strong> <p><a href="day-056.html">Day 56</a>, <a href="day-051.html">Day 51</a>; bring their exit artifacts.</p></div>
<div class="callout success"><strong>Exit artifact</strong><p>An evidence-based diagnosis for each fault and a failover validation plan, assembled as <code>day-057-failover-validation.md</code>.</p></div>
<p class="small">Source curriculum checked 2026-09-26; external documentation links are selected reading and may change. A tabletop result is a design exercise, not a production test.</p>
</section>

<aside class="toc" aria-label="On this page">
<strong>On this page</strong>
<a href="#part-1">1 · Topics</a>
<a href="#part-2">2 · Technical discussion</a>
<a href="#part-3">3 · Problems and solutions</a>
<a href="#part-4">4 · Labs</a>
<div class="toc-topic"><span>Cloud Router and BGP (dynamic route advertisement, MED, custom advertisements)</span><a href="#topic-01-overview">overview</a> · <a href="#topic-01-technical">discussion</a> · <a href="#topic-01-problem">problem</a> · <a href="#topic-01-lab">lab</a></div>
<div class="toc-topic"><span>Private Google Access for on-premises hosts</span><a href="#topic-02-overview">overview</a> · <a href="#topic-02-technical">discussion</a> · <a href="#topic-02-problem">problem</a> · <a href="#topic-02-lab">lab</a></div>
<div class="toc-topic"><span>Choosing VPN vs Interconnect (bandwidth, latency, cost, SLA, lead time)</span><a href="#topic-03-overview">overview</a> · <a href="#topic-03-technical">discussion</a> · <a href="#topic-03-problem">problem</a> · <a href="#topic-03-lab">lab</a></div>
</aside>
"""

print("Base hero and TOC defined.")
