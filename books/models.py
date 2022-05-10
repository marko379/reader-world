from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse


class Genres(models.Model):
	genre = models.CharField(max_length=30)

	def __str__(self):
		return self.genre


class Book(models.Model):

	title = models.CharField(max_length=200)
	writter = models.CharField(max_length=200)
	published = models.CharField(max_length=20)
	pages = models.PositiveSmallIntegerField()
	file = models.FileField(upload_to='book_files',null=True,blank=True)
	info = models.TextField()
	date_posted = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='books_photos',null=True,blank=True)
	slug = models.SlugField(max_length=200,null=True,blank=True)
	genres = models.ManyToManyField(Genres)
	likes = models.ManyToManyField(User,related_name='likes',blank=True)
	dislikes = models.ManyToManyField(User,related_name='dislikes',blank=True)


	def __str__(self):
		return self.title

	# slugify title and add num at the end of slug, every time new book is made, it counts all book's objects and then add finnaly number to slug
	def slugify_title(self):
		count = Book.objects.all().count()
		self.slug = slugify(self.title) + '-' + str(count)

	# resize image and save 
	def save(self):
		self.slugify_title()
		super().save() # this will execute and save everything above
		img = Image.open(self.image)
		SIZE= 298, 450
		# SIZE= 200, 200
		new_image= img.resize(SIZE, Image.ANTIALIAS)
		new_image.save(self.image.path)

	# 
	@property
	def likes_dislikes_procentage(self):
		total_likes_dislikes = self.likes.count() + self.dislikes.count()
		if total_likes_dislikes == 0:
			total_likes_procentage = 0
			total_dislikes_procentage = 0
		else:
			total_likes_procentage = (self.likes.count() / total_likes_dislikes) * 100
			total_dislikes_procentage = (self.dislikes.count() / total_likes_dislikes) * 100
		return round(total_likes_procentage), round(total_dislikes_procentage)

	# @property
	def files(self):
		if self.file:
			return self.file.url
		else:
			return 'no file'


	def get_absolute_url(self):		
		return reverse('books:book', kwargs={'slug' : self.slug})


class Rating_star_system(models.Model):
	star = models.OneToOneField(Book,on_delete=models.CASCADE,null=True,blank=True)
	star_1 = models.ManyToManyField(User,blank=True,related_name='star_1')
	star_2 = models.ManyToManyField(User,blank=True,related_name='star_2')
	star_3 = models.ManyToManyField(User,blank=True,related_name='star_3')
	star_4 = models.ManyToManyField(User,blank=True,related_name='star_4')
	star_5 = models.ManyToManyField(User,blank=True,related_name='star_5')

	def __str__(self):
		return self.star.title

	@property
	def total(self):
		add_all_users = self.star_1.count() + self.star_2.count() + self.star_3.count() + self.star_4.count() +self.star_5.count()
		multiplie_users = self.star_5.count() * 5 + self.star_4.count() * 4 + self.star_3.count() * 3 + self.star_2.count() * 2 + self.star_1.count() * 1

		if multiplie_users > 0 and add_all_users > 0:
			total_rating = multiplie_users/add_all_users
		else:
			total_rating = 0

		return round(total_rating,1) , add_all_users

	@property
	def each_star_procentage(self):
		add_all_users = self.star_1.count() + self.star_2.count() + self.star_3.count() + self.star_4.count() +self.star_5.count()

		if add_all_users != 0:
			star_1 = (self.star_1.count() / add_all_users) * 100
			star_2 = (self.star_2.count() / add_all_users) * 100	
			star_3 = (self.star_3.count() / add_all_users) * 100	
			star_4 = (self.star_4.count() / add_all_users) * 100	
			star_5 = (self.star_5.count() / add_all_users) * 100
			return round(star_1),round(star_2),round(int(star_3)), round(star_4), round(star_5),'{}%'.format(round(int(star_1))),'{}%'.format(round(int(star_2))),'{}%'.format(round(int(star_3))),'{}%'.format(round(int(star_4))),'{}%'.format(round(int(star_5)))
		else:
			pass



class Users_stars(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	stars = models.SmallIntegerField(null=True,blank=True)
	book = models.ForeignKey(Book,on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		if not self.user:
			return "{} //// user: ".format(self.book.title)
		return "BOOK: {}-------------USER: {}-------------STARS-GIVEN: {}".format(self.book.title,self.user.username,self.stars)



class Comments(models.Model):
	comment = models.TextField(max_length=30000,null=True,blank=True)
	book = models.ForeignKey(Book, on_delete=models.CASCADE,null=True,blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
	comment_likes = models.ManyToManyField(User,related_name='comment_likes',blank=True)
	comment_dislikes = models.ManyToManyField(User,related_name='comment_dislikes',blank=True)
	date_comment_modified = models.DateField(auto_now_add=True,null=True, blank=True) # objects firts time created
	date_comment_posted = models.DateField(auto_now=True,null=True, blank=True) # every time comm is modified i will save the time
	user_book_star = models.OneToOneField(Users_stars, on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		if not self.user:
			return 'BOOK: {}------------ USER: {} '.format(self.book.title,'anonimus-user')
		return 'BOOK: {}------------ USER: {} '.format(self.book.title,self.user.username)






