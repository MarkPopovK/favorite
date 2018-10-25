from django.contrib.auth.forms import AuthenticationForm
from django import forms


class RememberAuthForm(AuthenticationForm):
    remember_me = forms.BooleanField(label="Don't remember me", required=False)