from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from accounts.models import Account
from .forms import  ProductForm, CategoryForm, SubCategoryForm, UserForm, VariationForm ,CouponForm#LoginForm
from main.models import Product, Variation
from django.core.paginator import Paginator
from django.contrib import messages
from category.models import Category,Sub_Category
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from orders.models import Order, Payment, Coupon
from datetime import datetime,timedelta,date
from django.http import HttpResponse
import json

from django.db.models import Sum, Q, FloatField


import matplotlib.pyplot as plt
import numpy as np

# Create your views here.




def adminlogin(request):
    # if 'email' in request.session:
    #     return redirect('admindash')
    if  request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        print({'user':user})
        if user is not None and user.is_superadmin:
            
            login(request, user)
            request.session['email'] = email          
            return redirect('admindash')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('adminlogin')
    else:
      
        
        return render(request, 'adminpanel/adminlogin.html')



#Accounts

def users(request):
  dict_about={
    'users': Account.objects.all()
  }
  return render(request,'adminpanel/users.html',dict_about)


#Block user

def block_user(request,id):
    user= get_object_or_404(Account,id= id)
    user.is_active = False
    user.save()
    messages.success(request, 'User blocked')
    print('blocked',{id})
    return redirect('users')  

#Unblock User

def unblock_user(request,id):
    user= get_object_or_404(Account,id= id)
    user.is_active = True
    user.save()
    messages.success(request, 'User Unblocked')
    print('blocked',{id})
    return redirect('users')


#Products




def products(request):
  products = Product.objects.all().order_by('-id')
  
  paginator = Paginator(products, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'products': page_obj
  }
  return render(request, 'adminpanel/products.html', context)




def addProduct(request):
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Product added successfully.')
      return redirect('products')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('addProduct')
  else:
    form = ProductForm()
    context = {
      'form':form,
    }
    return render(request, 'adminpanel/addproduct.html', context)


def editProduct(request, id):
  product = Product.objects.get(id=id)
  
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES, instance=product)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Product edited successfully.')
      return redirect('products')
    else:
      messages.error(request, 'Invalid input')
      
  form =   ProductForm(instance=product)
  context = {
    'form':form,
    'product':product,
  }
  return render(request, 'adminpanel/editProduct.html', context)






def deleteProduct(request, id):
  product = Product.objects.get(id=id)
  product.delete()
  return redirect('products')





def product_offers(request):
  products = Product.objects.all().order_by('-product_offer')
  
  paginator = Paginator(products, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'products':page_obj,
  }
  return render(request, 'adminpanel/productOffers.html', context)


def add_product_offer(request):
  if request.method == 'POST' :
    product_name = request.POST.get('product_name')
    product_offer = request.POST.get('product_offer')
    product = Product.objects.get(product_name = product_name)
    product.product_offer =  product_offer
    product.save()
    messages.success(request,'Product offer added successfully')
    return redirect('product_offers')
  

def delete_product_offer(request, id):
  product = Product.objects.get(id=id)
  product.product_offer = 0
  product.save()
  messages.success(request, 'Product offer deleted successfully')
  return redirect('product_offers')


# variations


def product_variations(request):
  variations = Variation.objects.all().order_by('product')
  
  paginator = Paginator(variations, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'variations':page_obj,
  }
  return render(request, 'adminpanel/product_variations.html', context)


def delete_product_variation(request, id):
  variation = Variation.objects.get(id=id)
  variation.delete()
  messages.success(request, 'Variation deleted successfully!!!')
  return redirect('productvariations')


def edit_product_variation(request, id):
  variation = Variation.objects.get(id=id)
  
  if request.method == 'POST':
    form = VariationForm(request.POST, instance=variation)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Variation edited successfully.')
      return redirect('productvariations')
    else:
      messages.error(request, 'Invalid input')
      return redirect('edit_product_variation')
      
  form =   VariationForm(instance=variation)
  context = {
    'form':form,
    'variation':variation,
  }
  return render(request, 'adminpanel/editVariation.html', context)


