# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

Mesh 3D condivise (STL e GLB) delle applicazioni desktop e web di HYDRA-UMC, pubblicate una sola volta come pacchetto di release invece di essere copiate in ogni repository.

## Cos'è

La release `meshes-1` contiene `hydra-umc-meshes-1.tgz`: ogni mesh distinta memorizzata una sola volta, con un manifesto (`meshes.pack.json`) che elenca lo SHA-256 del pacchetto e di ogni file.

## Chi lo usa

HYDRA-UMC-STUDIO e HYDRA-UMC-SUITE lo scaricano su richiesta e verificano ogni file rispetto al manifesto prima di scrivere qualsiasi cosa (solo https, hash verificato, percorsi confinati alla cartella di destinazione).

## Verifica a mano

Confronta lo SHA-256 del file scaricato con `SHA256SUMS.txt`:

```
cbba8a5eccb97ad2017acc7d01a936999ec6bc99f8858921cc110ccc76ebb375  hydra-umc-meshes-1.tgz
```

## Licenza

GPL-3.0-or-later. Vedi LICENSE.
