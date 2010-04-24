# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic import list_detail
from django.views.generic import create_update
from djtut.feeds.models import Feed
from djtut import settings

publisher_info = {
    "queryset" : Feed.objects.all(),
}

feed_form = {
  'model' : Feed,
  'post_save_redirect': '/feeds',
  'login_required': True,
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


    #(r'^polls/$', 'index'),
    #(r'^polls/(?P<poll_id>\d+)/$', 'views.detail'),
    #(r'^polls/(?P<poll_id>\d+)/results/$', 'results'),
    #(r'^polls/(?P<poll_id>\d+)/vote/$', 'djtut.polls.views.vote'),
    (r'^admin/', include(admin.site.urls)),
    (r'^avatar/', include('avatar.urls')),
    (r'^pb/$', list_detail.object_list, publisher_info),
    #(r'^feed/create/$', create_update.create_object, feed_form), 
    #(r'^accounts/', include('registration.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    # Uncomment the next line to enable the admin:
)
