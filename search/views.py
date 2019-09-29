"""
This import is obligatory for the good of the system
Lib imports, they are important to help Django a have all tools for a good use
Imports of files, they are important for
this view file because it gives access to forms and templates
Imports of Django lib, is a base for well functioning
"""


# Import lib
import math
import string
import time
import requests

# Import Django
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.response import TemplateResponse

# Import file
from .forms import SignupForm, ConnectForm, FoodForm, ParagraphErrorList
from .models import Account, Substitution


"""
Index function is a function that manage the platform base
She get a input user and
execute a find with API OpenFoodFact and result function
"""


def index(request):
    context = {
    }
    # Get input user
    if request.method == 'POST':
        form = FoodForm(request.POST, error_class=ParagraphErrorList)
        food = form.cleaned_data['food']
        # Give a input
        result(food)
    else:
        # GET method. Create a new form to be used in the template.
        form = FoodForm()
    context['form_food'] = form
    return render(request, 'search/index.html', context)


"""
Sing_up function is the function for allow a user on sign up
"""


def sign_up(request):

    # Get all account
    All_accounts = User.objects.all()
    context = {
    }

    # Get a input
    if request.method == 'POST':
        form = SignupForm(request.POST, error_class=ParagraphErrorList)
        # Check input if she valid or not
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if email exist or not
            create_email = All_accounts.filter(username=email)
            wordpass = form.cleaned_data['wordpass']
            wordpass_2 = form.cleaned_data['wordpass_2']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            phone = form.cleaned_data['phone']
            date_birth = form.cleaned_data['date_of_birth']
            address = form.cleaned_data['postal_address']
            # Start a create account and checking information input
            if not create_email:
                # Check if the password is the same
                if wordpass == wordpass_2:
                    # Check if the special character in the password is present
                    exclude = set(string.punctuation)
                    for ch in wordpass:
                        if ch in exclude:
                            # Check if length of the password is good
                            if 12 >= len(wordpass) >= 6:
                                nb_list = ['1', '2', '3', '4', '5',
                                           '6', '7', '8', '9', '0']
                                for nb in wordpass:
                                    if nb in nb_list:
                                        # Check if length of
                                        # the phone number is good
                                        if 17 >= len(phone) >= 10:
                                            # Check if length of
                                            # the postal adress is good
                                            if 25 >= len(address) >= 1:
                                                # Add a new user
                                                # in the User table
                                                user = User.\
                                                    objects.create_user(
                                                        first_name=name,
                                                        last_name=surname,
                                                        username=email,
                                                        password=wordpass)
                                                """
                                                Add a new user in the Account
                                                table with a foreign
                                                key on User table
                                                for create more
                                                information on new user
                                                """
                                                new_account_db = \
                                                    Account(
                                                     user=user,
                                                     phone=phone,
                                                     date_of_birth=date_birth,
                                                     postal_address=address)
                                                # Save the new user
                                                user.save()
                                                new_account_db.save()
                                                form_food = FoodForm()
                                                context['form_food']\
                                                    = form_food
                                                form_connect = ConnectForm()
                                                context['form']\
                                                    = form_connect
                                                return render(
                                                    request,
                                                    'search/connect.html',
                                                    context)

                                            # Below the structure
                                            # of the "else" condition.
                                            # This structure
                                            # returns the errors potentials
                                            else:
                                                context['error'] = \
                                                    'Veuillez entrer' \
                                                    ' une adresse valide.'
                                        else:
                                            context['error'] = 'Veuillez' \
                                                               ' entrer un ' \
                                                               'numéro de ' \
                                                               'téléphone' \
                                                               ' valide ' \
                                                               '(exemple: ' \
                                                               '01-02-33-06' \
                                                               '-09 ou ' \
                                                               '+336-09-85' \
                                                               '-96-48)'
                                    else:
                                        context['error'] = \
                                            'Veuillez ajouter un ' \
                                            'chiffre à votre mot de passe.'
                            else:
                                context['error'] = \
                                    'La longueur du mot ' \
                                    'de passe doit être de 6 à 12 caractères.'
                        else:
                            context['error'] = \
                                'Veuillez ajouter un ' \
                                'caractère spécial à votre mot de passe.'
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


