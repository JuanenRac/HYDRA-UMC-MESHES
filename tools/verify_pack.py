#!/usr/bin/env python3
# =============================================================================
# HYDRA-UMC-MESHES - tools/verify_pack.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D)
# GPL-3.0-or-later - see LICENSE
#
# Checks that the manifest of the mesh package (meshes.pack.json) and the checksum file (SHA256SUMS.txt) agree: same archive name, same SHA-256,
# well-formed hashes for every file, sizes that are whole numbers, an https download address that ends with the archive name, no path that leaves the package and no duplicate path. With --archive it also checks a downloaded archive against the
# manifest (size and SHA-256) and with --extracted a folder it was unpacked into (every file present, of the size and the SHA-256 the manifest says, and no
# file the manifest does not list). --archive-members reads the archive as a stream and checks every member BEFORE anything is written (only regular files, all
# listed, of the size and SHA-256 of the manifest, none missing). --consumer-manifest compares a copy of the manifest kept by another program with this one;
# SHA256SUMS.txt carries the SHA-256 of the manifest (of its bytes with LF line ends). Standard library only.
# =============================================================================
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tarfile
from pathlib import Path
from urllib.parse import urlsplit

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


def is_size(value: object) -> bool:
    """A size is a whole number of bytes, zero or more (a boolean is not one, nor is a string or a fraction)."""
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def url_problem(url: object, name: object) -> str | None:
    """Why the download address is not acceptable (None when it is): it must be an https address with a host, no credentials, query or fragment, whose path ends with the archive name."""
    if not isinstance(url, str) or not url:
        return "the download address of the archive is not a text"
    parts = urlsplit(url)
    if parts.scheme != "https" or not parts.hostname:
        return f"the download address must be an https address with a host: {url!r}"
    if parts.username is not None or parts.password is not None or parts.query or parts.fragment:
        return f"the download address must not carry credentials, a query or a fragment: {url!r}"
    if not isinstance(name, str) or not name or parts.path.rsplit("/", 1)[-1] != name:
        return f"the download address does not end with the archive name {name!r}: {url!r}"
    return None


def manifest_digest(path: Path) -> str:
    """The SHA-256 of a manifest with LF line ends, so a checkout on Windows says the same as one on Linux."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def check_consumer_manifest(copy: Path, root: Path = ROOT) -> list[str]:
    """Why the manifest another program keeps is not the one published here (empty when it is the same)."""
    if not copy.is_file():
        return [f"the manifest {copy} is missing"]
    if manifest_digest(copy) == manifest_digest(root / "meshes.pack.json"):
        return []
    try:
        theirs = {str(e.get("path")): e.get("sha256") for e in json.loads(copy.read_text(encoding="utf-8")).get("files", [])}
    except (OSError, ValueError, AttributeError):
        return [f"the manifest {copy} cannot be read"]
    ours = {str(e.get("path")): e.get("sha256") for e in json.loads((root / "meshes.pack.json").read_text(encoding="utf-8")).get("files", [])}
    different = sorted(path for path in ours.keys() | theirs.keys() if ours.get(path) != theirs.get(path))
    shown = ", ".join(different[:5]) + (f" (+{len(different) - 5} more)" if len(different) > 5 else "")
    return [f"the manifest {copy} is not the published one" + (f": {shown}" if different else " (same files, other fields)")]


def check_archive_members(archive: Path, root: Path = ROOT) -> list[str]:
    """The problems of the content of an archive, found without unpacking it: it is read once, as a stream, and nothing is written."""
    manifest = json.loads((root / "meshes.pack.json").read_text(encoding="utf-8"))
    expected = {str(e.get("path", "")): e for e in manifest.get("files", [])}
    problems: list[str] = []
    seen: set[str] = set()
    try:
        with tarfile.open(archive, mode="r|gz") as tar:
            for member in tar:
                if member.isdir():
                    continue
                name = member.name[2:] if member.name.startswith("./") else member.name
                entry = expected.get(name)
                if not member.isreg():
                    problems.append(f"not a regular file: {name!r}")
                elif entry is None:
                    problems.append(f"not in the manifest: {name!r}")
                elif name in seen:
                    problems.append(f"twice in the archive: {name!r}")
                elif member.size != entry.get("size", member.size):
                    problems.append(f"wrong size: {name}")
                else:
                    seen.add(name)
                    source = tar.extractfile(member)
                    digest = hashlib.sha256()
                    for block in iter(lambda: source.read(1 << 20) if source else b"", b""):
                        digest.update(block)
                    if digest.hexdigest() != entry.get("sha256"):
                        problems.append(f"wrong SHA-256: {name}")
    except (OSError, tarfile.TarError) as error:
        return [*problems, f"the archive cannot be read: {error}"]
    refused = {line.split(": ", 1)[-1].strip("'") for line in problems}
    problems += [f"missing from the archive: {path}" for path in sorted(expected.keys() - seen - refused)]
    return problems


def check(root: Path = ROOT) -> list[str]:
    problems: list[str] = []
    manifest = json.loads((root / "meshes.pack.json").read_text(encoding="utf-8"))
    pack = manifest.get("pack", {})
    name, digest = pack.get("file"), pack.get("sha256")
    if not name or not HEX.match(str(digest or "")):
        problems.append("the manifest has no archive name or a malformed archive SHA-256")
    if "size" in pack and not is_size(pack["size"]):
        problems.append(f"the size of the archive is not a whole number of bytes: {pack['size']!r}")
    if "url" in pack:
        reason = url_problem(pack["url"], name)
        if reason:
            problems.append(reason)
    sums = {}
    for line in (root / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        if line.strip():
            h, _, n = line.partition("  ")
            sums[n.strip()] = h.strip()
    if sums.get(name) != digest:
        problems.append(f"SHA256SUMS.txt does not list {name} with the SHA-256 of the manifest")
    if "meshes.pack.json" in sums and sums["meshes.pack.json"] != manifest_digest(root / "meshes.pack.json"):
        problems.append("SHA256SUMS.txt lists meshes.pack.json with another SHA-256 than the manifest has")
    seen: set[str] = set()
    for entry in manifest.get("files", []):
        path = str(entry.get("path", ""))
        if not HEX.match(str(entry.get("sha256", ""))):
            problems.append(f"malformed SHA-256 for {path!r}")
        if "size" in entry and not is_size(entry["size"]):
            problems.append(f"the size of {path!r} is not a whole number of bytes: {entry['size']!r}")
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
    parser.add_argument("--archive-members", type=Path, help="a downloaded archive whose content is checked without unpacking it")
    parser.add_argument("--consumer-manifest", type=Path, help="a copy of meshes.pack.json kept by another program, to compare with this one")
    args = parser.parse_args(list(argv))
    problems = check() if root is None else check(root)
    where = ROOT if root is None else root
    if args.archive is not None:
        problems += check_archive(args.archive, where)
    if args.extracted is not None:
        problems += check_extracted(args.extracted, where)
    if args.archive_members is not None:
        problems += check_archive_members(args.archive_members, where)
    if args.consumer_manifest is not None:
        problems += check_consumer_manifest(args.consumer_manifest, where)
    for line in problems:
        print("FAIL:", line)
    print("VERIFY_PACK=PASS" if not problems else "VERIFY_PACK=FAIL")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
