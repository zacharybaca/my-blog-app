from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from blog.forms import CreateBlog

# Create your views here.
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('all_blogs')
            except IntegrityError:
                return render(request, 'signupuser.html', {'form': UserCreationForm()}, {'error': 'That Username Has Already Been Taken'})
        else:
            return render(request, 'signupuser.html', {'form': UserCreationForm()}, {'error': 'Passwords Did Not Match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'form': AuthenticationForm()}, {'error': 'The Username and Password Did Not Match'}) 
        else:
            login(request, user)
            return redirect('all_blogs') 

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index') 

@login_required
def createblog(request):
    if request.method == 'GET':
        return render(request, 'createblog.html', {'form': CreateBlog()})
    else:
        try:
            form = CreateBlog(request.POST)
            newpost = form.save(commit=False)
            newpost.user = request.user
            newpost.save()
            return redirect('all_blogs')
        except ValueError:
            return render(request, 'createblog.html', {'form': CreateBlog(), 'error': 'Bad Data'})