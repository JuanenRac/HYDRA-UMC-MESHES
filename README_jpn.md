# HYDRA-UMC-MESHES

[English](README.md) · [Español](README_spa.md) · [Deutsch](README_deu.md) · [Français](README_fra.md) · [Italiano](README_ita.md) · [日本語](README_jpn.md) · [中文](README_zho.md) · [Português](README_por.md)

HYDRA-UMC のデスクトップアプリとウェブアプリで共有する 3D メッシュ（STL と GLB）。各リポジトリにコピーする代わりに、リリースパッケージとして一度だけ公開します。

## 概要

リリース `meshes-1` には `hydra-umc-meshes-1.tgz` が含まれます。異なるメッシュを 1 つずつ保存し、パッケージと各ファイルの SHA-256 を列挙するマニフェスト（`meshes.pack.json`）が付きます。

## 利用者

HYDRA-UMC-STUDIO と HYDRA-UMC-SUITE が必要に応じてダウンロードし、何かを書き込む前にマニフェストと照合して各ファイルを検証します（https のみ、ハッシュ確認、パスは保存先フォルダ内に限定）。

## 手動での確認

ダウンロードしたファイルの SHA-256 を `SHA256SUMS.txt` と比較してください:

```
cbba8a5eccb97ad2017acc7d01a936999ec6bc99f8858921cc110ccc76ebb375  hydra-umc-meshes-1.tgz
```

## ライセンス

GPL-3.0-or-later。LICENSE を参照してください。
