# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(blank=False, unique=True)
    #created_by = models.ForeignKey(User, default=0, )
    #created_by = models.ForeignKey(User, editable=False, blank=True, null=True) 
    subscribers = models.ManyToManyField(User)



    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
	super(Feed, self).save(*args, **kwargs) # Call the "real" save() method.



class Story(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)

    def __unicode__(self):
        return self.title




