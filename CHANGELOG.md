# Changelog

## [Unreleased]

- **The check of the package manifest also checks the sizes and the download address:** the size of the archive and of every file, when given, must be a whole number of bytes (zero or more; a boolean, a fraction, a negative or a text is named), and the download address of the archive must be an https address with a host, without credentials, query or fragment, whose last path part is the archive name. The check reads the address as a URL (it does not search the text). Tests cover each case.
- **The check of the package manifest refuses more bad paths:** a path with a backslash that climbs out of the package (`a\..\..\x`) is refused on Linux as it would be on Windows, as are an empty path, an empty or `.` component, and two paths that differ only in case (they clash on Windows and macOS); tests cover each.
- **The download of the package can be checked on the disk, and its failures are simulated:** `tools/verify_pack.py --archive FILE` checks a downloaded archive against the manifest (present, the size, the SHA-256) and `--extracted DIR` checks the folder it was unpacked into (every file present, of the size and the SHA-256 the manifest says, and no file the manifest does not list). `tests/test_download_simulation.py` makes a real archive from a generator with a fixed seed and fails the download in every way a download fails (cut short, a bit flipped, padded, empty, absent) and the unpacking in every way an unpacking fails (a file missing, cut, changed, a stray file, half the files), in an order drawn from the seed; each failure is named, the repeat after an interrupted download is clean and a package that arrives whole says nothing. The evidence level is `simulator`; a download of the real package from the release by the apps stays pending.

- **The check of the package manifest is tested:** `tests/test_verify_pack.py` runs it on thirty packages made by a generator with a fixed seed (it says nothing about a package that is not damaged) and on the same packages damaged one way at a time (a malformed hash, a path that leaves the package, a path twice, a checksum file that names another archive or another hash, an archive without a name, a manifest with no files), and requires every damage to be named. The workflow "Package tests" runs them on every change under line and branch coverage and holds a floor of 95 % on `tools/verify_pack.py`.

- **The repository has a security policy:** `SECURITY.md` says where to report a vulnerability privately, like every repository of the ecosystem.

## [0.1.0] - The first revision of the shared mesh package

- **One package for the meshes of the desktop and web apps:** the release `meshes-1` carries one archive with every distinct STL and GLB mesh stored once, and a manifest with the SHA-256 of the archive and of each file.
- **A check of the manifest:** `tools/verify_pack.py` confirms that the manifest and the checksum file agree and that no path leaves the package; the CI runs it.
