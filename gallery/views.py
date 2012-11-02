from django.http import HttpResponse
from django.conf import settings

import Image, ImageOps, os

from gallery.models import Picture
from gallery.models import Gallery


def sync_db_and_folders(request):
	path = settings.MEDIA_ROOT+"/gallery/"
	for folder in os.listdir(path):
		if os.path.isdir(os.path.join(path, folder)):
			gallery, created = Gallery.objects.get_or_create(title=folder)
			for image in os.listdir(os.path.join(path, folder)):
				if not image[0] == ".":
					image, created = Picture.objects.get_or_create(title=os.path.splitext(image)[0].replace('-',' '), url_org="gallery/"+folder+"/"+image, gallery=gallery)


def resize_photos(request):
	sync_db_and_folders(request)

	columnwidth = 130

	pictures = Picture.objects.all()

	for picture in pictures:
		pic = Image.open(picture.url_org)

		result = resize_image(os.path.basename(picture.url_org.url), '_resize', 600, 400, pic, 'gallery/')
		if not result == None:
			picture.url_resize = result

		result = resize_image(os.path.basename(picture.url_org.url), '_'+str(picture.thumbnail_size)+'_thumb', columnwidth*picture.thumbnail_size+(5*(picture.thumbnail_size-1)), 600, pic, 'gallery/')
		if not result == None:
			picture.url_thumbnail = result

		picture.save()

	return HttpResponse("done.")

def resize_image(image_name, suffix, width, height, image, location):

	image_resized_name = os.path.splitext(image_name)[0]+suffix+os.path.splitext(image_name)[1]

	if not os.path.exists(settings.MEDIA_ROOT+"/"+location+image_resized_name):
		if image.mode not in ("L", "RGB"):
		    image = image.convert("RGB")

		image.thumbnail((width,height), Image.ANTIALIAS)
		image_resized = image
		image_resized.save(settings.MEDIA_ROOT+"/"+location+image_resized_name, 'JPEG', quality=100)
		image.seek(0)

		return location+image_resized_name

	image.seek(0)

	return None
