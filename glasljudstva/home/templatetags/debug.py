from django import template

register = template.Library()


@register.filter
def print(value):
    from pprint import pprint

    return pprint(value.__dir__())
