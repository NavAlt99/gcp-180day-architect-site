from bs4 import BeautifulSoup
from pathlib import Path

day_file = Path("days/day-058.html")
soup = BeautifulSoup(day_file.read_text(encoding="utf-8"), "html.parser")

print("Title:", soup.title.string)
print("Hero pill:", [p.text for p in soup.select(".hero .pill")])
print("Part count:", len(soup.select("section.part")))
print("Article count:", len(soup.select("article.topic-card")))
print("SVG count:", len(soup.select("svg")))
for i, svg in enumerate(soup.select("svg"), 1):
    title = svg.select_one("title")
    desc = svg.select_one("desc")
    t_text = title.text if title else "No title"
    d_text = desc.text[:50] if desc else "No desc"
    print(f"  SVG {i}: {t_text} (desc: {d_text}...)")

print("Table count:", len(soup.select("table")))
for i, tbl in enumerate(soup.select("table"), 1):
    cap = tbl.select_one("caption")
    c_text = cap.text if cap else "No caption"
    print(f"  Table {i}: {c_text}")

print("Pre blocks:", len(soup.select("pre")))
print("Completion section present:", bool(soup.select_one("section.completion")))
print("Exit artifact text:", [c.text for c in soup.select(".callout.success") if "Exit artifact" in c.text])
