from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm
from .forms import User_photo_form, User_form, Update_user ,PasswordForm
from .models import User_photo
from django.contrib.auth import authenticate, login,get_user_model
from django.contrib import messages
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage  
from .forms import account_activation_token
import re 



# # uidb64 is user_id encoded in b64
def register(request):
	if request.method == 'POST':
		form = User_form(request.POST)
		user_img_form = User_photo_form(request.POST,request.FILES)
		if form.is_valid() and user_img_form.is_valid() : #and user_img_form.is_valid()
			form.instance.is_active = False
			form.save()
			photo_user = user_img_form.save(commit=False)
			photo_user.user = form.instance 
			photo_user.save()
			#This is  to obtain the current cite domain   
			current_site_info = get_current_site(request)
			mail_subject = 'The Activation link has been sent to your email address'  
			message = render_to_string('users/acc_active_email.html', {  
				# 'form': form,  
				'domain': current_site_info.domain,  
				'uid': urlsafe_base64_encode(force_bytes(form.instance.pk)),
				'token':account_activation_token.make_token(form.instance),  
			})  
			to_email = form.cleaned_data.get('email')  
			email = EmailMessage(  
						mail_subject, message, to=[to_email]  
			)  
			email.send()  
			request.session['form_message'] = "form_message"
			request.session['username'] = form.instance.username
			messages.success(request, 'please go to your email and confirm/click on link to activate account!') 
			return redirect('users:confirmation_page')
		else:
			messages.error(request, 'Something went wrong.')
	else:
		form = User_form()
		user_img_form = User_photo_form()
	return render(request,'users/singup_form.html',{'form':form,'user_img_form':user_img_form})



def activate(request, uidb64, token):  
	User = get_user_model()  
	try:  
		uid = force_str(urlsafe_base64_decode(uidb64))
		# uid = force_text(urlsafe_base64_decode(uidb64))  
		user = User.objects.get(pk=uid)  
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
		user = None  
	if user is not None and account_activation_token.check_token(user, token):  
		user.is_active = True  
		user.save()  
		# request.session['form_message'] = "form_message"
		# request.session['username'] = user.username
		messages.success(request, 'hello {} , your account was created successfully, you can login now!'.format(user.username))
		return redirect('home') 
	else:  
		messages.error(request, 'link expired or invalid')
		return redirect('users:confirmation_page')
		# return HttpResponse('Activation link is invalid!')  


def confirmationView(request):  
	return render(request,'users/confirmation.html')



def log(request):
	# this next url will be sent from base.html 
	next_login_url = request.POST.get('next')
	check_url = re.search("password-reset-complete",next_login_url)
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		request.session['seesion_wellcome_login'] = 'session'
		request.session['username'] = username
		if check_url:
			messages.success(request, 'Wellcome {}! Your are logged in!'.format(username))
			return redirect("home")
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
		if request.FILES:
			# i am using here name word instead of path coz of s3 bucket
			delete_user_photo = user.user_photo.user_img.name
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
	return redirect('home')
	
def delete_user_profile(request):
	user = User.objects.get(id=request.user.id).delete()
	messages.success(request, 'profile is deleted :( ')
	return redirect('home')
	

def logout_view(request):
	logout(request)
	messages.success(request, 'You are logged out successfully!')
	return redirect('home')


def UpdatePassword(request):
	form = PasswordForm(user=request.user)
	if request.method == 'POST':
		form = PasswordForm(user=request.user, data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Hi {}.Your password is updated successfully! You can login now with your new password'.format(request.user.username))
			return redirect('home')
		else:
			messages.error(request, 'Something went wrong. Try again!')

	return render(request,'users/passwordChange.html',{'form':form}) 



