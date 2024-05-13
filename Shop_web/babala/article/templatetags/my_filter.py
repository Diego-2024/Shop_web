# 在你的 Django app 中的 templates/tags.py 文件

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='range')
@stringfilter
def range_filter(value):
    start, end = map(int, value.split(','))
    return list(range(start, end))


@register.filter(name='mul')
def mul(value, arg):
    try:
        return value * int(arg)
    except (ValueError, TypeError):
        return value
