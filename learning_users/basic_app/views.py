from django.shortcuts import render
from basic_app.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')


@login_required
def special(request):
    return HttpResponse("you are logget in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registrated = False

    if request.method == "POST":
        user_form=UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registrated = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()

    return render(request, 'basic_app/registration.html',
                                    {'user_form':user_form,
                                           'registrated':registrated})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)


        if user:
            if user.is_activate:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("acc not active")

        else:
            print("someasdasfaf")
            print("Username:{} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request, 'basic_app/login.html', {})
