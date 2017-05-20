# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.

def index(request):
    return render(request, 'FriendsApp/index.html')

def register(request):
    new_user = User.objects.register(request.POST)
    if 'the_user' in new_user:
        request.session['logged_user'] = new_user['the_user']
        messages.success(request, 'You successfully registered!')
        return redirect('/friends')
    else:
        for i in new_user['errors']:
            messages.error(request, i)
        return redirect('/')

def login(request):
    if request.method == 'POST':
        login_check = User.objects.login(request.POST)
        if 'the_user' in login_check:
            request.session['logged_user'] = login_check['the_user']
            messages.success(request, 'You successfully logged in!')
            return redirect('/friends')
        else:
            for i in login_check['errors']:
                messages.error(request, i)
            return redirect('/')

def friends(request):
    user = User.objects.get(id=request.session['logged_user'])
    print user.alias
    friends = []
    not_friends = []
    all_other_users = User.objects.exclude(id=request.session['logged_user'])
    for other_user in all_other_users:
        if other_user in user.friends.all():
            friends.append(other_user)
        elif other_user not in user.friends.all():
            not_friends.append(other_user)
    context = {
        'logged_in_user' : user,
        'friends' : friends,
        'not_friends' : not_friends
    }
    return render(request, 'FriendsApp/friends.html', context)

def logout(request):
    request.session['logged_user'] = {}
    return redirect('/')

def user(request, id):
    user = User.objects.get(id=id)
    context = {
    'user' : user
    }
    return render(request, 'FriendsApp/user.html', context)

def add(request, id):
    user = User.objects.get(id=request.session['logged_user'])
    new_friend = User.objects.get(id=id)
    user.friends.add(new_friend)
    return redirect('/friends')

def remove(request, id):
    user = User.objects.get(id=request.session['logged_user'])
    unfriend = User.objects.get(id=id)
    user.friends.remove(unfriend)
    return redirect('/friends')
