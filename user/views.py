from django.shortcuts import render,redirect
from orders.models import Address
from accounts.forms import AddressForm
from django.contrib import messages
from orders.models import Order,OrderProduct
from django.core.paginator import Paginator
from .models import WishlistItem, Wishlist
from main.models import Product
# Create your views here.



def myAddress(request):
  current_user = request.user
  address = Address.objects.filter(user=current_user)
  
  context = {
    'address':address,
  }
  return render(request, 'user/myAddress.html', context)

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST,request.FILES,)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name =form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone =  form.cleaned_data['phone']
            detail.email =  form.cleaned_data['email']
            detail.address_line1 =  form.cleaned_data['address_line1']
            detail.address_line2  = form.cleaned_data['address_line2']
            detail.district =  form.cleaned_data['district']
            detail.state =  form.cleaned_data['state']
            detail.city =  form.cleaned_data['city']
            detail.pincode =  form.cleaned_data['pincode']
            detail.save()
            messages.success(request,'Address added Successfully')
            return redirect('myAddress')
        else:
            messages.success(request,'Form is Not valid')
            return redirect('myAddress')
    else:
        form = AddressForm()
        context={
            'form':form
        }    
    return render(request,'user/add-address.html',context)
  

def edit_address(request, id):
  address = Address.objects.get(id=id)
  if request.method == 'POST':
    form = AddressForm(request.POST, instance=address)
    if form.is_valid():
      form.save()
      messages.success(request , 'Address Updated Successfully')
      return redirect('myAddress')
    else:
      messages.error(request , 'Invalid Inputs!!!')
      return redirect('myAddress')
  else:
      form = AddressForm(instance=address)
      
  context = {
            'form' : form,
        }
  return render(request , 'user/edit-address.html' , context)


def delete_address(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect('myAddress')


def myOrders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders':page_obj
    }

    return render(request,'user/myOrders.html',context)


def orderDetails(request,order_id):
    order_details = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_details:
        subtotal += i.product_price * i.quantity
        
    context = {
        'order_details':order_details,
        'order':order,
        'subtotal':subtotal    
    }

    return render(request,'user/orderDetails.html',context)


# Create your views here.
def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist


def add_wishlist(request,id):

    product = Product.objects.get(id=id)
    try:
       
        wishlist =  Wishlist.objects.get(wishlist_id = _wishlist_id(request))
    except Wishlist.DoesNotExist:
       
        wishlist = Wishlist.objects.create(
           
            wishlist_id = _wishlist_id(request)
        ) 
    
    wishlist.save()
    
    try :
        wishlist_item = WishlistItem.objects.get(product=product , user = request.user)
        wishlist_item.save()
    except WishlistItem.DoesNotExist:
        wishlist_item = WishlistItem.objects.create(
            product=product,
            
            wishlist = wishlist,
            user = request.user,
        )
        wishlist_item.save()



    return redirect('wishlist')



def wishlist(request):
    #if request.user.is_authenticated:
        # if Wishlist.objects.filter(wishlist_id = _wishlist_id(request)).exists():
        #     wishlist = Wishlist.objects.filter(wishlist_id = _wishlist_id(request))
        wishlistitem = WishlistItem.objects.filter(user = request.user)
        context = { 
                'wishlistitem':wishlistitem
            }
        return render(request,'user/wishlist.html',context)

    



def wishlist_remove(request,id):
    product = Product.objects.get(id = id )
    wishlist_item = WishlistItem.objects.filter(product=product , user = request.user)
    wishlist_item.delete()
    return redirect('wishlist')
  

