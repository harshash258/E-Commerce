from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Cart, Customer, Order, Shipment


class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius:20px;" />'.format(object.productImage.url))

    thumbnail.short_description = "Product Image"

    list_display = ('productId', 'thumbnail', 'productName', 'productDiscountedPrice', 'productTotalQty')
    list_display_links = ('productId', 'thumbnail', 'productName')
    list_editable = ('productDiscountedPrice',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phoneNumber', 'address')
    list_display_links = ('user', 'name', 'phoneNumber', 'address')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'dateOrdered', 'orderCompleted', 'transactionId')
    list_display_links = ('customer', 'dateOrdered', 'orderCompleted', 'transactionId')


class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderId', 'customer', 'orderDate', 'orderTotal')
    list_display_links = ('orderId', 'customer', 'orderDate', 'orderTotal')


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Shipment, ShipmentAdmin)
