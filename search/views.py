import string
import time

import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse

from .forms import SignupForm, ConnectForm, FoodForm, ParagraphErrorList
from .models import *


def index(request):
    context = {
    }

    if request.method == 'POST':
        form = FoodForm(request.POST, error_class=ParagraphErrorList)
        food = form.cleaned_data['food']
        result(food)
    else:
        # GET method. Create a new form to be used in the template.
        form = FoodForm()
    context['form'] = form
    return render(request, 'search/index.html', context)


def sign_up(request):
    All_accounts = Account.objects.all()
    context = {
    }

    if request.method == 'POST':
        form = SignupForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            email = form.cleaned_data['email']
            create_email = All_accounts.filter(email=email)
            print(create_email)
            wordpass = form.cleaned_data['wordpass']
            wordpass_2 = form.cleaned_data['wordpass_2']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            print(email, wordpass, wordpass_2, name, surname)
            if not create_email:
                if wordpass == wordpass_2:
                    exclude = set(string.punctuation)
                    for ch in wordpass:
                        if ch in exclude:
                            if 12 >= len(wordpass) >= 6:
                                nb_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                                for nb in wordpass:
                                    if nb in nb_list:
                                        print('Valid')
                                        user = User.objects.create_user(first_name=name,
                                                                        last_name=surname,
                                                                        username=email,
                                                                        password=wordpass)
                                        new_account_db = Account(email=email,
                                                                 wordpass=wordpass,
                                                                 name=name,
                                                                 surname=surname)
                                        user.save()
                                        new_account_db.save()
                                        print('Save in table')
                                        return render(request, 'search/connect.html')
                                    else:
                                        print('Il manque un chiffre')
                            else:
                                print('Wordpass not lenght')
                        else:
                            print('Miss a carac spec')
                else:
                    print('Wordpass is not same')
            else:
                message_error_useEmail = 'Email déjà utilisée'
                print(message_error_useEmail)
        else:
            context['errors'] = form.errors.items()
            print('False')
    else:
        # GET method. Create a new form to be used in the template.
        form = SignupForm()
    context['form'] = form
    return render(request, 'search/sign_up.html', context)


def connect(request):
    context = {
    }

    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = ConnectForm(request.POST, error_class=ParagraphErrorList)
            if form.is_valid():
                email = request.POST['email']
                wordpass = request.POST['wordpass']
                user_connected = authenticate(request, username=email, password=wordpass)
                if user_connected is not None:
                    login(request, user=user_connected)
                    request.session['member_id'] = user_connected.id
                    print(request.session['member_id'])
                    return render(request, 'search/dashboard.html', context)

                else:
                    message_id_error = "Adresse email et/ou mot de passe incorrect"
                    print(message_id_error)
            else:
                context['errors'] = form.errors.items()
                print('False')
        else:
            # GET method. Create a new form to be used in the template.
            form = ConnectForm()
        context['form'] = form
        return render(request, 'search/connect.html', context)

    if request.user.is_authenticated:
        if request:
            return render(request, 'search/dashboard.html', context)

        if request == 'search/favorites.html':
            return render(request, 'search/favorites.html', context)


def dashboard(request):
    context = {
    }

    if not request.user.is_authenticated:
        return render(request, 'search/connect.html', context)
    else:
        return render(request, 'search/dashboard.html', context)


def favorites(request):
    context = {
    }

    if not request.user.is_authenticated:
        return render(request, 'search/connect.html', context)
    else:
        return render(request, 'search/favorites.html', context)


def result(request):
    context = {
    }
    
    if request.method == 'POST':
        food = request.POST['food']
        """
        result = requests.get("https://fr.openfoodfacts.org/categories.json")
        response = result.json()
        i = 0
        a = 0
        
        search = True
        while search:
            for search_food_categories in response:
                response_products_all = response["tags"][i]["url"]
                print(i)
                result_products = requests.get(response_products_all + "/" + str(a) + ".json")
                response_products = result_products.json()
                for product in response_products['products']:
                    if product['product_name'] == food:
                        print(product['product_name'])
                        print(food)
                        nutrition_grades = ''
                        if 'nutrition_grades' in product:
                            nutrition_grades = product['nutrition_grades']
                        if nutrition_grades != "a":
                            pass
                        else:
                            print('Produit trouvé: ' + food)
                            print(product['nutrition_grades'])
                            print(product['product_name'])
                            search = False
                            return search
                    else:
                        break
                i += 1
                a += 1
                print('Produit introuvable')
        """
        i = 0
        code = "3"
        while len(code) != 14:
            result_code = requests.get("https://world.openfoodfacts.org/api/v0/product/" + code + str(i) + ".json")
            response_code = result_code.json()
            print(response_code)
            if response_code['status'] != 0:
                if 'product_name' not in response_code['product']:
                    i += 1
                else:
                    if response_code['product']['product_name'] == food:
                        print('True')
                    else:
                        i += 1
            else:
                i += 1

        return render(request, 'search/result.html', context)
    return render(request, 'search/result.html', context)


def disconnect(request, template_name='search/connect.html'):
    context = {
    }
    auth_logout(request)
    return TemplateResponse(request, template_name, context)


"""
https://world.openfoodfacts.org/cgi/search.pl?search_terms=nutella&search_simple=1&json=1 pour result
Un spinner pour charger connexion
Creer une FK dans Account qui pointe sur User
"""
