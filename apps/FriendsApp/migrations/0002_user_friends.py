# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-20 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FriendsApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(related_name='_user_friends_+', to='FriendsApp.User'),
        ),
    ]
