# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

Gemeinsame 3D-Netze (STL und GLB) der Desktop- und Web-Apps von HYDRA-UMC, einmal als Release-Paket veröffentlicht, statt in jedes Repository kopiert zu werden.

## Was es ist

Das Release `meshes-1` enthält `hydra-umc-meshes-1.tgz`: jedes verschiedene Netz einmal gespeichert, mit einem Manifest (`meshes.pack.json`), das den SHA-256 des Pakets und jeder Datei auflistet.

## Wer es nutzt

HYDRA-UMC-STUDIO und HYDRA-UMC-SUITE laden es bei Bedarf herunter und prüfen jede Datei gegen das Manifest, bevor etwas geschrieben wird (nur https, Hash geprüft, Pfade auf den Zielordner beschränkt).

## Von Hand prüfen

Vergleiche den SHA-256 der heruntergeladenen Datei mit `SHA256SUMS.txt`:

```
cbba8a5eccb97ad2017acc7d01a936999ec6bc99f8858921cc110ccc76ebb375  hydra-umc-meshes-1.tgz
```

## Lizenz

GPL-3.0-or-later. Siehe LICENSE.
