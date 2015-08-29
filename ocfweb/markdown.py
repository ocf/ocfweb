import logging
import re

import mistune
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse

_logger = logging.getLogger(__name__)

# tags of a format like: [[!meta title="Backups"]]
META_REGEX = re.compile('\[\[!meta ([a-z]+)="([^"]*)"\]\]')


class HtmlCommentsInlineLexerMixin:
    """Strip HTML comments inside lines."""

    def enable_html_comments(self):
        self.rules.html_comment = re.compile(
            '^<!--(.*?)-->'
        )
        self.default_rules.insert(0, 'html_comment')

    def output_html_comment(self, m):
        return ''


class HtmlCommentsBlockLexerMixin:
    """Strip blocks which consist entirely of HTML comments."""

    def enable_html_comments(self):
        self.rules.html_comment = re.compile(
            '^<!--(.*?)-->'
        )
        self.default_rules.insert(0, 'html_comment')

    def parse_html_comment(self, m):
        pass


class DjangoLinkInlineLexerMixin:
    """Turn special Markdown link syntax into Django links.

    In Django templates, we can use `url` tags, such as:
        {% url 'staff-hours' %}
        {% url 'doc' 'staff/backend/backups' %}

    In Markdown, we use the following fake syntax to generate Django links:
        [[human readable name|staff-hours]]
        [[human readable name|doc staff/backend/backups]]

    You can link to fragments with a # at the very end:
        [[human readable name|staff-hours#something]]
        [[human readable name|doc staff/backend/backups#something]]
    """

    split_words = re.compile('((?:(?:\\ )|\S)+)')

    def enable_django_links(self):
        self.rules.django_link = re.compile(
            '^\[\['
            '([\s\S]+?)'
            '\|'
            '([^#]+?)'
            '(?:#(.*?))?'
            '\]\]'
        )
        self.default_rules.insert(0, 'django_link')

    def output_django_link(self, m):
        text, target, fragment = m.group(1), m.group(2), m.group(3)

        def href(link, fragment):
            if fragment:
                return link + '#' + fragment
            return link

        words = DjangoLinkInlineLexerMixin.split_words.findall(target)
        name, *params = words
        try:
            return self.renderer.link(
                link=href(reverse(name, args=params), fragment),
                title=None,
                text=text,
            )
        except NoReverseMatch:
            # TODO: disable this once all docs have been cleaned up
            if len(words) == 1:
                # this is probably a legacy link:
                #  - either a full URL using bad syntax;
                #    change it to use Markdown syntax [link text](http://google.com/)
                #  - or a reference to another doc that doesn't start with `doc`;
                #    change it to be like [[link text|doc staff/backend/backups]]
                if re.match('^https?://', target):
                    _logger.warn(
                        'Matched wikilink against full URL, that should be fixed!\n'
                        'grep for url: "{}"'.format(target)
                    )
                    return self.renderer.link(
                        link=href(target, fragment),
                        title=None,
                        text=text,
                    )
                elif words[0] != 'doc':
                    # try interpreting it as a document
                    try:
                        link = href(reverse('doc', args=[words[0].rstrip('/')]), fragment)
                        _logger.warn(
                            'Matched wikilink without `doc`, that should be fixed!\n'
                            'grep for link: "{}"'.format(target)
                        )
                        return self.renderer.link(
                            link=link,
                            title=None,
                            text=text,
                        )
                    except NoReverseMatch:
                        # let the original exception raise, not this one
                        pass

            raise


class OcfMarkdownInlineLexer(
    mistune.InlineLexer,
    DjangoLinkInlineLexerMixin,
    HtmlCommentsInlineLexerMixin,
):
    pass


class OcfMarkdownBlockLexer(
    mistune.BlockLexer,
    HtmlCommentsBlockLexerMixin,
):
    pass


_renderer = mistune.Renderer(
    escape=True,
    hard_wrap=False,
)

_inline = OcfMarkdownInlineLexer(_renderer)
_inline.enable_html_comments()
_inline.enable_django_links()

_block = OcfMarkdownBlockLexer(mistune.BlockGrammar())
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
