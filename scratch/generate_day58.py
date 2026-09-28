import sys
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path("/home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site")
CONTENT_DAY58 = ROOT / "content" / "day-058-page.html"

# Extract header from original
soup_orig = BeautifulSoup(CONTENT_DAY58.read_text(encoding="utf-8"), "html.parser")
header_html = str(soup_orig.header)

print("Writing full generator script...")
