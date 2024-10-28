from django import template

register = template.Library()

@register.filter
def previtem(items, attribute):
    return items[items.index(items) - 1].__getattribute__(attribute)
