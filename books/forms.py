from django import forms
from django.forms import Form
from django.contrib.auth.models import User
from .models import Comments,Book   #, Replys
from django.forms import ModelForm, TextInput, EmailInput,PasswordInput
# from crispy_forms.helper import FormHelper



class Comment_form(forms.ModelForm):
	class Meta:
		model = Comments
		fields = ['comment']
		
	def __init__(self, *args, **kwargs):
		super(Comment_form, self).__init__(*args, **kwargs)

		self.fields['comment'].widget = forms.Textarea(attrs={'class': 'form-control', 'background-color':'ffcccc', 'rows': 5,'required': 'true', 'cols': 20,'placeholder': ("What do you think about this book?")})
		self.fields['comment'].label = False
		self.fields['comment'].strip = False


class Comment_form_disabled(forms.Form):

	disabled_field = forms.CharField(label=False,strip = False,widget=forms.Textarea(attrs={'class': 'form-control', 'background-color':'ffcccc', 'disabled':'true', 'rows': 5, 'cols': 20,'placeholder': ("please login/register to be able to comment")}))






class Rating_form(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['likes','dislikes']