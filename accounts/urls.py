from django.contrib import admin
from django.urls import path
from .views import userLogin,register,user,userLogout,address,add_address,change_password,useredit,password_reset_request,home,edituser,editProfile,verify_otp,resetdone

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', userLogin, name='login'),
    path('register/', register, name='register'),


    path('accounts/user/',user, name='user'),
    path("logout/", userLogout, name='logout'),
    path("editProfile/", editProfile, name='editProfile'),
    path("useredit/", useredit, name='useredit'),
    path("passwordReset/", password_reset_request, name="password_reset"),
     path("changePassword/",change_password, name='change_password'),
     path("edituser/",edituser, name='edituser'),
     path('verifyOtp/',verify_otp, name='verify_otp'),
    path('resetdone/',resetdone, name='resetdone'),

    path('add_address/', add_address, name='add_address'),
    path('address/', address, name='address'),
    



]