"""
The connect function is the function
allow a user of the connect on the platform
"""


def connect(request):
    context = {
    }
    # Check if user is connect or not
    if not request.user.is_authenticated:
        # Give a input
        if request.method == 'POST':
            form = ConnectForm(request.POST, error_class=ParagraphErrorList)
            # Check if input is good
            if form.is_valid():
                email = request.POST['email']
                wordpass = request.POST['wordpass']
                # Connect the user
                user_connected = \
                    authenticate(request, username=email, password=wordpass)
                # Check if input is good or not
                if user_connected is not None:
                    # Connect the user and allow
                    # stay connect (create asession for user)
                    login(request, user=user_connected)
                    request.session['member_id'] = user_connected.id
                    time.sleep(4)
                    return HttpResponseRedirect('dashboard.html')
                else:
                    # Return a error
                    context['form'] = form
                    context['form_food'] = FoodForm()
                    context['error_login'] = \
                        "Adresse email et/ou mot de passe incorrect"
                    return render(request, 'search/connect.html', context)
            else:
                # Return a error
                context['errors'] = form.errors.items()
        else:
            form = ConnectForm()
        context['form'] = form
        context['form_food'] = FoodForm()
        return render(request, 'search/connect.html', context)

    """
    If the user clicks on the login
    page and the user is logged in,
    him is return go to another page
    """
    if request.user.is_authenticated:
        if request:
            dashboard(request)
            return HttpResponseRedirect('dashboard.html')

        if request == 'search/favorites':
            return render(request, 'search/favorites.html', context)


"""
Dashboard is the handler of the user dashboard
"""


def dashboard(request):
    context = {
    }
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
                        form = FoodForm()
                        context['form_food'] = form
                        return render(request,
                                      'search/dashboard.html', context)


"""
Result is the function that displays the results after a search
With result.html she allow of display the foods
    with a icon save or not save for each users
"""


