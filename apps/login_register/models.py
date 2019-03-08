from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) <= 1:
            errors["first_name_len"] = "First name should be at least 2 characters"
        if len(postData['last_name']) <= 1:
            errors["last_name_len"] = "Last name should be at least 2 characters"
        if postData['first_name'].isalpha() == False:
            errors['first_name_char']="First Name can only contain letters."
        if postData['last_name'].isalpha() == False:
            errors['last_name_char']="Last Name can only contain letters."
        if len(postData['email']) < 8:
            errors["email_len"] = "Email address at least 8 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_invalid']= "Invalid email address"
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['email_exists']="Email already exists."
        if len(postData['password']) < 8:
            errors["password_len"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['password_invalid']= "Passwords do not match."
        if re.search('[0-9]', postData['password']) is None or re.search('[A-Z]', postData['password']) is None:
            errors['password_char']="Password must contain at least 1 digit and 1 capital letter."
        # compare that postData['password'] == postData['confirm_password']
        return errors

    def login_validator(self, postData):
        errors = {}
        user = self.filter(email=postData['login_email'])
        # if len(email_check) < 1:
        #     errors['login_email'] = "Cannot log in."
        if len(postData['login_email']) == 0:
            errors['email_empty']="Registered email please."
        if len(self.filter(email=postData['login_email'])) == 0:
            errors['no_email']="Email cannot be empty."
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['invalid_email']="Valid email please."
        if len(errors) == 0:
            if not bcrypt.checkpw(postData['login_password'].encode(), user[0].password.encode()):
                errors['wrong_password']="Valid password please."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()