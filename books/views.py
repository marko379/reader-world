from django.shortcuts import render,redirect, HttpResponseRedirect
from django.urls import reverse
from .models import Book, Genres,Comments,Rating_star_system,Users_stars
from .forms import Rating_form,Comment_form , Comment_form_disabled
from django.db.models import Count
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator


def vezba(request):
	book_id = 11
	books = Book.objects.get(id=book_id)
	return render(request,'books/vjezba.html',{'books':books})


def vezba_2(request):

	value = request.GET.get('xxx')
	if value:
		books = Book.objects.get(id=value).info
		update_form = Comment_form(initial={'comment': books})
	else:
		books = None
		update_form = None


	return render(request,'books/vjezba_2.html',{'update_form':update_form,'books':books})


def front(request):
	# request.session['form_message'] = "form_message" and request.session['username'] = form.instance.username are  made in user app in register.views
	# remember this is how u create session request.session['form_message'] = "form_message"
	# you created simply string form_message and request.session['form_message'] is simply how u create new session
	# because you creted it (form_message)  in register.views thats is in user app , seesion is created and saved over there, then after user is singed in succsefully page reload and user is sent to front page over here, becuse you saved session (form_message)  before you reloaded the page to here u are able to accsess it over here 
	username = None
	if( 'form_message' in request.session):
		username = request.session['username']
		messages.success(request, 'Wellcome {}! Before you CAN login you need to confirm your email address! please go to your email and conirm your addres'.format(username))
		request.session.clear()
	if ( 'session' in request.session):
		username = request.session['username']
		messages.success(request, 'Wellcome {}! Your are logged in!'.format(username))
	gen = Genres.objects.all()
	# get all books by likes, book with most likes is first ...
	book = Book.objects.annotate(num_authors=Count('likes')).order_by('-num_authors')
	return render(request,'books/front_page.html',{'gen':gen,'book':book,})


def return_books_by_ganres(request):
	# valeu = ['History','Adventure','cartoon'...]  source : book_page.html
	value = request.POST.getlist('value') # get list of all genres that client choos
	# based on values that client choose,,,book = Book.objects.filter(genres__genre__in=value)
	# we can filter multiple valeus with __in
	book = Book.objects.filter(genres__genre__in=value) # ['History','Adventure']
	return render(request,'books/books_by_genres.html',{'book':book})


def get_one_genre_books(request,gen):
	book = Book.objects.filter(genres__genre=gen)
	return render(request,'books/book_by_one_genre.html',{'book':book,'gen':gen})




