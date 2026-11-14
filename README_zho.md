# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

HYDRA-UMC 桌面和网页应用共用的 3D 网格（STL 和 GLB），以发布包的形式只发布一次，而不是复制到每个仓库。

## 📋 速览

| | |
|---|---|
| 版本 | `0.1.0` |
| 成熟度 | 可用 |
| 测试 | 11 (`python -m pytest tests -q`) |
| 技术栈 | GLB / JSON / SHA-256 / STL |
| 真实硬件 | 不适用：这里的内容不在硬件上运行 |

## 🚦 项目状态

每一行是本仓库的一个部分，灯号表示它今天做到了哪一步。内容依据仓库能够展示的证据（测试、构建、运行），而不是计划。

🟢 已完成并验证 · 🟡 可用，有已知限制 · 🟠 部分完成或尚未验证 · 🔴 未完成或不可用 · ⚪ 不适用

| 领域 | 状态 | 在这里的含义 |
|---|---|---|
| 软件 | 🟡 | 主要用途可用；上面的诚实性检查列出了仍然缺少的内容 |
| 测试 | 🟢 | 11 项自动测试，每次变更都会运行 |
| 真实硬件 | ⚪ | 不适用：这里的内容不在硬件上运行 |
| 文档 | 🟢 | 八种语言的 README，每次变更都会与清单核对 |

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
