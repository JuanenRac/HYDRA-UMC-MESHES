# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

Mesh 3D condivise (STL e GLB) delle applicazioni desktop e web di HYDRA-UMC, pubblicate una sola volta come pacchetto di release invece di essere copiate in ogni repository.

## 📋 In breve

| | |
|---|---|
| Versione | `0.1.0` |
| Maturità | Funzionale |
| Test | 11 (`python -m pytest tests -q`) |
| Tecnologia | GLB / JSON / SHA-256 / STL |
| Su hardware reale | Non applicabile: nulla qui gira su hardware |

## 🚦 Stato del progetto

Ogni riga è una parte di questo repository e il semaforo dice a che punto è oggi. È scritta in base a ciò che il repository può mostrare (test, compilazioni, esecuzioni), non a ciò che è previsto.

🟢 Fatto e verificato · 🟡 Funziona, con limiti noti · 🟠 Fatto a metà o non ancora verificato · 🔴 Non fatto o non funzionante · ⚪ Non applicabile

| Area | Stato | Cosa significa qui |
|---|---|---|
| Software | 🟡 | Funziona per il suo scopo principale; la verifica di onestà qui sopra elenca ciò che manca ancora |
| Test | 🟢 | 11 test automatici, eseguiti a ogni modifica |
| Hardware reale | ⚪ | Non applicabile: nulla qui gira su hardware |
| Documentazione | 🟢 | README in otto lingue, verificato rispetto al manifesto a ogni modifica |

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
