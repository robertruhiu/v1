from rest_framework import serializers


from cart.models import Cart
from frontend.serializers import ProfileSerializer


class CartSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = Cart
        fields = ('id','user','devspaid','checked_out','devspending','amount','conditions','type')

class CartSerializerupdater(serializers.ModelSerializer):
    user = ProfileSerializer

    class Meta:
        model = Cart
        fields = ('id','user','devspaid','checked_out','devspending','amount','transaction_id','conditions','type')


