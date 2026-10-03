# gravity-well

Hold mouse to spray stars, gravity spirals them into the black hole. Each bite flashes the accretion ring and drops a pitch-drop synth blip. Counter tracks mass eaten. Idles with auto-dripping stars.

## files (ready to copy)

- `ship.txt` — the ship. One line `data:text/html` URI. Copy all, paste in new tab address bar, Enter.
- `src.html` — readable source. Edit here, then rebuild.
- `meta.json` — title/description/badges for the gallery.
- `preview.svg` — gallery thumbnail (docs only, not part of the ship).

## rebuild

```sh
python ../../build.py
# or: python ../../build.py gravity-well
```

Checks: one line, ≤3072 bytes, no network (`http|src=|href|fetch|url(` etc).
