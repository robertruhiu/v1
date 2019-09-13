from django.urls import path


from cart.views import CartCreate, CartUpdate,Cartlist


app_name = "cart"

urlpatterns = [
    path('cartlist/<int:recruiter>', Cartlist.as_view()),
    path('cartcreate', CartCreate.as_view()),
    path('cartupdate/<int:pk>', CartUpdate.as_view()),


]
