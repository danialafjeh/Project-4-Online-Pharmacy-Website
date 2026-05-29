from django.shortcuts import render, redirect
from .models import Product, PharmacyInfo, Category, Brand, CustomerDeliveryInfo
from django.contrib import messages
from django.db.models import Q
from .forms import SignUpForm , UpdateUserForm, UpdatePasswordForm, DeliveryInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from cart.cart import Cart
import json

# Create your views here.

def home(request):
    sale_products = Product.objects.filter(is_sale=True)
    info = {'sale_prods':sale_products}
    return render(request, 'home.html', info)
    
def aboutus(request):
    about_pharmacy = PharmacyInfo.objects.get(id=1)
    info = {'information':about_pharmacy}
    return render(request, 'aboutus.html', info)

def active_sales(request):
    sale_products = Product.objects.filter(is_sale=True)
    info = {'all_sales':sale_products}
    return render(request, 'activesales.html', info)

def all_products(request):
    all_prods = Product.objects.all()
    info = {'all_prods':all_prods}
    return render(request, 'allproducts.html', info)

def category_page(request):
    all_cats = Category.objects.all()
    default_prods = Product.objects.filter(category__id=1)
    info = {
        'categories':all_cats , 
        'default_products':default_prods
    }
    return render(request, 'category.html', info)

def category_selection(request, cat):
    catname = cat.replace("-"," ")
    selected_cat = Category.objects.get(name=catname)
    products = Product.objects.filter(category=selected_cat)
    all_cats = Category.objects.all()
    info = {
        'selected_category':selected_cat , 
        'cat_products':products ,
        'categories':all_cats
    }
    return render(request, 'categoryselection.html', info)

def brands_page(request):
    all_brands = Brand.objects.all()
    default_prods = Product.objects.filter(brand__id=1)
    info = {
        'brands':all_brands ,
        'default_products':default_prods
    }
    return render(request, 'brands.html', info)

def brands_selection(request, brand):
    brandname = brand.replace("-"," ")
    selected_brand = Brand.objects.get(name=brandname)
    products = Product.objects.filter(brand=selected_brand)
    all_brands = Brand.objects.all()
    info = {
        'selected_brand':selected_brand ,
        'brand_products':products ,
        'brands':all_brands
    }
    return render(request, 'brandselection.html', info)

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(brand__name__icontains=searched))
        if not searched:
            messages.error(request, ('محصولی با این نام یافت نشد'))
            return redirect('search_products')
        else:
            messages.success(request, ('نتیجه جستجوی شما در حال نمایش است'))
            return render(request, 'search_products.html', {'searched':searched})
    else:
        return render(request, 'search_products.html')
    
#All different types of errors for Signup / Login forms :    
TRANSLATE_ERRORS = {
    "This field is required.": "این فیلد ضروری است.",
    "A user with that username already exists.": "این نام کاربری قبلاً ثبت شده است.",
    "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.":
        "نام کاربری نامعتبر است. فقط حروف، اعداد و کاراکترهای @ . + - _ مجاز هستند.",
    "The two password fields didn’t match.": "رمز عبور و تکرار آن یکسان نیستند.",
    "This password is too short. It must contain at least 8 characters.":
        "رمز عبور خیلی کوتاه است. باید حداقل ۸ کاراکتر باشد.",
    "This password is too common.": "این رمز عبور خیلی معمولی و قابل حدس است.",
    "This password is entirely numeric.": "رمز عبور نباید فقط از اعداد تشکیل شده باشد.",
    "The password is too similar to the username.":
        "رمز عبور بیش از حد شبیه نام کاربری است.",
    "The password is too similar to your first name.":
        "رمز عبور بیش از حد شبیه نام کوچک شماست.",
    "The password is too similar to your last name.":
        "رمز عبور بیش از حد شبیه نام خانوادگی شماست.",
    "The password is too similar to your email address.":
        "رمز عبور بیش از حد شبیه ایمیل شماست.",
    "Enter a valid value.": "مقدار وارد شده معتبر نیست.",
}

def signup_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            messages.success(request,("حساب کاربری شما با موفقیت ساخته شد"))
            return redirect('home')
        else:
            for field, errors in form.errors.items():
               for error in errors:
                  fa_error = TRANSLATE_ERRORS.get(error, error)
                  messages.error(request, fa_error)

               return redirect('signup_user')
    else:
        return render(request, 'signup.html',{'form':form})
    
def login_mainpage(request):
    #For choosing one of the two ways : 1. Customers login or 2. Admins login
    return render(request, 'login_mainpage.html')

