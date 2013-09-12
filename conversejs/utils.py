
import uuid

from django.conf import settings
from .models import XMPPAccount
from .boshclient import BOSHClient
from .register import register_account


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

    request = context.get('request')

    if not xmpp_login or not request.user.is_active:
        return context

    try:
        xmpp_account = XMPPAccount.objects.get(user=request.user.pk)
    except XMPPAccount.DoesNotExist:
        jid_domain = getattr(settings, 'CONVERSEJS_AUTO_REGISTER', False)
        if not jid_domain:
            return context

        xmpp_jid = request.user.username + u'@' + jid_domain
        xmpp_password = uuid.uuid4().hex # get a random uuid as password

        registered = register_account(xmpp_jid, xmpp_password,
                                      request.user.get_full_name(), request.user.email)

        if not registered:
            return context

        xmpp_account = XMPPAccount.objects.create(jid=xmpp_jid,
                                                  password=xmpp_password,
                                                  user=request.user)

    bosh = BOSHClient(xmpp_account.jid, xmpp_account.password,
                      settings.CONVERSEJS_BOSH_SERVICE_URL)
    jid, sid, rid = bosh.get_credentials()
    context.update({'jid': jid, 'sid': sid, 'rid': rid})

    return context
