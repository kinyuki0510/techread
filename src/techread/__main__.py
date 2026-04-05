import asyncio
import os

from rich.console import Console

from techread.api.qiita import QiitaClient
from techread.db.store import get_read_ids, init_db, mark_read
from techread.renderer.markdown import display_article
from techread.ui.selector import select_article

console = Console()


async def run() -> None:
    await init_db()

    token = os.environ.get("QIITA_API_TOKEN")
    try:
        async with QiitaClient(token=token) as client:
            articles = await client.fetch_articles()
    except RuntimeError as e:
        console.print(f"[red]エラー: {e}[/red]")
        return

    while True:
        read_ids = await get_read_ids()
        selected = select_article(articles, read_ids)

        if selected is None:
            break

        await mark_read(selected.id)
        display_article(selected)


def main() -> None:
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        console.print("\n終了します。")


if __name__ == "__main__":
    main()
