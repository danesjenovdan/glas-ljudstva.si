from urllib.parse import urlsplit

from django import template

register = template.Library()


@register.filter
def to_absolute_link(value):
    url = urlsplit(value)
    if url.netloc:
        return value
    if url.path.startswith("/"):
        return value
    return f"/{value}"


@register.filter
def is_external_link(value):
    url = urlsplit(value)
    return bool(url.netloc)
