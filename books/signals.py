from django.db.models.signals import post_save, pre_save, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Rating_star_system,Book,Users_stars


# this function does : whenever  new object book is created also new Rating_star_system object will be created and conected to the book
# instance represent a book , star is OneToOneField with a Book
# we made Rating_star_system to keep track of all  users that rated specific book ,
# Rating_star_system also has 5 properties, star_1,star_2 ... star_5, and each of those stars properties have star_1 = models.ManyToManyField(User,blank=True,related_name='star_1'),star_2 ...
# that means that every star contains all users coz of manytomany field 
# so if user rate it with 3 stars lets say , he will be send to star_3 property and saved , that is how we keep track of them
# rate_it_stars.html, views.rating_star_system, url.rating_star, models.Rating_star_system ...(all conected to this)
@receiver(post_save,sender=Book)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Rating_star_system.objects.create(star=instance)



# M2M_CHANGED https://docs.djangoproject.com/en/4.0/ref/signals/#m2m-changed
# WHAT THESE FUNCTION DO?
# THESE FUNCTION ARE MADE TO KEEP TRACK BETWEEN 2 MODELS (USER_STARS AND Rating_star_system )TO KNOW HOW MANY STARS WAS GIVEN TO BOOK FROM USER 
# THESE FUNCTION HAVE 2 PURPOSES, TO UPDATE MODEL OR TO CREATE NEW MODEL (USER_STARS) WHENEVER USER RATE A BOOK, NEW MODEL WILL BE CREATED IF USER DID NOT RATE THE BOOK(USER_STARS) , IF USER DID RATE THE BOOK THEN MODEL WILL BE ONLY UPDATED 
# M2M_CHANGED IS USED SPECIFICLY FOR TO DO SOMETHING WITH MANYTOMANYFIELDS
# SENDER IS MODEL Rating_star_system AND ITS INSTANCE STAR_1 (MANYTOMANYFIELD)
# WHENEVER STAR_1 INSTNCE HAS CHANGED SIGNAL WILL BE FIRED 
# post_add IS ACTION THAT IS BUILT INTO M2M_CHANGED (Sent after one or more objects are added to the relation.)
# pk_set = PRIMARY KEY OF ALL OBJECTS THAT ARE REGISTERD WITH star_1(RETURNED IN PYTHON SET)(BUILT IN m2m_changed)
# IF PK_SET LENGHT == 1 , (ONLY COZ I SOMETIMES MANUALY ADDING MORE USERS TO STAR INSTANCE SO TO ESCAPE ANY ERRORS)

# WHEN USER PRESS RATE BUTTON SIGNAL IS FIRED ,ACTION == POST_ADD , GRAB USER_ID FROM (PK_SET) AND POP IT OUT ,HOW FUNCTION KNOWS WHICH USER NEEDS TO BE POP OUT: BECUSE USER OBJECT IS ONE WHO IS DOING A CHANGE TO Rating_star_system OBJECT,  , THEN GRAB USER FROM USER FROM USER OBJECTS, THEN FILTER AND CHEK IF EXISTS USER_STARS MODEL WITH BOOK(instance.star(star = models.OneToOneField(Book))AND IF USER EXISTS, IF EXISTS THEN UPDATE STARS FIELD WITH NUMBER,IF DO NOT EXISTS THE CREATE NEW MODEL, SO BASICLLY IF USER RATE BOOK WITH 2 STAR THEN STAR_2 FIELD WILL BE UPDATED WIT THAT USER IF HE ALREDY DID RATE BOOK WITH OTHER STAR, IF HE DID NOT RATE THAT BOOK THEN NEW MODEL WILL BE CREATED WITH THAT BOOK STAR AND NUM , WITH NUM WE KEEP TRACK HOW MANY STARS USER GAVE 

