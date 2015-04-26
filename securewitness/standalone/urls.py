from django.conf.urls import url

from . import views
from standalone.views import download_report_file
urlpatterns = [
    url(r'reports/(?P<username>[a-zA-Z0-9-]+)/$', views.reports, name='reports'),
    url(r'viewreport/(?P<username>[a-zA-Z0-9-]+)/(?P<report_id>[0-9]+)/?$', views.detailed_report, name='detailed_report'),
    url(r'download/(?P<username>[a-zA-Z0-9-]+)/(?P<report_id>[0-9]+)/(?P<fileN>[0-9]+)/?$', download_report_file, name='download_report_file'),
    url(r'^$', views.login, name='login'),
    # url(r'^download/')
]
