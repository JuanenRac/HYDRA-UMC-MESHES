#!/usr/bin/env python3
# =============================================================================
# HYDRA-UMC-MESHES - tools/verify_pack.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D)
# GPL-3.0-or-later - see LICENSE
#
# Checks that the manifest of the mesh package (meshes.pack.json) and the checksum file (SHA256SUMS.txt) agree: same archive name, same SHA-256,
# well-formed hashes for every file, no path that leaves the package and no duplicate path. With --archive it also checks a downloaded archive against the
# manifest (size and SHA-256) and with --extracted a folder it was unpacked into (every file present, of the size and the SHA-256 the manifest says, and no
# file the manifest does not list). Standard library only.
# =============================================================================
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEX = re.compile(r"^[0-9a-f]{64}$")


def leaves_the_package(path: str) -> bool:
    """True for a path that is empty, absolute, drive-lettered, or climbs out of the package on ANY system: the check runs on Linux, where a
    backslash is an ordinary character, but the apps that unpack the package also run on Windows, where it separates folders."""
    parts = path.replace("\\", "/").split("/")
    return (
        not path
        or path.startswith(("/", "\\"))
        or ":" in path
        or any(part in ("", ".", "..") for part in parts)
    )


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
        if leaves_the_package(path):
            problems.append(f"path outside the package: {path!r}")
        if path in seen:
            problems.append(f"duplicate path: {path!r}")
        elif path.casefold() in {other.casefold() for other in seen}:
            problems.append(f"path that differs from another only in case (a clash on Windows and macOS): {path!r}")
        seen.add(path)
    if not manifest.get("files"):
        problems.append("the manifest lists no files")
    return problems


def _file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def check_archive(archive: Path, root: Path = ROOT) -> list[str]:
    """The problems of a downloaded archive: absent, of another size than the manifest says (an interrupted or padded download) or with another SHA-256."""
    pack = json.loads((root / "meshes.pack.json").read_text(encoding="utf-8")).get("pack", {})
    if not archive.is_file():
        return [f"the archive {archive.name} is missing"]
    problems: list[str] = []
    size = pack.get("size")
    actual = archive.stat().st_size
    if isinstance(size, int) and actual != size:
        problems.append(f"the archive has {actual} bytes and the manifest says {size}: the download is cut short or padded")
    found = _file_digest(archive)
    if found != pack.get("sha256"):
        problems.append(f"the SHA-256 of the archive is {found}, not the one of the manifest")
    return problems


def check_extracted(directory: Path, root: Path = ROOT) -> list[str]:
    """The problems of a folder the archive was unpacked into: a file missing, of another size or another SHA-256, or a file the manifest does not list."""
    manifest = json.loads((root / "meshes.pack.json").read_text(encoding="utf-8"))
    problems: list[str] = []
    listed: set[str] = set()
    for entry in manifest.get("files", []):
        path = str(entry.get("path", ""))
        if leaves_the_package(path):
            problems.append(f"path outside the package: {path!r}")
            continue
        listed.add(path)
        target = directory / path
        if not target.is_file():
            problems.append(f"missing: {path}")
            continue
        size = entry.get("size")
        if isinstance(size, int) and target.stat().st_size != size:
            problems.append(f"wrong size: {path}")
        elif _file_digest(target) != entry.get("sha256"):
            problems.append(f"wrong SHA-256: {path}")
    for found in sorted(p for p in directory.rglob("*") if p.is_file()):
        relative = found.relative_to(directory).as_posix()
        if relative not in listed:
            problems.append(f"not in the manifest: {relative}")
    return problems


def main(argv: list[str] | tuple[str, ...] = (), root: Path | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the manifest of the mesh package, and optionally a downloaded archive and the folder it was unpacked into.")
    parser.add_argument("--archive", type=Path, help="a downloaded archive to check against the manifest")
    parser.add_argument("--extracted", type=Path, help="a folder the archive was unpacked into")
    args = parser.parse_args(list(argv))
    problems = check() if root is None else check(root)
    where = ROOT if root is None else root
    if args.archive is not None:
        problems += check_archive(args.archive, where)
    if args.extracted is not None:
        problems += check_extracted(args.extracted, where)
    for line in problems:
        print("FAIL:", line)
    print("VERIFY_PACK=PASS" if not problems else "VERIFY_PACK=FAIL")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