def book(request,slug,page_num_update_comment=1):
	# print(page_num,'ddddddddddddddddddddddddddddddddd')
	# session you have explained in function above front
	if ( 'session' in request.session):
		username = request.session['username']
		messages.success(request, 'Wellcome {}! Your are logged in!'.format(username))

	# from front_page.html is sent and directed a slug over here 
	book = Book.objects.get(slug=slug)

	# every book as soon as is created has a model Rating_star_system hooked up to it thats is also new
	# star is onetoone field and requires a book
	# with this function we can get a lots of things , total people that rated book, total people per star, avarge rating number ...
	# models.Rating_star_system , star.html
	rating_star_system = Rating_star_system.objects.get(star=book.id)

	# return all genres of the book like, with values_list you return them as <QuerySet [(1,), (2,)]> of tuples and  values but with flat=true u return them as <QuerySet [1, 2]> only values 
	# default way is just book.genres.values that returns <QuerySet [{'value1': 1}, {'value2': 2}]>
	# so return all genres of the book as a single values in a list so we can filter aganist those values  
	list_book_genres = book.genres.values_list('genre', flat=True) 

	# return all books from model that have same genres or some of them with book on page 
	# we are doing this so we can offer user books with same genres in carousel on same page of book he is currentlly lookin at ,is just for user experiance , so user will have offered few books with same genres so user can chek them out,
	# book_page.html carousel
	return_books_by_ganres = Book.objects.filter(genres__genre__in=list_book_genres).annotate(num_authors=Count('likes')).order_by('-num_authors')

	# return all commnets of the book based on likes, comment with most likes will be on the top
	comment = Comments.objects.filter(book=book).annotate(num_authors=Count('comment_likes')).order_by('-num_authors')

	# get page number, if not page_num then get default value page_num_update_comment = 1 
	# if page num skip all of this and go to page = comments.page(page_num)
	# why this page_num_update_comment ? we made this if user updates his comment to be redirected to his comment so he can see it imediatly , it works when user press update, with update it will be automaticlly send the number of the page where comment was , and then redirected to return HttpResponseRedirect(reverse('books:book-comment', args=(book.slug,page_num,))) 
	page_num = request.GET.get('page_num')
	if page_num == None:
		page_num = page_num_update_comment

	# take all comments and split them 5 per page, so if 25 comments they will be split on 5 pages 5 comments
	comments = Paginator(comment, 5, orphans=4)
	# get page 1 
	page = comments.page(page_num)





	# get all Users_stars objects based on book
	# we want to show on our comments , user of each comment, and how many stars user has given to book
	# show_stars_on_comment.html
	user_stars_per_book_on_coment = Users_stars.objects.filter(book=book)

	# this we use to show if user rated book , and if not rated the book
	# check it rate_it_stars.html and models User_stars
	try:
		user_star_book = Users_stars.objects.get(Q(book=book) & Q(user_id=request.user.id))
	except ObjectDoesNotExist:
		user_star_book = None


	# use of this is to show user the books he recently viewd and offer them so he could click on them any time 
	# first will be executed else , there we make/save new session called viewed_recently and we add to it id of the book we are currently looking at as a list, so we have now viewed_recently saved in sessions
	# if we go and see other book, then will be executed if statment cox request.session now exists
	# every time user see new book if statment will be executed and operations remove ,insert,pop 
	# recently_viewed_books = Book.objects.filter(id__in=request.session['viewed_recently']) show books in html
	# check book_page.html
	viewed_recently = None
	if 'viewed_recently' in request.session:
		if book.id in request.session['viewed_recently']:
			request.session['viewed_recently'].remove(book.id)
		request.session['viewed_recently'].insert(0, book.id)
		if len(request.session['viewed_recently']) > 3:
			request.session['viewed_recently'].pop()
	else:
		# this will return list called viewed_recently
		request.session['viewed_recently'] = [book.id]
	request.session.modified = True
	recently_viewed_books = Book.objects.filter(id__in=request.session['viewed_recently'])


	# TO GET COMMENT USER WANTS TO UPDATE IT  /////////////  comm_idx   ////////////////
	# update code is in edit.html
	# when u press update button then comm_idx(comment.id) is sent here 
	# next step is cheking for comm_idx : if comm_idx
	# if we get  comm_idx then based on that comment.id and among other things we will get that comment   Comments.objects.get(Q(book=book) & Q(id=comm_idx)).comment  (comment content)
	# then we will use form so we can present to user a form and comment content inside of the form:     update_form = Comment_form(initial={'comment': comm,'comm_id':comm2}
	#Comments.objects.get(Q(book=book) & Q(id=comm_idx)).id this peace of a code is just to to identify our update form in book_page.html {% if comment.user == request.user and update_form.initial.comm_id == comment.id %}
	update_form = None
	comm_idx = request.GET.get('comm_idx')
	if comm_idx:
		# content of the comment
		comm = Comments.objects.get(Q(book=book) & Q(id=comm_idx)).comment
		comm2 = Comments.objects.get(Q(book=book) & Q(id=comm_idx)).id
		form = Comment_form()
		update_form = Comment_form(initial={'comment': comm,'comm_id':comm2})

	# TO UPDATE COMMENT ,check book_page.html
	# comm_id is sent here and update form is sent here that contains content of the comment
	# comm.comment = request.POST['comment']      uploading content of the comment
	if request.method =='POST':
		comm_id = request.POST.get('comm_id')
		if comm_id:
			comm = Comments.objects.get(Q(book=book) & Q(id=comm_id) & Q(user=request.user))
			comm.comment = request.POST['comment']
			comm.save()
			messages.success(request, 'Your comment was updated successfully')
			# return HttpResponseRedirect(reverse('books:book', args=(book.slug,)))
			return HttpResponseRedirect(reverse('books:book-comment', args=(book.slug,page_num,)))




		# comments publishing
		form = Comment_form(request.POST)
		if form.is_valid():
			form_save = form.save(commit=False)
			form_save.user = request.user
			form_save.book = book
			form.save()
			return HttpResponseRedirect(reverse('books:book', args=(book.slug,)))

	else:
		form = Comment_form()
		form_2 = Comment_form_disabled()
	return render(request,'books/book_page.html',{
		'book':book,
		'form':form,
		'return_books_by_ganres':return_books_by_ganres,
		'rating_star_system':rating_star_system,
		'user_star_book':user_star_book,
		'user_stars_per_book_on_coment':user_stars_per_book_on_coment,
		'recently_viewed_books':recently_viewed_books,
		'page':page,
		'comments':comments,
		'comment':comment,
		'update_form':update_form,
		'form_2': form_2
		})




