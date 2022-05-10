from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm
from .forms import User_photo_form, User_form, Update_user ,PasswordForm
from .models import User_photo
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile



def register(request):
	if request.method == 'POST':
		form = User_form(request.POST)
		user_img_form = User_photo_form(request.POST,request.FILES)
		if form.is_valid() and user_img_form.is_valid() : #and user_img_form.is_valid()
			form.save()
			photo_user = user_img_form.save(commit=False)
			photo_user.user = form.instance
			photo_user.save()
			# request sessin is created and will be able accses it after redirecting
			request.session['form_message'] = "form_message"
			request.session['username'] = form.instance.username
			return redirect('books:front')
		else:
			messages.error(request, 'Something went wrong.')
	else:
		form = User_form()
		user_img_form = User_photo_form()
	return render(request,'users/singup_form.html',{'form':form,'user_img_form':user_img_form})


def log(request):
	next_login_url = request.POST.get('next')
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		request.session['seesion_wellcome_login'] = 'session'
		request.session['username'] = username
		messages.success(request, 'Wellcome {}! Your are logged in!'.format(username))
		return redirect(next_login_url)

	else:
		messages.error(request, 'Something went wrong! You are not logged in. Try again!')
		return redirect(next_login_url)



def update_profile(request):
	if 'update_profile_session' in request.session:
		messages.success(request, 'Your profile is updated successfully!')
		del request.session['update_profile_session']
	user = User.objects.get(id=request.user.id)
	update_form2 = User_form(instance=user)
	photo_form =  User_photo_form(instance=user.user_photo)
	return render(request,'users/profile.html',{'user':user,'update_form2':update_form2,'photo_form':photo_form}) 


def edit_profile(request):
	user = User.objects.get(id=request.user.id)
	if request.method == 'POST':
		f = Update_user(request.POST)
		# so user_photo_form have got request.POST,request.FILES, because User_photo_form is not tied to particular user we have to to provide instance, thats how we connent right user to User_photo_form
		if request.FILES:
			delete_user_photo = user.user_photo.user_img.path
			fs = FileSystemStorage()
			fs.delete(delete_user_photo)
		updatePhoto = User_photo_form( request.POST,request.FILES,instance=request.user.user_photo)
		if f.is_valid() and updatePhoto.is_valid():
			first = f.cleaned_data['first_name']
			last = f.cleaned_data['last_name']
			email = f.cleaned_data['email']
			img = updatePhoto.cleaned_data['user_img']
		user = User.objects.filter(id=request.user.id).update(last_name=last,first_name=first,email=email)
		updatePhoto.save()
		request.session['update_profile_session'] = 'update_profile_session'
		
	return redirect('users:update_url')
	
def delete_user_profile(request):
	user = User.objects.get(id=request.user.id).delete()
	messages.success(request, 'profile is deleted :( ')
	return redirect('books:front')
	

def logout_view(request):
	logout(request)
	messages.success(request, 'You are logged out successfully!')
	return redirect('books:front')


def UpdatePassword(request):
	form = PasswordForm(user=request.user)
	if request.method == 'POST':
		form = PasswordForm(user=request.user, data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Hi {}.Your password is updated successfully! You can login now with your new password'.format(request.user.username))
			return redirect('books:front')
		else:
			messages.error(request, 'Something went wrong. Try again!')

	return render(request,'users/passwordChange.html',{'form':form}) 

