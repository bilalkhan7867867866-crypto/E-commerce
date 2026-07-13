from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Wishlist
from django.contrib.auth.decorators import login_required


@login_required
def product_list(request):
    products = Product.objects.filter(is_available = True)
    context = {
        'products':products
    }
    return render(request,'products/product_list.html',context)


@login_required
def product_detail(request,slug):
    product = get_object_or_404(Product,slug=slug)
    return render(request,'products/product_detail.html',{
        'product':product
    })


@login_required
def add_to_wishlist(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    Wishlist.objects.get_or_create(user=request.user,product=product)

    return redirect('wishlist')

@login_required
def remove_wishlist(request,wishlist_id):
    item = get_object_or_404(Wishlist,id=wishlist_id,user=request.user)
    item.delete()

    return redirect('wishlist')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user,).select_related('product')

    return render(request,'products/wishlist.html',{
        'wishlist_items':wishlist_items,
    })