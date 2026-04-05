.PHONY: install sync lint test run

## 初回セットアップ：依存関係を追加してlockファイルを生成
install:
	uv add httpx typer rich aiosqlite
	uv add --dev mypy pytest pytest-asyncio

## 環境再現：lockファイルから環境を復元（冪等）
sync:
	uv sync --all-groups

lint:
	uv run mypy .

test:
	uv run pytest

run:
	uv run techread
