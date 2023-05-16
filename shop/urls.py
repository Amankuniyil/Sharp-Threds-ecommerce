from django.contrib import admin
from django.urls import path
from main.views import home,etc,product_details

urlpatterns = [

       path('product_details/', product_details, name='product_details'),
       
       


]