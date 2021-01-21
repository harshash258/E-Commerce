from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Product(models.Model):
    productId = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=200)
    productDescription = models.CharField(max_length=300)
    productRealPrice = models.IntegerField()
    productDiscountedPrice = models.IntegerField()
    productImage = models.ImageField()
    productInformation = RichTextField()
    productTotalQty = models.IntegerField()
    alias = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.productName} -- {self.productDiscountedPrice}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100)
    profileImage = models.ImageField(blank=True, null=True, default='profile.png')
    phoneNumber = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.profileImage.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    dateOrdered = models.DateTimeField(auto_now_add=True)
    orderCompleted = models.BooleanField(default=False)
    transactionId = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.customer} : {self.transactionId}"

    @property
    def getCartTotal(self):
        orderItems = self.cart_set.all()
        total = sum([item.getProductTotal for item in orderItems])
        return total

    @property
    def getNumberOfItems(self):
        orderItems = self.cart_set.all()
        total = sum([item.quantity for item in orderItems])
        return total


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} : {self.quantity}"

    @property
    def getProductTotal(self):
        total = self.product.productDiscountedPrice * self.quantity
        return total
