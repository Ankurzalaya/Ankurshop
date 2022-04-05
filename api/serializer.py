from rest_framework import serializers
from shop.models import Products, Category, Adress, Order, Wishlist


class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class Productserializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class Adressserializer(serializers.ModelSerializer):
    class Meta:
        model = Adress
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        return self.Meta.model.objects.create(user=user, **validated_data)


class Wishlistserializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Wishlist
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        return self.Meta.model.objects.create(user=user, **validated_data)


class Orderserializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        return self.Meta.model.objects.create(user=user, **validated_data)
