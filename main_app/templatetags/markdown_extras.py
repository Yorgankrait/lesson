from django import template
import markdown as md

register = template.Library()

@register.filter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])