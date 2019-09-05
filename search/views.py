import string

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render

from .forms import SignupForm, ConnectForm, IngredientForm, ParagraphErrorList
from .models import *


def index(request):
    print(request)
    context = {
    }
    if not request.user.is_authenticated or request.user.is_authenticated:
        if request.method == 'POST':
            form = IngredientForm(request.POST, error_class=ParagraphErrorList)
            ingredient = form.cleaned_data['ingredient']
            result(ingredient)
            print(ingredient)
            return render(request, 'search/result.html', context)
        else:
            # GET method. Create a new form to be used in the template.
            form = IngredientForm()
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
        # return render(request, 'search/dashboard.html', context)
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
    if not request.user.is_authenticated:
        return render(request, 'search/connect.html', context)
    else:
        return render(request, 'search/result.html', context)


def disconnect(request):
    context = {
    }
    if not request.user.is_authenticated:
        return render(request, 'search/connect.html', context)
    else:
        users = User.objects.all()
        for users_connected in users:
            print(users_connected)
            print(users_connected.id)
            user = request.session['member_id']
            if users_connected.id == user:
                print('True')
                del request.session['member_id']
                print('disconnect')
                connect(request)
                return render(request, 'search/favorites.html', context)
