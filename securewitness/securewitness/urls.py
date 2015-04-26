from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'securewitness.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('registration.backends.simple.urls')),
                       # url(r'^standalone/', 'securewitness.views.standalone', name='login'),
                       url(r'^standalone/', include('standalone.urls')),
					   url(r'^upload/', include('upload.urls')),

)
