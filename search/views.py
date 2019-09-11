import string

import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
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
    All_accounts = User.objects.all()
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
            phone = form.cleaned_data['phone']
            date_of_birth = form.cleaned_data['date_of_birth']
            postal_address = form.cleaned_data['postal_address']
            print(email, wordpass, wordpass_2, name, surname, phone)
            if not create_email:
                if wordpass == wordpass_2:
                    exclude = set(string.punctuation)
                    for ch in wordpass:
                        if ch in exclude:
                            if 12 >= len(wordpass) >= 6:
                                nb_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                                for nb in wordpass:
                                    if nb in nb_list:
                                        if 15 >= len(phone) >= 10:
                                            if 25 >= len(postal_address) >= 1:
                                                print('Valid')
                                                user = User.objects.create_user(first_name=name,
                                                                                last_name=surname,
                                                                                username=email,
                                                                                password=wordpass)
                                                new_account_db = Account(user=user,
                                                                         phone=phone,
                                                                         date_of_birth=date_of_birth,
                                                                         postal_address=postal_address)
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
        form = FoodForm()
        food = request.POST['food']
        result_food = requests.get("https://world.openfoodfacts.org/cgi/search.pl?search_terms=" + food.lower() +
                                   "&search_simple=1&json=1")
        response = result_food.json()
        for result_response in response['products']:
            name_result = result_response['product_name']
            img_result = result_response['image_front_url']

            context['form'] = form
            context['img_result'] = img_result
            context['name_result'] = name_result

            i = 0
            while i != len(result_response['categories_tags']):
                search_categories = "https://fr.openfoodfacts.org/categorie"
                search_substitution = requests.get(search_categories + "/" + result_response['categories_tags'][i] +
                                                   ".json")
                result_substitution = search_substitution.json()
                for products in result_substitution:
                    if len(result_substitution['products']) != 0:
                        for products_result in result_substitution['products']:
                            if 'nutrition_grades' in products_result and \
                                    products_result['nutrition_grades'] == "a":
                                print(products_result['product_name'])
                                print(products_result['nutrition_grades'])
                            if 'nutrition_grades' in products_result and \
                                    products_result['nutrition_grades'] == "b":
                                print(products_result['product_name'])
                                print(products_result['nutrition_grades'])
                i += 1
                # return render(request, 'search/result.html', context)

    else:
        # GET method. Create a new form to be used in the template.
        form = FoodForm()
    context['form'] = form
    return render(request, 'search/result.html', context)


def disconnect(request, template_name='search/connect.html'):
    context = {
    }
    auth_logout(request)
    return TemplateResponse(request, template_name, context)


"""
https://world.openfoodfacts.org/cgi/search.pl?search_terms=nutella&search_simple=1&json=1 pour result
"""
