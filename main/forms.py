from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from .models import CustomerDeliveryInfo
from django import forms

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="نام ",
        max_length=50,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control text-right', 'name':'first_name', 'placeholder':'نام'})
    )
    last_name = forms.CharField(
        label="نام خانوادگی ",
        max_length=50,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control text-right', 'name':'last_name', 'placeholder':'نام خانوادگی'})
    )
    email = forms.EmailField(
        label="ایمیل ",
        widget=forms.TextInput(attrs={'type':'email', 'class':'form-control text-right', 'name':'email', 'placeholder':'آدرس ایمیل'})
    )
    username = forms.CharField(
        label="نام کاربری ",
        max_length=20,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control text-right', 'name':'username', 'placeholder':'نام کاربری',  'autofocus': False})
    )
    password1 = forms.CharField(
        label="رمز عبور بالای 8 کاراکتر خود را وارد کنید ",
        widget=forms.PasswordInput(
        attrs={
            'class':'form-control text-right',
            'name':'password',
            'type':'password',
            'placeholder': 'رمز عبور بالای 8 کاراکتر'
        }
        )
    )
    password2 = forms.CharField(
        label="رمز عبور خود را دوباره وارد کنید ",
        widget=forms.PasswordInput(
        attrs={
            'class':'form-control text-right',
            'name':'password',
            'type':'password',
            'placeholder': 'تکرار رمز عبور'
        }
        )
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        )

class UpdateUserForm(UserChangeForm):
    password = None

    first_name = forms.CharField(
        label="نام ",
        max_length=50,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control text-right', 'name':'first_name', 'placeholder':'نام'})
    )
    last_name = forms.CharField(
        label="نام خانوادگی ",
        max_length=50,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control text-right', 'name':'last_name', 'placeholder':'نام خانوادگی'})
    )
    username = forms.CharField(
        label="نام کاربری ",
        max_length=20,
        widget=forms.TextInput(attrs={'type':'text', 'class':'form-control text-right', 'name':'username', 'placeholder':'نام کاربری', 'autofocus': False})
    )
    email = forms.EmailField(
        label="ایمیل ",
        widget=forms.TextInput(attrs={'type':'email', 'class':'form-control text-right', 'name':'email', 'placeholder':'آدرس ایمیل'})
    )

    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')

class UpdatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="رمز عبور جدید خود را وارد کنید",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control text-right',
                'name':'password',
                'type':'password',
                 'placeholder': 'رمز عبور جدید بالای 8 کاراکتر'
            }
        )
    )
    new_password2 = forms.CharField(
        label=" رمز عبور جدید خود را دوباره وارد کنید ",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control text-right',
                'name':'password',
                'type':'password',
                'placeholder': 'تکرار رمز عبور جدید'
            }
        )
    )

    class Meta:
        model = User
        fields = ('new_password1','new_password2')

class DeliveryInfoForm(forms.ModelForm):
    full_name = forms.CharField(
        label="به نام ",
        widget=forms.TextInput(attrs={'class':'form-control text-right', 'type':'text',  'placeholder': 'سفارش به نام'}),
        required=True

    )
    phone = forms.CharField(
        label="شماره تماس ",
        widget=forms.TextInput(attrs={'class':'form-control text-right', 'type':'text', 'placeholder':'شماره تماس'}),
        required=True

    )
    address = forms.CharField(
        label="آدرس ",
        widget=forms.TextInput(attrs={'class':'form-control text-right', 'type':'textarea', 'placeholder':'آدرس'}),
        required=True

    )
    city = forms.CharField(
        label="شهر ",
        widget=forms.TextInput(attrs={'class':'form-control text-right', 'type':'text', 'placeholder':'شهر'}),
        required=False

    )
    province = forms.CharField(
        label="استان ",
        widget=forms.TextInput(attrs={'class':'form-control text-right', 'type':'text', 'placeholder':'استان'}),
        required=False

    )
    zip_code = forms.CharField(
        label="کد پستی ",
        widget=forms.TextInput(attrs={'class':'form-control text-right', 'type':'text', 'placeholder':'کد پستی'}),
        required=True

    )

    class Meta:
        model = CustomerDeliveryInfo
        fields = (
            'full_name',
            'phone',
            'province',
            'city',
            'address',
            'zip_code'
        ) 