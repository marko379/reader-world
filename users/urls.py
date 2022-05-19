from django.contrib import admin
from django.urls import path,include, reverse_lazy
from .import views
from django.contrib.auth import views as auth_views
# from .views import activate  


app_name = 'users'

urlpatterns = [

    path('sing-up/', views.register,name='register-url'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('log-in/', views.log,name='log'),
    path('logout/', views.logout_view ,name='logout'),
    path('update-profile/',views.update_profile,name='update_url'),
    path('edit-profile/',views.edit_profile,name='edit_url'),
    path('delete_profile_user/', views.delete_user_profile,name='delete-user'),
    path('password-change/', views.UpdatePassword,name='update_pass'),
    path('confirmation/', views.confirmationView,name='confirmation_page'),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),  

    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
    #     views.activate, name='activate'),      
]