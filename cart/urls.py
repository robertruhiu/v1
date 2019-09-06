from django.urls import path


from cart.views import CartCreate, CartUpdate, DeveloperOrderCreate, DeveloperOrderUpdate, DeveloperOrderList


app_name = "cart"

urlpatterns = [
    path('cart_create/<int:user_id>/', CartCreate.as_view(), name="cart-create"),
    path('cart_update/<int:pk>/', CartUpdate.as_view(), name="cart-update"),

    path('developer_order_create/<int:developer_id>/<int:cart_id>/', DeveloperOrderCreate.as_view(), name="developer-order-create"),
    path('developer_order_list/<int:cart_id>/', DeveloperOrderList.as_view(), name="developer-order-list"),
    path('developer_order_update/<int:pk>/', DeveloperOrderUpdate.as_view(), name="developer-order-update"),
]