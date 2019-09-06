from rest_framework import serializers


from cart.models import Cart, DeveloperOrder
from frontend.serializers import ProfileSerializer


class CartSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = Cart
        fields = ('id','user', 'total_amount')

class DeveloperOrderSerializer(serializers.ModelSerializer):
    developer = ProfileSerializer()
    cart = CartSerializer()

    class Meta:
        model = DeveloperOrder
        fields = ('id','developer', 'price', 'cart', )