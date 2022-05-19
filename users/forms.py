from django import forms
from django.forms import Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm
from .models import User_photo 
from django.forms import ModelForm, TextInput, EmailInput,PasswordInput


from django.contrib.auth.tokens import PasswordResetTokenGenerator  
import six  





class User_photo_form(forms.ModelForm):
	class Meta:
		model = User_photo
		fields = ['user_img']

	def __init__(self, *args, **kwargs):
		super(User_photo_form, self).__init__(*args, **kwargs)

		self.fields['user_img'].widget = forms.FileInput(attrs={'class': 'form-control',})

class Update_user(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email','first_name','last_name']
		
class User_form(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email','password1','password2','first_name','last_name']

	def clean_email(self):
		data = self.cleaned_data['email']
		user_email_count =  User.objects.filter(email=data).count()
		if user_email_count > 0 :
			raise forms.ValidationError("This email is already used")
		return data

	def __init__(self, *args, **kwargs):
		super(User_form, self).__init__(*args, **kwargs)

		self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control','rows': 1,'required': 'true', 'cols': 1,'placeholder': ("please enter your username")})
		self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control','rows': 1,'required': 'true', 'cols': 1,'placeholder': ("please enter your email")})
		self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control','rows': 1,'required': 'true', 'cols': 1,'placeholder': ("please enter your password")})
		self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control','rows': 1,'required': 'true', 'cols': 1,'placeholder': ("please confirm your password")})
		self.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control','rows': 1, 'cols': 1,'placeholder': ("please enter your first name* (optional)")})
		self.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control','rows': 1, 'cols': 1,'placeholder': ("please enter your last name* (optional)")})


class PasswordForm(PasswordChangeForm):

	def __init__(self, *args, **kwargs):
		super(PasswordForm, self).__init__(*args, **kwargs)

		self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-control','rows': 1,'required': 'true', 'cols': 1,'placeholder': ("old password")})
		self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control','rows': 1,'required': 'true', 'cols': 1,'placeholder': ("new password")})
		self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control','rows': 1,'required': 'true', 'cols': 1,'placeholder': ("confirm new password")})



# this will create token 
class TokenGen(PasswordResetTokenGenerator):  
	def _make_hash_value(self, user, timestamp):

		return (  
			six.text_type(user.pk) + six.text_type(timestamp) +  
			six.text_type(user.is_active)  
			)  
account_activation_token = TokenGen()  


# 97 oooooooooooooooooooooooooooooooooooooooooo
# 674396531 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
# 674396531 111111111111111111111111111111111111111111
# 97 2222222222222222222222222222222222222222222222222

# The unicode type was renamed to str in Python 3. Use six.text_type to
# make the modified code compatible with Python 2 and Python 3.
# six.text_type = Type for representing (Unicode) textual data. This is unicode() in Python 2 and str in Python 3.