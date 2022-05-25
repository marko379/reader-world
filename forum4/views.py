from django.shortcuts import render,redirect, HttpResponseRedirect
from books.models import Book, Genres,Comments,Rating_star_system,Users_stars
from django.db.models import Count
from django.contrib import messages


def homePageView(request):
	# request.session['form_message'] = "form_message" and request.session['username'] = form.instance.username are  made in user app in register.views
	# remember this is how u create session request.session['form_message'] = "form_message"
	# you created simply string form_message and request.session['form_message'] is simply how u create new session
	# because you creted it (form_message)  in register.views thats is in user app , seesion is created and saved over there, then after user is singed in succsefully page reload and user is sent to front page over here, becuse you saved session (form_message)  before you reloaded the page to here u are able to accsess it over here 
	username = None
	# if( 'form_message' in request.session):
	# 	username = request.session['username']
	# 	messages.success(request, 'Wellcome {}! Before you CAN login you need to confirm your email address! please go to your email and conirm your addres'.format(username))
	# 	request.session.clear()
	if ( 'session' in request.session):
		username = request.session['username']
		messages.success(request, 'Wellcome {}! Your are logged in!'.format(username))
	if ( 'update_profile_session' in request.session):
		messages.success(request, 'Your profile is updated successfully!')
	gen = Genres.objects.all()
	# get all books by likes, book with most likes is first ...
	book = Book.objects.annotate(num_authors=Count('likes')).order_by('-num_authors')
	return render(request,'homePage.html',{'gen':gen,'book':book,})
