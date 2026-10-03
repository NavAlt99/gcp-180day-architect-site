#!/usr/bin/env python3
"""Check one rendered day's Further study targets; relevance requires human review."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

SITE = Path(__file__).resolve().parents[1]
MAX_BYTES = 8 * 1024 * 1024


def study_links(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    found = {}
    for label in soup.find_all(["strong", "b", "h2", "h3", "h4", "h5"]):
        if not re.match(r"^further\s+study\b", label.get_text(" ", strip=True), re.I):
            continue
        if label.name.startswith("h"):
            nodes = []
            for sibling in label.next_siblings:
                if getattr(sibling, "name", None) in ("h2", "h3", "h4", "h5"):
                    break
                if hasattr(sibling, "select"):
                    nodes.append(sibling)
        else:
            nodes = [label.find_parent(["p", "li", "section", "article", "div"]) or label.parent]
        for node in nodes:
            for anchor in node.select("a[href]"):
                href = anchor["href"].strip()
                found[href] = {"url": href, "label": anchor.get_text(" ", strip=True)}
    return list(found.values())


def fetch_url(url: str, timeout: float) -> tuple[str, str, bytes]:
    request = Request(url, headers={"User-Agent": "GCP-curriculum-study-link-check/1.0"})
    with urlopen(request, timeout=timeout) as response:
        if not 200 <= response.status < 300:
            raise ValueError(f"HTTP {response.status}")
        content = response.read(MAX_BYTES + 1)
        if len(content) > MAX_BYTES:
            raise ValueError("Response exceeds 8 MiB; manual verification required")
        return response.geturl(), response.headers.get("Content-Type", ""), content


def check_link(url: str, page: Path, timeout: float = 15, fetch=fetch_url) -> dict:
    result = {"url": url, "status": "unverified", "relevance": "manual review required"}
    try:
        parsed = urlsplit(url)
        if parsed.scheme in ("http", "https"):
            final, content_type, body = fetch(urlunsplit(parsed._replace(fragment="")), timeout)
            result["final_url"] = final
            result["redirected"] = final != urlunsplit(parsed._replace(fragment=""))
            html = "html" in content_type.lower()
        elif not parsed.scheme and not parsed.netloc:
            target = (page.parent / unquote(parsed.path)).resolve() if parsed.path else page.resolve()
            if not target.is_file():
                raise ValueError(f"Missing local file: {target}")
            body = target.read_bytes()
            html = target.suffix.lower() in (".html", ".htm")
            result["final_url"] = str(target)
            result["redirected"] = False
        else:
            raise ValueError("Unsupported study-link scheme or protocol-relative URL")
        if html:
            soup = BeautifulSoup(body, "html.parser")
            result["title"] = soup.title.get_text(" ", strip=True) if soup.title else ""
        if parsed.fragment:
            fragment = unquote(parsed.fragment)
            if not html:
                raise ValueError("Non-HTML fragment requires manual verification")
            if not (soup.find(id=fragment) or soup.find("a", attrs={"name": fragment})):
                raise ValueError(f"Missing section fragment #{fragment}; dynamic anchors require manual verification")
        result["status"] = "pass"
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day", required=True, type=int, choices=range(1, 181), metavar="N")
    parser.add_argument("--report", type=Path, help="JSON evidence report path")
    parser.add_argument("--timeout", type=float, default=15, help="Per-request timeout in seconds")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    page = SITE / "days" / f"day-{args.day:03d}.html"
    links = study_links(page.read_text(encoding="utf-8"))
    results = []
    for link in links:
        result = check_link(link["url"], page, args.timeout)
        result["label"] = link["label"]
        results.append(result)
        print(f'{result["status"].upper()}: {link["url"]}', flush=True)
        if result.get("error"):
            print(f'  {result["error"]}', flush=True)
        elif result.get("redirected"):
            print(f'  Redirected to: {result["final_url"]} (review relevance)', flush=True)
    failures = sum(r["status"] != "pass" for r in results)
    report = {"day": args.day, "page": str(page), "checked_at": datetime.now(timezone.utc).isoformat(),
              "links": results, "unverified": failures,
              "limitation": "HTTP/local target and fragment checks only. Manually confirm title, section, and topic relevance.",
              "error": "No Further study links found" if not links else None}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Further study links: {len(results)}; unverified: {failures}. Topic relevance requires manual review.")
    return 1 if failures or not results else 0


if __name__ == "__main__":
    raise SystemExit(main())
