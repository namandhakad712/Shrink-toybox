# gravity-well — SHRINK ship

A tiny black-hole toy in one line of HTML. Hold mouse to spray stars, gravity spirals them in, each bite flashes the accretion ring and drops a synth blip. Mass counter tracks how much you fed the void. Idle auto-drips stars so it looks alive with no input.

Built for [shrink.hackclub.com](https://shrink.hackclub.com/): single `data:text/html` URI, self-contained, no network.

## ready-to-copy files

- `ship.txt` — the ship. One line, `2708 / 3072` bytes. Copy entire contents, paste in a new tab address bar, hit Enter.
- `src.html` — readable source (what to commit per rules, not just the minified line).
- `build.py` — minifies `src.html` → `ship.txt` + checks size and banned network patterns.

## try it

1. Open `ship.txt`, copy all.
2. Open new tab, paste in address bar, Enter.
3. Hold mouse / touch to feed. First click enables audio.

## rebuild

```sh
python build.py
```

Checks: one line, ≤3072 bytes, no `http|src=|href|fetch|url(` etc.

## checklist

1. one line 3072 max — `ship.txt`, 2708 bytes, no newlines.
2. self-contained — no CDN/img/font/API. Canvas + WebAudio only.
3. public repo + README — this repo.
4. readable source — `src.html`.
5. tracked hours — log ≥30min on Hackatime in one project per ship.

Badges aimed: `<canvas>`, web audio, interactive.
