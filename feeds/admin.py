# -*- coding: utf-8 -*-
from djtut.feeds.models import Feed
from django.contrib import admin
from djtut.feeds.models import Story

#class ChoiceInline(admin.TabularInline):
    #model = Choice
    #extra = 3

class FeedAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Add new feed',               {'fields': ['url']}),
    ]
    list_display = ('title', 'url')
    search_fields = ['title']

    def save_model(self, request, obj, form, change):
	print "save_model_admin"
        obj.created_by = request.user
        obj.save()

admin.site.register(Feed, FeedAdmin)

#admin.site.register(Feed)



