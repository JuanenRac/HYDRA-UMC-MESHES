# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

Gemeinsame 3D-Netze (STL und GLB) der Desktop- und Web-Apps von HYDRA-UMC, einmal als Release-Paket veröffentlicht, statt in jedes Repository kopiert zu werden.

## 📋 Auf einen Blick

| | |
|---|---|
| Version | `0.1.0` |
| Reifegrad | Funktionsfähig |
| Tests | 11 (`python -m pytest tests -q`) |
| Technik | GLB / JSON / SHA-256 / STL |
| Auf echter Hardware | Nicht zutreffend: nichts hiervon läuft auf Hardware |

## 🚦 Projektstatus

Jede Zeile ist ein Teil dieses Repositorys, und die Ampel sagt, wie weit er heute ist. Sie beruht auf dem, was das Repository zeigen kann (Tests, Builds, Läufe), nicht auf dem, was geplant ist.

🟢 Fertig und überprüft · 🟡 Funktioniert, mit bekannten Grenzen · 🟠 Teilweise fertig oder noch nicht überprüft · 🔴 Nicht gemacht oder funktioniert nicht · ⚪ Nicht zutreffend

| Bereich | Stand | Was das hier bedeutet |
|---|---|---|
| Software | 🟡 | Funktioniert für seinen Hauptzweck; die Ehrlichkeitsprüfung oben nennt, was noch fehlt |
| Tests | 🟢 | 11 automatische Tests, bei jeder Änderung ausgeführt |
| Echte Hardware | ⚪ | Nicht zutreffend: nichts hiervon läuft auf Hardware |
| Dokumentation | 🟢 | README in acht Sprachen, bei jeder Änderung gegen das Manifest geprüft |

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
