# warp-tunnel

Steer a hyperspace tunnel with your mouse. Hold to boost — the engine hum rises with speed and the rings fly faster. Distance counter tracks light-years.

## files (ready to copy)

- `ship.txt` — the ship. One line `data:text/html` URI. Copy all, paste in new tab address bar, Enter.
- `src.html` — readable source. Edit here, then rebuild.
- `meta.json` — title/description/badges for the gallery.
- `preview.svg` — gallery thumbnail (docs only, not part of the ship).

## rebuild

```sh
python ../../build.py
# or: python ../../build.py warp-tunnel
```

Checks: one line, ≤3072 bytes, no network (`http|src=|href|fetch|url(` etc).

Badges aimed: `<canvas>`, web audio, interactive, 3D (perspective projection).
