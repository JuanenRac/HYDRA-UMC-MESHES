# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

Maillages 3D partagés (STL et GLB) des applications de bureau et web de HYDRA-UMC, publiés une seule fois comme paquet de release au lieu d'être copiés dans chaque dépôt.

## 📋 En un coup d'œil

| | |
|---|---|
| Version | `0.1.0` |
| Maturité | Fonctionnel |
| Tests | 11 (`python -m pytest tests -q`) |
| Technologie | GLB / JSON / SHA-256 / STL |
| Sur matériel réel | Sans objet : rien ici ne s'exécute sur du matériel |

## 🚦 État du projet

Chaque ligne est une partie de ce dépôt et le feu dit où elle en est aujourd'hui. Elle est écrite d'après ce que le dépôt peut montrer (tests, compilations, exécutions), pas d'après ce qui est prévu.

🟢 Fait et vérifié · 🟡 Fonctionne, avec des limites connues · 🟠 À moitié fait ou pas encore vérifié · 🔴 Pas fait ou ne fonctionne pas · ⚪ Sans objet

| Domaine | État | Ce que cela veut dire ici |
|---|---|---|
| Logiciel | 🟡 | Fonctionne pour son usage principal ; la vérification d'honnêteté ci-dessus liste ce qui manque encore |
| Tests | 🟢 | 11 tests automatiques, exécutés à chaque modification |
| Matériel réel | ⚪ | Sans objet : rien ici ne s'exécute sur du matériel |
| Documentation | 🟢 | README en huit langues, vérifié par rapport au manifeste à chaque modification |

## Ce que c'est

La release `meshes-1` contient `hydra-umc-meshes-1.tgz` : chaque maillage distinct stocké une seule fois, avec un manifeste (`meshes.pack.json`) qui liste le SHA-256 du paquet et de chaque fichier.

## Qui l'utilise

HYDRA-UMC-STUDIO et HYDRA-UMC-SUITE le téléchargent à la demande et vérifient chaque fichier par rapport au manifeste avant d'écrire quoi que ce soit (https uniquement, hash vérifié, chemins confinés au dossier cible).

## Vérifier à la main

Comparez le SHA-256 du fichier téléchargé avec `SHA256SUMS.txt` :

```
cbba8a5eccb97ad2017acc7d01a936999ec6bc99f8858921cc110ccc76ebb375  hydra-umc-meshes-1.tgz
```

## Licence

GPL-3.0-or-later. Voir LICENSE.
