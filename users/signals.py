from django.db.models.signals import post_save, pre_save, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import User_photo

# Where ever you create new book create new model
# @receiver(post_save,sender=User)
# def cr(sender, instance,created, update_fields, **kwargs):
# 	for i in User.objects.all():
# 		name = i.username
# 		if not User.objects.filter(user_photo__user__username=name).exists():
# 			x= User.objects.get(username=name)
# 			User_photo.objects.create(user=x)



# @receiver(post_save,sender=User)
# def create_profile(sender, instance,created, update_fields, **kwargs):
# 	if created:
# 		User_photo.objects.create(user=instance)
		

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.user_photo.save()
