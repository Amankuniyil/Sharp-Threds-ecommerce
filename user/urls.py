from django.contrib import admin
from django.urls import path
from .views import add_address,edit_address,myAddress,delete_address,myOrders,orderDetails,wishlist,add_wishlist,wishlist_remove

urlpatterns = [
    path('myAddress/', myAddress, name='myAddress'),
 path('add_address/', add_address, name='add_address'),
  path('edit_address/<int:id>/', edit_address, name='edit_address'),
  path('delete_address/<int:id>/', delete_address, name='delete_address'),
  path('myOrders/', myOrders, name='myOrders'),
  path('orderDetails/<int:order_id>/', orderDetails, name='orderDetails'),
  path('wishlist',wishlist,name='wishlist'),
  path('add_wishlist/<int:id>',add_wishlist,name='add_wishlist'),
  path('wishlist_remove/<int:id>',wishlist_remove,name='wishlist_remove'),
  
  
]