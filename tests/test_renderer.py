from unittest.mock import patch

import pytest

from techread.api.qiita import Article
from techread.renderer.markdown import display_article


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


def test_display_article_terminal(article, capsys):
    with patch("builtins.input", return_value="1"):
        display_article(article)

    captured = capsys.readouterr()
    assert article.title in captured.out
    assert article.user_id in captured.out
    assert str(article.likes_count) in captured.out


def test_display_article_browser(article):
    with patch("builtins.input", return_value="2"), \
         patch("subprocess.run") as mock_run:
        display_article(article)

    mock_run.assert_called_once_with(
        ["wslview", article.url],
        check=False,
    )
