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
| 🕳️ `gravity-well` | feed stars to a hungry black hole! hold to spray, *gulp!* goes the mass counter | 2708 / 3072 bytes |
| 🌀 `warp-tunnel` | steer a hyperspace tunnel! hold to boost, engine hum rises with speed | 2465 / 3072 bytes |

More toys coming soon… the box is just getting started! 📦

---

## 🎮 how to play

**Option A — copy-paste magic:**
1. Open `projects/<toy>/ship.txt` and copy the whole line 📋
2. Open a new tab, paste it where the website address goes, press Enter 🎉
3. Play! (first click wakes up the sound 🔊)

**Option B — toy shelf:**
Open the gallery (`docs/index.html` on GitHub Pages) → click a picture for a live peek 👀 → press **Copy data URL** → paste in a new tab!

---

## 🗺️ toybox map

```text
projects/<toy>/src.html    💛 the toy's heart — edit this one!
projects/<toy>/ship.txt    🚀 the squished one-liner — copy-paste this to play
projects/<toy>/meta.json   🏷️ name tag + description for the shelf
projects/<toy>/preview.svg 🖼️ picture for the shelf (gallery only, never inside the toy)
docs/                      🎪 the toy shelf website (GitHub Pages)
docs/p/<toy>/              🤖 robot copies for the website (made by build.py, don't touch!)
build.py                   🗜️ the squish machine — shrinks every toy + checks the rules
```

---

## 🛠️ make a new toy

1. Copy `projects/gravity-well/` → `projects/<my-toy>/` 📦
2. Draw + beep in `src.html`, write a cute `meta.json`, doodle a new `preview.svg` 🎨
3. Run the squish machine: `python build.py` 🗜️ — it squeaks if you're over 3072 bytes or sneaked in internet stuff!
4. Commit `src.html` + `ship.txt` + `meta.json` + `preview.svg` 💌

---

## 🎪 toy shelf (GitHub Pages)

Settings → Pages → Deploy from branch → `/docs` — that's it! Plain HTML/CSS/JS, zero dependencies. Each card shows the picture + live demo + **Open / Copy / Source** buttons.
