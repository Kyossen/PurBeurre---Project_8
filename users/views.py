#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
Lib imports, they are important to help Django a have all tools for a good use
Imports of files, they are important for
this view file because it gives access to forms and templates
Imports of Django lib, is a base for well functioning"""


# Import lib
import string
import time

# Import Django
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse

# Import file
from search.forms import FoodForm
from .models import Substitution, Account
from .forms import SignupForm, ConnectForm, ParagraphErrorList


def sign_up(request):
    """Sing_up function is the function for allow a user on sign up"""
    context = {}
    if request.method == 'POST':
        form = SignupForm(request.POST, error_class=ParagraphErrorList)
        # Check input if she valid or not
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if email exist or not
            create_email = User.objects.filter(username=email)
            wordpass = form.cleaned_data['wordpass']
            wordpass_2 = form.cleaned_data['wordpass_2']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            phone = form.cleaned_data['phone']
            date_b = form.cleaned_data['date_of_birth']
            address = form.cleaned_data['postal_address']

            if not create_email:
                data = {
                    'email': email,
                    'password': wordpass,
                    'password_2': wordpass_2,
                    'name': name,
                    'surname': surname,
                    'phone': phone,
                    'date_b': date_b,
                    'address': address
                }
                return validate_signup(request, data)
            else:
                context['error'] = 'Cette adresse email est déjà utilisée.'
        else:
            context['errors'] = form.errors.items()
    else:
        # GET method. Create a new form to be used in the template.
        form = SignupForm()
    form_food = FoodForm()
    context['form_food'] = form_food
    context['form'] = form
    return render(request, 'search/sign_up.html', context)


def validate_signup(request, data):
    """Valid sign up is the function for check data input the user"""
    if data['password'] == data['password_2']:
        # Check if the special character in the password is present
        exclude = set(string.punctuation)
        for ch in exclude:
            if ch in data['password']:
                # Check if length of the datas is good
                if 12 >= len(data['password']) >= 6:
                    nb_list = ['1', '2', '3', '4', '5',
                               '6', '7', '8', '9', '0']
                    for nb in data['password']:
                        if nb in nb_list:
                            if 17 >= len(data['phone']) >= 10:
                                if 25 >= len(data['address']) >= 1:
                                    return save_user(request, data)
                                else:
                                    return errors_signup(request, 'lng_a')
                            else:
                                return errors_signup(request, 'nb_p')
                    else:
                        return errors_signup(request, 'nb')
                else:
                    return errors_signup(request, 'lng')
        else:
            return errors_signup(request, 'ch')
    else:
        return errors_signup(request, 'p_e')


def errors_signup(request, error):
    """Error sign up is the function for
    get a error and return this the user"""
    context = {}
    if 'p_e' in error:
        context['error'] = 'Les mots de passes ne sont pas identiques.'
    if 'ch' in error:
        context['error'] = 'Veuillez ajouter un' \
                           ' caractère spécial à votre mot de passe.'
    if 'lng' in error:
        context['error'] = 'La longueur du mot de ' \
                           'passe doit être de 6 à 12 caractères.'
    if 'nb' in error:
        context['error'] = 'Veuillez ajouter un chiffre à votre mot de passe.'
    if 'nb_p' in error:
        context['error'] = 'Veuillez entrer un numéro ' \
                           'de téléphone valide (exemple: 01-02-33-06-09).'
    if 'lng_a' in error:
        context['error'] = 'Veuillez entrer une adresse valide.'
    context['form_food'] = FoodForm()
    context['form'] = SignupForm()
    return render(request, 'search/sign_up.html', context)


def save_user(request, data):
    """Save user allow the database have save
     a new user in User table and Account table
    Account table have a foreign key on
     User table for find the user correctly"""
    context = {}
    new_user_db = User.objects.create_user(first_name=data['name'],
                                           last_name=data['surname'],
                                           username=data['email'],
                                           password=data['password'])
    new_account_db = Account(user=new_user_db,
                             phone=data['phone'],
                             date_of_birth=data['date_b'],
                             postal_address=data['address'])
    new_user_db.save()
    new_account_db.save()
    context['form_food'] = FoodForm()
    context['form'] = ConnectForm()
    return render(request, 'search/connect.html', context)


def connect(request):
    """The connect function is the function
    allow a user of the connect on the platform"""
    context = {}
    # Check if user is connect or not
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = ConnectForm(request.POST, error_class=ParagraphErrorList)
            # Check if input is good
            if form.is_valid():
                data = {
                    'email': request.POST['email'],
                    'password': request.POST['wordpass']
                }
                return check_connect(request, data)
            else:
                context['errors'] = form.errors.items()
        else:
            form = ConnectForm()
        context['form'] = form
        context['form_food'] = FoodForm()
        return render(request, 'search/connect.html', context)

    # If the user clicks on the login page and the user is logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect('dashboard.html')


def check_connect(request, data):
    """Here, the system check if information
     the user is good or not
    If they are good, the system create
     a session for the user"""
    context = {}
    user_connected = authenticate(request, username=data['email'],
                                  password=data['password'])
    # Check if input is good or not
    if user_connected is not None:
        # create a session for user
        login(request, user=user_connected)
        request.session['member_id'] = user_connected.id
        time.sleep(4)
        return HttpResponseRedirect('dashboard.html')
    else:
        context['form'] = ConnectForm()
        context['form_food'] = FoodForm()
        context['error_login'] = "Adresse email et/ou mot de passe incorrect"
        return render(request, 'search/connect.html', context)


def dashboard(request):
    """Dashboard is the handler of the user dashboard"""
    context = {}
    # Check if user is connect or not
    if not request.user.is_authenticated:
        return render(request, 'search/connect.html', context)
    else:
        # Find the user in all users
        user_all = User.objects.all()
        user_currently = request.session['member_id']
        for info in user_all:
            if user_currently == info.pk:
                context['username'] = info.username
                context['firstname'] = info.first_name
                context['lastname'] = info.last_name
                all_account = Account.objects.all()
                # Get all information the user
                for info_next in all_account:
                    if user_currently == info_next.user_id:
                        context['phone'] = info_next.phone
                        context['date_of_birth'] = info_next.date_of_birth
                        context['postal_address'] = info_next.postal_address
                        context['form_food'] = FoodForm()
                        return render(request, 'search/dashboard.html',
                                      context)


def disconnect(request, template_name='search/index.html'):
    """Disconnect is the method for disconnect a user"""
    context = {}
    # Check if user is connect
    if not request.user.is_authenticated:
        form = ConnectForm(request.POST, error_class=ParagraphErrorList)
        context['form'] = form
        context['form_food'] = FoodForm()
        return render(request, 'search/index.html', context)
    else:
        # If user is connect, user is disconnect and redirect to index page
        auth_logout(request)
        context['form_food'] = FoodForm()
        return TemplateResponse(request, template_name, context)


def favorites_user(request):
    """This method is a used for return a message if user
    not have saved a favorites, or continue the process
    display of the favorites"""
    context = {}
    food_all = Substitution.objects.filter(
        user__id=request.session['member_id'])
    # Check if user have already added of the favorites
    if len(food_all) != 0:
        return display_my_favorites(request, food_all)
    else:
        context['form_food'] = FoodForm()
        context['not_food'] = "Vous n'avez pas " \
                              "encore enregistré d'aliment."
        return render(request, 'search/favorites.html', context)


def display_my_favorites(request, food):
    """Display my favorite is the method
    for display the favorites of the user"""
    context = {}
    paginator = Paginator(food, 6)
    page = request.GET.get('page', 1)
    nb_page = paginator.get_page(page)
    context['nb_page'] = nb_page
    context['product_result'] = paginator.page(page)
    context['form_food'] = FoodForm()
    return render(request, 'search/favorites.html', context)
