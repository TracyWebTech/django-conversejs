from .conf import get_conversejs_settings
from .models import XMPPAccount
from .boshclient import BOSHClient


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
                      context['CONVERSEJS_BOSH_SERVICE_URL'])
    jid, sid, rid = bosh.get_credentials()
    context.update({'jid': jid, 'sid': sid, 'rid': rid})

    return context
