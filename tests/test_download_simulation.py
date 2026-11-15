# =============================================================================
# HYDRA-UMC-MESHES - tests/test_download_simulation.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""evidence=simulator: the download of the mesh package, played on a disk. A real archive is made from a generator with a fixed seed (the same bytes on every run) and a
manifest that describes it; the download then fails in each way a download can fail (cut short, a bit flipped, padded, empty, absent) and so does the unpacking (a file
missing, cut, changed, a stray file, half the files), always one way at a time and in an order drawn from the seed. Each failure must be named, the repeat after an
interrupted download must be clean, and a package that arrives whole must say nothing. Nothing is downloaded from the network."""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import random
import sys
import tarfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import verify_pack

SEED = 20260101


def make_package(root: Path, rng: random.Random, files: int = 10) -> tuple[bytes, dict[str, bytes]]:
    """Writes the manifest and the checksum file of a package into `root` and returns the bytes of its archive and the content of each file."""
    content = {f"parts/{rng.choice(['arms', 'beds', 'heads'])}/part{n:03d}.stl": rng.randbytes(rng.randint(200, 3000)) for n in range(files)}
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", mtime=0) as packed, tarfile.open(fileobj=packed, mode="w") as tar:
        for path, data in content.items():
            info = tarfile.TarInfo(path)
            info.size = len(data)
            info.mtime = 0
            tar.addfile(info, io.BytesIO(data))
    archive = buffer.getvalue()
    digest = hashlib.sha256(archive).hexdigest()
    manifest = {
        "schema": 1,
        "pack": {"name": "hydra-umc-meshes", "revision": 1, "file": "hydra-umc-meshes-1.tgz", "sha256": digest, "size": len(archive)},
        "files": [{"path": path, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)} for path, data in content.items()],
    }
    (root / "meshes.pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    (root / "SHA256SUMS.txt").write_text(f"{digest}  hydra-umc-meshes-1.tgz\n", encoding="utf-8")
    return archive, content


def unpack(archive: Path, target: Path) -> None:
    with tarfile.open(archive) as tar:
        tar.extractall(target, filter="data")


def spoil_archive(archive: bytes, how: str, rng: random.Random) -> bytes | None:
    if how == "cut short":
        return archive[: rng.randint(1, len(archive) - 1)]
    if how == "bit flipped":
        data = bytearray(archive)
        data[rng.randrange(len(data))] ^= 1 << rng.randrange(8)
        return bytes(data)
    if how == "padded":
        return archive + rng.randbytes(rng.randint(1, 64))
    if how == "empty":
        return b""
    return None  # absent


def test_a_download_that_arrives_whole_and_is_unpacked_says_nothing(tmp_path: Path) -> None:
    rng = random.Random(SEED)
    for index in range(10):
        root = tmp_path / f"pack{index}"
        root.mkdir()
        archive, _ = make_package(root, rng, files=rng.randint(1, 40))
        downloaded = tmp_path / f"download{index}.tgz"
        downloaded.write_bytes(archive)
        out = tmp_path / f"out{index}"
        unpack(downloaded, out)
        assert verify_pack.check(root) == []
        assert verify_pack.check_archive(downloaded, root) == []
        assert verify_pack.check_extracted(out, root) == []


def test_every_way_a_download_fails_is_named_and_the_repeat_after_it_is_clean(tmp_path: Path) -> None:
    rng = random.Random(SEED)
    ways = ["cut short", "bit flipped", "padded", "empty", "absent"]
    order = ways * 6
    rng.shuffle(order)
    root = tmp_path / "pack"
    root.mkdir()
    archive, _ = make_package(root, rng)
    target = tmp_path / "download.tgz"
    for how in order:
        spoiled = spoil_archive(archive, how, rng)
        target.unlink(missing_ok=True)
        if spoiled is not None:
            target.write_bytes(spoiled)
        problems = verify_pack.check_archive(target, root)
        assert problems, how
        if how == "absent":
            assert problems == ["the archive download.tgz is missing"]
        elif how == "bit flipped":
            assert len(problems) == 1 and "SHA-256 of the archive" in problems[0]
        else:
            assert any("cut short or padded" in line for line in problems), (how, problems)
        # the retry of the same download arrives whole
        target.write_bytes(archive)
        assert verify_pack.check_archive(target, root) == [], how


def test_every_way_the_unpacking_fails_is_named_by_the_file_it_hit(tmp_path: Path) -> None:
    rng = random.Random(SEED + 1)
    root = tmp_path / "pack"
    root.mkdir()
    archive, content = make_package(root, rng, files=12)
    whole = tmp_path / "whole.tgz"
    whole.write_bytes(archive)
    names = list(content)
    for round_ in range(20):
        out = tmp_path / f"out{round_}"
        unpack(whole, out)
        victim = rng.choice(names)
        how = rng.choice(["missing", "cut", "changed", "stray", "half"])
        if how == "missing":
            (out / victim).unlink()
            assert verify_pack.check_extracted(out, root) == [f"missing: {victim}"]
        elif how == "cut":
            (out / victim).write_bytes(content[victim][:-1])
            assert verify_pack.check_extracted(out, root) == [f"wrong size: {victim}"]
        elif how == "changed":
            data = bytearray(content[victim])
            data[0] ^= 0xFF
            (out / victim).write_bytes(bytes(data))
            assert verify_pack.check_extracted(out, root) == [f"wrong SHA-256: {victim}"]
        elif how == "stray":
            (out / "parts").mkdir(exist_ok=True)
            (out / "parts" / "stray.stl").write_bytes(b"solid")
            assert verify_pack.check_extracted(out, root) == ["not in the manifest: parts/stray.stl"]
        else:
            gone = names[len(names) // 2 :]
            for path in gone:
                (out / path).unlink()
            assert verify_pack.check_extracted(out, root) == [f"missing: {path}" for path in gone]


def test_a_folder_with_nothing_in_it_misses_every_file(tmp_path: Path) -> None:
    root = tmp_path / "pack"
    root.mkdir()
    _, content = make_package(root, random.Random(SEED), files=4)
    empty = tmp_path / "empty"
    empty.mkdir()
    assert verify_pack.check_extracted(empty, root) == [f"missing: {path}" for path in content]


def test_a_manifest_path_that_leaves_the_package_is_never_read_when_checking_the_folder(tmp_path: Path) -> None:
    root = tmp_path / "pack"
    root.mkdir()
    make_package(root, random.Random(SEED), files=2)
    manifest = json.loads((root / "meshes.pack.json").read_text(encoding="utf-8"))
    manifest["files"].append({"path": "../outside.stl", "sha256": "0" * 64, "size": 1})
    (root / "meshes.pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    secret = tmp_path / "outside.stl"
    secret.write_bytes(b"x")
    out = tmp_path / "out"
    out.mkdir()
    problems = verify_pack.check_extracted(out, root)
    assert "path outside the package: '../outside.stl'" in problems
    assert not any("wrong" in line for line in problems)


def test_the_command_line_checks_the_archive_and_the_folder_and_exits_with_the_result(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "pack"
    root.mkdir()
    archive, _ = make_package(root, random.Random(SEED), files=3)
    good = tmp_path / "good.tgz"
    good.write_bytes(archive)
    out = tmp_path / "out"
    unpack(good, out)
    assert verify_pack.main(["--archive", str(good), "--extracted", str(out)], root) == 0
    assert "VERIFY_PACK=PASS" in capsys.readouterr().out
    good.write_bytes(archive[:-3])
    (out / "stray.stl").write_bytes(b"solid")
    assert verify_pack.main(["--archive", str(good), "--extracted", str(out)], root) == 1
    printed = capsys.readouterr().out
    assert "FAIL:" in printed and "VERIFY_PACK=FAIL" in printed and "not in the manifest: stray.stl" in printed
