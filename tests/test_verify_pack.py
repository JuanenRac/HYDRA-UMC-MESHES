# =============================================================================
# HYDRA-UMC-MESHES - tests/test_verify_pack.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The check of the package manifest against its checksum file, run on packages made by a generator with a fixed seed and on the same packages damaged one way at a
time: a malformed hash, a path that leaves the package, a path twice, a checksum file that names another archive or another hash, a manifest with no files. The check
must name every damage and must say nothing about a package that is not damaged. The real manifest of this repository is checked too."""
from __future__ import annotations

import hashlib
import json
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import verify_pack

SEED = 20260101


def make_pack(root: Path, rng: random.Random, files: int = 12) -> dict:
    archive = f"hydra-umc-meshes-{rng.randint(1, 99)}.tgz"
    digest = hashlib.sha256(rng.randbytes(64)).hexdigest()
    manifest = {
        "schema": 1,
        "pack": {"name": "hydra-umc-meshes", "revision": 1, "file": archive, "sha256": digest},
        "files": [
            {"path": f"parts/{rng.choice(['arms', 'beds', 'heads'])}/part{index:03d}.stl", "sha256": hashlib.sha256(rng.randbytes(16)).hexdigest(), "size": rng.randint(100, 10**6)}
            for index in range(files)
        ],
    }
    (root / "meshes.pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    (root / "SHA256SUMS.txt").write_text(f"{digest}  {archive}\n", encoding="utf-8")
    return manifest


def rewrite(root: Path, change) -> None:
    manifest = json.loads((root / "meshes.pack.json").read_text(encoding="utf-8"))
    change(manifest)
    (root / "meshes.pack.json").write_text(json.dumps(manifest), encoding="utf-8")


def test_the_real_manifest_of_this_repository_is_consistent():
    assert verify_pack.check() == []
    assert verify_pack.main() == 0


def test_a_package_that_is_not_damaged_says_nothing_whatever_it_holds(tmp_path: Path):
    rng = random.Random(SEED)
    for index in range(30):
        root = tmp_path / f"pack{index}"
        root.mkdir()
        make_pack(root, rng, files=rng.randint(1, 80))
        assert verify_pack.check(root) == [], index


@pytest.mark.parametrize("bad", ["", "xyz", "ABCDEF" * 11, "a" * 63, "a" * 65, "g" * 64, None, 12345])
def test_a_malformed_hash_of_a_file_is_named_with_its_path(tmp_path: Path, bad):
    make_pack(tmp_path, random.Random(SEED))
    rewrite(tmp_path, lambda m: m["files"][3].__setitem__("sha256", bad))
    problems = verify_pack.check(tmp_path)
    assert len(problems) == 1 and problems[0].startswith("malformed SHA-256 for") and m_path(tmp_path, 3) in problems[0]


def m_path(root: Path, index: int) -> str:
    return json.loads((root / "meshes.pack.json").read_text(encoding="utf-8"))["files"][index]["path"]


@pytest.mark.parametrize("path", ["/etc/passwd", "\\windows\\system32", "../outside.stl", "parts/../../outside.stl", "C:/x.stl", "parts/a:b.stl"])
def test_a_path_that_leaves_the_package_is_named(tmp_path: Path, path: str):
    make_pack(tmp_path, random.Random(SEED))
    rewrite(tmp_path, lambda m: m["files"][0].__setitem__("path", path))
    assert any(problem.startswith("path outside the package") and repr(path) in problem for problem in verify_pack.check(tmp_path))


def test_a_path_listed_twice_is_named_once_for_each_repeat(tmp_path: Path):
    make_pack(tmp_path, random.Random(SEED))
    rewrite(tmp_path, lambda m: (m["files"].append(dict(m["files"][2])), m["files"].append(dict(m["files"][2]))))
    problems = verify_pack.check(tmp_path)
    assert problems.count(f"duplicate path: {m_path(tmp_path, 2)!r}") == 2


def test_a_checksum_file_that_names_another_archive_or_another_hash_is_named(tmp_path: Path):
    rng = random.Random(SEED)
    manifest = make_pack(tmp_path, rng)
    archive, digest = manifest["pack"]["file"], manifest["pack"]["sha256"]
    (tmp_path / "SHA256SUMS.txt").write_text(f"{digest}  other.tgz\n", encoding="utf-8")
    assert verify_pack.check(tmp_path) == [f"SHA256SUMS.txt does not list {archive} with the SHA-256 of the manifest"]
    (tmp_path / "SHA256SUMS.txt").write_text(f"{'0' * 64}  {archive}\n", encoding="utf-8")
    assert len(verify_pack.check(tmp_path)) == 1
    (tmp_path / "SHA256SUMS.txt").write_text("", encoding="utf-8")
    assert len(verify_pack.check(tmp_path)) == 1


def test_a_checksum_file_with_blank_lines_and_other_archives_is_still_read(tmp_path: Path):
    manifest = make_pack(tmp_path, random.Random(SEED))
    archive, digest = manifest["pack"]["file"], manifest["pack"]["sha256"]
    (tmp_path / "SHA256SUMS.txt").write_text(f"\n{'1' * 64}  old.tgz\n\n   \n{digest}  {archive}\n", encoding="utf-8")
    assert verify_pack.check(tmp_path) == []


@pytest.mark.parametrize("pack", [{}, {"file": "a.tgz"}, {"sha256": "a" * 64}, {"file": "", "sha256": "a" * 64}, {"file": "a.tgz", "sha256": "nothex"}, {"file": "a.tgz", "sha256": None}])
def test_an_archive_without_a_name_or_with_a_malformed_hash_is_named(tmp_path: Path, pack: dict):
    make_pack(tmp_path, random.Random(SEED))
    rewrite(tmp_path, lambda m: m.__setitem__("pack", pack))
    assert "the manifest has no archive name or a malformed archive SHA-256" in verify_pack.check(tmp_path)


def test_a_manifest_with_no_files_is_named(tmp_path: Path):
    make_pack(tmp_path, random.Random(SEED))
    rewrite(tmp_path, lambda m: m.__setitem__("files", []))
    assert verify_pack.check(tmp_path) == ["the manifest lists no files"]
    rewrite(tmp_path, lambda m: m.pop("files"))
    assert verify_pack.check(tmp_path) == ["the manifest lists no files"]


def test_every_damage_made_at_once_is_named_one_by_one_and_the_command_fails(tmp_path: Path, monkeypatch, capsys):
    make_pack(tmp_path, random.Random(SEED))
    rewrite(tmp_path, lambda m: (m["files"][0].__setitem__("sha256", "x"), m["files"][1].__setitem__("path", "../a"), m["files"].append(dict(m["files"][2]))))
    (tmp_path / "SHA256SUMS.txt").write_text("", encoding="utf-8")
    problems = verify_pack.check(tmp_path)
    assert len(problems) == 4
    monkeypatch.setattr(verify_pack, "check", lambda: problems)
    assert verify_pack.main() == 1
    out = capsys.readouterr().out
    assert "VERIFY_PACK=FAIL" in out and out.count("FAIL:") == 4


def test_a_manifest_that_is_not_json_or_a_missing_file_is_an_error_and_not_a_pass(tmp_path: Path):
    make_pack(tmp_path, random.Random(SEED))
    (tmp_path / "meshes.pack.json").write_text("{", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        verify_pack.check(tmp_path)
    (tmp_path / "meshes.pack.json").unlink()
    with pytest.raises(FileNotFoundError):
        verify_pack.check(tmp_path)
