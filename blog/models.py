from django.db import models
from django.contrib import admin
from django import forms
from django.forms.widgets import *
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User

from tinymce import models as tinymce_models

import tagging
from tagging.fields import TagField
from tagging.models import Tag

from gallery.models import Gallery

class Category(models.Model):
	'''
	Database for categories
	'''
	STATUS_CHOICES = (
		(1, 'Draft'),
		(2, 'Public'),
	)
	name = models.CharField(max_length=50, blank="False")
	meta = models.CharField(max_length=200, blank="False")
	status = models.IntegerField(choices=STATUS_CHOICES, default=2)
	color = models.CharField(max_length=6)
	order = models.IntegerField(unique='true')

	def __unicode__(self):
		return u'%s' % (self.name)

	def get_permalink(self):
		return "/"+self.name+"/"


class Post(models.Model):
	'''
	Database for posts
	'''

	STATUS_CHOICES = (
		(1, 'Draft'),
		(2, 'Public'),
	)
	title = models.CharField(max_length=200, blank="True")
	author = models.ForeignKey(User, blank=True, null=True)
	brief = tinymce_models.HTMLField()
	body = tinymce_models.HTMLField()
	status = models.IntegerField(choices=STATUS_CHOICES, default=2)
	date_created = models.DateTimeField(auto_now_add=True)
	date_published = models.DateTimeField(auto_now_add=False)
	tags = TagField()
	category = models.ForeignKey(Category)
	galleries = models.ManyToManyField(Gallery, blank=True)

	def __unicode__(self):
		return u'%s ' % (self.title)

	def get_tags(self):
		return Tag.objects.get_for_object(self)

	def get_permalink(self):
		return "/post/"+str(self.pk)+"/"+self.title.replace(" ","-").replace(".","").replace("'","").replace(",","")

	def get_fullpermalink(self):
		return "/post/gallery/"+str(self.pk)+"/"+self.title.replace(" ","-").replace(".","").replace("'","").replace(",","")



class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    topic = forms.CharField()
    message = forms.CharField(widget=Textarea())


