from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def register(self, postData):
        print "***REGISTRATION INITIALISED"
        errors = []
        if len(postData['name']) < 1:
            errors.append('Name cannot be blank.')
        if len(postData['name']) <3:
            errors.append('Name is too short.')
        if len(postData['alias']) < 1:
            errors.append('Alias cannot be blank.')
        if len(postData['email']) < 1:
            errors.append('Email cannot be blank.')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Email is in invalid format.')
        if len(postData['password']) < 1:
            errors.append('Password cannot be blank.')
        if len(postData['password']) <8:
            errors.append('Password is too short.')
        if len(postData['dob']) < 1:
            errors.append('Date of birth cannot be blank.')
        if not(postData['password'] == postData['confirm_pw']):
            errors.append('Please correctly confirm Password.')

        if errors:
            return {'errors' : errors}
        else:
            password = postData['password'].encode('utf-8')
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            print hashed
            print len(hashed)
            valid_user = User.objects.create(name=postData['name'], alias=postData['alias'], email=postData['email'], password=hashed, dob=postData['dob'])
            return {'the_user' : valid_user.id}

    def login(self, postData):
            print '***LOGIN INITIALISED***'
            errors = []
            login_user = User.objects.filter(email = postData['email'])
            if not login_user:
                errors.append('Email not registered.')
            else:
                password_check = postData['password']
                stored_password = login_user[0].password
                if not bcrypt.hashpw(password_check.encode('utf-8'), stored_password.encode('utf-8')) == stored_password:
                    errors.append('Password is incorrect.')
            if errors:
                return {'errors' : errors}
            else:
                return {'the_user' : login_user[0].id}

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    friends = models.ManyToManyField("self")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
