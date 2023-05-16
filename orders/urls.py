from django.contrib import admin
from django.urls import path
from .views import payments,place_order,cancel_order,return_order,cash_on_delivery,payments_completed,razorpay

urlpatterns = [
  path('place_order/', place_order, name='place_order'),
  path('payments/', payments, name='payments'),
  path('razorpay/', razorpay, name='razorpay'),
  path("cancel_order/<int:id>/",cancel_order,name='cancel_order'),
  path("return_order/<int:id>/",return_order,name='return_order'),
  path("cash_on_delivery/<int:id>/",cash_on_delivery,name='cash_on_delivery'),
  path('payments_completed/',payments_completed,name = 'payments_completed'),




]