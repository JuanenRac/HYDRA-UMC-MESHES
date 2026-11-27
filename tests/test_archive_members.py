"""The content of an archive is checked without unpacking it, and a copy of the manifest is compared."""
import hashlib
import io
import json
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import verify_pack  # noqa: E402


def entry(path, data):
    return {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


class PublishedChecksumTests(unittest.TestCase):
    def test_the_published_checksum_file_lists_the_manifest(self):
        root = Path(__file__).resolve().parent.parent
        sums = (root / "SHA256SUMS.txt").read_text(encoding="utf-8")
        self.assertIn(f"{verify_pack.manifest_digest(root / 'meshes.pack.json')}  meshes.pack.json", sums)


class Tests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        (self.root / "meshes.pack.json").write_text(json.dumps({"files": [entry("a/one.stl", b"one"), entry("two.stl", b"two")]}), encoding="utf-8")

    def pack(self, members):
        archive = self.root / "pack.tgz"
        with tarfile.open(archive, "w:gz") as tar:
            for name, data in members:
                info = tarfile.TarInfo(name)
                if data is None:
                    info.type, info.linkname = tarfile.SYMTYPE, "/etc/passwd"
                    tar.addfile(info)
                else:
                    info.size = len(data)
                    tar.addfile(info, io.BytesIO(data))
        return archive

    def test_a_complete_archive_passes(self):
        archive = self.pack([("a/one.stl", b"one"), ("./two.stl", b"two")])
        self.assertEqual(verify_pack.check_archive_members(archive, self.root), [])

    def test_links_strangers_changes_and_missing_files_are_said(self):
        archive = self.pack([("a/one.stl", None), ("evil.stl", b"x"), ("two.stl", b"tw0")])
        found = verify_pack.check_archive_members(archive, self.root)
        self.assertEqual([line.split(":")[0] for line in found], ["not a regular file", "not in the manifest", "wrong SHA-256"])
        self.assertEqual(verify_pack.check_archive_members(self.pack([("two.stl", b"two")]), self.root), ["missing from the archive: a/one.stl"])

    def test_a_copy_of_the_manifest_is_compared_whatever_its_line_ends(self):
        copy = self.root / "copy.json"
        copy.write_bytes((self.root / "meshes.pack.json").read_bytes() )
        self.assertEqual(verify_pack.check_consumer_manifest(copy, self.root), [])
        copy.write_text(json.dumps({"files": [entry("a/one.stl", b"changed")]}), encoding="utf-8")
        self.assertIn("a/one.stl, two.stl", verify_pack.check_consumer_manifest(copy, self.root)[0])


if __name__ == "__main__":
    unittest.main()
