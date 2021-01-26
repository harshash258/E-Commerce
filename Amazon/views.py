import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

from .forms import CreateUser
from .models import Product, Cart, Order, Customer


def index(request):
    data = request.GET.get('word')
    print(data)

    products = Product.objects.all()
    paginator = Paginator(products, 2)
    page = request.GET.get('page')
    page_product = paginator.get_page(page)

    fil = request.GET.get('price')
    print(fil)

    context = {
        'products': page_product
    }
    return render(request, "Amazon/index.html", context)


def viewProfile(request, username):
    user = User.objects.get(username=username)
    customer = Customer.objects.get(user=user)
    context = {
        'user': user,
        'customer': customer
    }
    return render(request, "Amazon/profile.html", context)


def register(request):
    form = CreateUser()
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            customer = Customer.objects.create(user=request.user, email=email)
            customer.save()
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
    return render(request, "Amazon/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def viewCart(request):
    global order
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, orderCompleted=False)
        items = order.cart_set.all()
        numberOfItems = order.getNumberOfItems
    else:
        return redirect('login')
    context = {
        'items': items,
        'order': order,
        'totalItems': numberOfItems
    }
    return render(request, "Amazon/cart.html", context)


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
        if product is not None:
            context = {
                'searchResults': product,
            }
            return render(request, "Amazon/searchResult.html", context)
        else:
            return HttpResponse("No Product Found")
    except Product.DoesNotExist:
        return HttpResponse("Page Not Found")


def addToCart(request):
    data = json.loads(request.body)
    productId = data['productID']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(productId=productId)

    checkOrder, created = Order.objects.get_or_create(customer=customer, orderCompleted=False)
    cartItem, created = Cart.objects.get_or_create(order=checkOrder, product=product)

    if action == 'add':
        cartItem.quantity = (cartItem.quantity + 1)
    elif action == 'remove':
        cartItem.quantity = (cartItem.quantity - 1)

    cartItem.save()

    if cartItem.quantity <= 0:
        cartItem.delete()
    return JsonResponse('Item was added to cart.', safe=False)


def checkOut(request):
    global order

    if request.user.is_authenticated:
        customer = request.user.customer
        user = Customer.objects.get(user=request.user)

        order, created = Order.objects.get_or_create(customer=customer, orderCompleted=False)
        items = order.cart_set.all()
        numberOfItems = order.getNumberOfItems
    else:
        return redirect('login')

    context = {
        'user': user,
        'items': items,
        'order': order,
        'totalItems': numberOfItems
    }

    return render(request, "Amazon/checkout.html", context)


def payment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        address2 = request.POST.get('address2')
        state = request.POST.get('state')
        pinCode = request.POST.get('pinCode')
        number = request.POST.get('number')
        fullAddress = name + " \n" + address + " " + address2 + " " + state + "-" + pinCode + " \nPhone Number: +91 " + number
        Customer.objects.filter(user=request.user).update(address=fullAddress)

    return render(request, "Amazon/payment.html")
