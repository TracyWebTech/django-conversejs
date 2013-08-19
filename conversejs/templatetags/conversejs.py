
from django import template

register = template.Library()
TEMPLATE_PATH = 'conversejs/includes/'

@register.inclusion_tag(TEMPLATE_PATH + 'initialize.html', takes_context=True)
def conversejs_initialize(context):
    request = context.get('request')
    return locals()

@register.inclusion_tag(TEMPLATE_PATH + 'chatpanel.html', takes_context=True)
def conversejs_chatpanel(context):
    request = context.get('request')
    return locals()

@register.inclusion_tag(TEMPLATE_PATH + 'static.html', takes_context=True)
def conversejs_static(context):
    request = context.get('request')
    STATIC_URL = context.get('STATIC_URL')
    return locals()
