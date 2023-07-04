from django.urls import path
from .views import register, profile, update_profile
from django.contrib.auth import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('registration/', register, name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile')
]
