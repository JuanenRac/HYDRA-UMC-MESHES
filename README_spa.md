# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

Mallas 3D compartidas (STL y GLB) de las aplicaciones de escritorio y web de HYDRA-UMC, publicadas una sola vez como paquete de release en lugar de copiarlas en cada repositorio.

## 📋 De un vistazo

| | |
|---|---|
| Versión | `0.1.0` |
| Madurez | Funcional |
| Tests | 11 (`python -m pytest tests -q`) |
| Tecnología | GLB / JSON / SHA-256 / STL |
| En hardware real | No aplica: nada de esto se ejecuta en hardware |

## 🚦 Estado del proyecto

Cada línea es una parte de este repositorio y la luz dice hasta dónde llega hoy. Se escribe con lo que el repositorio puede demostrar (pruebas, compilaciones, ejecuciones), no con lo previsto.

🟢 Hecho y verificado · 🟡 Funciona, con límites conocidos · 🟠 Hecho a medias o sin verificar · 🔴 Sin hacer o sin funcionar · ⚪ No aplica

| Área | Estado | Qué significa aquí |
|---|---|---|
| Software | 🟡 | Funciona para su propósito principal; la comprobación de honestidad de arriba lista lo que aún falta |
| Pruebas | 🟢 | 11 pruebas automáticas, ejecutadas en cada cambio |
| Hardware real | ⚪ | No aplica: nada de esto se ejecuta en hardware |
| Documentación | 🟢 | README en ocho idiomas, comprobado contra el manifiesto en cada cambio |

## Qué es

La release `meshes-1` lleva `hydra-umc-meshes-1.tgz`: cada malla distinta guardada una sola vez, con un manifiesto (`meshes.pack.json`) que lista el SHA-256 del paquete y de cada fichero.

## Quién lo usa

HYDRA-UMC-STUDIO y HYDRA-UMC-SUITE lo descargan cuando hace falta y verifican cada fichero contra el manifiesto antes de escribir nada (solo https, hash comprobado, rutas confinadas a la carpeta de destino).

## Verificar a mano

Compara el SHA-256 del fichero descargado con `SHA256SUMS.txt`:

```
cbba8a5eccb97ad2017acc7d01a936999ec6bc99f8858921cc110ccc76ebb375  hydra-umc-meshes-1.tgz
```

## Licencia

GPL-3.0-or-later. Consulta LICENSE.
