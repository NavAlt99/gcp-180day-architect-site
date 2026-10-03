# Reusable diagram icons

257 scalable, transparent-background SVG files:

- `gcp/core/`: 19 current official Google Cloud product icons. Prefer these when the service is available here.
- `gcp/legacy/`: 216 official legacy console icons, retained for broader service coverage. Legacy assets do not establish that a product is currently available or recommended.
- `generic/`: 22 project-authored network and concept icons with a consistent 64 × 64 viewBox. These are component illustrations, not vendor logos.

Open `index.html` for the visual catalog. `manifest.json` records stable IDs, labels, relative paths, collections, and source URLs; imported assets also record their archive paths and SHA-256 hashes. Official SVG artwork is preserved unchanged.

## Reuse in a day page

Paths below are relative to `days/day-NNN.html` or `content/day-NNN-page.html`:

```html
<img src="../assets/icons/gcp/core/compute-engine.svg"
     width="40" height="40" alt="Compute Engine">
```

Inside an architecture SVG, pair the image with a visible node label:

```html
<image href="../assets/icons/gcp/core/compute-engine.svg"
       x="24" y="24" width="40" height="40"
       preserveAspectRatio="xMidYMid meet" />
<text x="76" y="48">Compute Engine</text>
```

For a portable standalone diagram, embed the SVG file as a base64 `data:image/svg+xml` image URL. When inserting raw SVG markup inline, prefix all IDs and their references per diagram/node to avoid collisions. Keep official product colors and proportions. Generic icons use a fixed blue stroke; edit or style their inline markup if a different theme color is needed.

## Sources and rights

Official library: https://cloud.google.com/icons (retrieved 2026-10-02).

Archives:

- https://services.google.com/fh/files/misc/core-products-icons.zip
- https://services.google.com/fh/files/misc/google-cloud-legacy-icons.zip

Google product artwork and trademarks belong to Google. This project does not relicense those assets; follow Google's published usage guidance. The generic SVG artwork is authored for this project and may be reused and modified within it. No separate Google Cloud brand wordmark is included; `cloud-generic.svg` is a legacy component icon, not a brand-logo substitute.

## Regenerate

Download the two official archives, then run from the project root:

```sh
python3 scripts/create_icon_library.py \
  --core /tmp/gcp-core-icons.zip \
  --legacy /tmp/gcp-legacy-icons.zip
```

The generator also recreates the manifest and visual catalog. No remote image requests are needed to use this library.
