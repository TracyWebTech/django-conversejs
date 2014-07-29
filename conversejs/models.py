
from django.db import models

try:
    from django.conf import settings
except ImportError:
    from django.contrib.auth.models import User
else:
    User = settings.AUTH_USER_MODEL


class XMPPAccount(models.Model):
    user = models.ForeignKey(User, related_name='xmpp')
    jid = models.CharField(max_length=300)
    password = models.CharField(max_length=1024)

    def __unicode__(self):
        return u'{0}/{1}'.format(self.user, self.jid)
