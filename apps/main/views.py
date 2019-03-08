from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import *
from apps.login_register.models import *

def index(request):
    if not 'user_id' in request.session:
        return redirect('/login_register')
    context = {
        'all_users' : User.objects.all(),
        'all_books' : Book.objects.order_by('-created_at')
    }
    return render(request, "main/index.html", context)

def about(request):
    if not 'user_id' in request.session:
        return redirect('/login_register')
    context = {
        'all_users' : User.objects.all(),
        'all_books' : Book.objects.order_by('-created_at')
    }
    return render(request, "main/about.html", context)

def project(request):
    if not 'user_id' in request.session:
        return redirect('/login_register')
    context = {
        'all_users' : User.objects.all(),
        'all_books' : Book.objects.order_by('-created_at')
    }
    return render(request, "main/project.html", context)

def upload_new_book(request):
    if not 'user_id' in request.session:
        return redirect('/login_register')
    context = {
        'all_books' : Book.objects.all()
        # 'upload_info':request.session['user_id']
    }
    return render(request, "main/upload_new_book.html", context)

def process_new_book(request):
    errors=Book.objects.book_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
    request.session['title']=request.POST['title']
    request.session['author']=request.POST['author']
    request.session['category']=request.POST['category']
    request.session['description']=request.POST['description']
    uploaded_by = User.objects.get(id=request.session['user_id'])
    Book.objects.create( title=request.POST['title'],
                        author=request.POST['author'],
                        category=request.POST['category'],
                        description=request.POST['description'],
                        sample_chapter=request.FILES['sample_chapter'],
                        cover_image=request.FILES['cover_image'],
                        uploaded_by=uploaded_by)
    return redirect("/upload_new_book")

def reading_book(request):
    context = {
        'all_books' : Book.objects.all()
    }
    return render(request, "main/reading_book.html", context)

def my_book_list(request, id):
    if not 'user_id' in request.session:
        return redirect('/login_register')
    context = {
        'all_books' : Book.objects.order_by('-created_at')
    }
    return render(request, "main/my_book_list.html", context)

def show_book_edit(request, id):
    context = {
        'book' : Book.objects.get(id=id)
    }
    return render(request, "main/my_book_edit.html", context)

def process_book_edit(request, id):
    errors=Book.objects.book_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
    book = Book.objects.get(id=id)
    book.title = request.POST['title']
    book.author = request.POST['author']
    book.category = request.POST['category']
    book.description = request.POST['description']
    book.cover_image = request.POST['cover_image']
    book.sample_chapter = request.POST['sample_chapter']
    book.save()
    return redirect('/show_book_edit')

def show_book(request, id):
    context = {
        'book' : Book.objects.get(id=id)
    }
    return render(request, "main/show_book.html", context)

def reserve_book(request, id):
    book = Book.objects.get(id=id)
    my_book = User.objects.get(id=request.session['user_id'])
    my_book.reserved_by_user.add(book)
    return redirect("/")

def cancel(request, id):
    book = Book.objects.get(id=id)
    cancel_book = User.objects.get(id=request.session['user_id'])
    cancel_book.reserved_by_user.remove(book)
    return redirect('/')

def delete(request, id):
    book = Book.objects.get(id=id)
    if book.uploaded_by.id == request.session['user_id']:
        book.delete()
        return redirect('/')
    if book.uploaded_by.id == request.session['user_id']:
        book.delete()
        return redirect('/')
    else:
        return redirect('/')

def book_view(request, id):
    book_tracked, created = BookTracked.objects.get_or_create(id=id, ip=request.ip, user=request.session.user)
    if created:
        book_tracked.post.count += 1
        book_tracked.post.save()
    return redirect('/')
