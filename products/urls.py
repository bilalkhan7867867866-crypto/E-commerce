from django.urls import path
from .views import product_detail,product_list,wishlist_view,add_to_wishlist,remove_wishlist

urlpatterns = [
    path('',product_list,name='product_list'),
    path('product/<slug:slug>/',product_detail,name='product_detail'),


    path('wishlist/',wishlist_view,name='wishlist'),
    path('wishlist/add/<int:product_id>/',add_to_wishlist,name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/',remove_wishlist,name='remove_wishlist'),
]
