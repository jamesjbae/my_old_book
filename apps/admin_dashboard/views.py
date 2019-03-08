from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from apps.login_register.models import *

def index(request):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        'all_admins' : User.objects.all()
    }
    return render(request, "admin_dashboard/index.html", context)
