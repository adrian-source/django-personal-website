from django.contrib import admin
from blog.models import *
from tinymce.widgets import TinyMCE
from django.db import models

class PostAdmin(admin.ModelAdmin):
	formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 50}, )},
    }
	fields = ('title', 'author', 'brief', 'body', 'status', 'date_published', 'tags', 'category', 'galleries')
	list_display  = ('title', 'date_created', 'status', 'category')
	list_filter   = ('date_created', 'status')
	search_fields = ('title', 'body')
admin.site.register(Post, PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
	fields = ('name', 'status', 'color', 'order')
	list_display = ['name', 'order']
admin.site.register(Category, CategoryAdmin)