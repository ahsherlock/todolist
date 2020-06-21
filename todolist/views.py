from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.contrib.auth import login, logout, authenticate
# Create your views here.
def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # When user signs up, save them into database, log them in,
                # redirect to current to-do list
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')

            except IntegrityError:
                #If Username already exists, we go here
                return render(request, 'todo/signupuser.html',{'form': UserCreationForm(), 'error': 'That username already exists. Enter different one.'})

        else:
            #Tell them that the passwords dont match
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'The passwords do not match.'})

def home(request):
    return render(request, 'todo/home.html')


def currenttodos(request):
    return render(request, 'todo/currenttodos.html')


def logoutuser(request):
    #ABSOLUTELY NEEDED ELSE browsers will automatically log users out.
    # Something to do with the way browsers preload "GET" requests
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'todo/loginuser.html',{'form': AuthenticationForm(),'error':'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('currenttodos')