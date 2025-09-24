from django.shortcuts import render
from django.shortcuts import redirect
from .models import Product, Category, Cart, order, OrderItem
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.conf import settings
import random
import string



# Create your views here.
def home(request):
    categories = Category.objects.all()
    return render(request, 'store/index.html', {'categories': categories})   


def category_view(request, slug):
    if Category.objects.filter(slug=slug, status=True):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.get(slug=slug)
        return render(request, 'store/product.html', {'products': products, 'category': category})
    else:
        return render(request, 'store/product.html', {'message': 'No such category found'})

def product_view(request, cate_slug, prod_slug):
    if Category.objects.filter(slug=cate_slug, status=True):
        if Product.objects.filter(slug=prod_slug, status=True):
            product = Product.objects.get(slug=prod_slug)
            return render(request, 'store/view.html', {'product': product})
        else:
            return render(request, 'store/view.html', {'message': 'No such product found'})
    else:
        return render(request, 'store/view.html', {'message': 'No such category found'})
    


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'store/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'store/register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    return render(request, 'store/register.html')

def checkout_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.selling_price * item.product_qty for item in cart_items)
        
        if request.method == 'POST':
            payment_mode = request.POST.get('payment_mode')
            tracking_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            
            # Handle PayPal payment
            if payment_mode == 'PayPal':
                paypal_order_id = request.POST.get('paypal_order_id')
                paypal_payer_id = request.POST.get('paypal_payer_id')
                
                if paypal_order_id and paypal_payer_id:
                    # Create order with PayPal payment
                    new_order = order.objects.create(
                        user=request.user,
                        first_name=request.POST.get('first_name'),
                        last_name=request.POST.get('last_name'),
                        email=request.POST.get('email'),
                        phone=request.POST.get('phone'),
                        address=request.POST.get('address'),
                        city=request.POST.get('city'),
                        state=request.POST.get('state'),
                        country=request.POST.get('country'),
                        pincode=request.POST.get('pincode'),
                        total_price=total_price,
                        payment_mode=payment_mode,
                        payment_id=paypal_order_id,  # Store PayPal Order ID
                        tracking_no=tracking_no
                    )
                    
                    for item in cart_items:
                        OrderItem.objects.create(
                            order=new_order,
                            product=item.product,
                            price=item.product.selling_price,
                            quantity=item.product_qty
                        )
                    
                    cart_items.delete()
                    messages.success(request, f'PayPal payment successful! Order placed. Tracking No: {tracking_no}')
                    return redirect('home')
                else:
                    messages.error(request, 'PayPal payment details missing. Please try again.')
                    return redirect('checkout')
            
            else:
                # Handle COD payment
                new_order = order.objects.create(
                    user=request.user,
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    email=request.POST.get('email'),
                    phone=request.POST.get('phone'),
                    address=request.POST.get('address'),
                    city=request.POST.get('city'),
                    state=request.POST.get('state'),
                    country=request.POST.get('country'),
                    pincode=request.POST.get('pincode'),
                    total_price=total_price,
                    payment_mode='Cash on Delivery',
                    tracking_no=tracking_no
                )
                
                for item in cart_items:
                    OrderItem.objects.create(
                        order=new_order,
                        product=item.product,
                        price=item.product.selling_price,
                        quantity=item.product_qty
                    )
                
                cart_items.delete()
                messages.success(request, f'Order placed successfully! Tracking No: {tracking_no}')
                return redirect('home')
        
        # Convert INR to USD for PayPal (approximate rate)
        total_price_usd = total_price / 83  # 1 USD = ~83 INR
        
        # Get PayPal client ID from settings
        paypal_client_id = None
        if (hasattr(settings, 'PAYPAL_CLIENT_ID') and 
            settings.PAYPAL_CLIENT_ID != 'your_paypal_client_id_here'):
            paypal_client_id = settings.PAYPAL_CLIENT_ID
        
        return render(request, 'store/checkout.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'total_price_usd': total_price_usd,
            'paypal_client_id': paypal_client_id
        })
    else:
        return redirect('login')

def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                if Cart.objects.filter(user=request.user, product_id=prod_id):
                    messages.info(request, 'Product already in cart')
                    return redirect('cart')
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        messages.success(request, 'Product added successfully!')
                        return redirect('cart')
                    else:
                        messages.warning(request, 'Only ' + str(product_check.quantity) + ' quantity available')
                        return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect('login')
    return redirect('/')

def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.selling_price * item.product_qty for item in cart_items)
        return render(request, 'store/cart.html', {
            'cart_items': cart_items,
            'total_price': total_price
        })
    else:
        return redirect('login')

def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart_item = Cart.objects.get(id=item_id, user=request.user)
        cart_item.delete()
        messages.success(request, 'Item removed from cart')
        return redirect('cart')
    else:
        return redirect('login')

def update_cart_quantity(request):
    if request.method == 'POST' and request.user.is_authenticated:
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))
        cart_item = Cart.objects.get(id=item_id, user=request.user)
        cart_item.product_qty = quantity
        cart_item.save()
        messages.success(request, 'Quantity updated')
        return redirect('cart')
    else:
        return redirect('login')


def checkout(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You need to be logged in to add items to the cart.')
            return redirect('login')
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty', 1))
        product = Product.objects.get(id=product_id)
        if product and product_qty > 0:
            from .models import Cart
            cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
            if not created:
                cart_item.product_qty += product_qty
            else:
                cart_item.product_qty = product_qty
            cart_item.save()
            messages.success(request, 'Product added to cart successfully!')
        else:
            messages.error(request, 'Invalid product or quantity.')

        


    return render(request, 'store/cart.html')

def about_view(request):
    return render(request, 'store/about.html')

def contact_view(request):
    return render(request, 'store/contact.html')

def track_order_view(request):
    order_obj = None
    tracking_no = None
    
    if request.method == 'POST':
        tracking_no = request.POST.get('tracking_no')
        try:
            order_obj = order.objects.get(tracking_no=tracking_no)
        except order.DoesNotExist:
            order_obj = None
    
    return render(request, 'store/track_order.html', {
        'order': order_obj,
        'tracking_no': tracking_no
    })