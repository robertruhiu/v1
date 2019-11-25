from django.shortcuts import render
from rest_framework import generics, status

# Create your views here.
from rest_framework.permissions import IsAuthenticated


from accounts.models import Profile
from cart.models import Cart
from cart.serializers import CartSerializer,CartSerializerupdater

class CartCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializerupdater

class Cartlist(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer
    def get_queryset(self):
        recruiter_id = self.kwargs['recruiter']
        user = Profile.objects.get(id=recruiter_id)
        return Cart.objects.filter(user=user,checked_out=False)

class CartUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializerupdater

class CartGet(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


