from django.contrib import admin
from .models import Product, Cart, Customer, Order
from django.utils.html import format_html


class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius:20px;" />'.format(object.productImage.url))

    thumbnail.short_description = "Product Image"

    list_display = ('productId', 'thumbnail', 'productName', 'productDiscountedPrice', 'productTotalQty')
    list_display_links = ('productId', 'thumbnail', 'productName')
    list_editable = ('productDiscountedPrice',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
