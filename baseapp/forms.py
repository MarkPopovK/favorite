from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django import forms

from baseapp.models import Interest, Interested, User


class RememberAuthForm(AuthenticationForm):
    remember_me = forms.BooleanField(label="Don't remember me", required=False)


class EmailUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")


class InterestForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Interest
        exclude = ['user_interested', 'thumbnail']
        # widgets = {'user_interested': forms.HiddenInput()}

