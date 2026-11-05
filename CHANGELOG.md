# Changelog

## [Unreleased]

- **The repository has a security policy:** `SECURITY.md` says where to report a vulnerability privately, like every repository of the ecosystem.

## [0.1.0] - The first revision of the shared mesh package

- **One package for the meshes of the desktop and web apps:** the release `meshes-1` carries one archive with every distinct STL and GLB mesh stored once, and a manifest with the SHA-256 of the archive and of each file.
- **A check of the manifest:** `tools/verify_pack.py` confirms that the manifest and the checksum file agree and that no path leaves the package; the CI runs it.
