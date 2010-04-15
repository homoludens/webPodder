# Create your views here.

# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse

#from djtut.feeds.models import Feed
from django.http import Http404
#from django.shortcuts import render_to_response
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from djtut.feeds.models import Feed, Story, UserProfile

from django.contrib.auth.models import User


from django.forms import ModelForm

from django.http import HttpResponse

from django.views.generic.create_update import create_object
from django.views.generic.create_update import delete_object

from django.core.urlresolvers import reverse

from django.db.models.signals import post_save, pre_save
import feedparser

#p2.article_set.all()
#a1.publications.all()




def index(request):
    #print dir(request.user)
    if request.user.is_anonymous:
      latest_feed_list = Feed.objects.all()[:5]
    elif request.user.is_authenticated:
      user_profile = request.user.get_profile()
      latest_feed_list = user_profile.subscriptions.all()
    #latest_feed_list = Feed.objects.all()
    return render_to_response('feeds/index.html', {'latest_feed_list': latest_feed_list})


def stories(request, feed_id):
    p = get_object_or_404(Feed, pk=feed_id)
    all_stories = Story.objects.filter(feed=feed_id)
    return render_to_response('feeds/stories.html', {'feed': all_stories, 'title': p}, context_instance=RequestContext(request))

#closure: http://en.wikipedia.org/wiki/Closure_%28computer_science%29
def make_feed_form(request):
    class FeedForm(ModelForm):
	class Meta:
	    model=Feed
	    exclude=['title']

	def save(self, commit=True):
	    f = super(FeedForm, self).save(commit=False)

	    tmp_feed = feedparser.parse(f.url)
	    f.title = tmp_feed.feed.title
	    if commit: f.save()
	    
	    if f.pk: 
	      user_profile = request.user.get_profile()
	      user_profile.subscriptions.add(f)
	    
	    create_stories(f,tmp_feed)
	    return f

    return FeedForm

	 
def feed_create(request):
  
    FeedForm = make_feed_form(request)

    return create_object(request,
	form_class = FeedForm,
        #model=Feed,
        template_name='feeds/feed_form.html',
        post_save_redirect="/feeds",
	extra_context={'user':request.user}
    )


def feed_delete(request, feed_id):
    """Delete a note based on id"""
    return delete_object(request,
        model=Feed,
        object_id=feed_id,
        template_name='feeds/delete.html',
        post_delete_redirect="/feeds",
	extra_context={'feed_id':feed_id}
    )


def create_stories(feed_object,tmp_feed):
    for entry in tmp_feed['entries']:
      i = Story(   feed = feed_object,
                   title = entry.get('title'),
                   description = entry.get('summary'),
		   #url = entry.enclosures[0].href,
                   )
      i.save()