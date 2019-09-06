from django.shortcuts import render
from rest_framework import generics, status

# Create your views here.
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from cart.models import Cart, DeveloperOrder
from cart.serializers import CartSerializer, DeveloperOrderSerializer


class CartCreate(APIView):
    permission_classes = (AllowAny,)
    queryset = Cart.objects.all()

    def get_object(self, id):
        user = Profile.objects.get(id=id)
        return user

    def post(self, request, user_id):
        user = self.get_object(user_id)
        cart = Cart.objects.create(user=user)
        serializer = CartSerializer(cart)
        return serializer.data


class CartUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class DeveloperOrderCreate(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = DeveloperOrder.objects.all()

    def get_object(self, id):
        developer = Profile.objects.get(id=id)
        return developer

    def post(self, request, developer_id, cart_id):
        developer = self.get_object(developer_id)
        devorder = DeveloperOrder.objects.create(developer=developer, cart=cart)
        serializer = DeveloperOrderSerializer(devorder)
        return serializer.data

class DeveloperOrderUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = DeveloperOrder.objects.all()
    serializer_class = DeveloperOrderSerializer

# class DeveloperOrderList(APIView):
#     pass


class DeveloperOrderList(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = DeveloperOrderSerializer

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        # user = Profile.objects.get(id=candidate_id)
        my_cart = Cart.objects.get(id=cart_id)
        return DeveloperOrder.objects.filter(cart=my_cart)