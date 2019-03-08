from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from apps.login_register.models import *

def index(request, id):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id=id),
    }
    return render(request, 'user_dashboard/index.html', context)

def process_user_edit(request, id):
    user = User.objects.get(id=id)
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.save()
    return redirect("/show_book_edit")