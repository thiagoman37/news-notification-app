"""
news_summary.py
Claude API (web_search tool) でニュースを収集・要約し、ntfy.sh でプッシュ通知する
"""

import os
import sys
import json
import httpx
import anthropic
from datetime import datetime

# ── 設定 ──────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
NTFY_TOPIC        = os.environ["NTFY_TOPIC"]          # 例: my-news-abc123
NTFY_URL          = f"https://ntfy.sh/{NTFY_TOPIC}"

# 通知するニュースカテゴリ（自由にカスタマイズ）
NEWS_TOPICS = [
    "日本の最新ニュース・社会",
    "テクノロジー・AI",
    "世界経済・株式市場",
]

# ── ヘルパー関数 ──────────────────────────────────────

def get_time_label() -> str:
    """朝 or 夕のラベルを返す"""
    hour = datetime.now().hour
    return "🌅 朝のニュース" if hour < 12 else "🌇 夕方のニュース"


def fetch_news_summary() -> str:
    """Claude API (web_search) でニュースを取得・要約する"""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    topics_str = "\n".join(f"- {t}" for t in NEWS_TOPICS)
    today = datetime.now().strftime("%Y年%m月%d日")

    prompt = f"""今日（{today}）の最新ニュースを以下のカテゴリごとに調べて、
それぞれ1〜2文で日本語で要約してください。

カテゴリ：
{topics_str}

出力形式（必ずこの形式で）：
各カテゴリについて「▶ [カテゴリ名]」の見出しに続けて要約を書いてください。
全体で300文字以内に収めてください。"""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}],
    )

    # テキストブロックを結合
    summary_parts = []
    for block in response.content:
        if hasattr(block, "text"):
            summary_parts.append(block.text.strip())

    return "\n".join(summary_parts) if summary_parts else "ニュースの取得に失敗しました。"


def send_notification(title: str, body: str) -> None:
    """ntfy.sh へ通知を送る"""
    headers = {
        "Title": title.encode("utf-8"),
        "Priority": "default",
        "Tags": "newspaper",
        "Content-Type": "text/plain; charset=utf-8",
    }
    resp = httpx.post(NTFY_URL, content=body.encode("utf-8"), headers=headers, timeout=15)
    resp.raise_for_status()
    print(f"✅ 通知送信完了 (status={resp.status_code})")


# ── メイン ────────────────────────────────────────────

def main():
    print(f"[{datetime.now().isoformat()}] ニュース取得開始")

    try:
        summary = fetch_news_summary()
        print("── 要約 ──────────────────────")
        print(summary)
        print("──────────────────────────────")

        title = get_time_label()
        send_notification(title, summary)

    except anthropic.APIError as e:
        print(f"❌ Claude API エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except httpx.HTTPStatusError as e:
        print(f"❌ ntfy.sh エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
