#!/usr/bin/env python3
"""Build the generic (church-neutral) copy of Soul Winner.

The root index.html / report.html carry one church's Firebase config so its
live GitHub Pages site works. Anyone else must NOT use those files as-is, or
their visits would land in that church's database. This script copies the app
into generic/ with the Firebase config blanked out, adds CLAUDE.md (the setup
guide from tools/generic-CLAUDE.md), and zips it as
soul-winner-generic.zip for one-click download.

Run it after changing the app:   python3 tools/make_generic.py
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "generic"
ZIP = ROOT / "soul-winner-generic.zip"
COPY_AS_IS = ["sw.js", "manifest.json", "icon-192.png", "icon-512.png", "apple-touch-icon.png"]

BLANK_INDEX = """const FIREBASE_CONFIG_DEFAULT = {
  apiKey:            '',  // e.g. 'AIzaSyABC...'
  authDomain:        '',  // e.g. 'your-project.firebaseapp.com'
  databaseURL:       '',  // e.g. 'https://your-project-default-rtdb.firebaseio.com'
  projectId:         '',  // e.g. 'your-project'
  appId:             '',  // e.g. '1:123456789:web:abc123def456'
};"""

BLANK_REPORT = """  // Fallback — paste the same values you put in index.html
  return {
    apiKey:      '',
    authDomain:  '',
    databaseURL: '',
    projectId:   '',
    appId:       '',
  };"""


def replace_once(text, pattern, repl, name):
    new, n = re.subn(pattern, lambda _m: repl, text, count=1, flags=re.S)
    if n != 1:
        sys.exit(f"make_generic: could not find the Firebase config in {name}; update the pattern in tools/make_generic.py")
    return new


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    index = replace_once(index, r"const FIREBASE_CONFIG_DEFAULT = \{.*?\};", BLANK_INDEX, "index.html")
    (OUT / "index.html").write_text(index, encoding="utf-8")

    report = (ROOT / "report.html").read_text(encoding="utf-8")
    report = replace_once(report, r"  // Fallback — hardcoded \(matches index.html\)\n  return \{.*?\};", BLANK_REPORT, "report.html")
    (OUT / "report.html").write_text(report, encoding="utf-8")

    for name in COPY_AS_IS:
        shutil.copy2(ROOT / name, OUT / name)

    # Setup guide a church hands to Claude (Claude Code reads CLAUDE.md automatically)
    shutil.copy2(ROOT / "tools" / "generic-CLAUDE.md", OUT / "CLAUDE.md")

    # Safety check: no real-looking Firebase values may survive
    for f in OUT.glob("*.html"):
        text = f.read_text(encoding="utf-8")
        hits = re.findall(r"AIza[0-9A-Za-z_-]{20,}|[a-z0-9-]+-default-rtdb\.firebaseio\.com", text)
        hits = [h for h in hits if not h.startswith("your-project")]  # README-style placeholders are fine
        if hits:
            sys.exit(f"make_generic: {f.name} still contains a Firebase key or database URL: {hits[0]}")

    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.iterdir()):
            z.write(f, f"soul-winner/{f.name}")
    print(f"Wrote {OUT.relative_to(ROOT)}/ and {ZIP.name}")


if __name__ == "__main__":
    main()
