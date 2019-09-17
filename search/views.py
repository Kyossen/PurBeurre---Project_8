import math
import string
import time
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.core import serializers

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from setuptools.command.test import test

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
    context['form_food'] = form
    return render(request, 'search/index.html', context)


def sign_up(request):
    All_accounts = User.objects.all()
    context = {
    }

    if request.method == 'POST':
        form = SignupForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            email = form.cleaned_data['email']
            create_email = All_accounts.filter(username=email)
            wordpass = form.cleaned_data['wordpass']
            wordpass_2 = form.cleaned_data['wordpass_2']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            phone = form.cleaned_data['phone']
            date_of_birth = form.cleaned_data['date_of_birth']
            postal_address = form.cleaned_data['postal_address']
            if not create_email:
                if wordpass == wordpass_2:
                    exclude = set(string.punctuation)
                    for ch in wordpass:
                        if ch in exclude:
                            if 12 >= len(wordpass) >= 6:
                                nb_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
                                for nb in wordpass:
                                    if nb in nb_list:
                                        if 17 >= len(phone) >= 10:
                                            if 25 >= len(postal_address) >= 1:
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
                                                return render(request, 'search/connect.html', context)
                                            else:
                                                context['error'] = 'Veuillez entrer une adresse valide.'
                                        else:
                                            context['error'] = 'Veuillez entrer un numéro de téléphone valide ' \
                                                               '(exemple: 01-02-33-06-09 ou +336-09-85-96-48)'
                                    else:
                                        context['error'] = 'Veuillez ajouter un chiffre à votre mot de passe.'
                            else:
                                context['error'] = 'La longueur du mot de passe doit être de 6 à 12 caractères.'
                        else:
                            context['error'] = 'Veuillez ajouter un caractère spécial à votre mot de passe.'
                else:
                    context['error'] = 'Mot de passe non identique.'
            else:
                context['error'] = 'Email déjà utilisée.'
        else:
            context['errors'] = form.errors.items()
            print('False')
    else:
        # GET method. Create a new form to be used in the template.
        form = SignupForm()
    form_food = FoodForm()
    context['form_food'] = form_food
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
                    time.sleep(4)
                    return HttpResponseRedirect('dashboard.html')
                else:
                    time.sleep(4)
                    context['form'] = form
                    context['form_food'] = FoodForm()
                    context['error_login'] = "Adresse email et/ou mot de passe incorrect"
                    return render(request, 'search/connect.html', context)
            else:
                context['errors'] = form.errors.items()
        else:
            form = ConnectForm()
        context['form'] = form
        context['form_food'] = FoodForm()
        return render(request, 'search/connect.html', context)

    if request.user.is_authenticated:
        if request:
            dashboard(request)
            return HttpResponseRedirect('dashboard.html')

        if request == 'search/favorites.html':
            return render(request, 'search/favorites.html', context)

"""
def validate_connect(request):
    context = {
    }
    form = ConnectForm(request.POST, error_class=ParagraphErrorList)
    username = request.GET
    password = request.GET
    print(username)
    data = {
        'is_taken': User.objects.filter(username=username['username']).exists(),
        'is_taken_2': User.objects.filter(password=password['password'])
    }
    if data['is_taken']:
        username = username['username']
        wordpass = password['password']
        user_connected = authenticate(request, username=username, password=wordpass)
        if user_connected is not None:
            print('Is connected')
            login(request, user=user_connected)
            request.session['member_id'] = user_connected.id
            data['connected'] = True
            j_username = serializers.serialize('json', username)
            return JsonResponse(j_username)
        else:
            context['form'] = form
            context['error_login'] = "Adresse email et/ou mot de passe incorrect"
            return render(request, 'search/connect.html', context)
"""


def dashboard(request):
    context = {
    }

    if not request.user.is_authenticated:
        return render(request, 'search/connect.html', context)
    else:
        user_all = User.objects.all()
        user_currently = request.session['member_id']
        for info in user_all:
            if user_currently == info.pk:
                context['username'] = info.username
                context['firstname'] = info.first_name
                context['lastname'] = info.last_name
                all_account = Account.objects.all()
                for info_next in all_account:
                    if user_currently == info_next.user_id:
                        context['phone'] = info_next.phone
                        context['date_of_birth'] = info_next.date_of_birth
                        context['postal_address'] = info_next.postal_address
                        form = FoodForm()
                        context['form_food'] = form
                        return render(request, 'search/dashboard.html', context)


