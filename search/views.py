#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This import is obligatory for the good of the system
Lib imports, they are important to help Django a have all tools for a good use
Imports of files, they are important for
this view file because it gives access to forms and templates
Imports of Django lib, is a base for well functioning"""


# Import Django
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Import file
from users import views
from users.forms import ConnectForm
from users.models import Substitution
from .forms import FoodForm, ParagraphErrorList
from .models import Product


def index(request):
    """Index function is a function that manage the platform base
    She get a input user and execute a find with
    the database, and result function"""
    context = {}
    # Get input user
    if request.method == 'POST':
        form = FoodForm(request.POST, error_class=ParagraphErrorList)
    else:
        # GET method. Create a new form to be used in the template.
        form = FoodForm()
    context['form_food'] = form
    return render(request, 'search/index.html', context)


def result(request):
    """Result is the function that displays the results after a search
    With result.html she allow of display the foods
        with a icon save or not save for each users"""
    context = {}
    list_products = []
    if request.method == 'POST':
        # Check if input is good
        if request.POST.get('food') == "":
            context['form_food'] = FoodForm()
            context['error_result'] = "Nous avons eu un problème, pouvez " \
                                      "vous recommencer ? Merci."
            return render(request, 'search/result.html', context)
        else:
            food = request.POST['food']
            # Getting a more info on food
            return result_search(request, food, list_products)

    else:
        # Check if user use a correct url when the page is the next or previous
        if 'page' in request.GET:
            food = request.GET['search']
            return result_search(request, food, list_products)


def result_search(request, food, list_products):
    """This function is used for get information
    on the food in the database with a filter"""
    context = {}
    food = Product.objects.filter(name__icontains=food)
    for food_result in food:
        context['name_result'] = food_result.name
        context['img_result'] = food_result.image_url
        return result_search_categories(request, food_result.categories,
                                        list_products, context)
    if not food:
        return error_result(request, 'not_exist')


def result_search_categories(request, c_result, list_products, context):
    """This function is used for get information on the food
    that have a same categories that the choice user
    by the database"""
    context = context
    # filter the data
    result_Products = Product.objects.filter(categories_id=c_result)
    for search_food in result_Products:
        if search_food.nutrition_grade != "":
            if search_food not in list_products:
                list_products.append(search_food)

    context['product_result'] = list_products
    # Create a pagination for users.
    paginator = Paginator(list_products, 6)
    page = request.GET.get('page', 1)
    nb_page = paginator.get_page(page)
    context['nb_page'] = nb_page
    context['product_result'] = paginator.page(page)
    form = FoodForm()
    context['form_food'] = form
    # Get user info for display of the results
    return check_food_save_result(request, list_products, context)


def check_food_save_result(request, list_products, context):
    """This method allow display a food saved with a Font Awesome
    and if food don't save she display with a button for save"""
    context = context
    list_food_save = []
    if request.user.is_authenticated:
        # Get the food that user have saved
        food_all = Substitution.objects.filter(
            user=request.user)
        if len(food_all) == 0:
            context['save_food'] = list_food_save
        else:
            for food_save in food_all:
                for product in list_products:
                    g_product = product.name
                    # Check if the saved food is a same that display
                    if food_save.product == g_product:
                        list_food_save.append(food_save.product)
                        context['save_food'] = list_food_save
                    else:
                        context['save_food'] = list_food_save
    if not request.user.is_authenticated:
        context['save_food'] = list_food_save
    if 'page' in request.GET:
        context['search'] = request.GET['search']
    else:
        context['search'] = request.POST.get('food')
    return render(request, 'search/result.html', context)


def error_result(request, error):
    """This method is a method for return
    the potential errors when run a request"""
    context = {}
    if 'not_exist' in error:
        context['form_food'] = FoodForm()
        context['error_result'] = "Nous avons eu un problème, " \
                                  "pouvez vous recommencer ? Merci."
        return render(request, 'search/result.html', context, status=401)


def description(request):
    """Description is the method and the page for displaying
    more information on food and it provides access to the
    official page via a link to the OpenFoodFacts API"""
    context = {}
    # Check if product is present in the url
    product_id = request.GET.get('product')
    # Filter the id of the product for be sure that is a good product
    product = Product.objects.filter(code=product_id)
    for des_product in product:
        if des_product.name:
            context['product_name'] = des_product.name
            return description_result(request, product, context)
        else:
            context['error_description'] = "Nous n'avons pas d'informations " \
                                           "supplémentaires à disposition. " \
                                           "Toutes nos excuses."
            return render(request, 'search/description.html', context)
    if not product:
        return error_load_page(request, context)


