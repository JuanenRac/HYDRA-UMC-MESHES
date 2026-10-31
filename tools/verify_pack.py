#!/usr/bin/env python3
# =============================================================================
# HYDRA-UMC-MESHES - tools/verify_pack.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D)
# GPL-3.0-or-later - see LICENSE
#
# Checks that the manifest of the mesh package (meshes.pack.json) and the checksum file (SHA256SUMS.txt) agree: same archive name, same SHA-256,
# well-formed hashes for every file, no path that leaves the package and no duplicate path. Standard library only.
# =============================================================================
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEX = re.compile(r"^[0-9a-f]{64}$")


def check(root: Path = ROOT) -> list[str]:
    problems: list[str] = []
    manifest = json.loads((root / "meshes.pack.json").read_text(encoding="utf-8"))
    pack = manifest.get("pack", {})
    name, digest = pack.get("file"), pack.get("sha256")
    if not name or not HEX.match(str(digest or "")):
        problems.append("the manifest has no archive name or a malformed archive SHA-256")
    sums = {}
    for line in (root / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        if line.strip():
            h, _, n = line.partition("  ")
            sums[n.strip()] = h.strip()
    if sums.get(name) != digest:
        problems.append(f"SHA256SUMS.txt does not list {name} with the SHA-256 of the manifest")
    seen: set[str] = set()
    for entry in manifest.get("files", []):
        path = str(entry.get("path", ""))
        if not HEX.match(str(entry.get("sha256", ""))):
            problems.append(f"malformed SHA-256 for {path!r}")
        if path.startswith(("/", "\\")) or ".." in Path(path).parts or ":" in path:
            problems.append(f"path outside the package: {path!r}")
        if path in seen:
            problems.append(f"duplicate path: {path!r}")
        seen.add(path)
    if not manifest.get("files"):
        problems.append("the manifest lists no files")
    return problems


def main() -> int:
    problems = check()
    for line in problems:
        print("FAIL:", line)
    print("VERIFY_PACK=PASS" if not problems else "VERIFY_PACK=FAIL")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
