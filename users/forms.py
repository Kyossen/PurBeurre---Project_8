#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
Here, all forms used by the platform
These forms allow communication between a user and the system
They use the text fields of the form type for this"""

# Import Django
from django import forms
from django.contrib.auth import password_validation
from django.forms import ModelForm
from django.forms.utils import ErrorList

# Import file
from users.models import User

# Import lib
import string


class ParagraphErrorList(ErrorList):
    """The first one is a response error form
    I use this form for certain answers"""

    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % \
               ''.join(['<p class="small error">%s</p>' % e for e in self])


class ConnectForm(forms.Form):
    """Connect form is the form for connect on the platform
    This form manage l'input of the user when this connect"""
    email = forms.EmailField(
        label='userEmail',
        max_length=25,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True)

    wordpass = forms.CharField(
        label='userWP',
        max_length=12,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True)


class UserCreationForm(ModelForm):
    """This class is inherited from the form template.
    Because we are using Django's utilities
    with our Override on the Users class."""
    password = forms.CharField(
        label='Mot de passe',
        max_length=12,
        widget=forms.PasswordInput()
    )
    confirmation_password = forms.CharField(
        label='Confirmer votre mot de passe',
        max_length=12,
        widget=forms.PasswordInput(),
    )

    # Below we choose the order in which the form is displayed
    field_order = ["email", "password", 'confirmation_password',
                   "phone", "postal_address", "date_of_birth",
                   "last_name", "first_name"]

    def clean_confirmation_email(self):
        """Here we display the message if email is exist in database"""
        error_email = 'Cette adresse email est déjà utilisée.'
        self.add_error('email', error_email)
        return error_email

    def clean_confirmation_password(self):
        """This method is a method for check that
        password is same of the password confirmation"""
        password = self.cleaned_data.get('password')
        confirmation_password = self.cleaned_data.get('confirmation_password')
        if password and confirmation_password \
                and password != confirmation_password:
            raise forms.ValidationError('Les mots de passes ne '
                                        'sont pas identiques.')
        return confirmation_password

    def _post_clean(self):
        """Post clean is a method for check if password is
        conforme a standard password"""
        super(UserCreationForm, self)._post_clean()
        password = self.cleaned_data.get('password')
        number_confirmation = ['1', '2', '3', '4', '5',
                               '6', '7', '8', '9', '0']
        exclude = set(string.punctuation)
        CS = False
        NB = False
        error_cs = forms.ValidationError('Le mot de passe doit '
                                         'contenir un caractère spécial.')
        error_nb = forms.ValidationError('Le mot de passe doit '
                                         'contenir un chiffre.')
        if password:
            try:
                for c in password:
                    for nb in number_confirmation:
                        if nb in c:
                            NB = True
                    for cs in exclude:
                        if c in cs:
                            CS = True
                if NB is True and CS is True:
                    password_validation.validate_password(password,
                                                          self.instance)
                if NB is False:
                    raise error_nb
                if CS is False:
                    raise error_cs
            except forms.ValidationError as error:
                self.add_error('password', error)

    def clean_phone(self):
        """Clean phone is use for clean a character special of
        the user input and check length of the number"""
        phone = self.cleaned_data.get('phone')
        if 9 >= len(phone) >= 17:
            raise forms.ValidationError('Numéro incorrecte.')
        if ' ' in phone:
            phone = phone.replace(' ', '')
        if '-' in phone:
            phone = phone.replace('-', '')
        if '/' in phone:
            phone = phone.replace('/', '')
        return phone

    def save(self, commit=True):
        """This method ise using for save the password in the database"""
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(user.password)
        if commit:
            user.save()
        return user

    class Meta:
        # Here we a modif a form for form FR
        labels = {'phone': 'Numéro de téléphone',
                  'postal_address': 'Adresse postale',
                  'date_of_birth': 'Date de naissance'}
        model = User
        fields = ["email", "password", "phone",
                  "postal_address", "date_of_birth",
                  "last_name", "first_name"]