def login_customer(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_staff:
                login(request, user)
                current_user = CustomerDeliveryInfo.objects.get(user__id = request.user.id)
                saved_cart = current_user.shopping_cart
                if saved_cart:
                   converted_cart = json.loads(saved_cart)
                   cart = Cart(request)

                   for k,v in converted_cart.items():
                       cart.db_add(product=k , quantity=v)
            
                messages.success(request,('با موفقیت وارد حساب کاربری خود شدید'))
                return redirect('home')
            else:
                messages.error(request, ('حساب مورد نظر حساب مدیریتی است ! لطفا از بخش ورود ویژه مدیران وارد شوید'))
                return redirect('login_mainpage')
        else:
            messages.error(request, ('نام کاربری یا رمز عبور اشتباه است.'))
            return redirect('login_customer')
    else:
        return render(request, 'login_customer.html')

def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                current_user = CustomerDeliveryInfo.objects.get(user__id = request.user.id)
                saved_cart = current_user.shopping_cart
                if saved_cart:
                   converted_cart = json.loads(saved_cart)
                   cart = Cart(request)

                   for k,v in converted_cart.items():
                       cart.db_add(product=k , quantity=v)
            
                messages.success(request,('با موفقیت وارد حساب مدیریتی خود شدید'))
                return redirect('home')
            else:
                messages.error(request, ('شما دسترسی به پنل مدیریت ندارید. لطفا از بخش ورود ویژه مشتریان وارد شوید.'))
                return redirect('login_mainpage')
        else:
            messages.error(request, ('نام کاربری یا رمز عبور اشتباه است.'))
            return redirect('login_admin')
    else:
        return render(request, 'login_admin.html')
    
def logout_account(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, ('با موفقیت از حساب خود خارج شدید'))
        return redirect('home')
    else:
        messages.error(request, ('ابتدا باید وارد حساب کاربری خود شوید'))
        return redirect('home')

def profile_mainpage(request):
    if request.user.is_authenticated:
        #Sending user's account info from backend to frontend is by context processor.
        return render(request, 'profile_mainpage.html')
    else:
        messages.error(request, ('ابتدا باید وارد حساب کاربری خود شوید'))
        return redirect('home')

def account_info(request):
    if request.user.is_authenticated: 
        #Sending user's account info from backend to frontend is by context processor.
        return render(request, 'account_info.html')
    else:
        messages.error(request, ('ابتدا باید وارد حساب کاربری خود شوید'))
        return redirect('home')
    
def update_account_info(request):
    if request.user.is_authenticated:
       current_user = User.objects.get(id=request.user.id)
       form = UpdateUserForm(instance = current_user)
       if request.method == 'POST':
           form = UpdateUserForm(request.POST, instance = current_user)
           if form.is_valid():
               form.save()
               
               messages.success(request, ('اطلاعات حساب شما با موفقیت ویرایش شد'))
               return redirect('acc_info')
           else:
               messages.error(request,("مشکلی در ویرایش اطلاعات وجود داشت"))
               return redirect('update_acc_info')
       else:
           return render(request, 'update_account_info.html', {'form':form})
    else:
        messages.error(request,('ابتدا باید وارد حساب کاربری خود شوید'))
        return redirect('home')
    
def update_account_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        form_pass = UpdatePasswordForm(current_user)
        if request.method =='POST':
            form_pass = UpdatePasswordForm(current_user, request.POST)
            if form_pass.is_valid():
                form_pass.save()
                messages.success(request,('رمز عبور حساب شما با موفقیت ویرایش شد'))
                login(request, current_user)
                return redirect('acc_info')
            else:
                for field, errors in form_pass.errors.items():
                   for error in errors:
                      fa_error = TRANSLATE_ERRORS.get(error, error)
                      messages.error(request, fa_error)

                   return redirect('update_acc_password')
        else:
            return render(request,'update_account_password.html',{'form':form_pass})
    else:
        messages.error(request,('ابتدا باید وارد حساب کاربری خود شوید'))
        return redirect('home')
    
def add_deliveryinfo(request):
    if request.user.is_authenticated:
        current_user = CustomerDeliveryInfo.objects.get(user__id=request.user.id)
        form_delivery = DeliveryInfoForm(instance=current_user)
        if request.method == 'POST':
            form_delivery = DeliveryInfoForm(request.POST, instance=current_user)
            if form_delivery.is_valid():
                form_delivery.save()
                messages.success(request, ('مشخصات ارسال سفارش برای حساب شما با موفقیت ثبت شد'))
                return redirect('show_deliveryinfo')
            else:
                messages.error(request,("مشکلی در ثبت اطلاعات وجود داشت"))
                return redirect('add_deliveryinfo')
        else:
            return render(request, 'add_deliveryinfo.html', {'form':form_delivery})
    else:
        messages.error(request,('ابتدا باید وارد حساب کاربری خود شوید'))
        return redirect('home')

def show_deliveryinfo(request):
    if request.user.is_authenticated:
        customer_deliveryinfo = CustomerDeliveryInfo.objects.get(user__id=request.user.id)
        info = {'deliveryinfo':customer_deliveryinfo}
        return render(request, 'show_deliveryinfo.html', info)
    else:
        messages.error(request,('ابتدا باید وارد حساب کاربری خود شوید'))
        return redirect('home')

def product_details(request,pk):
    product = Product.objects.get(id=pk)
    suggested_products = Product.objects.all().exclude(id=product.id)
    info = {
        'product':product ,
        'suggested_prods':suggested_products
    }
    return render(request, 'product_details.html', info)

    

         

