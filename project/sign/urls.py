from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, UserProfileCreateView


urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='registration/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='registration/signup.html'),
         name='signup'),
    path('userprofile_create/',
         UserProfileCreateView.as_view(template_name='registration/create_user.html'),
         name='user_create_profile'),
]