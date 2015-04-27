from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.list import ListView


# Create your views here.

class usersView():
    users = User.objects.all()
    for u in users:
