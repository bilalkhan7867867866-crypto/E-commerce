from django.shortcuts import render,redirect
import uuid
from .models import Order,OrderItem,Payment
from cart.models import Cart,CartItem
from django.contrib.auth.decorators import login_required
import razorpay
from .forms import ShippingAddressForm  
from django.conf import settings

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    total = sum(item.total_price()
                for item in items)
    
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = request.user
            shipping.save()
    
            order = Order.objects.create(user=request.user,
                                 order_number = str(uuid.uuid4())[:10],
                                 total_amount = total,)
            
            client = razorpay.Client(auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET,
            ))

            razorpay_order = client.order.create({
                "amount":int(total*100),
                "currency":"INR",
                "payment_capture":1,    
            })

            Payment.objects.create(
                order = order,
                razorpay_order_id = razorpay_order['id'],
                amount = total,
            )
            return render(request,'orders/payment.html',{
                'order':order,
                'razorpay_order':razorpay_order,
                'total':total,
                'razorpay_key_id':settings.RAZORPAY_KEY_ID
            })
    else:
        form = ShippingAddressForm()
    return render(request,'orders/checkout.html',{
        'form':form,
        'items':items,
        'total':total,
    })


@login_required
def order_success(request):
    return render(request,'orders/order_success.html')

@login_required
def payment_success(request):
    payment_id = request.GET.get(
        'payment_id'
    )
    payment = Payment.objects.filter(
        razorpay_payment_id=""
    ).last()
    payment.razorpay_payment_id = (
        payment_id
    )
    payment.status = "Success"
    payment.save()
    return render(
        request,
        "orders/success.html"
    )

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders
        }
    )