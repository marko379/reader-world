from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class User_photo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_img = models.ImageField(default='default_user_img/user_img.png',upload_to='user_photos',null=True,blank=True)

	# def save(self):
	# 	super().save(*args, **kwargs) # this will execute and save everything above
	# 	user_img = Image.open(self.image)
	# 	SIZE= , 450
	# 	new_image= img.resize(SIZE, Image.ANTIALIAS)
	# 	new_image.save(self.image.path)

	def __str__(self):
		if self.user:
			return self.user.username
		else:
			return 'unknown'
