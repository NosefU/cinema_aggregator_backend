from django import template

register = template.Library()


@register.inclusion_tag('app_aggregator/navbar.html', takes_context=True)
def navbar(context):
    return context


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
