
import uuid

from .conf import get_conversejs_settings, CONVERSEJS_AUTO_REGISTER
from .models import XMPPAccount
from .boshclient import BOSHClient
from .register import register_account


def get_conversejs_context(context, xmpp_login=False):
    context.update(get_conversejs_settings())

    request = context.get('request')

    if not xmpp_login or not request.user.is_active:
        return context

    try:
        xmpp_account = XMPPAccount.objects.get(user=request.user.pk)
    except XMPPAccount.DoesNotExist:
        jid_domain = CONVERSEJS_AUTO_REGISTER
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
                      context['CONVERSEJS_BOSH_SERVICE_URL'])
    jid, sid, rid = bosh.get_credentials()
    context.update({'jid': jid, 'sid': sid, 'rid': rid})

    return context