def add_product_variation(request):
  
  if request.method == 'POST':
    form = VariationForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Variation added successfully.')
      return redirect('product_variations')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('add_product_variation')
    
  form = VariationForm()
  context = {
    'form':form
  }
  return render(request, 'adminpanel/addVariation.html', context)




#categories

def categories(request):
  categories = Category.objects.all().order_by('id')
  
  paginator = Paginator(categories, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'categories':page_obj
  }
  return render(request, 'adminpanel/categories.html', context)


def addCategory(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Category added successfully.')
      return redirect('categories')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('addCategory')
  else:
    form = CategoryForm()
    context = {
      'form':form,
    }
    return render(request, 'adminpanel/addCategory.html', context)
  


def editCategory(request, slug):
  category = Category.objects.get(slug=slug)
  
  if request.method == 'POST':
    form = CategoryForm(request.POST, request.FILES, instance=category)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Category edited successfully.')
      return redirect('categories')
    else:
      messages.error(request, 'Invalid input')
      return redirect('editCategory', slug)
      
  form =   CategoryForm(instance=category)
  context = {
    'form':form,
    'category':category,
  }
  return render(request, 'adminpanel/editCategory.html', context)



def deleteCategory(request, slug):
  category = Category.objects.get(slug=slug)
  category.delete()
  messages.success(request, 'Category deleted successfully.')
  return redirect('categories')




#subcategories

def subCategories(request, category_slug):
  subCategories = Sub_Category.objects.all().filter(category__slug=category_slug)
  context = {
    'subCategories':subCategories,
    'category_slug':category_slug,
  }
  return render(request, 'adminpanel/subCategories.html', context)



def sub_category(request):
  return render(request,'adminpanel/sub_category.html')




def addSubCategory(request, category_slug):
  category = Category.objects.get(slug=category_slug)
  if request.method == 'POST':
    form = SubCategoryForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request, 'Sub Category added successfully.')
      return redirect('subCategories', category_slug)
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('addSubCategory', category_slug)
  else:
    form = SubCategoryForm()
    context = {
      'form':form,
      'category':category
    }
    return render(request, 'adminpanel/addSubCategory.html', context)
  

def editSubCategory(request, slug):
  subCategory = Sub_Category.objects.get(slug=slug)
  cat_slug = subCategory.category.slug
  
  if request.method == 'POST':
    form = SubCategoryForm(request.POST, request.FILES, instance=subCategory)
    
    if form.is_valid():
      form.save()
      messages.success(request, 'Category edited successfully.')
      return redirect('subCategories', cat_slug)
    else:
      messages.error(request, 'Invalid input')
      return redirect('editSubCategory')
      
  form =   SubCategoryForm(instance=subCategory)
  context = {
    'form':form,
    'subCategory':subCategory,
  }
  return render(request, 'adminpanel/editSubCategory.html', context)


def deleteSubCategory(request, slug):
  sub_category = Sub_Category.objects.get(slug=slug)
  cat_slug = sub_category.category.slug
  sub_category.delete()
  messages.success(request, 'Sub Category deleted successfully.')
  return redirect('subCategories', cat_slug)
 
 
