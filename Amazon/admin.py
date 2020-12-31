from django.contrib import admin
from .models import Product, Cart, Customer, Order

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