# so basiclly if u press like button then like string is send over here , then it check if like button is pressed and if user exists in book.likes (manytomanyfield filled up with all users ), then just follow the code 
def book_like_dislike_system(request):
	dislike = request.POST.get('dislike')
	like = request.POST.get('like')
	user = request.POST.get('user')
	slug = request.POST.get('slug')
	book = Book.objects.get(slug=slug)

	if like and  book.likes.filter(id=user).exists():
		book.likes.remove(request.user)
	elif like and not book.likes.filter(id=user).exists():
		book.likes.add(user)
		if book.dislikes.filter(id=user).exists():
			book.dislikes.remove(request.user)
	elif dislike and book.dislikes.filter(id=user).exists():
		book.dislikes.remove(request.user)
	elif dislike and not book.dislikes.filter(id=user).exists():
		book.dislikes.add(user)
		if book.likes.filter(id=user).exists():
			book.likes.remove(request.user)
	return HttpResponseRedirect(reverse('books:book', args=(book.slug,)))


# same system as above
def comment_like_dislike_system(request):
	dislike = request.POST.get('dislike')
	like = request.POST.get('like')
	user = request.POST.get('user')
	slug = request.POST.get('slug')
	comment_id = request.POST.get('comment_id')
	comment = Comments.objects.get(id=comment_id)

	if like and  comment.comment_likes.filter(id=user).exists():
		comment.comment_likes.remove(request.user)
	elif like and not comment.comment_likes.filter(id=user).exists():
		comment.comment_likes.add(user)
		if comment.comment_dislikes.filter(id=user).exists():
			comment.comment_dislikes.remove(request.user)
	elif dislike and comment.comment_dislikes.filter(id=user).exists():
		comment.comment_dislikes.remove(request.user)
	elif dislike and not comment.comment_dislikes.filter(id=user).exists():
		comment.comment_dislikes.add(user)
		if comment.comment_likes.filter(id=user).exists():
			comment.comment_likes.remove(request.user)
	return HttpResponseRedirect(reverse('books:book', args=(slug,)))


# here you are reciving values from rate_it_stars.html (book_id and num that represents value)#
def rating_star_system(request,book_id):
	stars = request.POST.get('num')
	stars = int(stars)
	book = Book.objects.get(id=book_id)
	star_sytem = Rating_star_system.objects.get(star=book_id)

	# if user pressed star 1, then function checks, if star is 1 and user do not exists in property star_1, then add user to property star_1, but user might had rated it before lets say with 4 star, so after adding user to property star_1 search all other properties to see if user rated it previouslly , if he did that will be removed
	# then signals will be fired 
	if stars == 1 and not star_sytem.star_1.filter(id=request.user.id).exists():
		star_sytem.star_1.add(request.user)
		if star_sytem.star_2.filter(id=request.user.id).exists():
			star_sytem.star_2.remove(request.user)
		elif star_sytem.star_3.filter(id=request.user.id).exists():
			star_sytem.star_3.remove(request.user)
		elif star_sytem.star_4.filter(id=request.user.id).exists():
			star_sytem.star_4.remove(request.user)
		elif star_sytem.star_5.filter(id=request.user.id).exists():
			star_sytem.star_5.remove(request.user)

	elif stars == 2 and not star_sytem.star_2.filter(id=request.user.id).exists():
		star_sytem.star_2.add(request.user)
		if star_sytem.star_1.filter(id=request.user.id).exists():
			star_sytem.star_1.remove(request.user)
		elif star_sytem.star_3.filter(id=request.user.id).exists():
			star_sytem.star_3.remove(request.user)
		elif star_sytem.star_4.filter(id=request.user.id).exists():
			star_sytem.star_4.remove(request.user)
		elif star_sytem.star_5.filter(id=request.user.id).exists():
			star_sytem.star_5.remove(request.user)

	elif stars == 3 and not star_sytem.star_3.filter(id=request.user.id).exists():
		star_sytem.star_3.add(request.user)
		if star_sytem.star_1.filter(id=request.user.id).exists():
			star_sytem.star_1.remove(request.user)
		elif star_sytem.star_2.filter(id=request.user.id).exists():
			star_sytem.star_2.remove(request.user)
		elif star_sytem.star_4.filter(id=request.user.id).exists():
			star_sytem.star_4.remove(request.user)
		elif star_sytem.star_5.filter(id=request.user.id).exists():
			star_sytem.star_5.remove(request.user)


	elif stars == 4 and not star_sytem.star_4.filter(id=request.user.id).exists():
		star_sytem.star_4.add(request.user)
		if star_sytem.star_1.filter(id=request.user.id).exists():
			star_sytem.star_1.remove(request.user)
		elif star_sytem.star_2.filter(id=request.user.id).exists():
			star_sytem.star_2.remove(request.user)
		elif star_sytem.star_3.filter(id=request.user.id).exists():
			star_sytem.star_3.remove(request.user)
		elif star_sytem.star_5.filter(id=request.user.id).exists():
			star_sytem.star_5.remove(request.user)

	elif stars == 5 and not star_sytem.star_5.filter(id=request.user.id).exists():
		star_sytem.star_5.add(request.user)
		if star_sytem.star_1.filter(id=request.user.id).exists():
			star_sytem.star_1.remove(request.user)
		elif star_sytem.star_2.filter(id=request.user.id).exists():
			star_sytem.star_2.remove(request.user)
		elif star_sytem.star_3.filter(id=request.user.id).exists():
			star_sytem.star_3.remove(request.user)
		elif star_sytem.star_4.filter(id=request.user.id).exists():
			star_sytem.star_4.remove(request.user)
	messages.success(request, 'You rated this book with {} stars'.format(stars))
	return HttpResponseRedirect(reverse('books:book', args=(book.slug,)))



