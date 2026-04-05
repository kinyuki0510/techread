from collections.abc import AsyncGenerator
from pathlib import Path

import pytest

from techread.db.store import get_read_ids, init_db, mark_read


@pytest.fixture(autouse=True)
async def setup_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> AsyncGenerator[None, None]:
    db_path = str(tmp_path / "test.db")
    monkeypatch.setattr("techread.db.store.DB_PATH", db_path)
    await init_db()
    yield


async def test_initial_read_ids_is_empty() -> None:
    ids = await get_read_ids()
    assert ids == set()


async def test_mark_read_adds_id() -> None:
    await mark_read("abc123")
    ids = await get_read_ids()
    assert "abc123" in ids


async def test_mark_read_is_idempotent() -> None:
    await mark_read("abc123")
    await mark_read("abc123")
    ids = await get_read_ids()
    assert ids == {"abc123"}


async def test_multiple_ids() -> None:
    await mark_read("id1")
    await mark_read("id2")
    ids = await get_read_ids()
    assert ids == {"id1", "id2"}
