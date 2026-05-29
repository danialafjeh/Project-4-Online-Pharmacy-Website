from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product, CustomerDeliveryInfo
from .cart import Cart 
from django.contrib import messages

# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total_price = cart.get_total()
    info = {
        'products':cart_products, 
        'quantities':quantities, 
        'total_price':total_price
    }
    return render(request, 'cart_summary.html', info) 

def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = int(request.POST['product_id'])
        product_qty = int(request.POST['product_qty'])
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        messages.success(request, ("به سبد خرید شما با موفقیت اضافه شد"))
        return redirect('cart_summary')
    else:
        return redirect('home')
    
def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = int(request.POST['product_id'])
        cart.delete(product=product_id)
        messages.success(request, ("از سبد خرید شما با موفقیت حذف شد"))
        return redirect('cart_summary')
    else:
        return redirect('home')
    
def cart_finalcheck(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total_price = cart.get_total()
        user_delivery_info = CustomerDeliveryInfo.objects.get(user__id=request.user.id)

        required_fields = [
            user_delivery_info.full_name,
            user_delivery_info.phone,
            user_delivery_info.address,
            user_delivery_info.city,
            user_delivery_info.province,
            user_delivery_info.zip_code,
        ]

        if any(field in [None, "", " "] for field in required_fields):
            messages.error(request, ('ابتدا باید مشخصات ارسال سفارش خود را در حساب کاربری تان ثبت کنید'))
            return redirect('profile_mainpage')

        info = {
            'products':cart_products,
            'quantities':quantities, 
            'total_price':total_price, 
            'deliveryinfo':user_delivery_info
        }

        return render(request, 'cart_finalcheck.html', info)
    else:
        messages.error(request, ('ابتدا باید وارد حساب کاربری خود شوید'))
        return redirect('login_customer')
