from django.conf.urls import patterns, include, url
from django.contrib import admin
from upload import views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'securewitness.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^report/(?P<user>[a-zA-Z0-9-]+)/(?P<report>[a-zA-Z0-9-]+)/?',views.see_report.as_view(), name='report'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('registration.backends.simple.urls')),
                       # url(r'^standalone/', 'securewitness.views.standalone', name='login'),
                       url(r'^standalone/', include('standalone.urls')),
					   url(r'^upload/', include('upload.urls')),
                       url(r'^systemadmin/', include('systemadmin.urls')),

)