# Create your views here.
import re
import razorpay, hmac, hashlib, sys
from sqlite3 import paramstyle
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Products, Adress, Order, OrderLine, Wishlist, Contactus
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import CreateView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from cart.cart import Cart


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRATE))


class Index(View):
    def post(self, request):
        product = request.POST.get("product")
        print(product)
        render()

    def get(self, request):
        allprodutcs = Products.objects.all()
        prod = {"prod": allprodutcs}
        return render(request, "home.html", prod)


def Search(request):
    q = request.GET.get("query")
    products = Products.objects.filter(name__icontains=q)
    context = {"products": products}
    return render(request, "search.html", context)


# Views for Cart
@login_required
def cart_add(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    # print(product)
    cart.add(product=product)
    return redirect("shop:index")


@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.remove(product)
    return redirect("shop:cart_detail")


@login_required
def item_increment(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.add(product=product)
    return redirect("shop:cart_detail")


@login_required
def item_decrement(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("shop:cart_detail")


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("shop:cart_detail")


@login_required
def cart_detail(request):
    return render(request, "cart/cart_detail.html")


# Views for Wishlist
@login_required
def Addtowishlist(request, id):
    product = Products.objects.get(id=id)
    print(product)
    # import pdb;pdb.set_trace()
    wish_list, created = Wishlist.objects.get_or_create(
        product=product, user=request.user
    )

    messages.info(request, "The item was added to your wishlist")
    return redirect("shop:index")


@login_required
def Wishlist_detail(request):
    prod = Wishlist.objects.all()
    print(prod)
    prod = {"prod": prod}
    return render(request, "wish_detail.html", prod)


@login_required
def Deletewishlistitem(request, id):
    Wishlist.objects.filter(user=request.user, product_id=id).delete()
    messages.success(request, "Product Remove From Wishlist...")
    return redirect("shop:Wishlist_detail")


@login_required
def Wishlistclear(request):
    Wishlist.objects.all().delete()
    messages.success(request, "Product Remove From Wishlist...")
    return redirect("shop:Wishlist_detail")


# Views for checkout
class CheckoutCreateView(LoginRequiredMixin, CreateView):
    model = Adress
    template_name = "checkout.html"
    fields = ["firstAdress", "city", "state", "postalcode"]
    success_url = reverse_lazy("shop:Payment")

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.save()
        self.request.session["add"] = form.instance.id
        return super(CheckoutCreateView, self).form_valid(form)

        for key in request.session.keys():
            print(key)


# views for Contactus
class ContactView(SuccessMessageMixin, CreateView):
    model = Contactus
    template_name = "contact.html"
    fields = ["name", "email", "subjects", "message", "date"]
    success_message = "Thanks for Contacting Us."
    success_url = reverse_lazy("shop:index")

    def form_valid(self, form):
        form.save()
        return super(ContactView, self).form_valid(form)


# Views for payment
def Payment(request):
    total_bill = 0.0
    for key, value in request.session["cart"].items():
        total_bill = total_bill + (float(value["price"]) * value["quantity"])

    total_bill = total_bill * 100

    payment = client.order.create(
        {
            "amount": total_bill,
            "currency": "INR",
            "payment_capture": "1",
        }
    )
    # print(total_pay)
    order_id = payment["id"]

    address_id = request.session["add"]
    uid = request.session.get("_auth_user_id")
    user = User.objects.get(id=uid)
    add = Adress.objects.get(id=address_id)
    print(user, add)
    context = {"order_id": order_id, "total_money": total_bill}
    order = Order(
        user=request.user,
        amount=total_bill / 100,
        orderid=order_id,
        razorpaypaymentid=order_id,
        address=add
        # orderid=order_id
    )
    order.save()
    request.session["orderid"] = order.id
    print(request.session["orderid"])

    uid = request.session.get("_auth_user_id")
    user = User.objects.get(id=uid)
    cart = request.session.get("cart")
    # print(cart)
    orderlines = []
    for i in cart:
        # product= Products
        a = int(cart[i]["price"])
        b = cart[i]["quantity"]
        #  print(type(a))
        # print(type(b))
        total = a * b
        print(total)
        item = OrderLine(
            order=order,
            product=cart[i]["name"],
            quantity=cart[i]["quantity"],
            price=cart[i]["price"],
            total=total,
        )
        orderlines.append(item)
        # item.save()
    OrderLine.objects.bulk_create(orderlines)
    if request.method == "POST":
        print(request)
    return render(request, "Payment.html", context)


@csrf_exempt
def Succes(request):
    parameter = request.POST.dict()
    if client.utility.verify_payment_signature(parameter):
        order = Order.objects.filter(orderid=parameter["razorpay_order_id"]).first()
        order.paid = True
        order.save()
        return render(request, "thankyou.html", {"status": True})
    else:
        # TODO : Show payment fail message to user.
        return render(request, "thankyou.html", {"status": False})

def Order(request):
    Order = OrderLine.objects.all()
    print(OrderLine)

    return render(request,"order.html")