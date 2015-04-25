from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'reports/(?P<username>[a-zA-Z0-9-]+)/$', views.reports, name='reports'),
    url(r'^$', views.login, name='login'),
    # url(r'^download/')
]
