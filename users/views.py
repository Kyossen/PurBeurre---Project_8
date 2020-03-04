#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
Lib imports, they are important to help Django a have all tools for a good use
Imports of files, they are important for
this view file because it gives access to forms and templates
Imports of Django lib, is a base for well functioning"""

# Import lib
import time

# Import Django
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Import file
from search.forms import FoodForm
from .models import Substitution
from .forms import ConnectForm, ParagraphErrorList, UserCreationForm


def sign_up(request):
    """Sing_up function is the function for allow a user on sign up"""
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST, error_class=ParagraphErrorList)
        # Check input if she valid or not
        if form.is_valid():
            user = form.save()
            login(request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
            request.session['member_id'] = user.id
            return redirect('dashboard')
        else:
            context['form'] = form
            context['form_food'] = FoodForm()
            return render(request, 'search/sign_up.html', context, status=401)
    else:
        # GET method. Create a new form to be used in the template.
        form = UserCreationForm()
    context['form_food'] = FoodForm()
    context['form'] = form
    return render(request, 'search/sign_up.html', context)


def hasNumbers(inputString):
    """This method searches whether a string contains a number or not"""
    return any(char.isdigit() for char in inputString)


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
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('wordpass')
                return check_connect(request, email, password)

            else:
                context['errors'] = form.errors.items()
                return render(request, 'search/connect.html', context,
                              status=401)
        else:
            form = ConnectForm()
        context['form'] = form
        context['form_food'] = FoodForm()
        return render(request, 'search/connect.html', context)

    # If the user clicks on the login page and the user is logged in
    if request.user.is_authenticated:
        return HttpResponseRedirect('dashboard.html')


def check_connect(request, email, password):
    """Here, the system check if information
     the user is good or not
    If they are good, the system create
     a session for the user"""
    context = {}
    user_connected = authenticate(request, email=email, password=password)
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
        return render(request, 'search/connect.html', context, status=401)


def dashboard(request):
    """Dashboard is the handler of the user dashboard"""
    context = {}
    # Check if user is connect or not
    if not request.user.is_authenticated:
        return render(request, 'search/connect.html', context)
    else:
        # Find the user in all users
        user = request.user
        context['email'] = user.email
        context['firstname'] = user.first_name
        context['lastname'] = user.last_name
        # Get all information the user
        context['phone'] = user.phone
        context['date_of_birth'] = user.date_of_birth
        context['postal_address'] = user.postal_address
        context['form_food'] = FoodForm()
        return render(request, 'search/dashboard.html',
                      context)


def disconnect(request):
    """Disconnect is the method for disconnect a user"""
    context = {}
    # Check if user is connect
    if not request.user.is_authenticated:
        context['form_food'] = FoodForm()
        return render(request, 'search/index.html', context)
    else:
        # If user is connect, user is disconnect and redirect to home page
        auth_logout(request)
        context['form_food'] = FoodForm()
        return redirect('index')


def favorites_user(request):
    """This method is a used for return a message if user
    not have saved a favorites, or continue the process
    display of the favorites"""
    context = {}
    food_all = Substitution.objects.filter(
        user__id=request.user.id)
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
