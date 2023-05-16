from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import admindash,users,block_user,pdf_report,excel_report,line_chart,sales_report_year,sales_report_month,sales_report,update_order,add_coupon,coupons,add_product_offer,orders,delete_product_offer,product_offers,unblock_user,editProduct,edit_product_variation,delete_product_variation,add_product_variation,product_variations,deleteProduct,addProduct,sub_category,addCategory,addSubCategory,categories,addSubCategory,subCategories,editCategory,editSubCategory,adminlogin,deleteSubCategory,deleteCategory,products

urlpatterns = [
    path('adminlogin/', adminlogin, name='adminlogin'),
    path('admindash/', admindash, name='admindash'),

    path('line_chart/', line_chart, name='line_chart'),


    path('users', users, name='users'),
    # path('blockUser/<int:id>/',blockUser, name='blockUser'),
    path('blockuser/<int:id>/',block_user,name='blockuser'),
    path('unblockuser/<int:id>/',unblock_user,name='unblockuser'),


    path('products/', products, name='products'),
    path('addProduct/',addProduct, name='addProduct'),
    path('<int:id>/editProduct/', editProduct, name='editProduct'),
    path('<int:id>/deleteProduct/', deleteProduct, name='deleteProduct'),


    path('products/productVariations/', product_variations, name='product_variations'),
    path('products/product_variations/add_product_variation/', add_product_variation, name='add_product_variation'),
    path('products/product_variations/<int:id>/edit_variation', edit_product_variation, name='edit_product_variation'),
    path('products/product_variations/<int:id>/delete_variation', delete_product_variation, name='delete_product_variation'),
   

    path('categories/',categories, name='categories'),
    path('addCategory/',addCategory, name='addCategory'),
    path('editCategory/',editCategory, name='editCategory'),
    path('<str:slug>/editCategory/', editCategory, name='editCategory'),
    path('<str:slug>/deleteCategory/', deleteCategory, name='deleteCategory'),



    path('sub_category/',sub_category, name='sub_category'),
    path('<str:category_slug>/addSubCategory/', addSubCategory, name='addSubCategory'),
    path('addSubCategory/',addSubCategory, name='addSubCategory'),
    path('<str:slug>/editSubCategory/', editSubCategory, name='editSubCategory'),
    path('<str:slug>/deleteSubCategory/', deleteSubCategory, name='deleteSubCategory'),
    path('<str:category_slug>/subCategories/', subCategories, name='subCategories'),
    
  path('product_offers/',product_offers, name='product_offers'),
  path('add_product_offer/', add_product_offer, name='add_product_offer'),
  path('delete_product_offer/<int:id>/',delete_product_offer, name='delete_product_offer'),

    path('orders/', orders, name='orders'),
  path('update_order/<int:id>',update_order,name="update_order"),
    path('coupon_offers/',coupons,name="coupons"),
  path('add_coupon_offers/',add_coupon,name="add_coupon"),



  path('sales_report/',sales_report,name="sales_report"),
  path('sales_report_month/<int:id>',sales_report_month,name="sales_report_month"),
  path("sales_report_year/<int:id>",sales_report_year,name='sales_report_year'),
    
  path('pdf_report/<str:start_date>//<str:end_date>/', pdf_report, name='pdf_report'),  
  path('excel_report/<str:start_date>//<str:end_date>/', excel_report, name='excel_report')
      
   
    # path('addSubCategory',addSubCategory, name='addSubCategory'),
      

       
      
      


     

    

    
    

    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)