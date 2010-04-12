# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('djtut.feeds.views',
    # Example:
    # (r'^djtut/', include('djtut.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),


    (r'^$', 'index'),
    #(r'^(?P<feed_id>\d+)/$', 'detail'),
    #(r'^(?P<feed_id>\d+)/feeds/$', 'feeds'),
    (r'^(?P<feed_id>\d+)/$', 'stories'),
    #(r'^admin/', include(admin.site.urls)),
    #(r'^hello/$', 'hello'),
    #(r'^contact/$', 'contact'), 
    #(r'^new/$', 'feed_create'),  
    url(r'^new/$', 'feed_create', name='feed_form'),  
    url(r'^delete/(?P<feed_id>\d+)/$', 'feed_delete', name='feed_delete'),

    # Uncomment the next line to enable the admin:

)
