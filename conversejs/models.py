
from django.db import models

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()


class XMPPAccount(models.Model):
    user = models.ForeignKey(User, related_name='xmpp')
    jid = models.CharField(max_length=300)
    password = models.CharField(max_length=1024)

    def __unicode__(self):
        return u'{0}/{1}'.format(self.user, self.jid)
