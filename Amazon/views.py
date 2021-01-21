from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import Product, Cart, Order, Customer
from .forms import CreateUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import User
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

'''
def index(request):
    fil = request.getlist('price')
    if fil:
        if fil == "low":
            products = Product.objects.all().order_by('productDiscountedPrice')
        elif fil == "high":
            products = Product.objects.all().order_by('-productDiscountedPrice')
        else:
            products = Product.objects.all()
        context = {
            'products': products
        }
        return JsonResponse(context)
    else:
        context = {}
        return render(request, "Amazon/index.html", context)

'''


def index(request):
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
    return render(request, "Amazon/checkout.html")
