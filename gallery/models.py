from django.db import models
from tinymce import models as tinymce_models


class Gallery(models.Model):

	title = models.CharField(max_length=200, blank="true")
	description = tinymce_models.HTMLField()

	def __unicode__(self):
		return u'%s' % (self.title)

class Picture(models.Model):

	ONE = 1
	TWO = 2
	THREE = 3
	WIDTH_CHOICES = (
		(ONE, 'one column wide'),
		(TWO, 'two columns wide'),
		(THREE, 'three columns wide'),
	)
	title = models.CharField(max_length=200, blank="true")
	description = models.TextField(blank="true")

	thumbnail_size = models.IntegerField(choices=WIDTH_CHOICES, default=ONE)

	url_org = models.ImageField(upload_to="gallery/", max_length="200", blank="True")
	url_resize = models.ImageField(upload_to="gallery/", max_length="200", blank="True")
	url_thumbnail = models.ImageField(upload_to="gallery/", max_length="200", blank="True")
	url_wide = models.ImageField(upload_to="gallery/", max_length="200", blank="True")

	gallery = models.ForeignKey(Gallery, blank=True)

	def __unicode__(self):
		return u'%s' % (self.title)

	

	