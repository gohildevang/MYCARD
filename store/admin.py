from django.contrib import admin
from .models import Category, Product, Cart, order, OrderItem
# Register your models here.
admin.site.site_header = "My Ecom Admin"

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(order)
admin.site.register(OrderItem)