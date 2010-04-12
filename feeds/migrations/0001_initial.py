# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Feed'
        db.create_table('feeds_feed', (
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('feeds', ['Feed'])

        # Adding model 'Story'
        db.create_table('feeds_story', (
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Feed'])),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('feeds', ['Story'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Feed'
        db.delete_table('feeds_feed')

        # Deleting model 'Story'
        db.delete_table('feeds_story')
    
    
    models = {
        'feeds.feed': {
            'Meta': {'object_name': 'Feed'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'feeds.story': {
            'Meta': {'object_name': 'Story'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feeds.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }
    
    complete_apps = ['feeds']
