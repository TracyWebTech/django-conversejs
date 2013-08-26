
from django.conf import settings
from .models import XMPPAccount
from .boshclient import BOSHClient


def get_conversejs_settings():
    converse_settings = {
        'CONVERSEJS_AUTO_LIST_ROOMS': False,
        'CONVERSEJS_AUTO_SUBSCRIBE': False,
        'CONVERSEJS_BOSH_SERVICE_URL': 'https://bind.opkode.im',
        'CONVERSEJS_HIDE_MUC_SERVER': False,
        'CONVERSEJS_PREBIND': True,
        'CONVERSEJS_SHOW_CONTROLBOX_BY_DEFAULT': False,
        'CONVERSEJS_XHR_USER_SEARCH': False,
        'CONVERSEJS_DEBUG': settings.DEBUG,
    }
    
    for key, value in converse_settings.items():
        conf = getattr(settings, key, value)

        if isinstance(conf, bool):
            conf = unicode(conf).lower()
        
        converse_settings[key] = conf

    return converse_settings


def get_conversejs_context(context, xmpp_login=False):
    context.update(get_conversejs_settings())

    if not xmpp_login:
        return context

    request = context.get('request')

    try:
        xmpp_account = XMPPAccount.objects.get(user=request.user.pk)
    except XMPPAccount.DoesNotExist:
        return context

    bosh = BOSHClient(xmpp_account.jid, xmpp_account.password,
                      settings.CONVERSEJS_BOSH_SERVICE_URL)
    jid, sid, rid = bosh.get_credentials()
    context.update({'jid': jid, 'sid': sid, 'rid': rid})

    return context
