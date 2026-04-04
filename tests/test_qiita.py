from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from techread.api.qiita import Article, QiitaClient


MOCK_RESPONSE = [
    {
        "id": "abc123",
        "title": "テスト記事",
        "url": "https://qiita.com/test/items/abc123",
        "likes_count": 42,
        "user": {"id": "testuser"},
        "body": "# テスト\n本文です。",
    }
]


@pytest.fixture
def mock_client():
    with patch("techread.api.qiita.httpx.AsyncClient") as mock:
        instance = MagicMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=None)

        response = MagicMock()
        response.json.return_value = MOCK_RESPONSE
        response.raise_for_status = MagicMock()
        instance.get = AsyncMock(return_value=response)

        mock.return_value = instance
        yield


async def test_fetch_articles_returns_articles(mock_client):
    async with QiitaClient() as client:
        articles = await client.fetch_articles()

    assert len(articles) == 1
    assert isinstance(articles[0], Article)


async def test_fetch_articles_parses_fields(mock_client):
    async with QiitaClient() as client:
        articles = await client.fetch_articles()

    article = articles[0]
    assert article.id == "abc123"
    assert article.title == "テスト記事"
    assert article.url == "https://qiita.com/test/items/abc123"
    assert article.likes_count == 42
    assert article.user_id == "testuser"
    assert article.body == "# テスト\n本文です。"


async def test_fetch_articles_without_token(mock_client):
    async with QiitaClient(token=None) as client:
        articles = await client.fetch_articles()

    assert len(articles) == 1


async def test_fetch_articles_with_token(mock_client):
    async with QiitaClient(token="mytoken") as client:
        articles = await client.fetch_articles()

    assert len(articles) == 1
