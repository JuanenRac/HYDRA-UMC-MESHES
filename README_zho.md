# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

HYDRA-UMC 桌面和网页应用共用的 3D 网格（STL 和 GLB），以发布包的形式只发布一次，而不是复制到每个仓库。

## 这是什么

发布 `meshes-1` 包含 `hydra-umc-meshes-1.tgz`：每个不同的网格只存储一次，并附带清单（`meshes.pack.json`），列出该包和每个文件的 SHA-256。

## 谁在使用

HYDRA-UMC-STUDIO 和 HYDRA-UMC-SUITE 按需下载，并在写入任何内容之前对照清单校验每个文件（仅 https，校验哈希，路径限制在目标文件夹内）。

## 手动校验

将下载文件的 SHA-256 与 `SHA256SUMS.txt` 比较：

```
cbba8a5eccb97ad2017acc7d01a936999ec6bc99f8858921cc110ccc76ebb375  hydra-umc-meshes-1.tgz
```

## 许可证

GPL-3.0-or-later。参见 LICENSE。
