from django.conf.urls import patterns,url

from upload import views

urlpatterns = patterns('',
	url(r'report',views.report, name='report'),
	url(r'search=(?P<slug>[a-zA-Z0-9-]+)/$',views.search,name='search'),
	
)