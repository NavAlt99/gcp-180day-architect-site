#!/usr/bin/env python3
"""Inject or update sprint navigation rails across all authored day pages in content/."""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Ensure scripts dir is on sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

import build


def update_page_content(path: Path, days: list[dict]) -> bool:
    m = re.search(r"day-(\d+)-page\.html", path.name)
    if not m:
        return False
    day_num = int(m.group(1))
    day_obj = next(d for d in days if d["number"] == day_num)

    content = path.read_text(encoding="utf-8")

    # If Day 1, ensure legacy inline style block is removed
    if day_num == 1 and "<style>" in content:
        content = re.sub(r"<style>.*?</style>\s*", "", content, flags=re.S)

    rail_html = build.render_sprint_rail(day_obj, days)

    existing_rail_regex = r'<nav\b[^>]*class="[^"]*(?:foundation-rail|sprint-rail)[^"]*"[\s\S]*?</nav>'
    if re.search(existing_rail_regex, content):
        new_content = re.sub(existing_rail_regex, rail_html, content, count=1)
    else:
        hero_regex = r'(<section\b[^>]*class="[^"]*hero[^"]*"[\s\S]*?</section>)'
        m_hero = re.search(hero_regex, content)
        if not m_hero:
            raise ValueError(f"Could not find hero section in {path.name}")
        new_content = content[: m_hero.end()] + "\n" + rail_html + content[m_hero.end() :]

    if new_content != content:
        path.write_text(new_content, encoding="utf-8")
        return True
    return False


def main() -> None:
    days = build.parse_days()
    content_dir = SCRIPTS_DIR.parent / "content"
    pages = sorted(content_dir.glob("day-*-page.html"))

    updated_count = 0
    for page in pages:
        if update_page_content(page, days):
            updated_count += 1

    print(f"Processed {len(pages)} day pages. Updated: {updated_count}")


if __name__ == "__main__":
    main()
