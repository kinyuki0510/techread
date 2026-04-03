import asyncio
import os
import subprocess

import httpx
from rich.console import Console
from rich.markdown import Markdown

console = Console()


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


def open_in_browser(url: str) -> None:
    subprocess.run(["wslview", url], check=False)


def display_article(article: dict) -> None:
    console.print(f"\n[bold]{article['title']}[/bold]")
    console.print(f"著者: [cyan]{article['user']['id']}[/cyan]  LGTM: [yellow]{article['likes_count']}[/yellow]  URL: {article['url']}\n")

    console.print("[1] ターミナルで読む  [2] ブラウザで開く")
    choice = input("選択> ").strip()

    if choice == "2":
        open_in_browser(article["url"])
    else:
        console.print(Markdown(article["body"]))


async def poll(interval: int = 60) -> None:
    console.print("[bold green]ポーリング開始（Ctrl+C で終了）[/bold green]\n")
    seen_ids: set[str] = set()

    while True:
        articles = await fetch_articles()
        new_articles = [a for a in articles if a["id"] not in seen_ids]

        if new_articles:
            console.print(f"[yellow]{len(new_articles)}件の新着記事[/yellow]")
            for a in new_articles:
                console.print(f"  ・{a['title']} by {a['user']['id']}")
                seen_ids.add(a["id"])
        else:
            console.print("[dim]新着なし[/dim]")

        await asyncio.sleep(interval)


async def main() -> None:
    print("Fetching articles from Qiita...\n")
    articles = await fetch_articles()

    selected = select_article(articles)
    if selected is None:
        print("キャンセルされました。")
        return

    display_article(selected)


async def main_poll() -> None:
    try:
        await poll(interval=10)  # PoCなので10秒
    except KeyboardInterrupt:
        console.print("\n終了します。")


if __name__ == "__main__":
    asyncio.run(main_poll())
