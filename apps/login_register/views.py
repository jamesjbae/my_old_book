from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    request.session.clear()
    return render(request, 'login_register/index.html')

def login(request):
    request.session['action']='login'
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.items():
                messages.error(request, error, extra_tags=tag)
        return redirect('/login_register')
    else:
        user=User.objects.get(email=request.POST['login_email'])
        request.session['first_name']=user.first_name
        request.session['user_id']=user.id
        return redirect("/")

def register(request):
    request.session['action']='register'
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.items():
                messages.error(request, error, extra_tags=tag)
        # for key, value in errors.items():
                # messages.error(request, value)
        request.session['first_name']=request.POST['first_name']
        request.session['last_name']=request.POST['last_name']
        request.session['email']=request.POST['email']
        return redirect('/login_register')
    else:
        hash1=bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash1)
        user=User.objects.get(email=request.POST['email'])
        request.session['first_name']=user.first_name
        request.session['user_id']=user.id
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect('/')