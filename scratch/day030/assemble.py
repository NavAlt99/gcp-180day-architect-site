#!/usr/bin/env python3
"""
Assembles content/day-030-page.html from modular scratch files and the original day shell.
"""

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    # Read the original days/day-030.html to get the exact header shell and footer
    orig = read_file("days/day-030.html")
    split_token = '<div class="crumb">'
    header_shell = orig[:orig.index(split_token)]
    
    footer_token = '</main><footer class="site-footer">'
    footer_shell = orig[orig.index(footer_token):]

    hero_and_toc = read_file("scratch/day030/hero_and_toc.html")
    part1 = read_file("scratch/day030/part1.html")
    part2 = read_file("scratch/day030/part2.html")
    fig1 = read_file("scratch/day030/fig1.html")
    fig2 = read_file("scratch/day030/fig2.html")
    part3 = read_file("scratch/day030/part3.html")
    fig3 = read_file("scratch/day030/fig3.html")
    fig4 = read_file("scratch/day030/fig4.html")
    part4 = read_file("scratch/day030/part4.html")
    evidence = read_file("scratch/day030/evidence_and_pager.html")

    # Replace figure placeholders
    part2_assembled = part2.replace("INJECT_FIG_30_1_HERE", fig1).replace("INJECT_FIG_30_2_HERE", fig2)
    part3_assembled = part3.replace("INJECT_FIG_30_3_HERE", fig3).replace("INJECT_FIG_30_4_HERE", fig4)

    full_page = "\n".join([
        header_shell,
        hero_and_toc,
        part1,
        part2_assembled,
        part3_assembled,
        part4,
        evidence,
        footer_shell
    ])

    target = "content/day-030-page.html"
    with open(target, "w", encoding="utf-8") as f:
        f.write(full_page)

    print(f"Successfully assembled {target} ({len(full_page)} bytes, {len(full_page.splitlines())} lines)")

if __name__ == "__main__":
    main()
