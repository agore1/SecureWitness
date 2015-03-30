from django.conf.urls import patterns,url

from upload import views

urlpatterns = patterns('',
	url(r'report',views.report, name='report'),
)