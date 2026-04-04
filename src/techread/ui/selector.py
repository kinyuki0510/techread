import subprocess

from techread.api.qiita import Article


def select_article(articles: list[Article], read_ids: set[str]) -> Article | None:
    lines = [
        "{mark} {title} | {user} | LGTM:{likes}".format(
            mark="✓" if article.id in read_ids else " ",
            title=article.title,
            user=article.user_id,
            likes=article.likes_count,
        )
       for article in articles
    ]
    input_text = "\n".join(lines).encode()

    result = subprocess.run(
        ["fzf", "--ansi", "--prompt=記事を選択> "],
        input=input_text,
        stdout=subprocess.PIPE,
    )

    if result.returncode != 0:
        return None

    selected_line = result.stdout.decode("utf-8").strip()
    for article, line in zip(articles, lines):
        if line.strip() == selected_line:
            return article
    return None