def description_result(request, r_description, context):
    """Browse the database data and get the information
            for display in page description.html"""
    for des_product in r_description:
        if des_product.nutrition_grade != "":
            context['product_score'] = des_product.nutrition_grade
        if des_product.nutrition_grade == "":
            context['product_score'] = \
                "Nous ne dispons pas d'indice nutritionnel pour cet aliment."

        if des_product.image_url != "":
            context['product_img'] = des_product.image_url
        if des_product.image_url == "":
            context['product_img'] = \
                "Nous ne dispons pas d'image pour cet aliment."

        if des_product.ingredients == '':
            context['no_data'] = "Désolé nous ne dispons pas " \
                                 "de repère nutritionnel pour cet aliment."
        if des_product.ingredients != '':
            context['product_nutrition_data_per'] = des_product.ingredients
        context['product_url'] = des_product.url

        context['form_food'] = FoodForm()
        return render(request, 'search/description.html', context)


def error_load_page(request, context):
    """Check if url of the description is valid or not
    If he is not valid, this method return a error"""
    product_name = request.GET.get('product')
    if product_name is None or product_name == "":
        context['error_description'] = \
            "Nous avons eu un problème, pouvez vous recommencer ? Merci."
        context['form_food'] = FoodForm()
        return render(request, 'search/description.html', context)
    else:
        context['form_food'] = FoodForm()
        context['error_description'] = "Nous avons eu un problème, " \
                                       "pouvez vous recommencer ? Merci."
        return render(request, 'search/description.html', context)


def favorites(request):
    """Favorites is the method for add a favorites food in database of the users
    She is also the method for run the view for display
    of the favorites of the users"""
    context = {}
    product_id = request.GET.get('product')
    product = Product.objects.filter(code=product_id)
    for fav_product in product:
        if fav_product.name:
            context['product_name'] = fav_product.name
            return favorites_result(request, product)

    # If user open favorites page and not add favorites
    else:
        if request.user.is_authenticated:
            return views.favorites_user(request)
        # If user is not connect
        else:
            form = ConnectForm(request.POST, error_class=ParagraphErrorList)
            views.connect(request)
            context['form'] = form
            context['form_food'] = FoodForm()
            return render(request, 'search/connect.html', context)


def favorites_result(request, product):
    """Return a error or call a other method for
    continue a save process in favorites for user"""
    if product:
        return save_favorites(request, product)
    if not product:
        data = {'error_food': 'Suite à un incident technique nous ne '
                              'pouvons enregistrer cet aliment dans vos '
                              'favoris. Toutes nos excuses.'}
        return JsonResponse(data)


def save_favorites(request, new_favorites):
    """Save Favorites is the method that allows the system to check which
    foods the user has already saved and also backed up the new ones."""
    if request.user.is_authenticated:
        list_save = []
        food_all = Substitution.objects.filter(
            user__id=request.session['member_id'])
        for new_food in new_favorites:
            # Check if the user has already added a favorite
            if len(food_all) != 0:
                for food_save in food_all:
                    # Create a list of his already added products
                    list_save.append(food_save.product)
                    if new_food.name not in list_save:
                        pass
                    else:
                        data = {'error_food':
                                'Vous avez déjà enregistré cet aliment.'}
                        return JsonResponse(data)
            else:
                pass
            # Add the new product in the favorites products of user
            new_substitution_db = Substitution(
                user_id=request.session['member_id'],
                product=new_food.name,
                nutrition_grade=new_food.nutrition_grade,
                img_url=new_food.image_url,
                code=new_food.code)
            new_substitution_db.save()
            data = {'success_save': 'Enregistrement effectué.'}
            return JsonResponse(data)
    # If the user is not logged in
    else:
        data = {'error_food':
                'Vous devez être connecté pour effectuer cette enregistrement.'
                ' Merci'}
        return JsonResponse(data)


def copyright_page(request):
    """Copyright page is the method for
    redirect a user to the copyright page"""
    context = {}
    context['form_food'] = FoodForm()
    return render(request, 'search/copyright.html', context)
