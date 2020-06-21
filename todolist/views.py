from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth import login
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

def currenttodos(request):
    return render(request, 'todo/currenttodos.html')