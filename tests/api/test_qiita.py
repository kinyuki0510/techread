from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
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
def mock_client() -> Generator[None, None, None]:
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


async def test_fetch_articles_returns_articles(mock_client: None) -> None:
    async with QiitaClient() as client:
        articles = await client.fetch_articles()

    assert len(articles) == 1
    assert isinstance(articles[0], Article)


async def test_fetch_articles_parses_fields(mock_client: None) -> None:
    async with QiitaClient() as client:
        articles = await client.fetch_articles()

    article = articles[0]
    assert article.id == "abc123"
    assert article.title == "テスト記事"
    assert article.url == "https://qiita.com/test/items/abc123"
    assert article.likes_count == 42
    assert article.user_id == "testuser"
    assert article.body == "# テスト\n本文です。"


async def test_fetch_articles_without_token(mock_client: None) -> None:
    async with QiitaClient(token=None) as client:
        articles = await client.fetch_articles()

    assert len(articles) == 1


async def test_fetch_articles_with_token(mock_client: None) -> None:
    async with QiitaClient(token="mytoken") as client:
        articles = await client.fetch_articles()

    assert len(articles) == 1


async def test_fetch_articles_retries_on_network_error() -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = MOCK_RESPONSE
    mock_response.raise_for_status = MagicMock()

    with patch("techread.api.qiita.httpx.AsyncClient") as mock:
        instance = MagicMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=None)
        instance.get = AsyncMock(
            side_effect=[httpx.RequestError("timeout"), mock_response]
        )
        mock.return_value = instance

        async with QiitaClient() as client:
            articles = await client.fetch_articles()

    assert len(articles) == 1


async def test_fetch_articles_raises_after_two_network_errors() -> None:
    with patch("techread.api.qiita.httpx.AsyncClient") as mock:
        instance = MagicMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=None)
        instance.get = AsyncMock(side_effect=httpx.RequestError("timeout"))
        mock.return_value = instance

        async with QiitaClient() as client:
            with pytest.raises(RuntimeError, match="Network error"):
                await client.fetch_articles()


async def test_fetch_articles_raises_on_http_error() -> None:
    with patch("techread.api.qiita.httpx.AsyncClient") as mock:
        instance = MagicMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=None)

        error_response = MagicMock()
        error_response.status_code = 404
        error_response.text = "Not Found"
        error_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404", request=MagicMock(), response=error_response
        )
        instance.get = AsyncMock(return_value=error_response)
        mock.return_value = instance

        async with QiitaClient() as client:
            with pytest.raises(RuntimeError, match="API error 404"):
                await client.fetch_articles()
