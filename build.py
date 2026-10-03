"""Build all ships: projects/<slug>/src.html -> projects/<slug>/ship.txt + docs/projects.json."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
MAX = 3072
BAD = ["http", "src=", "href", "fetch(", "XMLHttpRequest", "import(", "@import", "url("]

def shrink(src_html: str) -> str:
    lines = []
    for ln in src_html.splitlines():
        s = ln.strip()
        if not s or s.startswith("//"):
            continue
        if " // " in s and "://" not in s:
            s = s.split(" // ")[0].rstrip()
        lines.append(s)
    one = re.sub(r"\s+", " ", " ".join(lines)).strip()
    enc = one.replace("%", "%25").replace("#", "%23").replace(" ", "%20")
    return "data:text/html," + enc, one

def main(slugs):
    projs = sorted([d for d in (ROOT / "projects").iterdir() if d.is_dir()]) if (ROOT / "projects").exists() else []
    if slugs:
        projs = [ROOT / "projects" / s for s in slugs]
    out, fail = [], False
    for d in projs:
        src = d / "src.html"
        if not src.exists():
            print(f"SKIP {d.name}: no src.html"); continue
        uri, one = shrink(src.read_text(encoding="utf-8"))
        (d / "ship.txt").write_text(uri, encoding="utf-8")
        found = [b for b in BAD if b in one]
        ok = len(uri) <= MAX and "\n" not in uri and not found
        meta = {}
        mf = d / "meta.json"
        if mf.exists():
            meta = json.loads(mf.read_text(encoding="utf-8"))
        print(f"{d.name}: raw={len(one)} ship={len(uri)}/{MAX} {'OK' if ok else 'FAIL'} banned={found or 'none'}")
        if not ok:
            fail = True
        preview = None
        for cand in ("preview.svg", "preview.png", "preview.jpg"):
            if (d / cand).exists():
                preview = f"p/{d.name}/{cand}"
                break
        out.append({
            "slug": d.name,
            "title": meta.get("title", d.name),
            "description": meta.get("description", ""),
            "badges": meta.get("badges", []),
            "bytes": len(uri),
            "percent": round(len(uri) / MAX * 100),
            "ship": f"p/{d.name}/ship.txt",
            "source": f"p/{d.name}/src.html",
            "preview": preview,
        })
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    # Pages serves docs/ as web root, so mirror per-project assets under docs/p/<slug>/
    for d in projs:
        src = d / "src.html"
        if not src.exists():
            continue
        dest = docs / "p" / d.name
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "src.html").write_bytes(src.read_bytes())
        ship = d / "ship.txt"
        if ship.exists():
            (dest / "ship.txt").write_bytes(ship.read_bytes())
        for cand in ("preview.svg", "preview.png", "preview.jpg"):
            if (d / cand).exists():
                (dest / cand).write_bytes((d / cand).read_bytes())
    for e in out:
        slug = e["slug"]
        e["ship"] = f"p/{slug}/ship.txt"
        e["source"] = f"p/{slug}/src.html"
        e["preview"] = None
        for cand in ("preview.svg", "preview.png", "preview.jpg"):
            if (docs / "p" / slug / cand).exists():
                e["preview"] = f"p/{slug}/{cand}"
                break
    (docs / "projects.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"docs/projects.json: {len(out)} projects")
    sys.exit(1 if fail else 0)

if __name__ == "__main__":
    main(sys.argv[1:])
