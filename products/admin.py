from django.contrib import admin
from .models import Product,Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','created_at')
    prepopulated_fields = {
        'slug':('name',)
    }

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','category','price','stock','is_available',)
    list_filter = ('category','is_available')
    search_fields = ('name','description',)
    prepopulated_fields = {
        'slug':('name',)
    }