
#Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.http import Http404
import razorpay
from home.models import Product
from .models import Cart, CartItem, Order



from home.models import Product
from .models import Cart, CartItem, Order

# helper to fetch/create session cart id
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def migrate_cart_session_to_user(request):
    session_cart_id=_cart_id(request)
    if request.user.is_authenticated:
        try:
            session_cart=Cart.objects.get(cart_id=session_cart_id)
            user_cart,created=Cart.objects.get_or_create(user=request.user)
            for item in CartItem.objects.filter(cart=session_cart):
                item.cart=user_cart
                item.save()
            session_cart.delete()
        except Cart.DoesNotExist:
            pass




def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    # Select cart (user or session)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = _cart_id(request)
        cart, created = Cart.objects.get_or_create(cart_id=cart_id)

    # Add product to cart
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )

    return redirect('cart:cart_detail')   # 👈 ALWAYS RETURN




def cart_detail(request, total=0, counter=0, cart_items=None):

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = _cart_id(request)
        cart, created = Cart.objects.get_or_create(cart_id=cart_id)

    # Get all items in cart
    cart_items = CartItem.objects.filter(cart=cart, active=True)

    # Calculate totals
    for item in cart_items:
        total += item.product.price * item.quantity
        counter += item.quantity

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter
    })



def cart_remove(request, product_id):
        if request.user.is_authenticated:
           cart,created=Cart.objects.get_or_create(user=request.user)
        else:
           cart,created=Cart.objects.get_or_create(cart_id=_cart_id(request))
           cart=Cart.object.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item=CartItem.objects.get(product=product,cart=cart)
     
        if cart_item.quantity > 1:
           cart_item.quantity -= 1
           cart_item.save()
        else:
             cart_item.delete()
        return redirect('cart:cart_detail')


def full_remove(request, product_id):
        if request.user.is_authenticated:
           cart,created=Cart.objects.get_or_create(user=request.user)
        else:
           cart,created=Cart.objects.get_or_create(cart_id=_cart_id(request))


        #cart=Cart.object.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item=CartItem.objects.get(product=product,cart=cart)
        cart_item.delete()
        return redirect('cart:cart_detail')



def start_payment(request):
    if request.method =="POSt":
        amount=int(request.POST.get("amount"))*100
        client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZOR_KEY_SECRETE))
        payment=client.order.create({
            "amount":amount,
            "currency":"INR",
            "payment_capture":"1"
        })
        order=order.objects.create(
            user=request.user,
            amount=amount/100,
            razorpay_order_id=payment['id']

        )
        context={
            "order":order,
            "payment":payment,
            "razorpay_key_id":settings.RAZORPAY_KEY_ID
        }
        return render(request,"payment.html",context)
    return render(request,"start_payment.html")


def payment_success(request):
    if request.method =="POST":
        data=request.POST
        order_id=data.get("razorpay_order_id")
        payment_id=data.get("razorpay_payment_id")
        signature=data.get("razorpay_signature")

        order=Order.objects.get(razorpay_order_id=order_id)
        order.razorpay_payment_id=payment_id
        order.razorpay_signature=signature
        order.is_paid=True
        order.save()
        return render(request,"success.html",{"order":order})
    return redirect("/")


# def checkout(request):
#     user=request.user
#     if not user.is_authenticated:
#         return redirect.user
#     cart_items=Cart.objects.filter(user=user)
  
   
#     total=sum(item.sub_price()for item in cart_item)
#     amount_paise=int(total * 100)
    
#     client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
#     payment = client.order.create({
#         'amount': amount_paise,
#         'currency': 'INR',
#         'payment_capture': '1'
#     })
 
#     order=Order.objects.create(
#        user=user, # type: ignore
#        total_amount=total, # type: ignore
#        razorpay_order_id=razorpay.Payment['id']

#      )
#     context={
#         'cart_items':cart_items,
#         'total':total,
#         'payment':payment,
#         'order':order,
#         'razorpay_key':settings.RAZORPAY_KEY_ID}
#     return render('request,payment.html',context)



def checkout(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('home:allprodcat')  # redirect to login if user is not authenticated

    # Get cart items
    cart_items = CartItem.objects.filter(user=user,active=True)

    if not cart_items.exists():
        return redirect('home:allprodcat')  # redirect if cart is empty

    # Calculate total
    total = sum(item.sub_total() for item in cart_items)
    amount_paise = int(total * 100)

    # Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'payment_capture': '1'
    })

    # Create order
    order = Order.objects.create(
        user=user,
        total_amount=total,
        razorpay_order_id=payment['id']
    )

    context = {
        'cart_items': cart_items,
        'total': total,
        'payment': payment,
        'order': order,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    }

    return render(request, 'payment.html', context)




def payment_success(request):
    order_id=request.GET.get('order.id')
    payment_id=request.GET.get('payment_id')
    signature=request.GET.get('signature')

    order=Order.objects.get(id=order_id)
    order.razorpay_payment_id=payment_id
    order.razorpay_signature=signature
    order.paid=True
    order.save()


    Cart.objects.filter(user=order.user).delete()
    return render(request,'success.html', {'order':order})





    

