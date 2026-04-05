from dataclasses import dataclass
from types import TracebackType
from typing import Any

import httpx


@dataclass
class Article:
    id: str
    title: str
    url: str
    likes_count: int
    user_id: str
    body: str


class QiitaClient:
    BASE_URL = "https://qiita.com/api/v2"

    def __init__(self, token: str | None = None) -> None:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers=headers,
            timeout=10.0,
        )

    async def __aenter__(self) -> "QiitaClient":
        await self._client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def fetch_articles(self, per_page: int = 20) -> list[Article]:
        params = {"per_page": per_page, "page": 1}
        last_error: httpx.RequestError | None = None
        for _ in range(2):
            try:
                response = await self._client.get("/items", params=params)
                response.raise_for_status()
                return [self._parse(a) for a in response.json()]
            except httpx.HTTPStatusError as e:
                raise RuntimeError(
                    f"API error {e.response.status_code}: {e.response.text}"
                ) from e
            except httpx.RequestError as e:
                last_error = e
        raise RuntimeError(f"Network error: {last_error}") from last_error

    def _parse(self, data: dict[str, Any]) -> Article:
        return Article(
            id=data["id"],
            title=data["title"],
            url=data["url"],
            likes_count=data["likes_count"],
            user_id=data["user"]["id"],
            body=data["body"],
        )
