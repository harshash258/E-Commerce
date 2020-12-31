from .models import Order


def getNumberOfItems(request):
    global numberOfItems
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, orderCompleted=False)
        items = order.cart_set.all()
        numberOfItems = order.getNumberOfItems
    return {
        'number': numberOfItems
    }
