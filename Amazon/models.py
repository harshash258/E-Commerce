from django.db import models
from django.conf import settings


class Product(models.Model):
    productId = models.CharField(primary_key=True, max_length=20)
    productName = models.CharField(max_length=100)
    productDescription = models.CharField(max_length=300)
    productRealPrice = models.IntegerField()
    productDiscountedPrice = models.IntegerField()
    productImage = models.ImageField()
    productInformation = models.TextField()
    productTotalQty = models.IntegerField()
    alias = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.productName} -- {self.productDiscountedPrice}"


class Order(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(Order)
    startDate = models.DateTimeField(auto_now_add=True)
    orderDate = models.DateTimeField()

    def __str__(self):
        return f"{self.user}"