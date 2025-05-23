from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_user, name='login_user'),
    path('collections/', views.collections, name='collections'),
    path('about/', views.about, name='about'),
    path('account/', views.account, name='account'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart_view, name='cart'),
    path('favorites/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
]

