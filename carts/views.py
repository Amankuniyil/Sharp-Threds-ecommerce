from django.shortcuts import render,redirect,get_object_or_404
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from main.models import Product, Variation
from orders.models import Address,Coupon,UserCoupon
from django.http import JsonResponse


# Create your views here.




def _cart_id(request):
  cart = request.session.session_key
  if not cart:
    cart = request.session.create()
  return cart


def cart(request, total=0, quantity=0, cart_items=None):
  tax=0
  grand_total=0
  product_price = 0
  
  try:
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(user = request.user, is_active=True).order_by('id')
    else:
      cart = Cart.objects.get(cart_id=_cart_id(request))
      cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('id')
      
    for cart_item in cart_items:
      #price_mult = int(cart_item.variations.all().values_list('price_multiplier')[0][0])
      product_price = int(cart_item.product.offer_price()) #* price_mult
      total += int(cart_item.product.offer_price())*int(cart_item.quantity)#*price_mult
      quantity += cart_item.quantity
      cart_item.price = product_price
      cart_item.save()
    tax = (5 * total)/100
    grand_total = total + tax
    grand_total = format(grand_total, '.2f')
  except ObjectDoesNotExist:
    pass
  
  context = {
    'total':total,
    'quantity':quantity,
    'cart_items':cart_items,
    'tax':tax,
    'grand_total':grand_total,
  }
  return render(request, 'carts/cart.html', context)

def add_cart(request, product_id):
  current_user = request.user
  product = Product.objects.get(id=product_id)
  if current_user.is_authenticated:
    product_variation = []
    if request.method == 'POST':
      for item in request.POST:
        key = item
        value = request.POST[key]
        
        try:
          variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
          product_variation.append(variation)
        except:
          pass
    
    is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
    if is_cart_item_exists:
      cart_item = CartItem.objects.filter(product=product, user=current_user)
      
      ex_var_list = []
      id = []
      for item in cart_item:
        existing_variation = item.variations.all()
        ex_var_list.append(list(existing_variation))
        id.append(item.id)
      
      if product_variation in ex_var_list:
        index = ex_var_list.index(product_variation)
        item_id = id[index]
        item = CartItem.objects.get(product=product, id=item_id)
        item.quantity += 1
        item.save()
        
      else:
        item = CartItem.objects.create(product=product, quantity=1, user=current_user)
        if len(product_variation) > 0:
          item.variations.clear()
          item.variations.add(*product_variation)
          
        item.save()
    else:
      cart_item = CartItem.objects.create(
        product=product,
        quantity = 1,
        user = current_user,
      )
      if len(product_variation) > 0:
        cart_item.variations.clear()
        cart_item.variations.add(*product_variation)
      cart_item.save()
      
    return redirect('cart')
  
  # if user is not authenticated
  else:
    product_variation = []
    if request.method == 'POST':
      for item in request.POST:
        key = item
        value = request.POST[key]
        
        try:
          variation = Variation.objects.get(product=product,variation_category__iexact=key, variation_value__iexact=value)
          product_variation.append(variation)
        except:
          pass
      
    try:
      cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
      cart = Cart.objects.create(cart_id=_cart_id(request))
    
    cart.save()
    
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
      cart_item = CartItem.objects.filter(product=product, cart=cart)
      
      ex_var_list = []
      id = []
      for item in cart_item:
        existing_variation = item.variations.all()
        ex_var_list.append(list(existing_variation))
        id.append(item.id)
      
      if product_variation in ex_var_list:
        index = ex_var_list.index(product_variation)
        item_id = id[index]
        item = CartItem.objects.get(product=product, id=item_id)
        item.quantity += 1
        item.save()
      else:
        item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if len(product_variation) > 0:
          item.variations.clear()
          item.variations.add(*product_variation)
          
        item.save()
    else:
      cart_item = CartItem.objects.create(
        product=product,
        quantity = 1,
        cart = cart,
      )
      if len(product_variation) > 0:
        cart_item.variations.clear()
        cart_item.variations.add(*product_variation)
      cart_item.save()
      
    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
  product = get_object_or_404(Product, id=product_id)
  
  try:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
      cart = Cart.objects.get(cart_id=_cart_id(request))
      cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    
    if cart_item.quantity > 1:
      cart_item.quantity  -= 1
      cart_item.save()
    else:
      cart_item.delete()
      
  except:
    pass
  return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
  product = get_object_or_404(Product, id=product_id)
  
  if request.user.is_authenticated:
    cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
  else:
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
  cart_item.delete()
  return redirect('cart')


def checkout(request, total=0, quantity=0, cart_items=None):
  tax=0
  grand_total=0
  address = Address.objects.filter(user = request.user)
  
  try:
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(user = request.user, is_active=True)
    else:
       cart = Cart.objects.get(cart_id=_cart_id(request))
       cart_items = CartItem.objects.filter(cart=cart, is_active=True)

    for cart_item in cart_items:
      total += int(cart_item.price)*int(cart_item.quantity)
      quantity += cart_item.quantity
    tax = (5 * total)/100
    grand_total = total + tax
    grand_total = format(grand_total, '.2f')
  except ObjectDoesNotExist:
    pass
  
  coupons = Coupon.objects.filter(active = True)

  for item in coupons:
    try:
        coupon = UserCoupon.objects.get(user = request.user,coupon = item)
    except:
        coupon = UserCoupon()
        coupon.user = request.user
        coupon.coupon = item
        coupon.save() 


  coupons = UserCoupon.objects.filter(user = request.user, used=False)
  
  context = {
    'address':address,
    'total':total,
    'quantity':quantity,
    'cart_items':cart_items,
    'tax':tax,
    'grand_total':grand_total,
    'coupons':coupons,
  }
  
  return render(request, 'carts/checkout.html', context)




def coupon(request):
  if request.method == 'POST':
    coupon_code = request.POST['coupon']
    grand_total = request.POST['grand_total']
    coupon_discount = 0
    try:
      instance = UserCoupon.objects.get(user = request.user ,coupon__code = coupon_code)

      if float(grand_total) >= float(instance.coupon.min_value):
        coupon_discount = ((float(grand_total) * float(instance.coupon.discount))/100)
        grand_total = float(grand_total) - coupon_discount
        grand_total = format(grand_total, '.2f')
        coupon_discount = format(coupon_discount, '.2f')
        msg = 'Coupon Applied successfully'
        instance.used = True
        instance.save()
      else:
          msg='This coupon is only applicable for orders more than ₹'+ str(instance.coupon.min_value)+ '\- only!'
    except:
            msg = 'Coupon is not valid'
    response = {
               'grand_total': grand_total,
               'msg':msg,
               'coupon_discount':coupon_discount,
               'coupon_code':coupon_code,
                }

  return JsonResponse(response)


def decrement_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    
    return redirect('cart')

def increment_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity < cart_item.product.stock:
      cart_item.quantity += 1
      cart_item.save()
    return redirect('cart')