def result(request):
    context = {
    }
    list_products = []
    # Give a input
    if request.method == 'POST':
        # Check if input is good
        if request.POST.get('food') == "":
            form = FoodForm()
            context['form_food'] = form
            context['error_result'] = "Nous avons eu " \
                                      "un problème, pouvez " \
                                      "vous recommencer ? Merci."
            return render(request, 'search/result.html', context)
        else:
            form = FoodForm()
            food = request.POST['food']
            print(food)
            """
            With the food choice,
            we do a request to OpenFoodFact
            for get the more information on food
            """
            result_food = requests.get(
                "https://world.openfoodfacts.org/cgi/search.pl?search_terms="
                + food.lower() +
                "&search_simple=1&json=1")
            response = result_food.json()
            # Check if the answer is exploitable or not
            if len(response['products']) != 0:
                # Read the answer from OpenFoodFact
                for result_response in response['products']:
                    if 'product_name' in result_response:
                        context['name_result'] = \
                            result_response['product_name']
                    if 'product_name' not in result_response:
                        context['error_result'] = "Nous sommes désolé, " \
                                                  "le produit demandé est " \
                                                  "introuvable."
                    if 'image_front_url' in result_response:
                        context['img_result'] = \
                            result_response['image_front_url']
                    if 'image_front_url' not in result_response:
                        context['img_result'] = "Nous sommes désolé, " \
                                                "le produit demandé est " \
                                                "introuvable."
                    if len(result_response['categories_tags']) != 0:
                        i = 0
                        """
                        Create an infinite loop to browse different
                            categories to retrieve answers for users
                        """
                        while True:
                            search_categories = \
                                "https://fr.openfoodfacts.org/categorie"
                            search_substitution = requests.get(
                                search_categories + "/" +
                                result_response['categories_tags'][i] +
                                ".json")
                            result_substitution = search_substitution.json()
                            # Read the answer from OpenFoodFact
                            for products in result_substitution:
                                if len(result_substitution['products']) != 0:
                                    for p_result in \
                                            result_substitution['products']:
                                        if 'nutrition_grades' \
                                            in p_result and \
                                            (p_result['nutrition_grades']
                                             == "a"
                                             or p_result['nutrition_grades']
                                             == "b"
                                             or p_result['nutrition_grades']
                                             == "c"
                                             or p_result['nutrition_grades']
                                             == "d"):
                                            if p_result not in list_products:
                                                # Add a result in the list
                                                # for the display
                                                # with result.html
                                                list_products.append(p_result)
                                        if 'nutrition_grades' not in p_result:
                                            p_result['nutrition_grades'] = ""
                                        context['product_result'] = \
                                            list_products

                                        """
                                        Create a pagination for users.
                                        This allows to browse of the
                                        results an multiple pages
                                        """
                                        list_for_page = []
                                        for page_nb in list_products:
                                            if page_nb['product_name'] \
                                                    not in list_for_page:
                                                list_for_page.append(
                                                    page_nb['product_name'])
                                        """
                                        paginator = Paginator(list_for_page, 10)
                                        print(request.POST.get('page'))
                                        page = request.GET.get('page')
                                        print(page)
                                        nb_page = paginator.get_page(page)
                                        """
                                        nb_page = math.ceil(len(list_for_page) / 10)
                                        context['nb_page'] = nb_page
                            # Stop the loop infinity and
                            # get user info for display of the results
                            if i + 1 == \
                                    len(result_response['categories_tags']):
                                form = FoodForm()
                                context['form_food'] = form
                                if request.user.is_authenticated:
                                    food_all = Substitution.objects.all()
                                    for food_save in food_all:
                                        user = request.session['member_id']
                                        if food_save.user_id == user:
                                            for product in list_products:
                                                if food_save.product == \
                                                        product['product_name']:

                                                    context['save_food'] = \
                                                        food_save.product
                                else:
                                    context['not_save_food'] = True
                                return render(request,
                                              'search/result.html', context)
                            i += 1
                    # Return a error
                    else:
                        form = FoodForm()
                        context = {'form_food': form,
                                   'error_result': "Nous sommes désolé,"
                                                   " le produit demandé "
                                                   "est introuvable."
                                                   " Il ce peux également que "
                                                   "nous n'ayons pas de "
                                                   "produit substituable "
                                                   "pour ce dernier...",
                                   'img_result': None}
                        return render(request, 'search/result.html', context)
            # Return a error
            else:
                form = FoodForm()
                context['form_food'] = form
                context['error_result'] =\
                    "Nous avons eu un problème, " \
                    "pouvez vous recommencer ? Merci."
                return render(request, 'search/result.html', context)
    else:
        # GET method. Create a new form to be used in the template.
        form = FoodForm()
    context['form_food'] = form
    return render(request, 'search/result.html', context)


"""
Description is the function for description page
"""


