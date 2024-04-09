from django import template
from django.conf import settings
from django.template.base import Node

register = template.Library()


class MediaPathNode(Node):
    def __init__(self, path):
        self.path = path

    def render(self, context):
        # Полный путь к медиафайлу
        return f"{settings.MEDIA_URL}{self.path.resolve(context)}"


@register.tag
def mediapath(parser, token):
    # Разбор токена
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("'{0}' takes one argument".format(bits[0]))

    path = parser.compile_filter(bits[1])
    return MediaPathNode(path)