def result(request):
    context = {
    }
    list_products = []
    if request.method == 'POST':
        form = FoodForm()
        food = request.POST['food']
        print(food)
        result_food = requests.get("https://world.openfoodfacts.org/cgi/search.pl?search_terms=" + food.lower() +
                                   "&search_simple=1&json=1")
        response = result_food.json()
        if len(response['products']) != 0:
            for result_response in response['products']:
                context['name_result'] = result_response['product_name']
                context['img_result'] = result_response['image_front_url']

                i = 0
                while True:
                    search_categories = "https://fr.openfoodfacts.org/categorie"
                    search_substitution = requests.get(search_categories + "/" + result_response['categories_tags'][i] +
                                                       ".json")
                    result_substitution = search_substitution.json()
                    for products in result_substitution:
                        if len(result_substitution['products']) != 0:
                            for products_result in result_substitution['products']:
                                if 'nutrition_grades' in products_result and \
                                        (products_result['nutrition_grades'] == "a"
                                         or products_result['nutrition_grades'] == "b"
                                         or products_result['nutrition_grades'] == "c"
                                         or products_result['nutrition_grades'] == "d"):
                                    list_products.append(products_result)
                                if 'nutrition_grades' not in products_result:
                                    products_result['nutrition_grades'] = ""
                                context['product_result'] = list_products

                    if i + 1 == len(result_response['categories_tags']):
                        form = FoodForm()
                        context['form_food'] = form
                        return render(request, 'search/result.html', context)
                    i += 1
        else:
            form = FoodForm()
            context['form_food'] = form
            context['error_result'] = "Nous avons eu un problème, pouvez vous recommencer ? Merci."
            return render(request, 'search/result.html', context)
    else:
        # GET method. Create a new form to be used in the template.
        form = FoodForm()
    context['form_food'] = form
    return render(request, 'search/result.html', context)


def description(request):
    context = {
    }
    if 'product' in request.GET:
        product_name = request.GET
        for product_result in product_name['product']:
            result_food = requests.get("https://world.openfoodfacts.org/cgi/search.pl?search_terms=" +
                                       product_name['product'] +
                                       "&search_simple=1&json=1")
            response = result_food.json()
            context['product_name'] = product_name['product']

            for product_add_favorites in response['products']:
                if 'nutrition_grades' in product_add_favorites and \
                        (product_add_favorites['nutrition_grades'] == "a"
                         or product_add_favorites['nutrition_grades'] == "b"
                         or product_add_favorites['nutrition_grades'] == "c"
                         or product_add_favorites['nutrition_grades'] == "d"):
                    context['product_score'] = product_add_favorites['nutrition_grades']
                if 'nutrition_grades' not in product_add_favorites:
                    product_add_favorites['nutrition_grades'] = ""
                if 'image_url' in product_add_favorites:
                    context['product_img'] = product_add_favorites['image_url']
                if 'url' in product_add_favorites:
                    context['product_url'] = product_add_favorites['url']
                form = FoodForm()
                context['form_food'] = form
                return render(request, 'search/description.html', context)

    if request.GET == '/search/description.html?product=':
        context['error_description'] = "Nous avons eu un problème, pouvez vous recommencer ? Merci."
        form = FoodForm()
        context['form_food'] = form
        return render(request, 'search/description.html', context)
    else:
        form = FoodForm()
        context['form_food'] = form
        context['error_description'] = "Nous avons eu un problème, pouvez vous recommencer ? Merci."
        return render(request, 'search/description.html', context)


