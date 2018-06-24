import string

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from web3auth.utils import recover_to_addr
from eth_utils import is_hex_address
from django.utils.translation import ugettext_lazy as _


def validate_eth_address(value):
    if not is_hex_address(value):
        raise forms.ValidationError(
            _('%(value)s is not a valid Ethereum address'),
            params={'value': value},
        )


class LoginForm(forms.Form):
    signature = forms.CharField(widget=forms.HiddenInput, max_length=132)
    address = forms.CharField(widget=forms.HiddenInput, max_length=42, validators=[validate_eth_address])

    def __init__(self, token, *args, **kwargs):
        self.token = token
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_signature(self):
        sig = self.cleaned_data['signature']
        if len(sig) != 132 or (sig[130:] != '1b' and sig[130:] != '1c') or \
            not all(c in string.hexdigits for c in sig[2:]):
            raise forms.ValidationError(_('Invalid signature'))
        return sig


class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = getattr(settings, "WEB3AUTH_USER_SIGNUP_FIELDS", ['email'])
