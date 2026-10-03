# shrink data-url ships

A mono-repo of tiny web apps, each a **single `data:text/html` file**. No build step to run them, no library, no CDN, no images, no fonts, no APIs.

Made for [shrink.hackclub.com](https://shrink.hackclub.com/) (YSWS). Started Oct 2026 with `gravity-well`.

## SHRINK limits (every ship obeys)

- whole app is one `data:text/html,` URI, **≤ 3072 bytes**, one line
- self-contained: network blocked at runtime — Canvas math + WebAudio only
- public repo + README + readable source (commit pre-shrink code, not just the minified line)
- ≥30 min Hackatime per ship, one Hackatime project = one ship

## layout

```text
projects/<slug>/src.html    readable source — edit this
projects/<slug>/ship.txt    the ship — one-line data URL, copy-paste ready
projects/<slug>/meta.json   title/description/badges for gallery
projects/<slug>/preview.svg thumbnail for gallery (docs only, never in ship)
docs/                       GitHub Pages gallery (index.html + projects.json)
docs/p/<slug>/               generated mirror of ship/src/preview for Pages (do not edit, from build.py)
build.py                    minifies every src.html -> ship.txt, checks limits, regenerates docs/projects.json
```

## use a ship

1. Open `projects/<slug>/ship.txt`, copy everything.
2. New tab → paste in address bar → Enter.
3. Or browse the gallery: `docs/index.html` (Pages) → click image for live demo → Copy data URL.

## add a ship

1. Copy `projects/gravity-well/` → `projects/<new-slug>/`, edit `src.html` + `meta.json`, replace `preview.svg`.
2. Run `python build.py` — fails if >3072 bytes or contains `http|src=|href|fetch|url(` etc.
3. Commit `src.html` + `ship.txt` + `meta.json` + `preview.svg`.

## gallery (GitHub Pages)

- source: `docs/` folder. Settings → Pages → Deploy from branch → `/docs`.
- no dependencies, plain HTML/CSS/JS. `index.html` fetches `projects.json`, each card shows preview image + live iframe demo + Open / Copy / Source buttons.

## ships

| slug | what | bytes |
|---|---|---|
| `gravity-well` | black-hole feeder toy, canvas + audio + interactive | 2708 / 3072 |
