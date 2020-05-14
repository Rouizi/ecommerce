from core.models import Order, OrderItem


def nb_of_items(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, ordered=False)
        if order.exists():
            order_items = OrderItem.objects.filter(order=order[0], ordered=False)

            return {'nb_of_items': order_items.count()}
        return {'nb_of_items': ''}
    return {'nb_of_items': ''}
