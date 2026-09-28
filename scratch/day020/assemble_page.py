import sys

def main():
    with open('content/day-020-page.html') as f:
        orig = f.read()

    idx_main = orig.find('<main')
    idx_close_main = orig.rfind('</main>')
    if idx_main == -1 or idx_close_main == -1:
        print("ERROR: could not find main tags in original", file=sys.stderr)
        sys.exit(1)

    outer_head = orig[:idx_main]
    outer_foot = orig[idx_close_main + len('</main>'):]

    with open('scratch/day020/hero_and_toc.html') as f:
        hero_toc = f.read()
    with open('scratch/day020/part1.html') as f:
        part1 = f.read()
    with open('scratch/day020/part2.html') as f:
        part2 = f.read()
    with open('scratch/day020/part3.html') as f:
        part3 = f.read()
    with open('scratch/day020/part4.html') as f:
        part4 = f.read()
    with open('scratch/day020/evidence_and_pager.html') as f:
        evidence_pager = f.read()

    body = '\n'.join([
        '  <main data-day="20" id="main">',
        hero_toc,
        part1,
        part2,
        part3,
        part4,
        evidence_pager,
        '  </main>'
    ])

    assembled = outer_head + body + outer_foot

    with open('content/day-020-page.html', 'w') as f:
        f.write(assembled)

    print(f"Successfully assembled content/day-020-page.html (size: {len(assembled)} bytes)")

if __name__ == '__main__':
    main()
