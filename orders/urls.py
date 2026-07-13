from django.urls import path
from .views import checkout,order_success

urlpatterns = [
    path('checkout/',checkout,name='checkout'),
    path('success/',order_success,name='order_success')
]
