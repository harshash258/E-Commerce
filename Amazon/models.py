from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    productId = models.CharField(primary_key=True, max_length=20)
    productName = models.CharField(max_length=200)
    productDescription = models.CharField(max_length=300)
    productRealPrice = models.IntegerField()
    productDiscountedPrice = models.IntegerField()
    productImage = models.ImageField()
    productInformation = models.TextField()
    productTotalQty = models.IntegerField()
    alias = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.productName} -- {self.productDiscountedPrice}"


