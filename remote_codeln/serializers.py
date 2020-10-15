from rest_framework import serializers

from remote_codeln.models import RemoteProject, Bid, EscrowPayment


class RemoteProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteProject
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid


class EscrowPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscrowPayment
