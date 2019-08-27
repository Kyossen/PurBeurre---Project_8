from django import forms
from django.forms.utils import ErrorList


class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])


class ContactForm(forms.Form):
    wordpass = forms.CharField(
        label='userWP',
        max_length=12,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True)

    email = forms.EmailField(
        label='userEmail',
        max_length=25,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True)

    name = forms.CharField(
        label='userName',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True)

    surname = forms.CharField(
        label='userSurname',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True)


class ConnectForm(forms.Form):
    wordpass = forms.CharField(
        label='userWP',
        max_length=12,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True)

    email = forms.EmailField(
        label='userEmail',
        max_length=25,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True)