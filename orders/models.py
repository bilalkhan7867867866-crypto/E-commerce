from django.db import models
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50,unique=True)
    total_amount = models.DecimalField(max_digits=12,decimal_places=2)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number
    
from products.models import Product
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12,decimal_places=2)

    def subtotal(self):
        return self.quantity*self.price
    
class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
class Payment(models.Model):
    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed')
    ]
    order = models.OneToOneField(Order,on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_payment_id = models.CharField(max_length=255,blank=True,null=True)
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default='Success')

    created_at = models.DateTimeField(
        auto_now_add=True
    )