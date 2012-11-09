
from django.shortcuts import render_to_response
from django.http import Http404
from django import template
from django.template import RequestContext
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect



from blog.models import ContactForm
from blog.models import Post
from blog.models import Category
from gallery.models import Picture

def category(request, cat):

	current_category = Category.objects.filter(name=cat)
	if not current_category.exists():
		raise Http404

	posts = Post.objects.filter(category__name=cat, status=2).select_related(depth=1).order_by('-date_published')


	try:
		template.loader.get_template(cat+".html")
		template_file = cat+".html"
	except template.TemplateDoesNotExist:
		template_file = "category.html"

	return render_to_response(template_file, {
		'current_category' : current_category.all()[0],
		'categories' : Category.objects.filter(status=2).order_by('order'),
		'posts': posts,
		'title': cat
		})


def gallerypost(request, id):
	return do_post(request, id, 'full')

def post(request, id):
	return do_post(request, id, 'notfull')

def do_post(request, id, gal):
	try:
		post = Post.objects.get(pk=id)
	except Event.DoesNotExist:
		event = "none"

	return render_to_response("post.html", {
		'categories' : Category.objects.filter(status=2).order_by('order'),
		'current_category' : post.category,
		'post': post,
		'gal': gal,
		'title': post.title
		})

def main(request):

	posts = Post.objects.filter(status=2).order_by('-date_published')

	try:
		template.loader.get_template("home.html")
		template_file = "home.html"
	except template.TemplateDoesNotExist:
		template_file = "category.html"

	return render_to_response(template_file, {
		'categories' : Category.objects.filter(status=2).order_by('order'),
		'posts' : posts,
		'list_categories' : 'true',
		'title' : 'home'
		})

def tag(request, tag):

	posts = Post.objects.filter(status=2, tags=tag).order_by('-date_published')

	return render_to_response("tag.html", {
		'categories' : Category.objects.filter(status=2).order_by('order'),
		'posts' : posts,
		'list_categories' : 'true',
		'title' : 'TAG: '+tag
		})


def contact(request):
	subject = request.POST.get('topic', '')
	name = request.POST.get('name', '')
	message = request.POST.get('message', '')
	from_email = request.POST.get('email', '')

	full_message = "From "+name+"("+from_email+"). The message says: "+message
	msg = ''

	if subject and message and from_email:
			try:
				send_mail(subject, full_message, from_email, ['adrian.sitterle@gmail.com'])
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return HttpResponseRedirect('/contact/thankyou/')
	elif subject:
		print from_email
		if not message:
			msg = 'You should write something in the message box. Otherwise, whats the point?'
		if not from_email:
			msg = 'You have to provide your email address. Otherwise, how can I reply back?'
		
	return render_to_response('contact.html', {
								'categories' : Category.objects.filter(status=2).order_by('order'),
								'form': ContactForm(),
								'msg' : msg,
								'name' : name,
								'email' : from_email,
								'message' : message,
								'title': 'contact me'
								}, RequestContext(request))

def emailsent(request):
			return render_to_response('thankyou.html', {
								'categories' : Category.objects.filter(status=2).order_by('order')
								})


def sitemap(request):
	sitemap = ""

	# root
	sitemap += "http://sitterle.co/\n"

	sitemap += "http://sitterle.co/contact\n"

	# loop through all categories
	for category in Category.objects.filter(status=2):
		sitemap += "http://sitterle.co/"+category.name+"/\n"

	# loop through all posts
	for post in Post.objects.filter(status=2):
		sitemap += "http://sitterle.co"+post.get_permalink()+"\n"
		sitemap += "http://sitterle.co"+post.get_fullpermalink()+"\n"

	return render_to_response('sitemap.txt', {
				'sitemap' : sitemap
		})

def robots(request):
	return render_to_response('robots.txt')
