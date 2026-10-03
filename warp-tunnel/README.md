# warp-tunnel

Steer a hyperspace tunnel with your mouse. Hold to boost — the engine hum rises with speed and the rings fly faster. Distance counter tracks light-years.

## files

- `src/index.html` — readable source. Edit this, keep it human-friendly.
- `build.mjs` + `package.json` — official SHRINK build (terser). Run `npm install` once at repo root, then `node build.mjs` here.
- `dist/uri.txt` — the ship. One line `data:text/html` URI (1417 / 3072 bytes). Copy all, paste in new tab address bar, Enter.
- `dist/index.html` — minified page, same thing without the data URI wrapper.
- `meta.json` — title/description/badges for the toybox gallery.
- `preview.png` — real screenshot for the gallery (never inside the ship).

Badges: canvas, web audio, interactive, 3D (perspective projection on canvas).
