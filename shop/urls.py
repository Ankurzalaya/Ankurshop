from django.urls import path
from .views import Index
from shop import views
from . import views
from shop import models


urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("Payment", views.Payment, name="Payment"),
    path("succes", views.Succes, name="succes"),
    path("search/", views.Search, name="search"),
    path("contact", views.ContactView.as_view(), name="contact"),
    path("checkout", views.CheckoutCreateView.as_view(), name="checkout-page"),
    # urls for cart
    path("cart/add/<int:id>/", views.cart_add, name="cart_add"),
    path("cart/item_clear/<int:id>/", views.item_clear, name="item_clear"),
    path("cart/item_increment/<int:id>/", views.item_increment, name="item_increment"),
    path("cart/item_decrement/<int:id>/", views.item_decrement, name="item_decrement"),
    path("cart/cart_clear/", views.cart_clear, name="cart_clear"),
    path("cart/cart-detail/", views.cart_detail, name="cart_detail"),
    # url of wishhlist
    path("Wishlistadd/<int:id>/", views.Addtowishlist, name="Wishlistadd"),
    path("Wishlist_detail/", views.Wishlist_detail, name="Wishlist_detail"),
    path(
        "Wishlist_item_delete/<int:id>/",
        views.Deletewishlistitem,
        name="Wishlist_item_delete",
    ),
    path("Wishlist_clear/", views.Wishlistclear, name="Wishlist_clear"),
]

app_name = "shop"
