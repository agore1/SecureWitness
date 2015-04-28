from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.list import ListView

from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.utils import timezone

from itertools import chain

from django.contrib.auth.models import User

from registration.models import in_group, Group
from systemadmin.models import UserProfile


# Create your views here.

class UserView(ListView):
    template_name = "userlist.html"

    model = User
    # folder = Folder;

    slug = None;

    def get_object(self, queryset=None):
        return queryset.get(slug=self.slug)

    def get_queryset(self):
        object_list = self.model.objects
        return object_list

    def get_context_data(self, **kwargs):
        con = super(UserView, self).get_context_data(**kwargs);
        con['user_name'] = self.kwargs.get('slug', None);
        if self.request.method == "POST":
            con["user_name"] = "delete";
        con['editable'] = False;
        if (con["user_name"] == self.request.user.username):
            con['editable'] = True;
        return con

    def post(self, request, *args, **kwargs):
        check_list = request.POST.getlist('checks[]')
        if(request.POST["action_taken"] == "add_group"):
            group_name = request.POST.get('color')
            #new_group, created = Group.objects.get_or_create(name=group_name)
            new_group = Group(name=group_name)
            new_group.save()
            for i in check_list:
                current = User.objects.get(username=i)
                group_entry = in_group()
                group_entry.user = current
                group_entry.group = new_group
                group_entry.save()
        elif(request.POST["action_taken"] == "make_admin"):
            for i in check_list:
                current = User.objects.get(username=i)
                s = current.profile
                s.is_admin = not s.is_admin
                s.save()
        elif(request.POST["action_taken"] == "suspend_user"):
            for i in check_list:
                current = User.objects.get(username=i)
                s = current.profile
                s.is_suspended = not s.is_suspended
                s.save()
        return redirect("/systemadmin/userlist/");
        #return HttpResponse(request.POST.items());