# bloom

A glowing blossom that breathes on its own. Move your mouse to morph it, click to pluck soft notes out of it. Works with touch too.

## files

- `src/index.html` — readable source. Edit this, keep it human-friendly.
- `build.mjs` + `package.json` — official SHRINK build (terser). Run `npm install` once at repo root, then `node build.mjs` here.
- `dist/uri.txt` — the ship. One line `data:text/html` URI. Copy all, paste in new tab address bar, Enter.
- `dist/index.html` — minified page, same thing without the data URI wrapper.
- `meta.json` — title/description/badges for the toybox gallery.
- `preview.png` — real screenshot for the gallery (never inside the ship).

Badges: web audio, interactive.
