# Generator for Day 58 Page
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path("/home/naveen/Documents/GCP/RoadMap/gcp-180day-architect-site")
ORIGINAL = ROOT / "content" / "day-058-page.html"

soup = BeautifulSoup(ORIGINAL.read_text(encoding="utf-8"), "html.parser")
header_html = str(soup.header)

print("Writing generator...")
