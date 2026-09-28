#!/usr/bin/env python3
"""author_engine.py — Deterministic compiler for 180-day GCP Architect curriculum pages.

Combines high-density architectural content (pure Python data specification)
with the site shell and generates accessible, responsive SVGs.
Eliminates LLM token waste on HTML/SVG boilerplate and prevents model drift.
"""

from __future__ import annotations

import argparse
from html import escape
import importlib.util
from pathlib import Path
import re
import subprocess
import sys

from bs4 import BeautifulSoup
import markdown

ROOT = Path(__file__).resolve().parents[1]
SITE_CONTENT = ROOT / "content"
SITE_DAYS = ROOT / "days"
SCRIPTS = ROOT / "scripts"


def wrap_svg(text: str, limit: int = 22, max_lines: int = 2) -> list[str]:
    """Break text into wrapped lines for SVG boxes without overflowing."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > limit:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines[:max_lines]


def render_incident_svg(day: int, index: int, topic: dict) -> str:
    """Generate dual-lane incident SVG diagram: Failed Path vs Corrected Path with Day 67 standards."""
    scenario = topic.get("scenario", {})
    if scenario.get("incident_svg_html"):
        return f'<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto">{scenario["incident_svg_html"]}</div></figure>'
    if scenario.get("svg_html"):
        return f'<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto">{scenario["svg_html"]}</div></figure>'

    diagram = scenario.get("diagram", ("Trigger event", "Root cause", "Impact", "Corrected control", "Expected outcome"))
    event, cause, impact, control, outcome = diagram

    uid = f"d{day:03d}-case-{index}"
    title = f"{topic.get('title', 'Topic')}: Failure Cascade vs Corrected Control"
    desc = (
        "Dual-lane architectural incident diagram showing the failed path with unmitigated root cause and blast radius, "
        "contrasted with the corrected path featuring an enforced defensive control and verified invariant."
    )

    facts = scenario.get("facts", "Synthetic case scenario.")
    inference = scenario.get("inference", "Architectural inference based on observed constraints.")
    expected = scenario.get("expected", "Expected post-fix behavior once verified.")

    e_lines = wrap_svg(event, limit=28, max_lines=3)
    c_lines = wrap_svg(cause, limit=28, max_lines=3)
    i_lines = wrap_svg(impact, limit=28, max_lines=3)
    ctrl_lines = wrap_svg(control, limit=28, max_lines=3)
    out_lines = wrap_svg(outcome, limit=28, max_lines=3)

    def render_card_text(lines, start_y, fill):
        return "".join(
            f'<text x="0" y="{start_y + j * 16}" text-anchor="middle" font-family="monospace" font-size="11" fill="{fill}">{escape(l)}</text>'
            for j, l in enumerate(lines)
        )

    failed_lane = f'''
  <!-- UPPER LANE: FAILED PATH -->
  <rect x="15" y="44" width="990" height="175" rx="6" fill="#180b12" stroke="#881337" stroke-width="1.5"/>
  <rect x="25" y="52" width="220" height="20" rx="3" fill="#2d0b13" stroke="#f43f5e" stroke-width="1"/>
  <text x="135" y="66" text-anchor="middle" font-family="monospace" font-size="9" fill="#f43f5e" font-weight="bold">FAILED PATH · UNMITIGATED CASCADE</text>

  <!-- Card 1: Trigger -->
  <g transform="translate(150, 140)">
    <rect x="-115" y="-50" width="230" height="100" rx="4" fill="#121526" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="0" y="-30" text-anchor="middle" font-family="monospace" font-size="10" fill="#94a3b8" font-weight="bold">1. INITIATING EVENT</text>
    {render_card_text(e_lines, -6, "#cbd5e1")}
    <rect x="-70" y="24" width="140" height="16" rx="2" fill="#1e293b"/>
    <text x="0" y="36" text-anchor="middle" font-family="monospace" font-size="8" fill="#94a3b8">[UNCHECKED TRIGGER]</text>
  </g>

  <!-- Arrow 1 -> 2 -->
  <line x1="270" y1="140" x2="350" y2="140" stroke="#f43f5e" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#{uid}-arr-fail)"/>
  <text x="310" y="132" text-anchor="middle" font-family="monospace" font-size="8" fill="#f43f5e">TRIGGERS</text>

  <!-- Card 2: Root Cause -->
  <g transform="translate(480, 140)">
    <rect x="-120" y="-50" width="240" height="100" rx="4" fill="#2a0a10" stroke="#f43f5e" stroke-width="2"/>
    <circle cx="-100" cy="-34" r="8" fill="#f43f5e"/>
    <text x="-100" y="-31" text-anchor="middle" font-family="monospace" font-size="8" fill="white" font-weight="bold">FI</text>
    <text x="10" y="-30" text-anchor="middle" font-family="monospace" font-size="10" fill="#f43f5e" font-weight="bold">2. ROOT CAUSE DEFECT</text>
    {render_card_text(c_lines, -6, "#fda4af")}
    <rect x="-70" y="24" width="140" height="16" rx="2" fill="#3b0d18"/>
    <text x="0" y="36" text-anchor="middle" font-family="monospace" font-size="8" fill="#fda4af">[MISSING CONTROL]</text>
  </g>

  <!-- Arrow 2 -> 3 -->
  <line x1="605" y1="140" x2="685" y2="140" stroke="#f43f5e" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#{uid}-arr-fail)"/>
  <text x="645" y="132" text-anchor="middle" font-family="monospace" font-size="8" fill="#f43f5e">CASCADES</text>

  <!-- Card 3: Impact -->
  <g transform="translate(820, 140)">
    <rect x="-125" y="-50" width="250" height="100" rx="4" fill="#380914" stroke="#f43f5e" stroke-width="2"/>
    <text x="0" y="-30" text-anchor="middle" font-family="monospace" font-size="10" fill="#f43f5e" font-weight="bold">3. IMPACT &amp; DEGRADATION</text>
    {render_card_text(i_lines, -6, "#fda4af")}
    <rect x="-75" y="24" width="150" height="16" rx="2" fill="#4c0519"/>
    <text x="0" y="36" text-anchor="middle" font-family="monospace" font-size="8" fill="#fda4af">[INVARIANT VIOLATION]</text>
  </g>
'''

    corrected_lane = f'''
  <!-- LOWER LANE: CORRECTED PATH -->
  <rect x="15" y="230" width="990" height="175" rx="6" fill="#061f15" stroke="#065f46" stroke-width="1.5"/>
  <rect x="25" y="238" width="230" height="20" rx="3" fill="#064e3b" stroke="#22c55e" stroke-width="1"/>
  <text x="140" y="252" text-anchor="middle" font-family="monospace" font-size="9" fill="#22c55e" font-weight="bold">CORRECTED PATH · ENFORCED CONTROL</text>

  <!-- Card 1: Same Trigger -->
  <g transform="translate(150, 326)">
    <rect x="-115" y="-50" width="230" height="100" rx="4" fill="#121526" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="0" y="-30" text-anchor="middle" font-family="monospace" font-size="10" fill="#94a3b8" font-weight="bold">1. SAME TRIGGER EVENT</text>
    {render_card_text(e_lines, -6, "#cbd5e1")}
    <rect x="-70" y="24" width="140" height="16" rx="2" fill="#1e293b"/>
    <text x="0" y="36" text-anchor="middle" font-family="monospace" font-size="8" fill="#94a3b8">[IDENTICAL INPUT]</text>
  </g>

  <!-- Arrow 1 -> 2 -->
  <line x1="270" y1="326" x2="350" y2="326" stroke="#22c55e" stroke-width="2.5" marker-end="url(#{uid}-arr-ok)"/>
  <text x="310" y="318" text-anchor="middle" font-family="monospace" font-size="8" fill="#22c55e">INTERCEPT</text>

  <!-- Invariant boundary enclosing Card 2 and 3 -->
  <rect x="345" y="244" width="645" height="150" rx="6" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="668" y="256" text-anchor="middle" font-family="monospace" font-size="9" fill="#f59e0b" font-weight="bold">INVARIANT VERIFICATION BOUNDARY: GUARDRAIL ENFORCED</text>

  <!-- Card 2: Enforced Control -->
  <g transform="translate(480, 326)">
    <rect x="-120" y="-50" width="240" height="100" rx="4" fill="#064e3b" stroke="#22c55e" stroke-width="2"/>
    <text x="0" y="-30" text-anchor="middle" font-family="monospace" font-size="10" fill="#22c55e" font-weight="bold">2. DEFENSIVE CONTROL</text>
    {render_card_text(ctrl_lines, -6, "#6ee7b7")}
    <rect x="-75" y="24" width="150" height="16" rx="2" fill="#022c22"/>
    <text x="0" y="36" text-anchor="middle" font-family="monospace" font-size="8" fill="#6ee7b7">[ACTIVE GUARDRAIL]</text>
  </g>

  <!-- Arrow 2 -> 3 -->
  <line x1="605" y1="326" x2="685" y2="326" stroke="#22c55e" stroke-width="2.5" marker-end="url(#{uid}-arr-ok)"/>
  <text x="645" y="318" text-anchor="middle" font-family="monospace" font-size="8" fill="#22c55e">PRESERVES</text>

  <!-- Card 3: Outcome -->
  <g transform="translate(820, 326)">
    <rect x="-125" y="-50" width="250" height="100" rx="4" fill="#022c22" stroke="#22c55e" stroke-width="2"/>
    <text x="0" y="-30" text-anchor="middle" font-family="monospace" font-size="10" fill="#22c55e" font-weight="bold">3. VERIFIED OUTCOME</text>
    {render_card_text(out_lines, -6, "#6ee7b7")}
    <rect x="-75" y="24" width="150" height="16" rx="2" fill="#064e3b"/>
    <text x="0" y="36" text-anchor="middle" font-family="monospace" font-size="8" fill="#6ee7b7">[INVARIANT DEFENDED]</text>
  </g>
'''

    legend = f'''
  <!-- Legend Bar -->
  <rect x="15" y="414" width="990" height="32" rx="4" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
  <line x1="28" y1="430" x2="60" y2="430" stroke="#22c55e" stroke-width="2.5"/>
  <text x="66" y="434" font-family="monospace" font-size="10" fill="#22c55e">CORRECTED PATH</text>
  <line x1="200" y1="430" x2="232" y2="430" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4,3"/>
  <text x="238" y="434" font-family="monospace" font-size="10" fill="#f43f5e">FAILED PATH</text>
  <rect x="360" y="424" width="12" height="12" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="380" y="434" font-family="monospace" font-size="10" fill="#f59e0b">VERIFICATION BOUNDARY</text>
  <circle cx="560" cy="430" r="5" fill="#f43f5e"/>
  <text x="572" y="434" font-family="monospace" font-size="10" fill="#f43f5e">FI = Fault Injection Point</text>
'''

    return f'''<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg role="img" aria-labelledby="{uid}-title {uid}-desc" viewBox="0 0 1020 455" width="100%" height="auto" style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="{uid}-title">{escape(title)}</title>
<desc id="{uid}-desc">{escape(desc)}</desc>
<defs>
  <marker id="{uid}-arr-ok" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#22c55e"/></marker>
  <marker id="{uid}-arr-fail" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/></marker>
  <marker id="{uid}-arr-warn" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#f59e0b"/></marker>
</defs>
<!-- Header Bar -->
<rect x="15" y="10" width="990" height="26" rx="4" fill="#1e293b" opacity="0.8"/>
<text x="25" y="27" font-family="monospace" font-size="11" fill="#cbd5e1" font-weight="bold">INCIDENT COMPARISON: {escape(topic.get('title', 'Topic'))}</text>
{failed_lane}
{corrected_lane}
{legend}
</svg></div>
<figcaption><strong>Supplied facts:</strong> {escape(facts)}<br><strong>Architectural inference:</strong> {escape(inference)}<br><strong>Expected post-fix behavior:</strong> {escape(expected)}</figcaption>
</figure>'''


def render_topology_svg(day: int, arch_diagram: dict) -> str:
    """Render a full multi-tier infrastructure topology SVG (matching Day 65/67 standards)."""
    uid = f"d{day:03d}-top"
    title = arch_diagram.get("title", f"Day {day} System Operations & Infrastructure Topology")
    desc = arch_diagram.get("desc", "Multi-tier operational architecture showing infrastructure layers, request traces, and security boundaries.")
    caption = arch_diagram.get("caption", "Architecture topology, request traces, and boundary verification.")
    vb_w = arch_diagram.get("width", 1100)
    vb_h = arch_diagram.get("height", 640)

    layers_html = []
    for l in arch_diagram.get("layers", []):
        ly = l.get("y", 10)
        lh = l.get("h", 88)
        lw = l.get("w", vb_w - 20)
        lx = l.get("x", 10)
        fill = l.get("fill", "#1e3a5f")
        op = l.get("opacity", 0.5)
        title_color = l.get("title_color", "#93c5fd")
        layers_html.append(f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="6" fill="{fill}" opacity="{op}"/>')
        layers_html.append(f'<text x="{lx + 14}" y="{ly + 28}" font-family="monospace" font-size="13" fill="{title_color}" font-weight="bold">{escape(l.get("name", ""))}</text>')
        if l.get("desc"):
            layers_html.append(f'<text x="{lx + 14}" y="{ly + 46}" font-family="monospace" font-size="11" fill="#64748b">{escape(l["desc"])}</text>')

    comps_html = []
    for c in arch_diagram.get("components", []):
        cx, cy, cw, ch = c["x"], c["y"], c["w"], c["h"]
        fill = c.get("fill", "#1e293b")
        stroke = c.get("stroke", "#38bdf8")
        sw = c.get("stroke_width", 1.5)
        sd = f' stroke-dasharray="{c["dash"]}"' if c.get("dash") else ""
        text_color = c.get("text_color", stroke)
        comps_html.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{sd}/>')
        lines = wrap_svg(c.get("name", ""), limit=28, max_lines=2)
        ty = cy + (22 if len(lines) == 1 else 17)
        for j, line in enumerate(lines):
            comps_html.append(f'<text x="{cx + cw // 2}" y="{ty + j * 15}" text-anchor="middle" font-family="monospace" font-size="11" fill="{text_color}" font-weight="bold">{escape(line)}</text>')
        if c.get("detail"):
            d_lines = wrap_svg(c["detail"], limit=32, max_lines=2)
            d_y = cy + ch - (12 if len(d_lines) == 1 else 18)
            for j, d_line in enumerate(d_lines):
                comps_html.append(f'<text x="{cx + cw // 2}" y="{d_y + j * 13}" text-anchor="middle" font-family="monospace" font-size="10" fill="#94a3b8">{escape(d_line)}</text>')

    bounds_html = []
    for b in arch_diagram.get("boundaries", []):
        bx, by, bw, bh = b["x"], b["y"], b["w"], b["h"]
        b_color = b.get("color", "#f59e0b")
        bounds_html.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="4" fill="none" stroke="{b_color}" stroke-width="2" stroke-dasharray="5,3"/>')
        bounds_html.append(f'<text x="{bx + bw // 2}" y="{by + bh + 14}" text-anchor="middle" font-family="monospace" font-size="10" fill="{b_color}" font-weight="bold">{escape(b.get("label", "BOUNDARY"))}</text>')

    flows_html = []
    for f in arch_diagram.get("flows", []):
        x1, y1, x2, y2 = f["x1"], f["y1"], f["x2"], f["y2"]
        flow_type = f.get("type", "ok")
        if flow_type == "ok":
            color, marker = "#22c55e", f"{uid}-arr-ok"
            sw = 2.5
            dash = ""
        elif flow_type == "fail":
            color, marker = "#f43f5e", f"{uid}-arr-fail"
            sw = 2.0
            dash = ' stroke-dasharray="6,4"'
        elif flow_type == "warn":
            color, marker = "#f59e0b", f"{uid}-arr-warn"
            sw = 2.0
            dash = ' stroke-dasharray="4,3"'
        else:
            color, marker = "#38bdf8", f"{uid}-arr-blue"
            sw = 2.0
            dash = ""
        flows_html.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{dash} marker-end="url(#{marker})"/>')
        if f.get("label"):
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2 - 6
            flows_html.append(f'<text x="{mid_x}" y="{mid_y}" text-anchor="middle" font-family="monospace" font-size="9" fill="{color}">{escape(f["label"])}</text>')

    probes_html = []
    for p in arch_diagram.get("probes", []):
        px, py = p["cx"], p["cy"]
        p_color = p.get("color", "#f43f5e")
        probes_html.append(f'<circle cx="{px}" cy="{py}" r="12" fill="{p_color}" opacity="0.85"/>')
        probes_html.append(f'<text x="{px}" y="{py + 4}" text-anchor="middle" font-family="monospace" font-size="9" fill="white" font-weight="bold">{escape(p.get("badge", "FI"))}</text>')
        if p.get("label"):
            probes_html.append(f'<text x="{px + 18}" y="{py + 4}" font-family="monospace" font-size="10" fill="{p_color}">{escape(p["label"])}</text>')

    leg_y = vb_h - 44
    legend_html = [
        f'<rect x="10" y="{leg_y}" width="{vb_w - 20}" height="36" rx="4" fill="#0f172a" opacity="0.8" stroke="#1e293b"/>',
        f'<line x1="22" y1="{leg_y + 18}" x2="62" y2="{leg_y + 18}" stroke="#22c55e" stroke-width="2.5"/>',
        f'<text x="68" y="{leg_y + 22}" font-family="monospace" font-size="11" fill="#22c55e">CORRECTED / AUTHORIZED</text>',
        f'<line x1="250" y1="{leg_y + 18}" x2="290" y2="{leg_y + 18}" stroke="#f43f5e" stroke-width="2" stroke-dasharray="6,4"/>',
        f'<text x="296" y="{leg_y + 22}" font-family="monospace" font-size="11" fill="#f43f5e">FAILED / DENIED</text>',
        f'<rect x="460" y="{leg_y + 12}" width="12" height="12" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4,2"/>',
        f'<text x="480" y="{leg_y + 22}" font-family="monospace" font-size="11" fill="#f59e0b">VERIFY BOUNDARY</text>',
        f'<circle cx="670" cy="{leg_y + 18}" r="6" fill="#f43f5e"/>',
        f'<text x="682" y="{leg_y + 22}" font-family="monospace" font-size="11" fill="#f43f5e">FI = Fault Injection Point</text>',
    ]

    return f'''<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg role="img" aria-labelledby="{uid}-title {uid}-desc" viewBox="0 0 {vb_w} {vb_h}" width="100%" height="auto" style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="{uid}-title">{escape(title)}</title>
<desc id="{uid}-desc">{escape(desc)}</desc>
<defs>
  <marker id="{uid}-arr-ok" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#22c55e"/></marker>
  <marker id="{uid}-arr-fail" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/></marker>
  <marker id="{uid}-arr-warn" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#f59e0b"/></marker>
  <marker id="{uid}-arr-blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#38bdf8"/></marker>
</defs>
{"".join(layers_html)}
{"".join(bounds_html)}
{"".join(comps_html)}
{"".join(flows_html)}
{"".join(probes_html)}
{"".join(legend_html)}
</svg></div>
<figcaption>{escape(caption)}</figcaption>
</figure>'''


def render_sophisticated_flow_svg(day: int, arch_diagram: dict) -> str:
    """Render a multi-tier architectural flow SVG with Day 67 standards."""
    uid = f"d{day:03d}-arch-flow"
    title = arch_diagram.get("title", f"Day {day} Enterprise Architecture Flow")
    desc = arch_diagram.get("desc", "Multi-tier architecture and control evaluation flow.")
    caption = arch_diagram.get("caption", "Architecture decision flow, policy enforcement, and boundary verification.")

    nodes = arch_diagram.get("nodes", [
        ("1. Ingress & Identity", "Workload Authentication"),
        ("2. Security & Policy Gate", "CEL Condition & Claims"),
        ("3. Runtime & Control", "Impersonation & Execution"),
        ("4. Execution & Audit", "Resource State & Logging"),
    ])

    tiers_meta = [
        {"pill": "TIER 1 · INGRESS / VECTOR", "stroke": "#38bdf8", "fill": "#0c2033", "spec": ["Protocol: HTTPS / TLS 1.3", "Identity: Authenticated Caller", "Ingress: External Gateway"], "badge": "[REQUEST VECTOR]"},
        {"pill": "TIER 2 · SECURITY & POLICY", "stroke": "#f59e0b", "fill": "#241808", "spec": ["Validation: Cryptographic Check", "Policy: CEL Attribute Rule", "Intercept: Fail-Closed Gate"], "badge": "[AUTHORIZATION GATE]"},
        {"pill": "TIER 3 · CONTROL & RUNTIME", "stroke": "#c084fc", "fill": "#1e0d2c", "spec": ["Service: GCP Managed Runtime", "Token: Short-Lived Credential", "Boundary: VPC / PSC Network"], "badge": "[CREDENTIAL MINT]"},
        {"pill": "TIER 4 · EXECUTION & AUDIT", "stroke": "#22c55e", "fill": "#062316", "spec": ["Target: Workload Data Plane", "Audit: Structured Cloud Log", "Invariant: Zero Key Leakage"], "badge": "[AUDIT TRACEABLE]"}
    ]

    cards_html = []
    arrows_html = []

    for i in range(min(4, len(nodes))):
        node_title, node_sub = nodes[i]
        meta = tiers_meta[i]
        x = 22 + i * 270
        y = 65
        w = 246
        h = 275

        sub_lines = wrap_svg(node_sub, limit=26, max_lines=2)
        sub_svg = "".join(f'<text x="{x + w // 2}" y="{y + 64 + j * 14}" text-anchor="middle" font-family="monospace" font-size="11" fill="#94a3b8">{escape(line)}</text>' for j, line in enumerate(sub_lines))

        spec_box_y = y + 105
        spec_lines_svg = "".join(f'<text x="{x + 14}" y="{spec_box_y + 22 + j * 16}" font-family="monospace" font-size="10" fill="#cbd5e1">• {escape(s)}</text>' for j, s in enumerate(meta["spec"]))

        cards_html.append(f'''
  <!-- Card {i+1} -->
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{meta["fill"]}" stroke="{meta["stroke"]}" stroke-width="1.5"/>
  <rect x="{x + 12}" y="{y + 12}" width="{w - 24}" height="20" rx="3" fill="#121526" stroke="{meta["stroke"]}" stroke-width="1"/>
  <text x="{x + w // 2}" y="{y + 26}" text-anchor="middle" font-family="monospace" font-size="9" fill="{meta["stroke"]}" font-weight="bold">{meta["pill"]}</text>
  <text x="{x + w // 2}" y="{y + 48}" text-anchor="middle" font-family="monospace" font-size="12" fill="#f8fafc" font-weight="bold">{escape(node_title)}</text>
  {sub_svg}
  <rect x="{x + 10}" y="{spec_box_y}" width="{w - 20}" height="76" rx="4" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
  <text x="{x + 14}" y="{spec_box_y + 12}" font-family="monospace" font-size="8" fill="{meta["stroke"]}">RUNTIME SPECIFICATIONS:</text>
  {spec_lines_svg}
  <rect x="{x + 14}" y="{y + h - 34}" width="{w - 28}" height="22" rx="3" fill="#121526" stroke="{meta["stroke"]}" stroke-width="1"/>
  <text x="{x + w // 2}" y="{y + h - 20}" text-anchor="middle" font-family="monospace" font-size="10" fill="{meta["stroke"]}" font-weight="bold">{meta["badge"]}</text>
''')
        if i < 3:
            ax1 = x + w
            ax2 = ax1 + 24
            labels = ["ASSERTION", "EXCHANGE", "AUTHORIZE"]
            arrows_html.append(f'''
  <line x1="{ax1}" y1="{y + 130}" x2="{ax2}" y2="{y + 130}" stroke="#22c55e" stroke-width="2.5" marker-end="url(#{uid}-arr-ok)"/>
  <text x="{(ax1 + ax2) // 2}" y="{y + 122}" text-anchor="middle" font-family="monospace" font-size="8" fill="#22c55e">{labels[i]}</text>
''')

    denial_html = f'''
  <!-- Denial intercept branch -->
  <path d="M415 340 V375 H415" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#{uid}-arr-fail)"/>
  <rect x="292" y="380" width="246" height="48" rx="4" fill="#2a0a10" stroke="#f43f5e" stroke-width="1.5"/>
  <text x="415" y="400" text-anchor="middle" font-family="monospace" font-size="10" fill="#f43f5e" font-weight="bold">POLICY INTERCEPT: MISMATCH / DENIAL</text>
  <text x="415" y="416" text-anchor="middle" font-family="monospace" font-size="9" fill="#fda4af">HTTP 403 Forbidden · Zero Token Issued</text>
'''

    boundary_html = f'''
  <rect x="282" y="52" width="796" height="388" rx="8" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="6,4"/>
  <text x="680" y="432" text-anchor="middle" font-family="monospace" font-size="10" fill="#f59e0b" font-weight="bold">INVARIANT ENFORCEMENT &amp; VERIFICATION BOUNDARY</text>
'''

    legend_html = f'''
  <!-- Legend Bar -->
  <rect x="22" y="448" width="1056" height="32" rx="4" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
  <line x1="36" y1="464" x2="68" y2="464" stroke="#22c55e" stroke-width="2.5"/>
  <text x="74" y="468" font-family="monospace" font-size="10" fill="#22c55e">FORWARD AUTHORIZED FLOW</text>
  <line x1="260" y1="464" x2="292" y2="464" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4,3"/>
  <text x="298" y="468" font-family="monospace" font-size="10" fill="#f43f5e">INTERCEPTED / DENIED PATH</text>
  <rect x="495" y="458" width="12" height="12" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="515" y="468" font-family="monospace" font-size="10" fill="#f59e0b">VERIFICATION BOUNDARY</text>
  <circle cx="700" cy="464" r="5" fill="#38bdf8"/>
  <text x="712" y="468" font-family="monospace" font-size="10" fill="#38bdf8">INGRESS VECTOR</text>
'''

    return f'''<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto"><svg role="img" aria-labelledby="{uid}-title {uid}-desc" viewBox="0 0 1100 490" width="100%" height="auto" style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;display:block;">
<title id="{uid}-title">{escape(title)}</title>
<desc id="{uid}-desc">{escape(desc)}</desc>
<defs>
  <marker id="{uid}-arr-ok" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#22c55e"/></marker>
  <marker id="{uid}-arr-fail" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#f43f5e"/></marker>
  <marker id="{uid}-arr-warn" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#f59e0b"/></marker>
  <marker id="{uid}-arr-blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#38bdf8"/></marker>
</defs>
<!-- Header Banner -->
<rect x="22" y="12" width="1056" height="34" rx="4" fill="#1e293b" opacity="0.8"/>
<text x="36" y="34" font-family="monospace" font-size="12" fill="#38bdf8" font-weight="bold">DAY {day:03d} SYSTEM ARCHITECTURE &amp; CONTROL FLOW</text>
<text x="1066" y="34" text-anchor="end" font-family="monospace" font-size="11" fill="#94a3b8">TIERED PIPELINE · AUTOMATED VERIFICATION</text>
{boundary_html}
{"".join(cards_html)}
{"".join(arrows_html)}
{denial_html}
{legend_html}
</svg></div>
<figcaption>{escape(caption)}</figcaption>
</figure>'''


def render_architecture_svg(day: int, arch_diagram: dict, data: dict = None) -> str:
    """Generate responsive architecture diagram matching Day 67 standards."""
    if isinstance(arch_diagram, str) and arch_diagram.strip():
        raw = arch_diagram.strip()
        if raw.startswith("<figure"):
            return raw
        caption = data.get("exit_summary", "Architecture decision flow and boundary verification.") if data else "Architecture decision flow and boundary verification."
        return f'<figure class="diagram-container"><div style="max-width:100%;overflow-x:auto">{raw}</div><figcaption>{escape(caption)}</figcaption></figure>'

    if not isinstance(arch_diagram, dict) or not arch_diagram:
        return ""

    if arch_diagram.get("type") == "topology":
        return render_topology_svg(day, arch_diagram)

    return render_sophisticated_flow_svg(day, arch_diagram)


def render_code_blocks(text: str) -> str:
    """Ensure all markdown code blocks and inline code follow validate.py rules."""
    return markdown.markdown(text, extensions=["tables", "fenced_code"])


def compile_day_page(day_num: int, data: dict) -> None:
    """Compile the day page override from data specification."""
    override_file = SITE_CONTENT / f"day-{day_num:03d}-page.html"
    source_day_file = SITE_DAYS / f"day-{day_num:03d}.html"

    if not override_file.exists():
        if not source_day_file.exists():
            raise FileNotFoundError(f"Source file {source_day_file} missing.")
        override_file.write_text(source_day_file.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Initialized Day {day_num} override from {source_day_file.name}")

    soup = BeautifulSoup(override_file.read_text(encoding="utf-8"), "html.parser")

    def put_section(section_id: str, inner_markup: str) -> None:
        section = soup.select_one(f"#{section_id}")
        if not section:
            raise ValueError(f"Section #{section_id} not found in page shell.")
        heading = section.find("h2", recursive=False)
        for child in list(section.contents):
            if child is not heading:
                child.extract()
        section.append(BeautifulSoup(inner_markup, "html.parser"))

    topics = data.get("topics", [])

    # ─── PART 1: Topics of the Day ──────────────────────────────────────
    part1_intro = data.get("part1_intro", f"Day {day_num} examines core architecture principles and trade-offs.")
    exit_summary = data.get("exit_summary", "Completed exercises and verified architecture decisions.")

    p1_html = [
        f'<p class="intro">{escape(part1_intro)}</p>',
        f'<p class="callout"><strong>Exit evidence:</strong> {escape(exit_summary)}</p>'
    ]
    for i, t in enumerate(topics, 1):
        key = t["key"]
        p1_html.append(
            f'<article id="{key}-overview" class="topic-card overview">'
            f'<h3>{i}. {escape(t["title"])}</h3>'
            f'<p>{escape(t["overview"])}</p>'
            f'<p class="problem-preview"><strong>Problem preview:</strong> {escape(t["preview"])}</p>'
            f'<p><a href="#{key}-technical">Technical discussion →</a> <a href="#{key}-problem">Real-world problem →</a> <a href="#{key}-lab">Step-by-step lab →</a></p>'
            f'</article>'
        )
    put_section("part-1", "".join(p1_html))

    # ─── PART 2: Technical Discussion ───────────────────────────────────
    part2_intro = data.get("part2_intro", "Trace technical control and data boundaries, observable signals, and trade-offs.")
    arch_diagram = data.get("arch_diagram", {})
    arch_svg_html = data.get("arch_svg_html", data.get("arch_diagram_html", ""))
    if not arch_svg_html and arch_diagram:
        arch_svg_html = render_architecture_svg(day_num, arch_diagram, data)
    table_html = data.get("arch_table_html", "")

    p2_html = [
        f'<p class="intro">{escape(part2_intro)}</p>',
        table_html,
        arch_svg_html
    ]
    for i, t in enumerate(topics, 1):
        key = t["key"]
        questions = "".join(f"<li>{escape(q)}</li>" for q in t.get("questions", []))
        q_section = f'<h4>Architectural evaluation questions</h4><ul>{questions}</ul>' if questions else ""
        ref_link = t.get("reference", "")
        ref_label = t.get("reference_label", "Google Cloud Documentation")
        ref_html = f'<p><strong>Further study:</strong> <a href="{escape(ref_link)}" target="_blank" rel="noopener">{escape(ref_label)}</a>.</p>' if ref_link else ""
        tech_body = render_code_blocks(t.get("technical", ""))

        p2_html.append(
            f'<article id="{key}-technical" class="topic-card technical">'
            f'<h3>{i}. {escape(t["title"])}: technical mechanics</h3>'
            f'{tech_body}'
            f'{q_section}'
            f'{ref_html}'
            f'</article>'
        )
    put_section("part-2", "".join(p2_html))

    # ─── PART 3: Problem and Solution ───────────────────────────────────
    part3_intro = data.get("part3_intro", "Illustrative real-world scenarios and diagnostic failure investigations.")
    p3_html = [f'<p class="intro">{escape(part3_intro)}</p>']

    for i, t in enumerate(topics, 1):
        key = t["key"]
        scenario = t.get("scenario", {})
        diag_steps = "".join(f"<li>{escape(s)}</li>" for s in scenario.get("diagnostic_steps", []))
        diag_html = f'<p><strong>Diagnostic sequence:</strong></p><ol>{diag_steps}</ol>' if diag_steps else ""

        fix_steps = "".join(f"<li>{escape(s)}</li>" for s in scenario.get("remediation_steps", []))
        if fix_steps:
            fix_html = f'<p><strong>Defensible remediation:</strong></p><ol>{fix_steps}</ol>'
        else:
            fix_text = scenario.get("fix", "")
            if "\n" in fix_text or "```" in fix_text:
                fix_html = render_code_blocks(f"**Defensible remediation:** {fix_text}")
            else:
                fix_html = f'<p><strong>Defensible remediation:</strong> {escape(fix_text)}</p>' if fix_text else ""

        inc_svg = render_incident_svg(day_num, i, t)

        scenario_text = scenario.get("scenario", scenario.get("symptom", ""))
        impact_text = scenario.get("impact", "")
        impact_p = f'<p><strong>Failure symptoms and impact:</strong> {escape(impact_text)}</p>' if impact_text else ""
        constraints_text = scenario.get("constraints", "")
        constraints_p = f'<p><strong>Constraints:</strong> {escape(constraints_text)}</p>' if constraints_text else ""

        evidence_text = scenario.get("evidence", "")
        if evidence_text:
            if evidence_text.startswith("<"):
                evidence_html = evidence_text
            else:
                if not evidence_text.lower().startswith("**evidence:**") and not evidence_text.lower().startswith("evidence:"):
                    evidence_html = render_code_blocks(f"**Evidence:** {evidence_text}")
                else:
                    evidence_html = render_code_blocks(evidence_text)
        else:
            evidence_html = ""

        root_text = scenario.get("root", "")
        if "\n" in root_text or "```" in root_text:
            root_html = render_code_blocks(f"**Root cause:** {root_text}")
        else:
            root_html = f'<p><strong>Root cause:</strong> {escape(root_text)}</p>' if root_text else ""

        verify_text = scenario.get("verify", "")
        if "\n" in verify_text or "```" in verify_text:
            verify_html = render_code_blocks(f"**Verification:** {verify_text}")
        else:
            verify_html = f'<p><strong>Verification:</strong> {escape(verify_text)}</p>' if verify_text else ""

        residual_text = scenario.get("residual", "")
        if "\n" in residual_text or "```" in residual_text:
            residual_html = render_code_blocks(f"**Residual risk:** {residual_text}")
        else:
            residual_html = f'<p><strong>Residual risk:</strong> {escape(residual_text)}</p>' if residual_text else ""

        p3_html.append(
            f'<article id="{key}-problem" class="topic-card problem">'
            f'<h3>{i}. {escape(t["title"])} · field case</h3>'
            f'<p><strong>Enterprise scenario:</strong> {escape(scenario_text)}</p>'
            f'{impact_p}'
            f'{constraints_p}'
            f'{evidence_html}'
            f'{root_html}'
            f'{diag_html}'
            f'{fix_html}'
            f'{verify_html}'
            f'{residual_html}'
            f'{inc_svg}'
            f'</article>'
        )
    put_section("part-3", "".join(p3_html))

    # ─── PART 4: Step-by-Step Labs ──────────────────────────────────────
    part4_intro = data.get("part4_intro", "Hands-on exercises and tabletop verification procedures.")
    p4_html = [f'<p class="intro">{escape(part4_intro)}</p>']

    for i, t in enumerate(topics, 1):
        key = t["key"]
        lab = t.get("lab", {})
        steps_html = []
        for step in lab.get("steps", []):
            rendered_step = render_code_blocks(step)
            # Remove wrapping <p> if single paragraph inside <li>
            rendered_step = re.sub(r"^<p>(.*?)</p>$", r"\1", rendered_step, flags=re.S)
            steps_html.append(f'<li>{rendered_step}</li>')

        # Format Callouts in Day 40-50 high-contrast container style
        accept_content = lab.get("accept", "")
        verification_content = lab.get("verification", "")
        trouble_content = lab.get("trouble", "Inspect system logs and check configuration syntax.")
        cleanup_content = lab.get("cleanup", "No chargeable resources created.")
        artifact_file = lab.get("file", f"day-{day_num:03d}-{key}.md")

        callouts_html = []
        if verification_content or accept_content:
            acceptance_body = accept_content or verification_content
            if verification_content and accept_content:
                acceptance_body = f"{verification_content}\n\n**Artifact acceptance:** {accept_content} (File: `{artifact_file}`)."
            elif artifact_file:
                acceptance_body = f"{acceptance_body}\n\n(Target File: `{artifact_file}`)."
            callouts_html.append(
                f'<div class="callout success"><strong>Expected result / acceptance</strong>{render_code_blocks(acceptance_body)}</div>'
            )
        if trouble_content:
            callouts_html.append(
                f'<div class="callout caution"><strong>Troubleshooting</strong>{render_code_blocks(trouble_content)}</div>'
            )
        if cleanup_content:
            callouts_html.append(
                f'<div class="callout"><strong>Cleanup and cost</strong>{render_code_blocks(cleanup_content)}</div>'
            )

        p4_html.append(
            f'<article id="{key}-lab" class="topic-card lab">'
            f'<h3>Exercise {i}: {escape(lab.get("name", t["title"]))}</h3>'
            f'<p><strong>Goal:</strong> {escape(lab.get("goal", ""))}</p>'
            f'<p><strong>Expected result:</strong> {escape(lab.get("expected", ""))}</p>'
            f'<p><strong>Mode:</strong> {escape(lab.get("mode", "local exercise"))} · <strong>Prerequisite:</strong> {escape(lab.get("prereq", "Prior day artifacts"))}</p>'
            f'<p><strong>Preflight:</strong> {escape(lab.get("preflight", "Review environment and open editor."))}</p>'
            f'<h4>Exact execution</h4>'
            f'<ol>{"".join(steps_html)}</ol>'
            f'{"".join(callouts_html)}'
            f'<label class="check"><input type="checkbox" data-progress="lab-{day_num}-{key}"> I completed and checked this topic exercise</label>'
            f'</article>'
        )
    put_section("part-4", "".join(p4_html))

    # ─── COMPLETION SUMMARY ─────────────────────────────────────────────
    completion = soup.select_one(".completion")
    if completion:
        for old in completion.select(".exit-summary"):
            old.decompose()
        completion.append(BeautifulSoup(f'<p class="exit-summary">Exit artifact: {escape(exit_summary)}</p>', "html.parser"))

    override_file.write_text(str(soup), encoding="utf-8")
    print(f"Updated override: {override_file}")


def build_and_validate(day_num: int) -> None:
    """Build day page and run site-wide validator."""
    print(f"\nBuilding Day {day_num}...")
    res = subprocess.run(
        [sys.executable, str(SCRIPTS / "build.py"), "--day", str(day_num)],
        cwd=str(ROOT),
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        print("Build failed:\n", res.stderr or res.stdout)
        sys.exit(res.returncode)
    print(res.stdout.strip())

    print("\nRunning validator...")
    res_val = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True
    )
    if res_val.returncode != 0:
        print("Validation errors:\n", res_val.stderr or res_val.stdout)
        sys.exit(res_val.returncode)
    print("Validation passed successfully! 0 errors.")


def load_day_module(path: Path) -> dict:
    """Dynamically load day data module."""
    spec = importlib.util.spec_from_file_location("day_data_module", path)
    if not spec or not spec.loader:
        raise ImportError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "DAY_DATA"):
        return getattr(module, "DAY_DATA")
    if hasattr(module, "DATA"):
        return getattr(module, "DATA")
    # Alternatively collect variables
    return {
        "day": getattr(module, "DAY", None),
        "topics": getattr(module, "TOPICS", []),
        "part1_intro": getattr(module, "PART1_INTRO", ""),
        "part2_intro": getattr(module, "PART2_INTRO", ""),
        "part3_intro": getattr(module, "PART3_INTRO", ""),
        "part4_intro": getattr(module, "PART4_INTRO", ""),
        "arch_diagram": getattr(module, "ARCH_DIAGRAM", {}),
        "arch_svg_html": getattr(module, "ARCH_SVG_HTML", getattr(module, "ARCH_DIAGRAM_HTML", "")),
        "arch_table_html": getattr(module, "ARCH_TABLE_HTML", ""),
        "exit_summary": getattr(module, "EXIT_SUMMARY", ""),
    }


def parse_range(range_str: str) -> list[int]:
    """Parse range string like '1-93', '1 - 93', '83..92', or '1,2,5'."""
    clean = range_str.replace(" ", "").replace("..", "-")
    days = []
    for part in clean.split(","):
        if "-" in part:
            start, end = part.split("-", 1)
            days.extend(range(int(start), int(end) + 1))
        else:
            days.append(int(part))
    return sorted(list(set(days)))


def process_single_day(day_num: int, data_path_override: str = "") -> None:
    data_path = Path(data_path_override) if data_path_override else ROOT / "scratch" / f"day_data_{day_num:03d}.py"
    if data_path.exists():
        print(f"Loading data from {data_path}...")
        data = load_day_module(data_path)
        compile_day_page(day_num, data)
        res = subprocess.run(
            [sys.executable, str(SCRIPTS / "build.py"), "--day", str(day_num)],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        if res.returncode != 0:
            sys.exit(f"Build failed for Day {day_num}:\n{res.stderr or res.stdout}")
        print(f"Built Day {day_num}: {SITE_DAYS / f'day-{day_num:03d}.html'}")
    else:
        override_file = ROOT / "content" / f"day-{day_num:03d}-page.html"
        if not override_file.exists():
            print(f"Skipping Day {day_num}: neither {data_path} nor {override_file} exists.")
            return
        soup = BeautifulSoup(override_file.read_text(encoding="utf-8"), "html.parser")
        labs = soup.select("article.lab")
        modified = False
        for lab in labs:
            for p in lab.select("p"):
                p_text = p.get_text()
                if "Skill Level:" in p_text or "Difficulty:" in p_text:
                    p.decompose()
                    modified = True
        if modified:
            override_file.write_text(str(soup), encoding="utf-8")
            print(f"Removed exercise difficulty labels in {override_file.name}")
        res = subprocess.run(
            [sys.executable, str(SCRIPTS / "build.py"), "--day", str(day_num)],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        if res.returncode != 0:
            sys.exit(f"Build failed for Day {day_num}:\n{res.stderr or res.stdout}")
        print(f"Built Day {day_num}: {SITE_DAYS / f'day-{day_num:03d}.html'}")


def main():
    parser = argparse.ArgumentParser(description="Deterministic authoring engine for 180-day GCP curriculum.")
    parser.add_argument("--day", type=int, default=None, help="Day number (1-180)")
    parser.add_argument("--range", type=str, default="", help="Range of days to author/update (e.g. '1-93' or '1 - 93')")
    parser.add_argument("--data", type=str, default="", help="Path to day data file (defaults to scratch/day_data_NNN.py)")
    args = parser.parse_args()

    if not args.day and not args.range:
        parser.error("Must specify either --day or --range.")

    if args.range:
        target_days = parse_range(args.range)
        print(f"Processing {len(target_days)} days in range {args.range}: {target_days[0]} to {target_days[-1]}...")
        for d in target_days:
            process_single_day(d)
        print("\nAll target days built. Running site-wide validator...")
        res_val = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        if res_val.returncode != 0:
            print("Validation errors:\n", res_val.stderr or res_val.stdout)
            sys.exit(res_val.returncode)
        print(res_val.stdout.strip())
        print("Validation passed successfully! 0 errors.")
    else:
        process_single_day(args.day, args.data)
        print("\nRunning validator...")
        res_val = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        if res_val.returncode != 0:
            print("Validation errors:\n", res_val.stderr or res_val.stdout)
            sys.exit(res_val.returncode)
        print(res_val.stdout.strip())
        print("Validation passed successfully! 0 errors.")


if __name__ == "__main__":
    main()
