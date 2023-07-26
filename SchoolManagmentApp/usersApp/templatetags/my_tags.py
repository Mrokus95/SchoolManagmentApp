from django import template

register = template.Library()

@register.filter
def not_in_list(value, arg):
    return value not in arg