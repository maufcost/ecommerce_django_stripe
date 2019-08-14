from . import views
from django.urls import path

urlpatterns = [
    path("", views.cart_home, name="cart-home-upn"),
    path("update/", views.cart_update, name="cart-update-upn"),
]
