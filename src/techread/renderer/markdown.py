import subprocess

from rich.console import Console
from rich.markdown import Markdown

from techread.api.qiita import Article

console = Console()


def display_article(article: Article) -> None:
    console.print(f"\n[bold]{article.title}[/bold]")
    console.print(
        f"著者: [cyan]{article.user_id}[/cyan]  "
        f"LGTM: [yellow]{article.likes_count}[/yellow]  "
        f"URL: {article.url}\n"
    )

    console.print("[1] ターミナルで読む  [2] ブラウザで開く")
    choice = input("選択> ").strip()

    if choice == "2":
        _open_in_browser(article.url)
    else:
        console.print(Markdown(article.body))


def _open_in_browser(url: str) -> None:
    subprocess.run(["wslview", url], check=False)
