from __future__ import unicode_literals
from django.db import models
from apps.login_register.models import *

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors={}
        if len(postData['title']) < 3:
            errors['title_error']="Title must be at least 3 Characters."
        if len(postData['description']) < 3:
            errors['description_error'] = 'Description must be at least 3 chracters.'
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    sample_chapter = models.FileField(blank=True, null=True,
        upload_to="chapters/%Y/%m/%D/")
    cover_image = models.FileField(blank=True, null=True, 
        upload_to ="covers/%Y/%m/%D/")
    reserved_by = models.ForeignKey(User, related_name='reserved_by_user', null=True)
    uploaded_by = models.ForeignKey(User, related_name='uploaded_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class BookTracked(models.Model):
    book_tracked = models.ForeignKey(Book, related_name='book_views' )
    ip = models.CharField(max_length=16) #only accounting for ipv4
    user = models.ForeignKey(User, related_name='user_views') #if you want to track logged in or anonymous