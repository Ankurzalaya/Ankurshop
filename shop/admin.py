from django.contrib import admin

from shop.models import (
    Category,
    Order,
    Products,
    Contactus,
    Cart,
    Profile,
    OrderLine,
    Adress,
    CartItem,
    Wishlist,
)
from django.contrib import admin


class OrderLineTubleinline(admin.TabularInline):
    model = OrderLine


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineTubleinline]


# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
admin.site.register(Adress)
admin.site.register(Profile)
admin.site.register(OrderLine)
admin.site.register(CartItem)
admin.site.register(Contactus)
admin.site.register(Wishlist)
