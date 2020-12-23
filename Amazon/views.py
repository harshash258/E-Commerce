from django.shortcuts import render, HttpResponse
from .models import Product


def index(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, "Amazon/index.html", context)


def signIn(request):
    return render(request, "Amazon/signIn.html")


def viewProduct(request, slug):
    try:
        product = Product.objects.get(productName=slug)
        context = {
            'productName': product.productName,
            'product': product
        }
        return render(request, "Amazon/viewProduct.html", context)
    except Product.DoesNotExist:
        return HttpResponse("Page Not Found")


def searchProduct(request):
    name = request.POST.get("search")
    try:
        product = Product.objects.filter(productName__contains=name)
        context = {
            'searchResults': product,
        }
        return render(request, "Amazon/searchResult.html", context)
    except Product.DoesNotExist:
        return HttpResponse("Page Not Found")
