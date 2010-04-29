# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic import list_detail
from django.views.generic import create_update
from djtut.feeds.models import Feed, User
from djtut import settings


feed_form = {
  'model' : Feed,
  'post_save_redirect': '/feeds',
  'login_required': True,
}

feed_list_info = {
    'queryset' :   Feed.objects.all(),
    'allow_empty': True,
}

user_list_info = {
    'queryset' :   User.objects.all(),
    'allow_empty': True,
}

urlpatterns = patterns('',
    (r'^polls/', include('djtut.polls.urls')),
    (r'^feeds/', include('djtut.feeds.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    # Example:
    # (r'^djtut/', include('djtut.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^$', 'django.views.generic.list_detail.object_list', feed_list_info),
    #(r'^users/$', 'django.views.generic.list_detail.object_list', user_list_info),	
    (r'^users/$', 'djtut.feeds.views.user_list'),	
    (r'^users/(?P<user_id>\d+)/$', 'djtut.feeds.views.user_subscribtions'),
    #(r'^polls/$', 'index'),
    #(r'^polls/(?P<poll_id>\d+)/$', 'views.detail'),
    #(r'^polls/(?P<poll_id>\d+)/results/$', 'results'),
    #(r'^polls/(?P<poll_id>\d+)/vote/$', 'djtut.polls.views.vote'),
    (r'^admin/', include(admin.site.urls)),
    (r'^avatar/', include('avatar.urls')),
    #(r'^feed/create/$', create_update.create_object, feed_form), 
    #(r'^accounts/', include('registration.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    # Uncomment the next line to enable the admin:
)