def orders(request):
  orders = Order.objects.filter(is_ordered=True).order_by('-id')
  
  paginator = Paginator(orders, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = {
    'orders':page_obj,
  }
  return render(request, 'adminpanel/orders.html', context)


def update_order(request, id):
  if request.method == 'POST':
    order = get_object_or_404(Order, id=id)
    status = request.POST.get('status')
    order.status = status 
    order.save()
    if status  == "Delivered":
      try:
          payment = Payment.objects.get(payment_id = order.order_number, status = False)
          print(payment)
          if payment.payment_method == 'Cash On Delivery':
              payment.status = True
              payment.save()
      except:
          pass
    order.save()
    
  return redirect('orders')



def coupons(request):
  coupons = Coupon.objects.all()
  context = {
    'coupons':coupons,
  }
  return render(request, 'adminpanel/coupons.html', context)



def add_coupon(request):
  if request.method == 'POST':
    form = CouponForm(request.POST , request.FILES)
    if form.is_valid():
      form.save()
      messages.success(request,'Coupon Added successfully')
      return redirect('coupons')
    else:
      messages.error(request, 'Invalid input!!!')
      return redirect('add_coupon')
  form = CouponForm()
  context = {
    'form':form,
  }
  return render(request, 'adminpanel/addCoupon.html', context)







def sales_report(request):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    years = []
    today_date=str(date.today())
    start_date=today_date
    end_date=today_date

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        val = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = val+timedelta(days=1)
        orders = Order.objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
    else:
        orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
    
    year = today.year
    for i in range (3):
        val = year-i
        years.append(val)
    

    context = {
        'orders':orders,
        'today_date':today_date,
        'years':years,
        'start_date':start_date,
        'end_date':end_date,
    }
    

    return render(request, 'adminpanel/sales_report.html', context)

 
def sales_report_month(request,id):
    today = datetime.today()
    today_date = today.strftime("%Y-%m-%d")
    month = today.month
    year = today.strftime("%Y")
    one_week = datetime.today() - timedelta(days=7)
    order_count_in_month = Order.objects.filter(created_at__year = year,created_at__month=month, is_ordered=True).count() 
    orders = Order.objects.filter(created_at__month = id,payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
    today_date=str(date.today())
    returned = Order.objects.filter(created_at__month = id,is_returned = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).count() 
    cancelled = Order.objects.filter(status = "Cancelled").count()
    out_of_delivery = Order.objects.filter(status ="Out for delivery").count()
    delivered = Order.objects.filter(status = "Delivered").count()
    
    
    context = {
        'orders':orders,
        'order_count_in_month':order_count_in_month,
        'returned':returned,
        'cancelled':cancelled,
        'out_of_delivery':out_of_delivery,
        'delivered':delivered,
    }
    return render(request,'adminPanel/sales_report_table.html',context)
  

def sales_report_year(request,id):
    orders = Order.objects.filter(created_at__year = id,payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()    
    today_date=str(date.today())
    context = {
        'orders':orders,
        'today_date':today_date
    }
    return render(request,'adminPanel/sales_report_table.html',context) 

  
def pdf_report(request, start_date, end_date):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    
    if start_date == end_date:
      orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
    else:
      orders = Order .objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
    
    template_path = 'adminPanel/sales-report-pdf.html'
    context = {'orders': orders,}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=sales_report' + str(datetime.now()) +'.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
  
  
def excel_report(request, start_date, end_date):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    
    if start_date == end_date:
      orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = True).values_list('user_order_page__product__product_name', Sum('user_order_page__quantity'),'user_order_page__product__stock', Sum('order_total'))
    else:
      orders = Order.objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = True).values_list('user_order_page__product__product_name', Sum('user_order_page__quantity'),'user_order_page__product__stock', Sum('order_total'))
      
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=sales_report' + str(datetime.now()) +'.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales_report')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Item Name', 'Item sold', 'In stock', 'Amount Received']
    
    for col_num in range(len(columns)):
      ws.write(row_num, col_num, columns[col_num], font_style)
      
    font_style = xlwt.XFStyle()
    
    rows = orders
    
    for row in rows:
      row_num += 1

      for col_num in range(len(row)):
        ws.write(row_num, col_num, str(row[col_num]), font_style)
        
    wb.save(response)

    return response



