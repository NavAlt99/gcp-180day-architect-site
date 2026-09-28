import sys
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path("/home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site")
CONTENT_DAY58 = ROOT / "content" / "day-058-page.html"

# Load the existing file to extract navigation header
soup_orig = BeautifulSoup(CONTENT_DAY58.read_text(encoding="utf-8"), "html.parser")
header_html = str(soup_orig.header)

print(f"Extracted header ({len(header_html)} chars)")
