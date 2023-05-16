from django.shortcuts import render,redirect,HttpResponse
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import MyAccountManager,Account
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm,EditProfileForm,AddressForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from twilio.rest import Client
import random
import pyotp
from django.conf import settings
from orders.models import Address

# Create your views here.

def register(request):
  if 'email' in request.session :
                return render(request, "main/home.html")
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data['password']
           
      user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
      
      user.save()

      if user.is_active:
        messages.success(request, 'Phone verified')
        return redirect('login')
      else:
            totp = pyotp.TOTP(settings.OTP_SECRET)
            otp = totp.now()
            msg_html = render_to_string(
                'accounts/email.html', {'otp': otp})

            send_mail(f'Please verify your E-mail', f'Your One-Time Verification Password is {otp}', settings.EMAIL_HOST_USER, [
                email], html_message=msg_html, fail_silently=False)

            request.session['otp'] = otp
            request.session['email'] = email
            return redirect('verify_otp')
  else:    
    form = RegistrationForm()
  context = {
    'form': form
  }
  
  return render (request, 'accounts/register.html', context)



def userLogin(request):
    if 'email' in request.session :
                return render(request, "main/home.html")
    if  request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        print({'user':user})
        if user is not None:
            
            login(request, user)
            request.session['email'] = email          
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login')
    else:
      
        
        return render(request, 'accounts/login.html')
    


def user(request):

    context = {}
    if request.user.is_authenticated:
        context['user'] = request.user
    return render( request,'accounts/user.html',context)  


def userLogout(request):
  auth.logout(request)
  return redirect('login')



def editProfile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = UserForm(request.POST, request.FILES, instance=request.user)  # request.FILES is show the selected image or file

        if form.is_valid() :
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return render(request,'accounts/user.html')
        
        else:
            return redirect('editProfile')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = UserForm(instance=request.user)
        args = {}
        # args.update(csrf(request))
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'accounts/useredit.html', args)



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
    
            return render(request,'accounts/user.html')
   
 
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/changepswd.html', {
        'form': form
    })

def useredit(request):
   return render(request,'accounts/useredit.html')



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = Account.objects.filter(Q(email=data))
                        
			if associated_users.exists():
                               
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                                     
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'pdjango55@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ('resetdone')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="accounts/password_reset.html", context={"password_reset_form":password_reset_form})
def resetdone(request):
    return render(request,'accounts/resetdone.html')



def home(request):


        return render(request,'main/home.html')


def edituser(request):

    return render(request,'accounts/useredit.html')



def send_otp(request, phone_number):


    TWILIO_AUTH_TOKEN = '7b42f350986d72fc85ddc0b7fa425b5b'
    TWILIO_ACCOUNT_SID = 'ACdc1055926dd49c11314f4c1ea70f3453'
    TWILIO_PHONE_NUMBER = '+16203748524'
    otp = random.randint(1000, 9999)
    request.session['otp'] = otp
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=('+91{}'.format(phone_number))
    )
    print(message)


# def resend_otp(request, phone_number):
#     TWILIO_AUTH_TOKEN = '7b42f350986d72fc85ddc0b7fa425b5b'
#     TWILIO_ACCOUNT_SID = 'ACdc1055926dd49c11314f4c1ea70f3453'
#     TWILIO_PHONE_NUMBER = '+16203748524'
#     phone_number = request.session['phone_number']
#     otp = random.randint(1000, 9999)
#     request.session['otp'] = otp
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     message = client.messages.create(
#         body=f"Your OTP is {otp}",
#         from_=TWILIO_PHONE_NUMBER,
#         to=('+91{}'.format(phone_number))
#     )
#     return redirect('verify-otp')


def verify_otp(request):
    # if 'otp' not in request.session:
    #     return redirect('home')

    # if request.user.is_authenticated:
    #     return redirect('profile')

    error = ''
    if request.method == 'POST':
        otp = request.session['otp']
        print(f'otp is{otp}')
        user_otp = request.POST['otp']

        if user_otp != '':
            email = request.session['email']

            if 'otp' in request.session and int(user_otp) == int(request.session['otp']):
                print(f'user otp is{user_otp}')

                user = Account.objects.get(email=email)
                user.is_active = True
                user.save()
                del request.session['otp']
                del request.session['email']
                messages.success(
                    request, 'Email, please login to continue')
                return redirect('login')
            else:
                return render(request, 'accounts/otp.html', {'error': 'Invalid OTP'})
    return render(request, 'accounts/otp.html', {'error': error})


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
            return redirect('address')
        else:
            messages.success(request,'Form is Not valid')
            return redirect('address')
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
      return redirect('address')
    else:
      messages.error(request , 'Invalid Inputs!!!')
      return redirect('address')
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
    return redirect('address')

def address(request):
    address = Address.objects.filter(user = request.user)
    context = {
    'address':address,

  }
    return render(request,'accounts/address.html',context)


