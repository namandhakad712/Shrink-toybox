import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).parent
MAX = 3072
BAD = ["http", "src=", "href", "fetch(", "XMLHttpRequest", "import(", "@import", "url("]

def toy_dirs():
    return sorted([d for d in ROOT.iterdir() if d.is_dir() and (d / "src" / "index.html").exists()])

def js_ok(js, label):
    import subprocess
    import tempfile
    import os
    node = shutil.which("node")
    if not node:
        return True
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(js)
        path = f.name
    r = subprocess.run([node, "--check", path], capture_output=True, text=True)
    os.unlink(path)
    if r.returncode != 0:
        print(label + " broken js:\n" + r.stderr[:1500])
        return False
    return True

def verify(d):
    uri_file = d / "dist" / "uri.txt"
    if not uri_file.exists():
        print("FAIL " + d.name + ": run node build.mjs inside " + d.name)
        return None
    uri = uri_file.read_text(encoding="utf-8").strip()
    size = len(uri.encode("utf-8"))
    html = unquote(uri.split(",", 1)[1]) if uri.startswith("data:text/html,") else ""
    found = [b for b in BAD if b in html]
    m = re.search(r"<script>(.*)</script>", html, re.S)
    ok = uri.startswith("data:text/html,") and size <= MAX and "\n" not in uri and not found and js_ok(m.group(1) if m else "", d.name)
    print(d.name + ": " + str(size) + "/" + str(MAX) + " " + ("OK" if ok else "FAIL"))
    return uri if ok else None

def build_site(good, dest):
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "p").mkdir(parents=True)
    for f in ("index.html", ".nojekyll"):
        src = ROOT / "docs" / f
        if src.exists():
            shutil.copy(src, dest / f)
    entries = []
    for slug, uri in good.items():
        d = ROOT / slug
        meta = {}
        mf = d / "meta.json"
        if mf.exists():
            meta = json.loads(mf.read_text(encoding="utf-8"))
        preview = None
        for cand in ("preview.svg", "preview.png", "preview.jpg"):
            if (d / cand).exists():
                (dest / "p" / slug).mkdir(parents=True, exist_ok=True)
                shutil.copy(d / cand, dest / "p" / slug / cand)
                preview = "p/" + slug + "/" + cand
                break
        size = len(uri.encode("utf-8"))
        entries.append({
            "slug": slug,
            "title": meta.get("title", slug),
            "description": meta.get("description", ""),
            "badges": meta.get("badges", []),
            "bytes": size,
            "percent": round(size / MAX * 100),
            "dataUrl": uri,
            "sourceHtml": (d / "src" / "index.html").read_text(encoding="utf-8"),
            "preview": preview
        })
    (dest / "projects.json").write_text(json.dumps(entries, indent=1), encoding="utf-8")
    print("site -> " + str(dest) + " (" + str(len(entries)) + " toys)")

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
    toys = toy_dirs()
    want = [ROOT / s for s in slugs if (ROOT / s).is_dir()] if slugs else toys
    checked = {}
    for d in toys:
        uri = verify(d)
        if uri:
            checked[d.name] = uri
    build_site(checked, ROOT / site)
    names = [d.name for d in want]
    sys.exit(0 if names and all(n in checked for n in names) else 1)

if __name__ == "__main__":
    main(sys.argv[1:])
