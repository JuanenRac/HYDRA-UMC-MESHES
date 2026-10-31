# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

Maillages 3D partagés (STL et GLB) des applications de bureau et web de HYDRA-UMC, publiés une seule fois comme paquet de release au lieu d'être copiés dans chaque dépôt.

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
