# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

Malhas 3D partilhadas (STL e GLB) das aplicações de ambiente de trabalho e web do HYDRA-UMC, publicadas uma só vez como pacote de release em vez de serem copiadas para cada repositório.

## O que é

A release `meshes-1` inclui `hydra-umc-meshes-1.tgz`: cada malha distinta guardada uma só vez, com um manifesto (`meshes.pack.json`) que lista o SHA-256 do pacote e de cada ficheiro.

## Quem o utiliza

O HYDRA-UMC-STUDIO e o HYDRA-UMC-SUITE descarregam-no quando é necessário e verificam cada ficheiro contra o manifesto antes de escrever o que quer que seja (apenas https, hash verificado, caminhos confinados à pasta de destino).

## Verificar manualmente

Compare o SHA-256 do ficheiro descarregado com `SHA256SUMS.txt`:

```
cbba8a5eccb97ad2017acc7d01a936999ec6bc99f8858921cc110ccc76ebb375  hydra-umc-meshes-1.tgz
```

## Licença

GPL-3.0-or-later. Consulte LICENSE.
