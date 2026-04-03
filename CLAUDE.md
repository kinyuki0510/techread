## Project Overview

**techread** — A terminal-based Qiita reader that notifies you of new/recommended articles and LGTM events on your own articles.

Core features:
- Poll Qiita API for new articles, recommended articles, and LGTM events on own articles
- Select articles interactively via fzf
- Display articles as raw Markdown (in terminal via rich) or rendered HTML (open in Windows default browser via wslview)
- Toggle between raw and rendered view
- OSS-ready: no hardcoded credentials; API key loaded from environment variable only

## Directory Structure

- `src/techread/` — Python package. Organize into subdirectories by domain (api, ui, renderer, etc.) as needed.
- `tests/` — mirrors the structure of `src/techread/`.
- Do not pre-create empty directories or files.

## Polling Strategy

- Qiita API has no webhook/event push. Use polling.
- Default interval: 60 seconds (configurable via env var `TECHREAD_POLL_INTERVAL`).
- Targets: new articles, recommended articles, LGTM events on own articles.
- Refer to https://qiita.com/api/v2/docs for endpoint details.

## WSL Notes

- Rendered Markdown is opened via `wslview <url>` (requires `wslu` package on WSL).
- If `wslview` is not available, fall back to printing the URL and notifying the user.
- Do NOT assume `xdg-open` works in WSL environments.

## Tech Stack

- Python 3.12+
- Package manager: uv
- HTTP client: httpx (async)
- CLI framework: typer
- Markdown rendering: rich
- Type checking: mypy
- Testing: pytest, pytest-asyncio
- Article selection: fzf (external command, invoked via subprocess)

## Security

| # | Item | Status |
|---|------|--------|
| 1 | API key must be loaded from environment variable only. Never hardcode. | ✅ By design |
| 2 | fzf invoked via `subprocess` with `shell=False` and list args. Never interpolate user input into shell string. | 🔲 To implement |
| 3 | Validate all URLs before passing to `wslview`. Must match `https://qiita.com/` prefix. | 🔲 To implement |
| 4 | Validate and sanitize all API responses before rendering. | 🔲 To implement |
| 5 | HTTPS only for all API calls. Reject any non-HTTPS URLs. | 🔲 To implement |
| 6 | Never log or print API keys or tokens. | 🔲 To implement |
| 7 | No secrets in code, config files, or git history. `.env` is gitignored. | ✅ By design |

## Error Handling & Logging

- On network error: retry once, then surface the error to the user with a clear message.
- On API error (4xx/5xx): do not retry. Show the status code and message to the user.
- Logging: use `stderr` for debug output. Never log API keys, tokens, or user credentials.
- Config priority: CLI args > environment variables > defaults.

## Git Flow

- GitHub Flow: branch from `main`, open PR, merge back to `main`.
- Do NOT create a `develop` branch.
- Branch naming: `feature/<name>`, `fix/<name>`, `chore/<name>`

## Rules

- Always use type hints.
- Use `uv` for all package operations. Do NOT use pip directly.
- Virtual environment must be activated before running any Python command.
- Write tests before implementation (TDD).
- All async functions must be tested with pytest-asyncio.
- Test coverage must include all public functions and all async code paths.
- When requirements are unclear or unspecified, ask before implementing. Do not assume.

## Commands

- `uv run pytest` : run tests
- `uv run mypy .` : type check
- `uv run python -m techread` : run app
- `wslview <url>` : open URL in Windows default browser

## Do NOT

- Do NOT run `git commit` or `git push` without explicit user approval.
- Do NOT run `git push --force` under any circumstances.
- Do NOT add features, refactoring, or improvements beyond what was asked.
- Do NOT add comments or docstrings to code you did not change.
- Do NOT add excessive error handling for scenarios that cannot happen.
- Do NOT create new files unless absolutely necessary.
- Do NOT read or use `.env` files or any files containing secrets.
- Do NOT implement code without writing tests first. Tests are never optional.
- Do NOT run `gh pr create`, `gh issue create`, or any gh commands that write to remote without explicit user approval.
