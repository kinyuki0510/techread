from unittest.mock import patch

import pytest

from techread.api.qiita import Article
from techread.renderer.markdown import _open_in_browser, display_article


@pytest.fixture
def article() -> Article:
    return Article(
        id="id1",
        title="令嬢がPythonを学ぶ100の理由",
        url="https://qiita.com/test/items/id1",
        likes_count=999,
        user_id="ojousama",
        body="# ごきげんよう\n\nPythonとは何と優雅な言語でしょう。\n\n```python\nprint('ほほほ')\n```\n",
    )


def test_display_article_terminal(article: Article, capsys: pytest.CaptureFixture[str]) -> None:
    with patch("builtins.input", return_value="1"):
        display_article(article)

    captured = capsys.readouterr()
    assert article.title in captured.out
    assert article.user_id in captured.out
    assert str(article.likes_count) in captured.out


def test_display_article_browser(article: Article) -> None:
    with patch("builtins.input", return_value="2"), \
         patch("subprocess.run") as mock_run, \
         patch("shutil.which", return_value="/usr/bin/wslview"):
        display_article(article)

    mock_run.assert_called_once_with(
        ["wslview", article.url],
        check=False,
    )


def test_open_invalid_url_prints_error(capsys: pytest.CaptureFixture[str]) -> None:
    _open_in_browser("https://evil.com/malicious")
    captured = capsys.readouterr()
    assert "無効なURL" in captured.out


def test_open_wslview_not_found(capsys: pytest.CaptureFixture[str]) -> None:
    with patch("shutil.which", return_value=None):
        _open_in_browser("https://qiita.com/test/items/abc")
    captured = capsys.readouterr()
    assert "wslview" in captured.out
    assert "https://qiita.com/test/items/abc" in captured.out
