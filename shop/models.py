from django.db import models
from django.contrib.auth.models import User
import datetime


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, default="", blank=True)


# adress = models.ForeignKey(Adress, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category, related_name="category", on_delete=models.CASCADE
    )
    description = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to="uploads/products/")

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        return self.objects.filter(category=category_id)


class Adress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstAdress = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postalcode = models.IntegerField(default=455001)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.today)
    accepted = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    orderid = models.CharField(max_length=100, blank=True)
    razorpaypaymentid = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)
    address = models.ForeignKey(Adress, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk}"

    @staticmethod
    def get_orders_by_customer(user_id):
        return self.objects.filter(user=user_id).order_by("-date")


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(max_length=50)
    total = models.FloatField(null=True)

    def __str__(self):
        return f"{self.order.orderid}" if self.order.orderid else f"{self.order.id}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField(default=0)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    total_items = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)


class Contactus(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subjects = models.CharField(max_length=200)
    message = models.TextField(max_length=300)
    date = models.DateTimeField(default=datetime.datetime.today)

    def __str__(self):
        return self.email


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        default=None,
    )

    class Meta:
        unique_together = (("user", "product"),)
