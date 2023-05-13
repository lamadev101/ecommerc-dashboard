from django.contrib import admin
from main.models import *

# Register your models here.   
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'amount', 'qty', 'size', 'packing', 'payment_mode', 'payment_status', 'shipment', 'order_date', 'delivery_date', 'remarks')
    list_filter = ['payment_status', 'payment_mode', 'shipment']
    search_fields = ['product']
admin.site.register(Orders, OrderAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'cross_price', 'selling_price', 'draft', 'created_at']
admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image']
admin.site.register(Category, CategoryAdmin)

class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'qty', 'created_at', 'updated_at']
admin.site.register(ProductSize, ProductSizeAdmin)

class VariantImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'created_at', 'updated_at']
admin.site.register(VariantImage, VariantImageAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'district', 'street', 'gender', 'height', 'weight', 'created_at']
    list_filter = ['gender', 'district']
admin.site.register(Customer, CustomerAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['pId', 'name', 'image', 'created_at']
admin.site.register(Payment, PaymentAdmin)

class ExpensesAdmin(admin.ModelAdmin):
    list_display = ['eId', 'title', 'weight', 'length', 'unit_price', 'total_amount', 'activity_date', 'refrences', 'remarks']
admin.site.register(Expenses, ExpensesAdmin)

class SoldProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'total_qty', 'sold_qty', 'remaining_qty', 'remarks', 'created_at']
admin.site.register(SoldProduct, SoldProductAdmin)

# admin.site.site_url = 'http://aviationnepalnews.com'
admin.site.site_url = 'https://sastoodokan.com'