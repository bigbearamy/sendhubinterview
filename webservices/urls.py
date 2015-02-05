from django.conf.urls import patterns, url

from webservices import views

urlpatterns = patterns('',
    #psat User Interface URL patterns, NOT part of PFPi psat API
    url(r'^$', views.index, name='home_user'),
    url(r'^webservices/submit$', views.submitjob_user, name='submitjob_user')
)