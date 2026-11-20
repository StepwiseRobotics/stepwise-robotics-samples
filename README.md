# Stepwise Robotics Samples

GPUがなくても、クラウドで一歩ずつ始めるロボット学習のサンプルコード集です。
Zennの記事・本「Stepwise Robotics」と連動しています。

> **English:** Step-by-step sample code for learning robot simulation and robot learning
> (NVIDIA Isaac Sim / Isaac Lab) on cloud GPUs, without a local GPU.

[![CI](https://github.com/StepwiseRobotics/stepwise-robotics-samples/actions/workflows/ci.yml/badge.svg)](https://github.com/StepwiseRobotics/stepwise-robotics-samples/actions/workflows/ci.yml)

## 構成

| フォルダ | 内容 |
|---|---|
| `examples/` | 記事・本ごとのサンプル（番号順に進める） |
| `src/stepwise_samples/` | サンプルで共通して使うユーティリティ |
| `tests/` | GPUなしで実行できるテスト |
| `tools/` | 公開前チェックなどの補助スクリプト |

## 動作環境

| 項目 | 内容 |
|---|---|
| 対象 | Isaac Sim 6.2 / Isaac Lab 3.0（各サンプルのREADMEに対象バージョンを明記） |
| GPU | RTコア付きのNVIDIA RTX GPU（例：AWS g6e.xlarge の L40S） |
| Python | 3.11 |

GPUが必要なサンプルは、クラウドGPUでの実行を前提にしています。
費用の目安と、使い終わったあとの停止方法も各サンプルのREADMEに書いています。

## はじめかた

```bash
git clone https://github.com/StepwiseRobotics/stepwise-robotics-samples.git
cd stepwise-robotics-samples
pip install -e ".[dev]"
pytest
```

## サンプル一覧

| # | サンプル | 関連する記事 | 状態 |
|---|---|---|---|
| 00 | クラウドGPUの費用見積もり（`stepwise_samples.cloud_cost`） | 準備中 | ✅ |
| 01 | AWSでIsaac Sim / Isaac Labを立ち上げる | 準備中 | 🚧 |

## ライセンス

[MIT License](LICENSE)

NVIDIA Isaac Sim / Isaac Lab などの外部ソフトウェアは、それぞれのライセンスに従います。
このリポジトリは個人の学習・解説を目的としたもので、NVIDIAとは関係ありません。
