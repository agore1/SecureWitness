from django.conf.urls import patterns,url

from upload import views

urlpatterns = patterns('',
	url(r'search=(?P<slug>[_\+a-zA-Z0-9-%]+)/$',views.search.as_view(),name='search_results'),
    url(r'search/$',views.search_form,name='search'),
    url(r'report/$',views.report, name='report'),
)