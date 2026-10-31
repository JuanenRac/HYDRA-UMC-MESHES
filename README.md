# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

Shared 3D meshes (STL and GLB) of the HYDRA-UMC desktop and web apps, published once as a release package instead of being copied into each repository.

## What it is

The release `meshes-1` carries `hydra-umc-meshes-1.tgz`: every distinct mesh stored once, with a manifest (`meshes.pack.json`) that lists the SHA-256 of the package and of each file.

## Who uses it

HYDRA-UMC-STUDIO and HYDRA-UMC-SUITE download it on demand and verify every file against the manifest before writing anything (https only, hash checked, paths confined to the target folder).

## Verify by hand

Compare the SHA-256 of the downloaded file with `SHA256SUMS.txt`:

```
cbba8a5eccb97ad2017acc7d01a936999ec6bc99f8858921cc110ccc76ebb375  hydra-umc-meshes-1.tgz
```

## Licence

GPL-3.0-or-later. See LICENSE.
