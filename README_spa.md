# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

Mallas 3D compartidas (STL y GLB) de las aplicaciones de escritorio y web de HYDRA-UMC, publicadas una sola vez como paquete de release en lugar de copiarlas en cada repositorio.

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