def favorites(request):
    context = {
    }
    if 'product' in request.GET:
        product_name = request.GET
        for product_result in product_name['product']:
            result_food = requests.get("https://world.openfoodfacts.org/cgi/search.pl?search_terms=" +
                                       product_name['product'] +
                                       "&search_simple=1&json=1")
            response = result_food.json()
            context['product_name'] = product_name['product']

            for product_add_favorites in response['products']:
                if 'nutrition_grades' in product_add_favorites and \
                        (product_add_favorites['nutrition_grades'] == "a"
                         or product_add_favorites['nutrition_grades'] == "b"
                         or product_add_favorites['nutrition_grades'] == "c"
                         or product_add_favorites['nutrition_grades'] == "d"):
                    context['product_score'] = product_add_favorites['nutrition_grades']
                if 'nutrition_grades' not in product_add_favorites:
                    product_add_favorites['nutrition_grades'] = ""
                if 'image_url' in product_add_favorites:
                    context['product_img'] = product_add_favorites['image_url']

                if request.user.is_authenticated:
                    users_all = User.objects.all()
                    food_all = Substitution.objects.all()
                    list_save = []
                    list_for_save = []
                    for user_save in users_all:
                        user = request.session['member_id']
                        if user_save.id == user:
                            for food_save in food_all:
                                if user == food_save.user_id:
                                    product_add = product_name['product']
                                    list_save.append(food_save.product)
                                    if product_add not in list_save:
                                        list_for_save.append(product_add)
                                    else:
                                        context['error_food'] = 'Vous avez déjà enregistré cet aliment'
                                        form = FoodForm()
                                        context['form_food'] = form
                                        return render(request, 'search/favorites.html', context)
                                else:
                                    product_add = product_name['product']
                                    if product_add not in list_save:
                                        list_for_save.append(product_add)
                            print(list_for_save[0])
                            new_substitution_db = Substitution(user_id=user_save.id,
                                                               product=list_for_save[0],
                                                               nutrition_grade=product_add_favorites['nutrition_grades'])
                            new_substitution_db.save()
                    form = FoodForm()
                    context['form_food'] = form
                    return render(request, 'search/result.html', context)
                else:
                    form = FoodForm()
                    context['form_food'] = form
                    context['error_food'] = 'Vous devez être connecté pour effectuer cette requête. Merci'
                    return render(request, 'search/result.html', context)
    else:
        list_favorites = []
        if request.user.is_authenticated:
            food_all = Substitution.objects.all()
            for food_display in food_all:
                user = request.session['member_id']
                if food_display.user_id == user:
                    list_favorites.append(food_display.product)

            i = 0
            list_products = []
            while i != len(list_favorites):
                print(list_favorites[i])
                result_food = requests.get("https://world.openfoodfacts.org/cgi/search.pl?search_terms=" +
                                           list_favorites[i] +
                                           "&search_simple=1&json=1")
                response = result_food.json()
                for display in response['products']:
                    if display['product_name'] not in list_products:
                        list_products.append(display['product_name'])
                        if 'nutrition_grades' in display and \
                                (display['nutrition_grades'] == "a"
                                 or display['nutrition_grades'] == "b"
                                 or display['nutrition_grades'] == "c"
                                 or display['nutrition_grades'] == "d"):
                            if display['nutrition_grades'] not in list_products:
                                list_products.append(display['nutrition_grades'])
                        if 'nutrition_grades' not in display:
                            display['nutrition_grades'] = ""
                            if display['nutrition_grades'] not in list_products:
                                list_products.append(display['nutrition_grades'])
                        if 'image_url' in display:
                            list_products.append(display['image_url'])
                        else:
                            pass

                        list_products.append(display)
                        context['product_result'] = list_products

                        paginator = Paginator(list_products, 6)
                        page = request.GET.get('page')
                        nb_page = paginator.get_page(page)
                        context['nb_page'] = nb_page

                i += 1
            form = FoodForm()
            context['form_food'] = form
            return render(request, 'search/favorites.html', context)
        else:
            form = ConnectForm(request.POST, error_class=ParagraphErrorList)
            connect(request)
            context['form'] = form
            form_food = FoodForm()
            context['form_food'] = form_food
            return render(request, 'search/connect.html', context)


def disconnect(request, template_name='search/connect.html'):
    context = {
    }
    if not request.user.is_authenticated:
        form = ConnectForm(request.POST, error_class=ParagraphErrorList)
        context['form'] = form
        form_food = FoodForm()
        context['form_food'] = form_food
        return render(request, 'search/connect.html', context)
    else:
        auth_logout(request)
        return TemplateResponse(request, template_name, context)


"""
Clique sur boutton connecter et recherche
Pagination favoris et placement resultat correctement favoris et result
Suivre les esquisse et demandes du cahier des charges
"""
