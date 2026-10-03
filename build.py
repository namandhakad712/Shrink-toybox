import re, pathlib
src = pathlib.Path(__file__).with_name("src.html").read_text(encoding="utf-8")
# collapse to one line: strip each line, drop comments? keep // comments would break one-liner -> strip them
lines = []
for ln in src.splitlines():
    s = ln.strip()
    if not s: continue
    if s.startswith("//"): continue
    # strip inline // comments (naive: cut ' // ' outside strings -- our code only uses // for full-line + trailing comments)
    # remove trailing comment if ' // ' present and line has no '://'
    if " // " in s and "://" not in s:
        s = s.split(" // ")[0].rstrip()
    lines.append(s)
one = " ".join(lines)
one = re.sub(r"\s+", " ", one).strip()
# minimal URL-encoding for data URI pasted in address bar (match shrink examples)
enc = one.replace("%", "%25").replace("#", "%23").replace(" ", "%20")
uri = "data:text/html," + enc
pathlib.Path(__file__).with_name("ship.txt").write_text(uri, encoding="utf-8")
print(f"raw one-line: {len(one)} bytes")
print(f"ship.txt (data URI): {len(uri)} bytes / 3072 max")
print("OK" if len(uri) <= 3072 and "\n" not in uri else "FAIL")
# banned network patterns check
import sys
bad = ["http", "src=", "href", "fetch(", "XMLHttpRequest", "import(", "@import", "url("]
found = [b for b in bad if b in one]
print("banned:", found if found else "none")
sys.exit(0 if len(uri) <= 3072 and not found else 1)
