from django.db import models
from django.contrib.auth.forms import UserCreationForm
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


class UserLogin(UserCreationForm):
    userId = models.CharField(primary_key=True, max_length=20)
    userEmail = models.EmailField()
    userPassword = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.userId} : {self.userEmail}"
