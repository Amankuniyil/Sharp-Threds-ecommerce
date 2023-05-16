from django import forms
from django.forms import ModelForm
from .models import Account
from orders.models import Address
# from orders.models import Address



class RegistrationForm(forms.ModelForm):
  
  password = forms.CharField(widget=forms.PasswordInput)
  confirm_password = forms.CharField(widget=forms.PasswordInput)
                                                                
    
  class Meta:
    model = Account
    fields = ['first_name', 'last_name', 'email', 'phone_number']
    
  def init(self, *args, **kwargs):
    super(RegistrationForm,self).init(*args, **kwargs)
    # self.fields['first_name'].widget.attrs['placeholder'] = ' First Name'
    # self.fields['first_name'].widget.attrs['style'] = 'background: #171717; border:0;box-shadow: none;text-align:left;:focus:border:'
    # self.fields['last_name'].widget.attrs['placeholder'] = ' Last Name'
    # self.fields['last_name'].widget.attrs['style'] = 'background: #171717; border:0;'
    # self.fields['email'].widget.attrs['placeholder'] = ' Email Address'
    # self.fields['email'].widget.attrs['style'] = 'background: #171717; border:0;'
    # self.fields['phone_number'].widget.attrs['placeholder'] = ' Mobile Number'
    # self.fields['phone_number'].widget.attrs['style'] = 'background: #171717; border:0;'
    # self.fields['phone_number'].widget.attrs['maxlength'] = 10

    for field  in self.fields:
      self.fields[field].widget.attrs['class'] = 'form-control'
  
  def clean(self):
    cleaned_data = super(RegistrationForm, self).clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')
    
    if password != confirm_password:
      raise forms.ValidationError("Password does not match!!")
    
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields  = ['first_name','last_name', 'email', 'phone_number',]

    def init(self, *args, **kwargs):
        super(UserForm,self).init(*args, **kwargs)  
        for field  in self.fields:
             self.fields[field].widget.attrs['class'] = 'form-control'
             
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields=['first_name','last_name','phone','email','address_line1','address_line2','district','state','city', 'pincode']
    
    def init(self, *args, **kwargs):
      super(AddressForm,self).init(*args, **kwargs)  
      for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields  = ['first_name','last_name', 'email', 'phone_number',]

    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)  
        for field  in self.fields:
             self.fields[field].widget.attrs['class'] = 'form-control'


class EditProfileForm(ModelForm):
         class Meta:
          model = Account
          fields = (
                 'first_name','last_name', 'email', 'phone_number',
                )
# class ProfileForm(ModelForm):
#          class Meta:
#            model = Account 
#            fields = ('first_name', 'last_name', 'phone_number') #Note that we didn't mention user field here.