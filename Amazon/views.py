import datetime
import json
import time

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import User
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

from .filters import ProductFilters
from .forms import CreateUser
from .models import Product, Cart, Order, Customer, Shipment


def index(request):
    products = Product.objects.all()
    price_filter = ProductFilters(request.GET, queryset=products)

    context = {
        'filter': price_filter
    }
    return render(request, "Amazon/index.html", context)


@login_required(login_url='login')
def viewProfile(request, username):
    user = User.objects.get(username=username)
    customer = Customer.objects.get(user=user)
    context = {
        'user': user,
        'customer': customer,
        'shipment': Shipment.objects.filter(customer=request.user.customer)
    }
    return render(request, "Amazon/profile.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUser()
        if request.method == 'POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                passwordAgain = form.cleaned_data.get('password2')
                if password != passwordAgain:
                    messages.error(request, "Passwords do not match.")
                    return redirect('register')
                else:
                    form.save()
                    email = form.cleaned_data.get('email')
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                    customer = Customer.objects.create(user=user, email=email)
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
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Username or password incorrect")
        return render(request, "Amazon/login.html")


def logoutUser(request):
    logout(request)
    return redirect('index')


def viewCart(request):
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
        product = Product.objects.get(url=slug)
        context = {
            'productName': product.productName,
            'product': product
        }
        return render(request, "Amazon/viewProduct.html", context)
    except Product.DoesNotExist:
        return HttpResponse("Page Not Found")


def searchProduct(request):
    name = request.POST.get('search')
    page_number = request.GET.get('page')

    products = Product.objects.all()

    if name:
        products = products.filter(productName__contains=name)

    try:
        page_product = Paginator(products, 2).get_page(page_number)
    except EmptyPage:
        return render(request, "Amazon/searchResult.html", {'message': "No Product Found"})

    return render(request, "Amazon/searchResult.html", {
        'searchResults': page_product,
        'name': name
    })


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
    fullAddress = ''
    number = ''
    if request.method == "POST" and 'name' in request.POST:
        name = request.POST.get('name')
        address = request.POST.get('address')
        address2 = request.POST.get('address2')
        state = request.POST.get('state')
        pinCode = request.POST.get('pinCode')
        number = request.POST.get('number')
        fullAddress = address + ", " + address2 + " " + state + " - " + pinCode
        checkName = Customer.objects.filter(user=request.user).values('name')
        print(checkName)
        Customer.objects.filter(user=request.user).update(address=fullAddress, phoneNumber=number, name=name)

    elif request.POST == "POST" and 'address' in request.POST:
        fullAddress = request.POST.get('address')

    print(fullAddress)
    print(number)
    return render(request, "Amazon/payment.html")


def orderSuccessful(request):
    number = Customer.objects.filter(user=request.user).values('phoneNumber')
    fullAddress = Customer.objects.filter(user=request.user).values('address')
    timeIn = round(time.time() * 1000)
    total = Order.objects.get(customer=request.user.customer, orderCompleted=False).getCartTotal
    print(total)
    if request.method == 'POST':
        modeOfPayment = request.POST.get('paymentMethod')
        order = Shipment(customer=request.user.customer, orderId=timeIn,
                         orderDate=datetime.datetime.now().replace(microsecond=0), address=fullAddress,
                         phoneNumber=number, orderTotal=total, modeOfPayment=modeOfPayment)
        order.save()
        user = Customer.objects.get(user=request.user)
        preOrder = Order.objects.get(customer=user)
        carts = Cart.objects.filter(order=preOrder)
        for cart in carts:
            order.products.add(cart)

        carts.update(orderId=timeIn)
        preOrder.delete()
    else:
        return HttpResponse("Problem in Placing the Order")
    context = {
        'shipment': Shipment.objects.filter(customer=request.user.customer, orderId=timeIn),
        'cart': Cart.objects.filter(orderId=timeIn)
    }
    return render(request, "Amazon/order_success.html", context)
