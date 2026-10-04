// Read-only expression for the supported browser's playwright.evaluate API.
// Run after the page's CSS/JS loads, at desktop and 390x844 in BOTH themes.
() => {
  const errors = [];
  const color = value => (value.match(/[\d.]+/g) || []).map(Number);
  const luminance = rgb => rgb.slice(0, 3).map(n => {
    const x = n / 255;
    return x <= .04045 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4;
  }).reduce((sum, x, i) => sum + x * [.2126, .7152, .0722][i], 0);
  const captions = [...document.querySelectorAll('.foundation-refresh figure figcaption')].map(el => {
    const style = getComputedStyle(el);
    const canvas = getComputedStyle(el.closest('figure')).backgroundColor;
    const a = luminance(color(style.color)), b = luminance(color(canvas));
    const contrast = (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
    if (contrast < 4.5) errors.push('Diagram caption contrast below 4.5:1');
    return {color: style.color, background: canvas, contrast};
  });
  if (document.documentElement.scrollWidth > innerWidth + 1) errors.push('Document horizontal overflow');
  const labels = [...document.querySelectorAll('.side-heading, .topic-card h4')].map(el => {
    const style = getComputedStyle(el), rgb = color(style.color);
    if (Number(style.fontWeight) < 700 || rgb[2] <= rgb[0]) errors.push('Teaching label is not blue and bold: ' + el.textContent);
    return {text: el.textContent, color: style.color, weight: style.fontWeight};
  });
  const diagrams = [...document.querySelectorAll('figure svg')].map(svg => {
    const rect = svg.getBoundingClientRect(), wrapper = svg.parentElement;
    const clipped = [...svg.querySelectorAll('text')].filter(el => {
      const t = el.getBoundingClientRect();
      return t.left < rect.left - 1 || t.right > rect.right + 1 || t.top < rect.top - 1 || t.bottom > rect.bottom + 1;
    }).map(el => el.textContent);
    if (clipped.length) errors.push('SVG labels outside canvas: ' + clipped.join('; '));
    if (rect.width > wrapper.clientWidth + 1 && !['auto', 'scroll'].includes(getComputedStyle(wrapper).overflowX)) errors.push('Wide SVG lacks horizontal scroll wrapper');
    return {title: svg.querySelector('title')?.textContent, clipped, wrapperWidth: wrapper.clientWidth, scrollWidth: wrapper.scrollWidth, scrollLeft: wrapper.scrollLeft};
  });
  const blocks = document.querySelectorAll('pre > code').length;
  const copies = document.querySelectorAll('.copy-code').length;
  if (blocks !== copies) errors.push('Code/copy-button count mismatch');
  return {theme: document.documentElement.dataset.theme, viewport: [innerWidth, innerHeight], errors, labels, captions, diagrams, codeBlocks: blocks, copyButtons: copies,
    limits: 'DOM checks do not detect every node overlap, gradient contrast, arrow ambiguity, or technical error. Visual and source review are still required.'};
}
