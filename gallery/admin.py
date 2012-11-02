from django.contrib import admin
from gallery.models import *

class GalleryAdmin(admin.ModelAdmin):
	fields = ('title', 'description')
	search_fields = ('title', 'description')
admin.site.register(Gallery, GalleryAdmin)

class PictureAdmin(admin.ModelAdmin):
	fields = ('title', 'description', 'thumbnail_size', 'url_org', 'gallery')
	list_display = ('title', 'gallery')
admin.site.register(Picture, PictureAdmin)