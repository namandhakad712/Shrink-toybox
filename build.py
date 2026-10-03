"""Build all ships: projects/<slug>/src.html -> projects/<slug>/ship.txt.

Also assembles a deployable Pages site (gitignored) from the docs/ template
plus live content from projects/ — no duplicated files committed to docs/.

Usage:
  python build.py                build ships + assemble ./site/
  python build.py gravity-well   build one ship (+ site)
  python build.py --site out     assemble site into ./out/
"""
import json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).parent
MAX = 3072
BAD = ["http", "src=", "href", "fetch(", "XMLHttpRequest", "import(", "@import", "url("]

def shrink(src_html: str) -> str:
    # Split HTML shell vs JS: newlines separate statements inside <script>,
    # so JS lines must be re-joined with ';' (ASI would break on spaces).
    # Rule for src.html: one statement per line inside <script>.
    m = re.search(r"<script>(.*)</script>", src_html, re.S)
    js = m.group(1) if m else ""
    js_lines = []
    for ln in js.splitlines():
        s = ln.strip()
        if not s or s.startswith("//"):
            continue
        if " // " in s and "://" not in s:
            s = s.split(" // ")[0].rstrip()
        js_lines.append(s)
    js_one = ";".join(js_lines)
    html_lines = []
    for ln in (src_html[:m.start()] if m else src_html).splitlines():
        s = ln.strip()
        if s:
            html_lines.append(s)
    tail = (src_html[m.end():] if m else "").strip()
    one = re.sub(r"\s+", " ", " ".join(html_lines)).strip()
    one += " <script>" + js_one + "</script>" + (" " + tail if tail else "")
    one = re.sub(r"\s+", " ", one).strip()
    enc = one.replace("%", "%25").replace("#", "%23").replace(" ", "%20")
    return "data:text/html," + enc, one

def js_syntax_ok(js: str) -> bool:
    import subprocess, tempfile, os
    node = shutil.which("node")
    if not node:
        return True  # can't verify here; CI/browser will
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(js)
        path = f.name
    r = subprocess.run([node, "--check", path], capture_output=True, text=True)
    os.unlink(path)
    if r.returncode != 0:
        print("JS SYNTAX ERROR:\n" + r.stderr[:1500])
        return False
    return True

def build_site(projs, dest: Path):
    """Assemble deployable site from docs/ template + live projects/ content."""
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "p").mkdir(parents=True)
    for f in ("index.html", ".nojekyll"):
        src = ROOT / "docs" / f
        if src.exists():
            shutil.copy(src, dest / f)
    entries = []
    for d in projs:
        src = d / "src.html"
        ship = d / "ship.txt"
        if not src.exists() or not ship.exists():
            continue
        meta = {}
        mf = d / "meta.json"
        if mf.exists():
            meta = json.loads(mf.read_text(encoding="utf-8"))
        uri = ship.read_text(encoding="utf-8")
        preview = None
        for cand in ("preview.svg", "preview.png", "preview.jpg"):
            if (d / cand).exists():
                (dest / "p" / d.name).mkdir(parents=True, exist_ok=True)
                shutil.copy(d / cand, dest / "p" / d.name / cand)
                preview = f"p/{d.name}/{cand}"
                break
        entries.append({
            "slug": d.name,
            "title": meta.get("title", d.name),
            "description": meta.get("description", ""),
            "badges": meta.get("badges", []),
            "bytes": len(uri),
            "percent": round(len(uri) / MAX * 100),
            "dataUrl": uri,
            "sourceHtml": src.read_text(encoding="utf-8"),
            "preview": preview,
        })
    (dest / "projects.json").write_text(json.dumps(entries, indent=1), encoding="utf-8")
    print(f"site -> {dest} ({len(entries)} projects)")

def main(args):
    site = "site"
    slugs = []
    i = 0
    while i < len(args):
        if args[i] == "--site" and i + 1 < len(args):
            site = args[i + 1]
            i += 2
        else:
            slugs.append(args[i])
            i += 1
    slugs = [s for s in slugs if (ROOT / "projects" / s).is_dir()]
    projs = sorted([d for d in (ROOT / "projects").iterdir() if d.is_dir()]) if (ROOT / "projects").exists() else []
    if slugs:
        projs = [ROOT / "projects" / s for s in slugs]
    fail = False
    for d in projs:
        src = d / "src.html"
        if not src.exists():
            print(f"SKIP {d.name}: no src.html"); continue
        uri, one = shrink(src.read_text(encoding="utf-8"))
        (d / "ship.txt").write_text(uri, encoding="utf-8")
        found = [b for b in BAD if b in one]
        mjs = re.search(r"<script>(.*)</script>", one)
        syntax = js_syntax_ok(mjs.group(1) if mjs else "")
        ok = len(uri) <= MAX and "\n" not in uri and not found and syntax
        print(f"{d.name}: raw={len(one)} ship={len(uri)}/{MAX} {'OK' if ok else 'FAIL'} banned={found or 'none'}")
        if not ok:
            fail = True
    built = [d for d in (sorted([x for x in (ROOT / 'projects').iterdir() if x.is_dir()])) if (d / "ship.txt").exists()] if (ROOT / "projects").exists() else []
    build_site(built, ROOT / site)
    sys.exit(1 if fail else 0)

if __name__ == "__main__":
    main(sys.argv[1:])
