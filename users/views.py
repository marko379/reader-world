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
import re 


from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site  
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage  
from .forms import account_activation_token 




# is_active , user exists but cannot login if is_active = False
# get_current_site = This is  to obtain the current cite domain
# Django’s send_mail() and send_mass_mail() functions are actually thin wrappers that make use of the EmailMessage class.

##### current_site_info.domain
# A domain name is a string of text that maps to a numeric IP address, used to access a website from client software. In plain English, a domain name is the text that a user types into a browser window to reach a particular website. For instance, the domain name for Google is ‘google.com’.
# The actual address of a website is a complex numerical IP address (e.g. 103.21.244.0), but thanks to DNS, users are able to enter human-friendly domain names and be routed to the websites they are looking for. This process is known as a DNS lookup. DNS = Domain Name System (DNS) is the phonebook of the Internet. 
#  get_current_site(request)= 127.0.0.1:8000 /// get_current_site(request).domain = reader-world

#  render_to_string basiclly takes template as a first argument, then 2nd argument is dictanoary that takes values of what we want to show in that template, then it show everuthing like a string

# PasswordResetTokenGenerator
# account_activation_token.make_token(form.instance),   account_activation_token is sub class of PasswordResetTokenGenerator and has 2 methods : make_token and check_token, after token is made will be sent to user email, when user click on the link that user recived it will take him/her to function activate, then token and uid will be cheked

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
			# return HttpResponse('Please proceed confirm your email address to complete the registration')  
			# request sessin is created and will be able accses it after redirecting
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



# urlsafe_base64_encode(s)[source]¶
# Encodes a bytestring to a base64 string for use in URLs, stripping any trailing equal signs.
# urlsafe_base64_decode(s)[source]
# Decodes a base64 encoded string, adding back any trailing equal signs that might have been stripp
# when user click on link that is being sent to his email, information will be sent here, 
# uidb64 is user_id encoded in base64
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
		return redirect('books:front') 
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
			return redirect("books:front")
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





















# def register(request):
# 	if request.method == 'POST':
# 		form = User_form(request.POST)
# 		user_img_form = User_photo_form(request.POST,request.FILES)
# 		if form.is_valid() and user_img_form.is_valid() : #and user_img_form.is_valid()
# 			form.instance.is_active = False
# 			form.save()
# 			photo_user = user_img_form.save(commit=False)
# 			photo_user.user = form.instance 
# 			photo_user.save()
# 			#This is  to obtain the current cite domain   
# 			current_site_info = get_current_site(request)
# 			mail_subject = 'The Activation link has been sent to your email address'  
# 			message = render_to_string('users/acc_active_email.html', {  
# 				# 'form': form,  
# 				'domain': current_site_info.domain,  
# 				'uid': urlsafe_base64_encode(force_bytes(form.instance.pk)),
# 				'token':account_activation_token.make_token(form.instance),  
# 			})  
# 			to_email = form.cleaned_data.get('email')  
# 			email = EmailMessage(  
# 						mail_subject, message, to=[to_email]  
# 			)  
# 			email.send()  
# 			return HttpResponse('Please proceed confirm your email address to complete the registration')  
# 			# request sessin is created and will be able accses it after redirecting
# 			request.session['form_message'] = "form_message"
# 			request.session['username'] = form.instance.username
# 			return redirect('books:front')
# 		else:
# 			messages.error(request, 'Something went wrong.')
# 	else:
# 		form = User_form()
# 		user_img_form = User_photo_form()
# 	return render(request,'users/singup_form.html',{'form':form,'user_img_form':user_img_form})