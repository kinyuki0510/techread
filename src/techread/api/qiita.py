from dataclasses import dataclass

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

    async def __aexit__(self, *args: object) -> None:
        await self._client.__aexit__(*args)

    async def fetch_articles(self, per_page: int = 20) -> list[Article]:
        response = await self._client.get(
            "/items",
            params={"per_page": per_page, "page": 1},
        )
        response.raise_for_status()
        return [self._parse(a) for a in response.json()]

    def _parse(self, data: dict) -> Article:
        return Article(
            id=data["id"],
            title=data["title"],
            url=data["url"],
            likes_count=data["likes_count"],
            user_id=data["user"]["id"],
            body=data["body"],
        )
