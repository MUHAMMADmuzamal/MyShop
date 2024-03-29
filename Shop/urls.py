from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path('signup', views.handleSignup, name='SignUp'),
    path('login', views.handleLogin, name='Login'),
    path('logout', views.handleLogout, name='LogOut'),
    path('allproducts/<str:cat>', views.showAllProducts, name='LogOut'),
    path('cart', views.cart, name='Cart'),
]