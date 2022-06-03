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





def return_books_by_ganres(request):
	values_list = request.POST.getlist('value') # get list of all genres that client choos
	value_string = ' , '.join(values_list)
	book = Book.objects.filter(genres__genre__in=values_list).distinct() # ['History','Adventure']
	return render(request,'books/books_by_genres.html',{'book':book,'value_string':value_string})


def get_one_genre_books(request,gen):
	book = Book.objects.filter(genres__genre=gen)
	return render(request,'books/book_by_one_genre.html',{'book':book,'gen':gen})




def book(request,slug,page_num_update_comment=1):
	if ( 'session' in request.session):
		username = request.session['username']
		messages.success(request, 'Wellcome {}! Your are logged in!'.format(username))
	book = Book.objects.get(slug=slug)
	rating_star_system = Rating_star_system.objects.get(star=book.id) 
	list_book_genres = book.genres.values_list('genre', flat=True) 
	return_books_by_ganres = Book.objects.filter(genres__genre__in=list_book_genres).annotate(num_authors=Count('likes')).order_by('-num_authors')
	comment = Comments.objects.filter(book=book).annotate(num_authors=Count('comment_likes')).order_by('-num_authors')
	page_num = request.GET.get('page_num')
	if page_num == None:
		page_num = page_num_update_comment

	comments = Paginator(comment, 5, orphans=4)
	page = comments.page(page_num)
	user_stars_per_book_on_coment = Users_stars.objects.filter(book=book)
	try:
		user_star_book = Users_stars.objects.get(Q(book=book) & Q(user_id=request.user.id))
	except ObjectDoesNotExist:
		user_star_book = None
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
	update_form = None
	comm_idx = request.GET.get('comm_idx')
	if comm_idx:
		# content of the comment
		comm = Comments.objects.get(Q(book=book) & Q(id=comm_idx)).comment
		comm2 = Comments.objects.get(Q(book=book) & Q(id=comm_idx)).id
		form = Comment_form()
		update_form = Comment_form(initial={'comment': comm,'comm_id':comm2})
	if request.method =='POST':
		comm_id = request.POST.get('comm_id')
		if comm_id:
			comm = Comments.objects.get(Q(book=book) & Q(id=comm_id) & Q(user=request.user))
			comm.comment = request.POST['comment']
			comm.save()
			messages.success(request, 'Your comment was updated successfully')
			return HttpResponseRedirect(reverse('books:book-comment', args=(book.slug,page_num,)))

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
	return render(request,'books/book_page.html',
		{
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
