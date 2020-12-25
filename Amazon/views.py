from django.shortcuts import render, HttpResponse, redirect
from .models import Product
from .forms import CreateUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def index(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, "Amazon/index.html", context)


def register(request):
    form = CreateUser()
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            messages.error(request, "Error in creating a Account")
            return redirect('register')
    context = {
        'form': form,
    }
    return render(request, "Amazon/register.html", context)


def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Username or password incorrect")
    context = {

    }
    return render(request, "Amazon/signIn.html", context)


def logoutUser(request):
    logout(request)
    return redirect('index')


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
