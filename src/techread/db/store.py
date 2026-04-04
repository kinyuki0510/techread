import aiosqlite

DB_PATH = "techread.db"


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS read_articles (
                id TEXT PRIMARY KEY,
                read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await db.commit()


async def get_read_ids() -> set[str]:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT id FROM read_articles")
        return {row[0] async for row in cursor}


async def mark_read(article_id: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO read_articles (id) VALUES (?)",
            (article_id,),
        )
        await db.commit()
