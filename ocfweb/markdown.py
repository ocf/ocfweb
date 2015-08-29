import re

import mistune

# tags of a format like: [[!meta title="Backups"]]
META_REGEX = re.compile('\[\[!meta ([a-z]+)="([^"]*)"\]\]')


class HtmlCommentsInlineLexer(mistune.InlineLexer):
    """Strip HTML comments inside lines."""

    def enable_html_comments(self):
        self.rules.html_comment = re.compile(
            '^<!--(.*?)-->'
        )
        self.default_rules.insert(0, 'html_comment')

    def output_html_comment(self, m):
        return ''


class HtmlCommentsBlockLexer(mistune.BlockLexer):
    """Strip blocks which consist entirely of HTML comments."""

    def enable_html_comments(self):
        self.rules.html_comment = re.compile(
            '^<!--(.*?)-->'
        )
        self.default_rules.insert(0, 'html_comment')

    def parse_html_comment(self, m):
        pass


_renderer = mistune.Renderer(
    escape=True,
    hard_wrap=False,
)

_inline = HtmlCommentsInlineLexer(_renderer)
_inline.enable_html_comments()

_block = HtmlCommentsBlockLexer(mistune.BlockGrammar())
_block.enable_html_comments()

markdown = mistune.Markdown(
    renderer=_renderer,
    inline=_inline,
    block=_block,
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
