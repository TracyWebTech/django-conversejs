
from django import template
from ..utils import get_conversejs_context

register = template.Library()
TEMPLATE_PATH = 'conversejs/includes/'


@register.inclusion_tag(TEMPLATE_PATH + 'initialize.html', takes_context=True)
def conversejs_initialize(context):
    return get_conversejs_context(context, xmpp_login=True)


@register.inclusion_tag(TEMPLATE_PATH + 'chatpanel.html', takes_context=True)
def conversejs_chatpanel(context):
    return get_conversejs_context(context)


@register.inclusion_tag(TEMPLATE_PATH + 'static.html', takes_context=True)
def conversejs_static(context):
    return get_conversejs_context(context)

