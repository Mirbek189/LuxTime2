from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_user, name='login_user'),
    path('collections/', views.collections, name='collections'),
    path('about/', views.about, name='about'),
]
