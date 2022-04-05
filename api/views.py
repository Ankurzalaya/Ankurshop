# from django.urls import path, include
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from shop.models import Products, Category, Adress, Order, Wishlist
from .serializer import (
    Productserializer,
    Categoryserializer,
    Orderserializer,
    Adressserializer,
    Wishlistserializer,
)

# from rest_framework import permission
from rest_framework import serializers, viewsets

# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import FormParser, MultiPartParser

from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Create your views CategoryViewSethere.
class CategoryViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = Categoryserializer
    parser_classes = (FormParser, MultiPartParser)


class ProductViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Products.objects.all()
    serializer_class = Productserializer
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)


class AdressViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Adress.objects.all()
    serializer_class = Adressserializer
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = Orderserializer
    #  authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class WishlistViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Wishlist.objects.all()
    serializer_class = Wishlistserializer
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class SearchListView(ListAPIView):
    queryset = Products.objects.all()
    serializer_class = Productserializer
    filter_backends = [SearchFilter]
    # filter_backends = [DjangoFilterBackend]
    search_fields = ["name"]
