from textwrap import dedent

from django import template
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

register = template.Library()


@register.tag
def pygments(parser, token):
    _, lang = token.split_contents()
    nodelist = parser.parse(('endpygments',))
    parser.delete_first_token()
    return PygmentsNode(nodelist, lang)


class PygmentsNode(template.Node):
    html_formatter = HtmlFormatter(noclasses=True)

    def __init__(self, nodes, lang):
        self.nodes = nodes
        self.lang = lang

    def render(self, context):
        return highlight(
            dedent(
                ''.join(
                    node.render(context)
                    for node in self.nodes
                ),
            ).strip('\n'),
            get_lexer_by_name(self.lang),
            self.html_formatter,
        )
