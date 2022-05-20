from django.db.models.signals import post_save, pre_save, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Rating_star_system,Book,Users_stars


@receiver(post_save,sender=Book)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Rating_star_system.objects.create(star=instance)



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






















