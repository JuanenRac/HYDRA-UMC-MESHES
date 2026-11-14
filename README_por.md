# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

Malhas 3D partilhadas (STL e GLB) das aplicações de ambiente de trabalho e web do HYDRA-UMC, publicadas uma só vez como pacote de release em vez de serem copiadas para cada repositório.

## 📋 Num relance

| | |
|---|---|
| Versão | `0.1.0` |
| Maturidade | Funcional |
| Testes | 11 (`python -m pytest tests -q`) |
| Tecnologia | GLB / JSON / SHA-256 / STL |
| Em hardware real | Não aplicável: nada aqui corre em hardware |

## 🚦 Estado do projeto

Cada linha é uma parte deste repositório e a luz diz até onde chega hoje. É escrita com o que o repositório consegue demonstrar (testes, compilações, execuções), não com o que está previsto.

🟢 Feito e verificado · 🟡 Funciona, com limites conhecidos · 🟠 Feito a meio ou ainda por verificar · 🔴 Por fazer ou a não funcionar · ⚪ Não aplicável

| Área | Estado | O que significa aqui |
|---|---|---|
| Software | 🟡 | Funciona para o seu propósito principal; a verificação de honestidade acima lista o que ainda falta |
| Testes | 🟢 | 11 testes automáticos, executados a cada alteração |
| Hardware real | ⚪ | Não aplicável: nada aqui corre em hardware |
| Documentação | 🟢 | README em oito idiomas, verificado contra o manifesto a cada alteração |

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
