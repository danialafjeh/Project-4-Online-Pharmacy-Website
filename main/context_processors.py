from cart.cart import Cart

def cart(request):
    return {'shopping_cart':Cart(request)}