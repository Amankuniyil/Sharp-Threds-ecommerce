from django.contrib import admin
from django.urls import path
from .views import home,etc,product_details,base,search,contact,blog

urlpatterns = [

       path('', home, name='home'),
       path('etc/', etc, name='etc'),
       path('contact/',contact, name='contact'),
       path('blog/',blog, name='blog'),
       path('shop/<slug:category_slug>/', etc, name='products_by_category'),
       path('shop/<slug:category_slug>/<slug:sub_category_slug>/', etc, name='products_by_sub_category'),
       path('shop/<slug:category_slug>/<slug:sub_category_slug>/<slug:product_slug>/', product_details, name='product_details'),
       path('product_details/', product_details, name='product_details'),
       path('base/',base,name='base'),
       path('shop_filter/',etc, name='shop_filter'),
       path('search/',search, name='search'),
       



]