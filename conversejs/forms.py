
from django import forms
from .models import XMPPAccount


class XMPPAccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = XMPPAccount
