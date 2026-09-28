import re
from pathlib import Path

content = Path("days/day-057.html").read_text(encoding="utf-8")
header_match = re.search(r'(<!doctype html>.*?<header class="site-nav">.*?</header>)', content, re.DOTALL)
if not header_match:
    print("Header not matched!")
else:
    print("Header matched! Length:", len(header_match.group(1)))
