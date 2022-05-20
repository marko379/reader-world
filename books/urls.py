from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'books'

urlpatterns = [


	path('books-by-genres/',views.return_books_by_ganres,name='books_by_ganres'),
	path('comment-rating-system/',views.comment_like_dislike_system,name='comment_system'),
	path('book-rating-system/',views.book_like_dislike_system,name='system'),
	path('books-you-have-searched-for/',views.search_book,name='search'),
	path('delete-comment/<int:comm_id>/<int:book_id>/',views.delete_comment,name='comm_delete'),
	path('star/<int:book_id>/',views.rating_star_system,name='rating_star'),
	path('un-rate/<str:slug>/<int:user_id>/',views.delete_user_stars,name='user_stars_delete'),
	path('book-by-genre/<str:gen>/',views.get_one_genre_books ,name='one_genre'),

	path('page-num-update-comm/<slug:slug>/<page_num_update_comment>/',views.book, name='book-comment'),
	path('book/<slug:slug>/',views.book, name='book'),

]