def description(request):
    context = {
    }
    # Check if product is present in the url
    if 'product' in request.GET:
        product_name = request.GET
        # If product is present execute a request to OpenFoodFact
        for product_result in product_name['product']:
            result_food = requests.get(
                "https://world.openfoodfacts.org/cgi/search.pl?search_terms=" +
                product_name['product'] +
                "&search_simple=1&json=1")
            response = result_food.json()
            context['product_name'] = product_name['product']
            """
            Browse the answer and get the information
                for display in page description.html
            """
            for product_descritpion in response['products']:
                if 'nutrition_grades' in product_descritpion and \
                        (product_descritpion['nutrition_grades'] == "a"
                         or product_descritpion['nutrition_grades'] == "b"
                         or product_descritpion['nutrition_grades'] == "c"
                         or product_descritpion['nutrition_grades'] == "d"):
                    context['product_score'] = \
                        product_descritpion['nutrition_grades']
                if 'nutrition_grades' not in product_descritpion:
                    product_descritpion['nutrition_grades'] = ""
                if 'image_url' in product_descritpion:
                    context['product_img'] = product_descritpion['image_url']
                if 'url' in product_descritpion:
                    context['product_url'] = product_descritpion['url']
                if 'ingredients_text_fr' in product_descritpion:
                    context['product_nutrition_data_per'] = \
                        product_descritpion['ingredients_text_fr']
                if 'ingredients_text_fr' not in product_descritpion:
                    product_descritpion['ingredients_text_fr'] = ""

                form = FoodForm()
                context['form_food'] = form
                return render(request, 'search/description.html', context)

    """
    Check url of the description is valid or not
    If not valid, return a error
    """
    if request.GET == '/search/description.html?product=':
        context['error_description'] = \
            "Nous avons eu un problème, pouvez vous recommencer ? Merci."
        form = FoodForm()
        context['form_food'] = form
        return render(request, 'search/description.html', context)
    else:
        form = FoodForm()
        context['form_food'] = form
        context['error_description'] = \
            "Nous avons eu un problème, pouvez vous recommencer ? Merci."
        return render(request, 'search/description.html', context)


"""
Favorites is the function for add a favorites food in database for users
She is also the function for display the favorites for the users
"""


