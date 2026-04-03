import asyncio
import os
import subprocess

import httpx


async def fetch_articles() -> list[dict]:
    token = os.environ.get("QIITA_API_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            "https://qiita.com/api/v2/items",
            headers=headers,
            params={"per_page": 5, "page": 1},
        )
        response.raise_for_status()
        return response.json()


def select_article(articles: list[dict]) -> dict | None:
    lines = [
        f"{article['title']} | {article['user']['id']} | LGTM:{article['likes_count']}"
        for article in articles
    ]
    input_text = "\n".join(lines).encode()

    result = subprocess.run(
        ["fzf", "--ansi", "--prompt=記事を選択> "],
        input=input_text,
        stdout=subprocess.PIPE,
    )

    if result.returncode != 0:
        return None

    selected_line = result.stdout.decode().strip()
    for article in articles:
        if selected_line.startswith(article["title"]):
            return article
    return None


def display_article(article: dict) -> None:
    print(f"\nタイトル : {article['title']}")
    print(f"著者     : {article['user']['id']}")
    print(f"LGTM     : {article['likes_count']}")
    print(f"URL      : {article['url']}")
    print("\n--- 本文 ---\n")
    print(article["body"])


async def main() -> None:
    print("Fetching articles from Qiita...\n")
    articles = await fetch_articles()

    selected = select_article(articles)
    if selected is None:
        print("キャンセルされました。")
        return

    display_article(selected)


if __name__ == "__main__":
    asyncio.run(main())
