import re

import mistune

# tags of a format like: [[!meta title="Backups"]]
META_REGEX = re.compile('\[\[!meta ([a-z]+)="([^"]*)"\]\]')

markdown = mistune.Markdown(
    renderer=mistune.Renderer(
        escape=True,
        hard_wrap=False,
    ),
)


def get_meta_tags(text):
    """Return tuple (text, meta dict) for the given text.

    Meta tags are stripped from the Markdown source, but the Markdown is
    not rendered.
    """
    meta = {}

    def repl(match):
        meta[match.group(1)] = match.group(2)
        return ''

    text = META_REGEX.sub(repl, text)
    return text, meta


def markdown_and_meta(text):
    """Return tuple (html, meta dict) for the given text."""
    text, meta = get_meta_tags(text)
    return markdown(text), meta
