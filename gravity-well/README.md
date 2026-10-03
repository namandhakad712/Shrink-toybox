# gravity-well

Hold mouse to spray stars, gravity spirals them into the black hole. Each bite flashes the accretion ring and drops a pitch-drop synth blip. Counter tracks mass eaten. Idles with auto-dripping stars.

## files

- `src/index.html` — readable source. Edit this, keep it human-friendly.
- `build.mjs` + `package.json` — official SHRINK build (terser). Run `npm install` once at repo root, then `node build.mjs` here.
- `dist/uri.txt` — the ship. One line `data:text/html` URI (1627 / 3072 bytes). Copy all, paste in new tab address bar, Enter.
- `dist/index.html` — minified page, same thing without the data URI wrapper.
- `meta.json` — title/description/badges for the toybox gallery.
- `preview.svg` — gallery thumbnail (docs only, never in ship).

Badges: canvas, web audio, interactive.
