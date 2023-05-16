from django.contrib import admin
from django.urls import path
from .views import cart,add_cart,remove_cart,remove_cart_item,checkout,coupon,increment_cart_item,decrement_cart_item

urlpatterns = [

  path('cart/', cart, name='cart'),
         
  path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
  path('remove_cart/<int:product_id>/<int:cart_item_id>/', remove_cart, name='remove_cart'),
  path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', remove_cart_item, name='remove_cart_item'),
  
  path('checkout/', checkout, name='checkout'),
  path("coupon/",coupon,name='coupon'),
  path('increment_cart_item/<int:cart_item_id>/',increment_cart_item, name='increment_cart_item'),
        
  path('decrement_cart_item/<int:cart_item_id>/',decrement_cart_item, name='decrement_cart_item')
       


]