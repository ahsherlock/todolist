from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
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

@login_required
def currenttodos(request):
    #Get current list of thetodos that belong to user and are not completed
    #If dateCompleted == null then the task isnt completed
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})
@login_required
def completedtodos(request):
    #Get current list of the completedtodos that belong to user
    #If dateCompleted isnt Null then the task is completed
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos})

@login_required
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

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        #Someone has posted shit, this is what happens next
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error':'Bad data was passed in. Y U Dis? Try again.' })



@login_required
def viewtodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk)
    #making it editable. form created from model, can pass model instance and information will be filled
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form':form})
    else:
        #If it's a POST request
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error':'Bad Information, Try again.'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')
@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')