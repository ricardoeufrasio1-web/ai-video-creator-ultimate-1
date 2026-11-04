#!/usr/bin/env python3
"""Build a portable Agent Skills folder and ZIP using only Python's standard library."""
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist"
NAME = "ai-video-creator-ultimate"
PACKAGE = DIST / NAME
ARCHIVE = DIST / (NAME + ".zip")
FILES = ["SKILL.md", "LICENSE", "THIRD_PARTY_NOTICES.md"]
DIRS = ["docs", "modules", "tools", "examples", "templates"]
SKIP = {".git", "node_modules", "__pycache__", ".pytest_cache", "dist"}

def copy_filtered(source, target):
    for item in source.rglob("*"):
        rel = item.relative_to(source)
        if any(part in SKIP for part in rel.parts) or not item.is_file():
            continue
        if item.suffix == ".pyc" or item.suffix == ".log":
            continue
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, dest)

def main():
    if PACKAGE.exists():
        shutil.rmtree(PACKAGE)
    if ARCHIVE.exists():
        ARCHIVE.unlink()
    PACKAGE.mkdir(parents=True)
    for filename in FILES:
        source = ROOT / filename
        if not source.is_file():
            raise SystemExit("Required file missing: " + filename)
        shutil.copy2(source, PACKAGE / filename)
    for dirname in DIRS:
        source = ROOT / dirname
        if source.is_dir():
            copy_filtered(source, PACKAGE / dirname)
    DIST.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in sorted(PACKAGE.rglob("*")):
            if item.is_file():
                archive.write(item, item.relative_to(DIST))
    print("Skill folder:", PACKAGE)
    print("Skill ZIP:", ARCHIVE)
    print("Package created. Import and execution support depend on the target agent.")

if __name__ == "__main__":
    main()