# These models are for if user rate book, this is sender=Rating_star_system.star_1.through, if change happens at star_1 this functon will be fired and it will be created new object model Users_stars  or updated existing model  Users_stars if user previouslly rated a book,
# THIS FUNCTION IS MADE TO MAKE OBJECT THAT WILL HAVE USER, HOW MANY STARS USER GAVE TO BOOK, AND BOOK ITSELF, SE WE CAN EASY ACCSESS THESE DETAILS WHEREVER WE WANT
@receiver(m2m_changed, sender=Rating_star_system.star_1.through) # STAR_1 FIELD
def create_profile_user_stars_1(sender, instance,pk_set,action,**kwargs):
	num = 1
	if len(pk_set) == 1 and  action == 'post_add':
		pk_set = pk_set.pop()
		user = User.objects.get(id=pk_set)
		if Users_stars.objects.filter(book=instance.star,user=user).exists():
			update_user = Users_stars.objects.filter(book=instance.star,user=user).update(stars=num)

		else:
			Users_stars.objects.create(book=instance.star,user=user,stars=num)
	else:
		return


@receiver(m2m_changed, sender=Rating_star_system.star_2.through) # STAR_2 FIELD
def create_profile_user_stars_2(sender, instance,pk_set,action,**kwargs):
	num = 2
	if len(pk_set) == 1 and  action == 'post_add':
		pk_set = pk_set.pop()
		user = User.objects.get(id=pk_set)
		if Users_stars.objects.filter(book=instance.star,user=user).exists():
			update_user = Users_stars.objects.filter(book=instance.star,user=user).update(stars=num)
		else:
			Users_stars.objects.create(book=instance.star,user=user,stars=num)
	else:
		return


@receiver(m2m_changed, sender=Rating_star_system.star_3.through) # STAR_3 FIELD
def create_profile_user_stars_3(sender, instance,pk_set,action,**kwargs):
	num = 3
	if len(pk_set) == 1 and  action == 'post_add':	
		pk_set = pk_set.pop()
		user = User.objects.get(id=pk_set)
		if Users_stars.objects.filter(book=instance.star,user=user).exists():
			update_user = Users_stars.objects.filter(book=instance.star,user=user).update(stars=num)

		else:
			Users_stars.objects.create(book=instance.star,user=user,stars=num)
	else:
		return


@receiver(m2m_changed, sender=Rating_star_system.star_4.through) # STAR_4 FIELD
def create_profile_user_stars_4(sender, instance,pk_set,action,**kwargs):
	num = 4
	if len(pk_set) == 1 and  action == 'post_add':	
		pk_set = pk_set.pop()
		user = User.objects.get(id=pk_set)
		if Users_stars.objects.filter(book=instance.star,user=user).exists():
			update_user = Users_stars.objects.filter(book=instance.star,user=user).update(stars=num)

		else:
			Users_stars.objects.create(book=instance.star,user=user,stars=num)
	else:
		return


@receiver(m2m_changed, sender=Rating_star_system.star_5.through) # STAR_5 FIELD
def create_profile_user_stars_5(sender, instance,pk_set,action,**kwargs):
	num = 5
	if len(pk_set) == 1 and  action == 'post_add':	
		pk_set = pk_set.pop()
		user = User.objects.get(id=pk_set)
		if Users_stars.objects.filter(book=instance.star,user=user).exists():
			update_user = Users_stars.objects.filter(book=instance.star,user=user).update(stars=num)
		else:
			save_user = Users_stars.objects.create(book=instance.star,user=user,stars=num)
	else:
		return


























# @receiver(m2m_changed, sender=Rating_star_system.star_1.through)
# def create_profile_user_stars_1(sender, instance,pk_set,action,**kwargs):
# 	num = 1
# 	if pk_set and  action == 'post_add':	
# 		pk_set = pk_set.pop()
# 		user = User.objects.get(id=pk_set)
# 		if Users_stars.objects.filter(book=instance.star,user=user).exists():
# 			Users_stars.objects.update(stars=num)
# 		else:
# 			Users_stars.objects.create(book=instance.star,user=user,stars=num)
# 	else:
# 		return


