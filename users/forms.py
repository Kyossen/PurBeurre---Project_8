#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
Here, all forms used by the platform
These forms allow communication between a user and the system
They use the text fields of the form type for this"""

from django import forms
from django.forms.utils import ErrorList


class ParagraphErrorList(ErrorList):
    """The first one is a response error form
    I use this form for certain answers"""
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % \
               ''.join(['<p class="small error">%s</p>' % e for e in self])


class SignupForm(forms.Form):
    """Signup form is the form for sign up on the platform
    This form manage l'input of the user when this sign up"""
    wordpass = forms.CharField(
        label='userWP',
        max_length=12,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True)

    wordpass_2 = forms.CharField(
        label='userWP_2v',
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

    phone = forms.CharField(
        label='userPhone',
        max_length=17,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True)

    date_of_birth = forms.DateField(
        label='userDate_of_birth',
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        required=True)

    postal_address = forms.CharField(
        label='userPostal_address',
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True)


class ConnectForm(forms.Form):
    """Connect form is the form for connect on the platform
    This form manage l'input of the user when this connect"""
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
