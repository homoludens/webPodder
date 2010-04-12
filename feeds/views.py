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
from djtut.feeds.models import Feed, Story

from django.contrib.auth.models import User


from django.forms import ModelForm



from django.db.models.signals import post_save, pre_save
import feedparser


def index(request):
    latest_feed_list = Feed.objects.all()
    return render_to_response('feeds/index.html', {'latest_feed_list': latest_feed_list})


def stories(request, feed_id):
    p = get_object_or_404(Feed, pk=feed_id)
    #all_stories = Story.objects.get(feed=feed_id)
    all_stories = Story.objects.filter(feed=feed_id)
    return render_to_response('feeds/stories.html', {'feed': all_stories, 'title': p})


from django.http import HttpResponse

def hello(request):
    #return HttpResponse("Hello world")
    #return HttpResponse("Welcome to the page at %s" % request.path)
    #ua = request.META.get('HTTP_USER_AGENT', 'unknown')
    #return HttpResponse("Your browser is %s" % ua)
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))


from django.core.mail import send_mail
#from django.http import HttpResponseRedirect
#from django.shortcuts import render_to_response

def contact(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    return render_to_response('contact_form.html', {
        'errors': errors,
        'subject': request.POST.get('subject', ''),
        'message': request.POST.get('message', ''),
        'email': request.POST.get('email', ''),
    })



from django.views.generic.create_update import create_object
from django.views.generic.create_update import delete_object

from django.core.urlresolvers import reverse


#closure: http://en.wikipedia.org/wiki/Closure_%28computer_science%29
def make_feed_form(request):
    class FeedForm2(ModelForm):
	class Meta:
	    model=Feed
	    exclude=['title', 'created_by']

	def save(self, commit=True):
	    f = super(FeedForm2, self).save(commit=False)
	    tmp_feed = feedparser.parse(f.url)
	    f.title = tmp_feed.feed.title
	    if not f.pk: f.created_by = request.user
	    if commit: f.save()
	    create_stories(f,tmp_feed)
	    return f

    return FeedForm2



class FeedForm(ModelForm):
    class Meta:
	 model=Feed
	 #fields = ['url','title']
	 #exclude=['title']
	 exclude=['title', 'created_by']
	 
def feed_create(request):
  
    FeedForm2 = make_feed_form(request)

    return create_object(request,
	form_class = FeedForm2,
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
    )


def create_stories(feed_object,tmp_feed):
    for entry in tmp_feed['entries']:
      i = Story(   feed = feed_object,
                   title = entry.get('title'),
                   description = entry.get('summary'),
		   #url = entry.enclosures[0].href,
                   )
      i.save()