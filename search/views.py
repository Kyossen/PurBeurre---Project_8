from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import ContactForm, ConnectForm, ParagraphErrorList
from .models import *


def index(request):
    template = loader.get_template('search/index.html')
    return HttpResponse(template.render(request=request))


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
    user_connected = False
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
                    i += 1
                    try:
                        if user_wp[i] == All_accounts[i]:
                            print('Connected')
                            user_connected = True
                            dashboard(user_connected)

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
    if user_connected is False:
        return render(request, 'search/connect.html', context)
    else:
        context['connected'] = user_connected
        return render(request, 'search/dashboard.html', context)


def dashboard(request):
    user_connected = request
    print(user_connected)
    return render(request, 'search/dashboard.html')


def favorites(request):
    template = loader.get_template('search/favorites.html')
    return HttpResponse(template.render(request=request))