# if u put 3 words in a search, the words will be recived here as value, then we will split word into list 
# ['word-1','word-2','word-3']
# how it works? you have 8 spaces for words to search them, but if u put 2 words only in search,  program will add those 2 words for 8 times to fill up 8 spaces (Q(title__icontains=value[0])), so the logic is program will still find what user is looking for coz 2 words or 2 words repeted 8 times are still the same for program 
# 2 words ['diet' , 'keto' ] or 8 words ['diet' , 'keto', 'diet' , 'keto','diet' , 'keto','diet' , 'keto'] is the same for search
# if user put more then 8 words in search, program will look for first 8 words and ignore rest
# 

def search_book(request):
	value = request.POST.get('value')
	value = value.split()  # ['aa', 'bb', 'cc']
	num = 0
	while len(value) <= 8:
		add_value = value[num]
		value.append(add_value)
		num = num + 1 


	queryset = Book.objects.filter(
    	Q(title__icontains=value[0]) &
    	Q(title__icontains=value[1]) &
    	Q(title__icontains=value[2]) &
    	Q(title__icontains=value[3]) &
    	Q(title__icontains=value[4]) &
    	Q(title__icontains=value[5]) &
    	Q(title__icontains=value[6]) &
    	Q(title__icontains=value[7]) 
	)

	return render(request,'books/searched_books.html',{'queryset':queryset})



def delete_comment(request,comm_id,book_id):
	messages.success(request, 'Your comment was deleted successfully')
	book = Book.objects.get(id=book_id)
	comment = Comments.objects.filter(book=book,id=comm_id).delete()
	return HttpResponseRedirect(reverse('books:book', args=(book.slug,)))


def delete_user_stars(request,user_id,slug):
	messages.success(request, 'You unrated this book successfully')
	book = Book.objects.get(slug=slug)
	delete_stars = Users_stars.objects.get(Q(book=book) & Q(user=request.user)).delete()
	return HttpResponseRedirect(reverse('books:book', args=(book.slug,)))



# def update_comment(request,comm_id,book_slug):
# 	messages.success(request, 'Your comment was updated successfully' , extra_tags='comm_updated')
# 	book = Book.objects.get(slug=book_slug)
# 	comment = Comments.objects.get(id=comm_id)
# 	update_form = Comment_form(initial={'comment': comment.comment})	
# 	return render(request,'books/update_comment.html',{
# 		'update_form':update_form,
# 		'edited_comment':edited_comment,
# 		'book':book})
















# form2 = Comment_form(initial={'Email': GetEmailString()}) u can use methods inside
	# if form.is_valid(): IF U USE POST INSTEAD OF GET METHOD
 #    	form.cleaned_data['Email'] = GetEmailString()



'''
					##### KAKO RASPAKIRATI QUERYSET U OBICNU LISTU
	xxx = book.genres.values_list('genre', flat=True) 
	print(list(xxx),'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')


'''