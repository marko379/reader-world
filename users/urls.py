from django.contrib import admin
from django.urls import path,include
from .import views
from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [
    path('sing-up/', views.register,name='register-url'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('log-in/', views.log,name='log'),
    path('logout/', views.logout_view ,name='logout'),
    path('update-profile/',views.update_profile,name='update_url'),
    path('edit-profile/',views.edit_profile,name='edit_url'),
    # path('change-password/',  views.UpdatePassword, name='password-change'),
    path('delete_profile_user/', views.delete_user_profile,name='delete-user'),
    path('password-change/', views.UpdatePassword,name='update_pass'),
]