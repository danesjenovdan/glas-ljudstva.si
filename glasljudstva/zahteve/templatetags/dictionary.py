from django import template

register = template.Library()


@register.filter
def dictionary(dict, key):
    return dict.get(key, "")
