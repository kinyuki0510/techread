from unittest.mock import MagicMock, patch

import pytest

from techread.api.qiita import Article
from techread.ui.selector import select_article


@pytest.fixture
def articles() -> list[Article]:
    return [
        Article(
            id="id1",
            title="Python入門",
            url="https://qiita.com/test/items/id1",
            likes_count=10,
            user_id="user1",
            body="本文1",
        ),
        Article(
            id="id2",
            title="asyncio解説",
            url="https://qiita.com/test/items/id2",
            likes_count=20,
            user_id="user2",
            body="本文2",
        ),
    ]


def make_fzf_result(selected_line: str, returncode: int = 0) -> MagicMock:
    result = MagicMock()
    result.returncode = returncode
    result.stdout = selected_line.encode("utf-8")
    return result


def test_select_first_article(articles: list[Article]) -> None:
    selected_line = "  Python入門 | user1 | LGTM:10"
    with patch("subprocess.run", return_value=make_fzf_result(selected_line)):
        selected = select_article(articles, read_ids=set())

    assert selected is not None
    assert selected.id == "id1"


def test_select_read_article(articles: list[Article]) -> None:
    selected_line = "✓ asyncio解説 | user2 | LGTM:20"
    with patch("subprocess.run", return_value=make_fzf_result(selected_line)):
        selected = select_article(articles, read_ids={"id2"})

    assert selected is not None
    assert selected.id == "id2"


def test_cancel_returns_none(articles: list[Article]) -> None:
    with patch("subprocess.run", return_value=make_fzf_result("", returncode=130)):
        selected = select_article(articles, read_ids=set())

    assert selected is None
