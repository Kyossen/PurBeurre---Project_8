from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import ContactForm, ConnectForm, ParagraphErrorList, IngredientForm
from .models import *


def index(request):
    print(request)
    context = {
    }
    if request.method == 'POST':
        form = IngredientForm(request.POST, error_class=ParagraphErrorList)
        ingredient = form.cleaned_data['ingredient']
        result(ingredient)
        print(ingredient)
        return render(result(ingredient), 'search/connect.html')
    else:
        # GET method. Create a new form to be used in the template.
        form = IngredientForm()
    context['form'] = form
    return render(request, 'search/index.html', context)


def sign_up(request):
    context = {
    }
    if request.method == 'POST':
        form = ContactForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            email = form.cleaned_data['email']
            wordpass = form.cleaned_data['wordpass']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            print(email, wordpass, name, surname)
            print('Valid')
            new_account_db = Account(email=email,
                                     wordpass=wordpass,
                                     name=name,
                                     surname=surname)
            new_account_db.save()
            # print(new_account_db)

            print('Save in table')
        else:
            context['errors'] = form.errors.items()
            print('False')
    else:
        # GET method. Create a new form to be used in the template.
        form = ContactForm()
    context['form'] = form
    return render(request, 'search/sign_up.html', context)


def connect(request):
    user_connected = request
    print(user_connected)
    All_accounts = Account.objects.all()
    context = {
    }
    if request.method == 'POST':
        form = ConnectForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            i = 0
            email = form.cleaned_data['email']
            wordpass = form.cleaned_data['wordpass']
            user_mail = All_accounts.get(email=email)
            user_wp = All_accounts.filter(wordpass=wordpass)
            for find_account in All_accounts:
                if user_mail == All_accounts[i]:
                    try:
                        if user_wp[i] == All_accounts[i]:
                            print('Connected')
                            user_connected = True
                            stay_connect(user_connected)

                        else:
                            i += 1

                    except:
                        message_id_error = "Adresse email et/ou mot de passe incorrect"
                        print(message_id_error)
        else:
            context['errors'] = form.errors.items()
            print('False')
    else:
        # GET method. Create a new form to be used in the template.
        form = ConnectForm()
    context['form'] = form
    if user_connected is True:
        context['connected'] = user_connected
        return render(request, 'search/dashboard.html', context)
    else:
        return render(request, 'search/connect.html', context)


def dashboard(request):
    user_connected = request
    return render(request, 'search/dashboard.html')


def favorites(request):
    template = loader.get_template('search/favorites.html')
    return HttpResponse(template.render(request=request))


def stay_connect(request):
    context = {
    }
    user_connected = request
    if user_connected is True:
        context['connected'] = user_connected
        print(context)
    connect(user_connected)
    print(user_connected)
    index(user_connected)
    dashboard(user_connected)
    sign_up(user_connected)
    favorites(user_connected)
    return user_connected, context


def result(request):
    template = loader.get_template('search/result.html')
    print(request)
    return HttpResponse(template.render(request=request))
