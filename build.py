"""Verify ships + assemble the Pages site (gitignored) from docs/ template.

Official per-toy build is `node build.mjs` inside each projects/<slug>/
(src/index.html -> dist/uri.txt, committed). This script only verifies and
assembles — it never minifies, so what reviewers read is what ships.

Usage:
  python build.py                verify all + assemble ./site/
  python build.py gravity-well   verify one toy (+ site)
  python build.py --site out     assemble site into ./out/
"""
import json, re, shutil, sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).parent
MAX = 3072
BAD = ["http", "src=", "href", "fetch(", "XMLHttpRequest", "import(", "@import", "url("]

def js_syntax_ok(js: str, label: str) -> bool:
    import subprocess, tempfile, os
    node = shutil.which("node")
    if not node:
        print(f"{label}: node missing, syntax check skipped")
        return True
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(js)
        path = f.name
    r = subprocess.run([node, "--check", path], capture_output=True, text=True)
    os.unlink(path)
    if r.returncode != 0:
        print(f"{label}: JS SYNTAX ERROR:\n" + r.stderr[:1500])
        return False
    return True

def verify(d: Path) -> str | None:
    """Returns data URL if the toy passes all checks, else None."""
    src = d / "src" / "index.html"
    uri_f = d / "dist" / "uri.txt"
    if not src.exists():
        print(f"SKIP {d.name}: no src/index.html"); return None
    if not uri_f.exists():
        print(f"FAIL {d.name}: no dist/uri.txt — run `node build.mjs` in projects/{d.name}"); return None
    if src.stat().st_mtime > uri_f.stat().st_mtime:
        print(f"FAIL {d.name}: dist/uri.txt older than src — rerun `node build.mjs`"); return None
    uri = uri_f.read_text(encoding="utf-8").strip()
    nbytes = len(uri.encode("utf-8"))
    html = unquote(uri.split(",", 1)[1]) if uri.startswith("data:text/html,") else ""
    found = [b for b in BAD if b in html]
    mjs = re.search(r"<script>(.*)</script>", html, re.S)
    ok = (
        uri.startswith("data:text/html,")
        and nbytes <= MAX
        and "\n" not in uri
        and not found
        and js_syntax_ok(mjs.group(1) if mjs else "", d.name)
    )
    print(f"{d.name}: {nbytes}/{MAX} {'OK' if ok else 'FAIL'} banned={found or 'none'}")
    return uri if ok else None

def build_site(good: dict, dest: Path):
    """Assemble deployable site from docs/ template + live projects/ content."""
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "p").mkdir(parents=True)
    for f in ("index.html", ".nojekyll"):
        src = ROOT / "docs" / f
        if src.exists():
            shutil.copy(src, dest / f)
    entries = []
    for slug, uri in good.items():
        d = ROOT / "projects" / slug
        meta = {}
        mf = d / "meta.json"
        if mf.exists():
            meta = json.loads(mf.read_text(encoding="utf-8"))
        preview = None
        for cand in ("preview.svg", "preview.png", "preview.jpg"):
            if (d / cand).exists():
                (dest / "p" / slug).mkdir(parents=True, exist_ok=True)
                shutil.copy(d / cand, dest / "p" / slug / cand)
                preview = f"p/{slug}/{cand}"
                break
        entries.append({
            "slug": slug,
            "title": meta.get("title", slug),
            "description": meta.get("description", ""),
            "badges": meta.get("badges", []),
            "bytes": len(uri.encode("utf-8")),
            "percent": round(len(uri.encode("utf-8")) / MAX * 100),
            "dataUrl": uri,
            "sourceHtml": (d / "src" / "index.html").read_text(encoding="utf-8"),
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
    all_dirs = sorted([d for d in (ROOT / "projects").iterdir() if d.is_dir()]) if (ROOT / "projects").exists() else []
    projs = [ROOT / "projects" / s for s in slugs] if slugs else all_dirs
    checked = {}
    for d in all_dirs:
        uri = verify(d)
        if uri:
            checked[d.name] = uri
    build_site(checked, ROOT / site)
    sys.exit(0 if all(n in checked for n in [d.name for d in projs]) and projs else 1)

if __name__ == "__main__":
    main(sys.argv[1:])
