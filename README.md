# 登板日予測Bot

千葉ロッテマリーンズの投手の登板日を予測し、Slack等への通知を行うBot

## 📁 ディレクトリ構成

```
yokoyama-bot/
├── scraper/           # スクレイピング処理（SPAIAから登板記録取得）
│   └── fetch_spaia_log.py
├── data/             # 収集したCSVなどの生データ
│   └── yokoyama_spaia_log.csv
├── ml/               # モデルの学習・予測スクリプト
│   ├── train_model.py
│   └── predict_next_day.py
├── notifier/         # 通知処理（Slack / LINE）
│   └── notify.go
├── scheduler/        # 定期実行設定（cronやGitHub Actionsなど）
├── .env             # 通知用のトークンなど（gitには含めない）
└── README.md
```

## 🚀 初期セットアップ

git clone <リポジトリ名>
cd yokoyama-bot
pip install -r requirements.txt

## ライセンスについて

このリポジトリは再配布および商用利用を禁止しています。
