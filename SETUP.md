# ニュース通知ボット セットアップ手順

GitHub Actions + Claude API + ntfy.sh でスマホへ毎日ニュースを通知します。

---

## ファイル構成

```
your-repo/
├── news_summary.py           ← メインスクリプト
└── .github/
    └── workflows/
        └── news.yml          ← GitHub Actions 設定
```

---

## セットアップ手順

### 1. GitHub リポジトリを作成

1. [github.com](https://github.com) で新規リポジトリを作成（名前は任意、Private でもOK）
2. `news_summary.py` と `.github/workflows/news.yml` をプッシュ

```bash
git init
git add .
git commit -m "初回コミット"
git remote add origin https://github.com/あなたのユーザー名/リポジトリ名.git
git push -u origin main
```

---

### 2. Anthropic API キーを取得

1. [console.anthropic.com](https://console.anthropic.com) にアクセス
2. **API Keys** → **Create Key** でキーを発行
3. `sk-ant-...` の形式のキーをコピーして保管

---

### 3. ntfy.sh チャンネル名を決める

1. スマホに **ntfy** アプリをインストール（iOS / Android 両対応・無料）
2. 任意のチャンネル名を決める（例: `takuya-news-20260314`）
   - **ランダム文字列を入れると他人に傍受されにくくなります**
3. アプリでそのチャンネルを「Subscribe」（購読）する

---

### 4. GitHub Secrets に登録

リポジトリページ → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| シークレット名       | 値                                |
|-----------------|-----------------------------------|
| `ANTHROPIC_API_KEY` | `sk-ant-...` （Claudeの APIキー）  |
| `NTFY_TOPIC`        | `takuya-news-20260314` （自分で決めたチャンネル名） |

---

### 5. 動作確認（手動実行）

リポジトリページ → **Actions** → **News Summary Notification** → **Run workflow**

ログに「✅ 通知送信完了」と表示されれば成功です。

---

## カスタマイズ

### ニュースのカテゴリを変える

`news_summary.py` の `NEWS_TOPICS` リストを編集してください。

```python
NEWS_TOPICS = [
    "日本の最新ニュース・社会",
    "テクノロジー・AI",
    "世界経済・株式市場",
]
```

### 通知時刻を変える

`news.yml` の cron 式を変更してください（**UTC 基準**です）。

| 希望時刻 (JST) | cron 式 (UTC) |
|------------|---------------|
| 朝 6:00    | `0 21 * * *`  |
| 朝 7:00    | `0 22 * * *`  |
| 朝 8:00    | `0 23 * * *`  |
| 夕 18:00   | `0 9 * * *`   |
| 夕 19:00   | `0 10 * * *`  |
| 夕 20:00   | `0 11 * * *`  |

---

## コスト目安

| サービス | 費用 |
|--------|------|
| GitHub Actions | 無料（月2,000分まで） |
| Claude API | 1回あたり約0.5〜2円（月60円程度） |
| ntfy.sh | 無料 |
| **合計** | **月100円以下** |
