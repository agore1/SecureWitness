from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic.base import TemplateView
from SecureWitness.securewitness.systemadmin import views
from SecureWitness.securewitness.systemadmin.views import UserView

urlpatterns = patterns('',
                       url(r'^userlist/$',
                           UserView.as_view(),
                           name='userlist'),
                       )