# Changelog

## [Unreleased]

- **The check of the package manifest is tested:** `tests/test_verify_pack.py` runs it on thirty packages made by a generator with a fixed seed (it says nothing about a package that is not damaged) and on the same packages damaged one way at a time (a malformed hash, a path that leaves the package, a path twice, a checksum file that names another archive or another hash, an archive without a name, a manifest with no files), and requires every damage to be named. The workflow "Package tests" runs them on every change under line and branch coverage and holds a floor of 95 % on `tools/verify_pack.py`.

- **The repository has a security policy:** `SECURITY.md` says where to report a vulnerability privately, like every repository of the ecosystem.

## [0.1.0] - The first revision of the shared mesh package

- **One package for the meshes of the desktop and web apps:** the release `meshes-1` carries one archive with every distinct STL and GLB mesh stored once, and a manifest with the SHA-256 of the archive and of each file.
- **A check of the manifest:** `tools/verify_pack.py` confirms that the manifest and the checksum file agree and that no path leaves the package; the CI runs it.
