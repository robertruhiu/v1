from rest_framework import serializers

from remote_codeln.models import RemoteProject, Bid, EscrowPayment, Issue


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

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
