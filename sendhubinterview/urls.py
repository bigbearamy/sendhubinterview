from django.conf.urls import patterns, include, url
from webservices.urls import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^',  include('webservices.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),

    # url(r'^$', 'sendhubinterview.views.home', name='home'),
    # url(r'^sendhubinterview/', include('sendhubinterview.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
