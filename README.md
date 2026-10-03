# 🧸 shrink-toybox

> a toybox of tiny universes — every toy fits in **one line**!

Each toy is a whole game in a single `data:text/html` link. No installs, no libraries, no images, no internet. Just copy, paste, and play! ✨

Made for [shrink.hackclub.com](https://shrink.hackclub.com/) 🌀 · Started Oct 2026 with `gravity-well` 🕳️

---

## 📏 toybox rules (every toy obeys!)

1. 🧵 **one line only** — the whole toy is one `data:text/html,` link, **≤ 3072 bytes**
2. 🎒 **packs its own lunch** — no CDN, no images, no fonts, no APIs. Canvas doodles + WebAudio beeps only!
3. 📖 **show your work** — readable `src.html` lives here, not just the squished one-liner
4. ⏱️ **built with love + time** — ≥30 min on Hackatime per toy

---

## 🧃 what's inside?

| toy | what does it do? | size |
|---|---|---|
| 🕳️ `gravity-well` | feed stars to a hungry black hole! hold to spray, *gulp!* goes the mass counter | 1677 / 3072 bytes |
| 🌀 `warp-tunnel` | steer a hyperspace tunnel! hold to boost, engine hum rises with speed | 1482 / 3072 bytes |
| 🌸 `bloom` | a glowing blossom that breathes. move to morph it, click to pluck notes | 1918 / 3072 bytes |

More toys coming soon… the box is just getting started! 📦

---

## 🎮 how to play

**Option A — copy-paste magic:**
1. Open `<toy>/dist/uri.txt` and copy the whole line 📋
2. Open a new tab, paste it where the website address goes, press Enter 🎉
3. Play! (first click wakes up the sound 🔊)

**Option B — toy shelf:**
Open the gallery (`docs/index.html` on GitHub Pages) → click a picture for a live peek 👀 → press **Copy data URL** → paste in a new tab!

---

## 🗺️ toybox map

```text
<toy>/src/index.html  💛 the toy's heart — edit this one, keep it readable!
<toy>/build.mjs       🗜️ official SHRINK squish (terser) — run node build.mjs
<toy>/package.json    📦 declares terser (installed once at root)
<toy>/dist/uri.txt    🚀 the squished one-liner — copy-paste this to play
<toy>/dist/index.html minified page without the data URI wrapper
<toy>/meta.json       🏷️ name tag + description for the shelf
<toy>/preview.svg     🖼️ picture for the shelf (gallery only, never inside the toy)
package.json                   📦 root workspace (terser hoisted here, one install)
docs/                          🎪 the toy shelf template (content baked in by the Action)
build.py                       ✅ checks every toy (size, no-internet, syntax) + assembles site/
```

---

## 🛠️ make a new toy

1. Copy `gravity-well/` → `<my-toy>/` 📦
2. Draw + beep in `src/index.html`, write a cute `meta.json`, doodle a new `preview.svg` 🎨
3. Squish it: `node build.mjs` inside the toy folder (first time ever: `npm install` at root) 🗜️ — it tells you bytes used vs 3072!
4. Check everything: `python build.py` ✅ — verifies size, no-internet, JS syntax for all toys
5. Commit `src/` + `dist/` + `build.mjs` + `meta.json` + `preview.svg` 💌 (and push often — reviewers check your history!)

---

## 🎪 toy shelf (GitHub Pages, free)

No committed duplicates, no extra config. Push to GitHub, then Settings → Pages → Source: **GitHub Actions**. The `toybox-pages` workflow runs `python build.py --site site` on every push — it reads the live `<toy>/dist/uri.txt` + `preview.svg` from the outer folder, bakes them into the site (preview image + data URL box + copy button + live demo + view-source per card), and deploys. Zero hosting cost.

Preview locally the same way the Action does: `python build.py`, then serve `site/` (e.g. `python -m http.server -d site`).

> ⚠️ heads-up from the SHRINK guides: READMEs must sound **human-written** — reviewers reject projects whose README reads AI-made. Before shipping, rewrite this file and each toy's README in your own words!
