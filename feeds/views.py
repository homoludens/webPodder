# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader
from django.http import Http404,  HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.template import RequestContext

from djtut.feeds.models import Feed, Story, UserProfile
from django.contrib.auth.models import User


from django.forms import ModelForm

from django.views.generic.create_update import create_object, delete_object

from django.core.urlresolvers import reverse

from django.db.models.signals import post_save, pre_save
import feedparser
from django.template.loader import render_to_string
from django import forms


def index(request):
    if request.user.is_authenticated():
      user_profile = request.user.get_profile()
      latest_feed_list = user_profile.subscriptions.all()
    else:
      latest_feed_list = Feed.objects.all()[:5]

    return render_to_response('feeds/index.html', {'latest_feed_list': latest_feed_list,'user':request.user })


def stories(request, feed_id):
    p = get_object_or_404(Feed, pk=feed_id)
    all_stories = Story.objects.filter(feed=feed_id)
    #return render_to_response('feeds/stories.html', {'feed': all_stories, 'title': p}, context_instance=RequestContext(request))
    
    context = RequestContext(request)
    context['dynamic_div'] = 'result'
    context['ref_url'] = '/feeds/'+feed_id+'/'
    context['feed'] = all_stories
    context['title'] = p

    return HttpResponse(render_to_string('feeds/stories.html', context),mimetype='text/plain')

#closure: http://en.wikipedia.org/wiki/Closure_%28computer_science%29
def make_feed_form(request):
    class FeedForm(ModelForm):
	class Meta:
	    model=Feed
	    exclude=['title']
	    
	def clean_url(self):
	    try:
	      f = Feed.objects.get(url=self.cleaned_data['url'])
	    except Feed.DoesNotExist:
	      return self.cleaned_data['url']
	      
	    if f.pk:
	      user_profile = request.user.get_profile()
	      try:
		a = user_profile.subscriptions.get(pk=f.pk)
		raise forms.ValidationError('You are already subscribed to %s' % f.title)
		print "try"
	      except Feed.DoesNotExist:
		user_profile.subscriptions.add(f)
		raise forms.ValidationError('Podcast %s is added to your profile' % f.title) 
		print "except"      
	    
	    if not (self.cleaned_data.get('url')):
		raise forms.ValidationError('You must enter valid URL')
	      
	    return self.cleaned_data['url']


	def save(self, commit=True):
	    print "save"
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
    """Create new feed"""
    FeedForm = make_feed_form(request)
  
    return create_object(request,
	form_class = FeedForm,
        #model=Feed,
        template_name='feeds/feed_form.html',
        post_save_redirect="/feeds",
	extra_context={'user':request.user}
    )


def feed_delete(request, feed_id):
    """Delete feed"""
    return delete_object(request,
        model=Feed,
        object_id=feed_id,
        template_name='feeds/delete.html',
        post_delete_redirect="/feeds",
	extra_context={'feed_id':feed_id}
    )


def feed_unsubscribe_confirm(request, feed_id):
    """Confirm unsubscribe from feed"""    
    return render_to_response('feeds/unsubscribe.html', {'feed_id': feed_id,'user':request.user })

def feed_unsubscribe(request, feed_id):
    """Unsubscribe from feed"""
    f = Feed.objects.get(pk=feed_id)
    user_profile = request.user.get_profile()
    user_profile.subscriptions.remove(f)
    
    next_url = request.GET.get('next', '/feeds')
    return HttpResponseRedirect(next_url)

def create_stories(feed_object,tmp_feed):
    """Create stories for new feed"""
    for entry in tmp_feed['entries']:
      i = Story(   feed = feed_object,
                   title = entry.get('title'),
                   description = entry.get('summary'),
		   #description = entry['content'][0]['value']                   
		   #url = entry.enclosures[0].href,
                   )
      try:
	i.save()
      except:
	raise forms.ValidationError('Feed with problems')
      
      
      
from django import template
register = template.Library()

@register.filter
def truncate(value, arg):
    """
    Truncates a string after a given number of chars  
    Argument: Number of chars to truncate after
    """
    try:
        length = int(arg)
    except ValueError: # invalid literal for int()
        return value # Fail silently.
    if not isinstance(value, basestring):
        value = str(value)
    if (len(value) > length):
        return value[:length] + "..."
    else:
        return value