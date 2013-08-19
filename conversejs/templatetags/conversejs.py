
from django import template

from ..utils import get_conversejs_settings

register = template.Library()
TEMPLATE_PATH = 'conversejs/includes/'


@register.inclusion_tag(TEMPLATE_PATH + 'initialize.html', takes_context=True)
def conversejs_initialize(context):
    tag_context = {
        'request': context.get('request'),
    }

    tag_context.update(get_conversejs_settings())
    return tag_context


@register.inclusion_tag(TEMPLATE_PATH + 'chatpanel.html', takes_context=True)
def conversejs_chatpanel(context):
    return { 'request': context.get('request'), }


@register.inclusion_tag(TEMPLATE_PATH + 'static.html', takes_context=True)
def conversejs_static(context):
    return {
        'request': context.get('request'),
        'STATIC_URL': context.get('STATIC_URL'),
    }