def favorites(request):
    context = {
    }
    # Check if product is present in the url
    if 'product' in request.GET:
        product_name = request.GET
        # If product is present execute a request to OpenFoodFact
        for product_result in product_name['product']:
            result_food = requests.get(
                "https://world.openfoodfacts.org/cgi/search.pl?search_terms=" +
                product_name['product'] +
                "&search_simple=1&json=1")
            response = result_food.json()
            context['product_name'] = product_name['product']
            """
            Browse the answer and get the need information
            for add the favorite in database
            """
            for product_add_favorites in response['products']:
                if 'nutrition_grades' in product_add_favorites and \
                        (product_add_favorites['nutrition_grades'] == "a"
                         or product_add_favorites['nutrition_grades'] == "b"
                         or product_add_favorites['nutrition_grades'] == "c"
                         or product_add_favorites['nutrition_grades'] == "d"):
                    context['product_score'] = \
                        product_add_favorites['nutrition_grades']
                if 'nutrition_grades' not in product_add_favorites:
                    product_add_favorites['nutrition_grades'] = ""
                if 'image_url' in product_add_favorites:
                    context['product_img'] = product_add_favorites['image_url']
                if 'image_url' not in product_add_favorites:
                    product_add_favorites['image_url'] = ""

                # Check if user is connect
                if request.user.is_authenticated:
                    users_all = User.objects.all()
                    food_all = Substitution.objects.all()
                    list_save = []
                    list_for_save = []
                    # Check which user want add the favorite
                    for user_save in users_all:
                        user = request.session['member_id']
                        if user_save.id == user:
                            if len(food_all) != 0:
                                for food_save in food_all:
                                    # Check if the user
                                    # has already added a favorite
                                    if user == food_save.user_id:
                                        product_add = product_name['product']
                                        list_save.append(food_save.product)
                                        # If the new product
                                        # not in list product of the user
                                        if product_add not in list_save:
                                            list_for_save.append(product_add)
                                        # If the new product is
                                        # in list product of the user
                                        else:
                                            data = {'error_food':
                                                    'Vous avez déjà '
                                                    'enregistré cet aliment.'}
                                            return JsonResponse(data)
                                    else:
                                        product_add = product_name['product']
                                        if product_add not in list_save:
                                            list_for_save.append(product_add)
                            else:
                                product_add = product_name['product']
                                if product_add not in list_save:
                                    list_for_save.append(product_add)
                            print(list_for_save[0])
                            # Add the new product
                            # in the favorites products of user
                            new_substitution_db = Substitution(
                                user_id=user_save.id,
                                product=list_for_save[0],
                                nutrition_grade=product_add_favorites[
                                   'nutrition_grades'],
                                img_url=product_add_favorites['image_url'])
                            new_substitution_db.save()
                    data = {'success_save': 'Enregistrement effectué.'}
                    return JsonResponse(data)
                # Si l'utilisateur n'est pas
                #   connecté mais essaie d'ajouter un favori,
                #   le système renvoie une erreur.
                else:
                    data = {'error_food':
                            'Vous devez être connecté '
                            'pour effectuer cette requête. Merci'}
                    return JsonResponse(data)
    # If user open favorites page and not add favorites
    else:
        list_products = []
        dict_data = {}
        i = 0
        # Check if user is connect
        if request.user.is_authenticated:
            # Create a list for browse all favorites
            food_all = Substitution.objects.all()
            if len(food_all) != 0:
                for food_display in food_all:
                    user = request.session['member_id']
                    # Check if user have already added of the favorites
                    if food_display.user_id == user:
                        list_products.append(food_display.product)
                        # Create a dict for display the favorites
                        dict_data['products_' + str(i)] = \
                            food_display.product,\
                            food_display.nutrition_grade, \
                            food_display.img_url
                        i += 1
                        continue
                    # If user not have already added of the favorites
                    # Return a error
                    else:
                        form_food = FoodForm()
                        context['form_food'] = form_food
                        context['not_food'] = "Vous n'avez pas" \
                                              "encore enregistré d'aliment."
                        return render(request,
                                      'search/favorites.html', context)

                """
                Stop the loop, return the results
                    and create a pagination running like result
                """
                if i == len(list_products):
                    page_items = tuple(dict_data.items())
                    paginator = Paginator(page_items, 6)
                    page = request.GET.get('page')
                    nb_page = paginator.get_page(page)

                    form = FoodForm()
                    context['nb_page'] = nb_page
                    context['product_result'] = dict_data
                    context['form_food'] = form
                    return render(request, 'search/favorites.html', context)
            # If user not have already added of the favorites
            # Return a error
            else:
                form_food = FoodForm()
                context['form_food'] = form_food
                context['not_food'] = "Vous n'avez pas" \
                                      "encore enregistré d'aliment."
                return render(request, 'search/favorites.html', context)
        # If user is not connect
        else:
            form = ConnectForm(request.POST, error_class=ParagraphErrorList)
            connect(request)
            context['form'] = form
            form_food = FoodForm()
            context['form_food'] = form_food
            return render(request, 'search/connect.html', context)


"""
Disconnect is the function for disconnect a user
"""


def disconnect(request, template_name='search/index.html'):
    context = {
    }
    # Check if user is connect
    if not request.user.is_authenticated:
        form = ConnectForm(request.POST, error_class=ParagraphErrorList)
        context['form'] = form
        form_food = FoodForm()
        context['form_food'] = form_food
        # If user is not connect, user is redirect to index page
        return render(request, 'search/index.html', context)
    else:
        # If user is connect, user is disconnect and redirect to index page
        auth_logout(request)
        form = FoodForm()
        context['form_food'] = form
        return TemplateResponse(request, template_name, context)


"""
copyright page is the function for
    redirect a user to the copyright page
"""


def copyright_page(request):
    context = {}
    form_food = FoodForm()
    context['form_food'] = form_food
    return render(request, 'search/copyright.html', context)

"""
# A faire

font-awesome page 2 esquisse

PEP8 Python3 -> Finir views.py

# Correction

#Ajout manquant

#Aide
Finition page favoris -> Pagination
Finition page result -> Pagination
Finition page description -> Repère nutritionnel
Finition page Dashboard -> mobile responsive
Finition page inscription



Responsive en fonction des esquisses -> attendre fin prochaine session
"""