def admindash(request):
    today = datetime.today()
    today_date = today.strftime("%Y-%m-%d")
    month = today.month
    year = today.strftime("%Y")
    one_week = datetime.today() - timedelta(days=7)
    order_count_in_month = Order.objects.filter(created_at__year = year,created_at__month=month, is_ordered=True).count() 
    order_count_in_day =Order.objects.filter(created_at__date = today, is_ordered=True).count()
    order_count_in_week = Order.objects.filter(created_at__gte = one_week, is_ordered=True).count()
    number_of_users  = Account.objects.filter(is_admin = False).count()
    paypal_orders = Payment.objects.filter(payment_method="PayPal",status = True).count()
    razorpay_orders = Payment.objects.filter(payment_method="RazerPay",status = True).count()
    cash_on_delivery_count = Payment.objects.filter(payment_method="Cash On Delivery",status = True).count()

    total_payment_count = paypal_orders + razorpay_orders + cash_on_delivery_count
    try:
        total_payment_amount = Payment.objects.filter(status = True).annotate(total_amount=Cast('amount_paid', FloatField())).aggregate(Sum('total_amount'))
        
    except:
        total_payment_amount=0
        
    if isinstance(total_payment_amount, dict) and 'total_amount__sum' in total_payment_amount:
      revenue = total_payment_amount['total_amount__sum']
      revenue = format(revenue, '.2f')
    
    else:
      revenue = 0
           
    blocked_user = Account.objects.filter(is_active = False,is_superadmin = False).count()
    unblocked_user = Account.objects.filter(is_active = True,is_superadmin = False).count()

    today_sale = Order.objects.filter(created_at__date = today_date,payment__status = True, is_ordered=True).count()
    today = today.strftime("%A")
    new_date = datetime.today() - timedelta(days = 1)
    yester_day_sale =   Order.objects.filter(created_at__date = new_date,payment__status = True, is_ordered=True).count()  
    yesterday = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_2 = Order.objects.filter(created_at__date = new_date,payment__status = True, is_ordered=True).count()
    day_2_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_3 = Order.objects.filter(created_at__date = new_date,payment__status = True, is_ordered=True).count()
    day_3_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_4 = Order.objects.filter(created_at__date = new_date,payment__status = True, is_ordered=True).count()
    day_4_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_5 = Order.objects.filter(created_at__date = new_date,payment__status = True, is_ordered=True).count()
    day_5_name = new_date.strftime("%A")
    #status
    ordered = Order.objects.filter(status = 'Order Confirmed', is_ordered=True).count()
    shipped = Order.objects.filter(status = "Shipped").count()
    out_of_delivery = Order.objects.filter(status ="Out for delivery").count()
    delivered = Order.objects.filter(status = "Delivered").count()
    returned = Order.objects.filter(status = "Returned").count()
    cancelled = Order.objects.filter(status = "Cancelled").count()

    context ={
        'order_count_in_month':order_count_in_month,
        'order_count_in_day':order_count_in_day,
        'order_count_in_week':order_count_in_week,
        'number_of_users':number_of_users,
        'paypal_orders':paypal_orders,
        'razorpay_orders':razorpay_orders,
        'total_payment_count':total_payment_count,
        'revenue':revenue,
        'ordered':ordered,
        'shipped':shipped,
        'out_of_delivery':out_of_delivery,
        'delivered':delivered,
        'returned':returned,
        'cancelled':cancelled,
        'cash_on_delivery_count':cash_on_delivery_count,
        'blocked_user':blocked_user,
        'unblocked_user':unblocked_user,
        'today_sale':today_sale,
        'yester_day_sale':yester_day_sale,
        'day_2':day_2,
        'day_3':day_3,
        'day_4':day_4,
        'day_5':day_5,
        'today':today,
        'yesterday':yesterday,
        'day_2_name':day_2_name,
        'day_3_name':day_3_name,
        'day_4_name':day_4_name,
        'day_5_name':day_5_name
        
    }
    return render(request, 'adminpanel/admindash.html', context)



def line_chart(request):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    years = []
    today_date=str(date.today())
    start_date=today_date
    end_date=today_date
    order_count_in_month = Order.objects.filter(created_at__year = year,created_at__month=month, is_ordered=True).count() 
    data = [1, 2, 3, 4, 5]  # replace with your own data

    context = {
        'data': json.dumps(data),
    }
    return render(request, 'adminpanel/line_chart.html', context)



    
    



  

