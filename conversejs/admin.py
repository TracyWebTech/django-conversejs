
from django.contrib import admin
from .models import XMPPAccount
from .forms import XMPPAccountForm


class XMPPAccountAdmin(admin.ModelAdmin):
    form = XMPPAccountForm 

admin.site.register(XMPPAccount, XMPPAccountAdmin)