# @receiver(m2m_changed, sender=Rating_star_system.star_2.through)
# def create_profile_user_stars_2(sender, instance,pk_set,action,**kwargs):
# 	num = 2
# 	if pk_set and  action == 'post_add':	
# 		pk_set = pk_set.pop()
# 		user = User.objects.get(id=pk_set)
# 		if Users_stars.objects.filter(book=instance.star,user=user).exists():
# 			Users_stars.objects.update(stars=num)
# 		else:
# 			Users_stars.objects.create(book=instance.star,user=user,stars=num)
# 	else:
# 		return



# @receiver(m2m_changed, sender=Rating_star_system.star_3.through)
# def create_profile_user_stars_3(sender, instance,pk_set,action,**kwargs):
# 	num = 3
# 	if pk_set and  action == 'post_add':	
# 		pk_set = pk_set.pop()
# 		user = User.objects.get(id=pk_set)
# 		if Users_stars.objects.filter(book=instance.star,user=user).exists():
# 			Users_stars.objects.update(stars=num)
# 		else:
# 			Users_stars.objects.create(book=instance.star,user=user,stars=num)
# 	else:
# 		return



# @receiver(m2m_changed, sender=Rating_star_system.star_4.through)
# def create_profile_user_stars_4(sender, instance,pk_set,action,**kwargs):
# 	num = 4
# 	if pk_set and  action == 'post_add':	
# 		pk_set = pk_set.pop()
# 		user = User.objects.get(id=pk_set)
# 		if Users_stars.objects.filter(book=instance.star,user=user).exists():
# 			Users_stars.objects.update(stars=num)
# 		else:
# 			Users_stars.objects.create(book=instance.star,user=user,stars=num)
# 	else:
# 		return




# @receiver(m2m_changed, sender=Rating_star_system.star_5.through)
# def create_profile_user_stars_5(sender, instance,pk_set,action,**kwargs):
# 	num = 5
# 	if pk_set and  action == 'post_add':	
# 		pk_set = pk_set.pop()
# 		user = User.objects.get(id=pk_set)
# 		if Users_stars.objects.filter(book=instance.star,user=user).exists():
# 			Users_stars.objects.update(stars=num)
# 		else:
# 			Users_stars.objects.create(book=instance.star,user=user,stars=num)
# 	else:
# 		return




# @receiver(m2m_changed, sender=Rating_star_system.star_1.through)
# @receiver(m2m_changed, sender=Rating_star_system.star_2.through)
# @receiver(m2m_changed, sender=Rating_star_system.star_3.through)
# @receiver(m2m_changed, sender=Rating_star_system.star_4.through)
# @receiver(m2m_changed, sender=Rating_star_system.star_5.through)
# def create_profile_user_stars(sender, instance, **kwargs):
# 	print(kwargs,instance,'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')




# @receiver(pre_save,sender=Rating_star_system)
# def create_profile_user_stars(sender, instance,update_fields, **kwargs):
# 	# if not Users_stars.objects.filter(book=instance.star).exists():
# 	print(instance.star_1.all(),update_fields,'dddddddddddddddddddddddddddddddddd')
# 	Users_stars.objects.create(book=instance.star)




# @receiver(post_save,sender=Rating_star_system)
# def create_profile_user_stars(sender, instance, created, **kwargs):
# 	if not Users_stars.objects.filter(book=instance.star).exists():
# 		Users_stars.objects.create(book=instance.star)






# @receiver(pre_save,sender=Rating_star_system)
# def create_users_stars(sender, instance, **kwargs):
# 	print('fffffffffffffffffffffffffffffffffffffffffffffffffff')


# @receiver(post_save,sender=Rating_star_system)
# def create_profile(sender, instance, created, **kwargs):
# 	# if not created:
# 	# print(instance.num_2,'dddddddddddddddddddddddddddddddddd')
# 	Users_stars.objects.create(book=instance.star)