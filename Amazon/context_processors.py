from .models import Order


def getNumberOfItems(request):
    global numberOfItems
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, orderCompleted=False)
        numberOfItems = order.getNumberOfItems
    else:
        numberOfItems = 0
    return {
        'number': numberOfItems
    }
