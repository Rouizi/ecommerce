from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F


from core.models import Item, OrderItem, Order, Size
from core.forms import SizeForm, CheckoutForm
from users.models import Address


class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                return self.num_pages
            else:
                raise


class HomeView(ListView):
    model = Item
    template_name = "core/home.html"
    paginate_by = 9
    paginator_class = SafePaginator

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        items = Item.objects.all()
        paginator = self.paginator_class(items, self.paginate_by)

        page = self.request.GET.get('page', 1)
        list_items = paginator.page(page)

        order_by = self.request.GET.get('order_by', None)
        filter_by = self.request.GET.get('filter_by', None)
        category = self.request.GET.get('category', None)

        if order_by and filter_by and category:
            if filter_by == 'N' or filter_by == 'BS':
                items = Item.objects.filter(
                    category=category, label=filter_by).order_by(order_by)
            elif filter_by == 'discount':
                items = Item.objects.filter(
                    category=category
                ).exclude(discount_price__isnull=True).order_by(order_by)

            paginator = self.paginator_class(items, self.paginate_by)
            list_items = paginator.page(page)
            context['order_by'] = order_by
            context['filter_by'] = filter_by
            context['category'] = category

        elif order_by:
            items = Item.objects.order_by(order_by)
            if filter_by:
                if filter_by == 'N' or filter_by == 'BS':
                    items = Item.objects.filter(
                        label=filter_by).order_by(order_by)
                elif filter_by == 'discount':
                    items = Item.objects.exclude(
                        discount_price__isnull=True).order_by(order_by)
                context['filter_by'] = filter_by
            if category:
                items = Item.objects.filter(
                    category=category).order_by(order_by)
                context['category'] = category

            paginator = self.paginator_class(items, self.paginate_by)
            list_items = paginator.page(page)
            context['order_by'] = order_by

        elif filter_by:
            if filter_by == 'N' or filter_by == 'BS':
                items = Item.objects.filter(label=filter_by)
                if category:
                    items = items.filter(category=category)
                    context['category'] = category
                if order_by:
                    items = items.order_by(order_by)
                    context['order_by'] = order_by
            elif filter_by == 'discount':
                items = Item.objects.exclude(discount_price__isnull=True)
                if category:
                    items = items.filter(category=category)
                    context['category'] = category
                if order_by:
                    items = items.order_by(order_by)
                    context['order_by'] = order_by

            paginator = self.paginator_class(items, self.paginate_by)
            list_items = paginator.page(page)
            context['filter_by'] = filter_by

        elif category:
            items = Item.objects.filter(category=category)
            if filter_by:
                if filter_by == 'N' or filter_by == 'BS':
                    items = items.filter(label=filter_by)
                elif filter_by == 'discount':
                    items = items.exclude(discount_price__isnull=True)
            if order_by:
                items = items.order_by(order_by)
                context['order_by'] = order_by
            context['filter_by'] = filter_by

            paginator = self.paginator_class(items, self.paginate_by)
            list_items = paginator.page(page)
            context['category'] = category

        context['home'] = True
        context['items'] = list_items
        context['page_range'] = paginator.page_range
        return context


@method_decorator(login_required, name='post')
class ItemDetailView(DetailView):
    model = Item
    template_name = 'core/product.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        form = SizeForm()
        context['form'] = form

        return context

    def post(self, request, *args, **kwargs):
        form = SizeForm(request.POST)
        self.object = self.get_object()
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['form'] = form

        if form.is_valid():
            size_request = form.cleaned_data.get('size')
            quantity_request = form.cleaned_data.get('quantity')

            size_item = Size.objects.get(name=size_request)
            sizes = {'S': 'SMALL', 'M': 'MEDIUM', 'L': 'LARGE'}

            stock_item = self.object.stockitem_set.filter(size=size_item)
            if stock_item.exists():
                stock_item = stock_item[0]
                order_item = OrderItem.objects.filter(
                    user=request.user,
                    item=self.object,
                    size=stock_item.size,
                    ordered=False
                )
                # Users cannot order more than 20 identical products
                if order_item.exists() and order_item[0].quantity + quantity_request > 20:
                    msg = 'You cannot add more than 20 identical products to the cart.'
                    messages.error(request, msg)
                elif stock_item.stock == 0:
                    msg = f'This product is out of stock for {sizes[size_request]} size.'
                    messages.error(request, msg)
                elif quantity_request > stock_item.stock:
                    msg = f'There are only {stock_item.stock} product(s) of this size in stock.'
                    messages.error(request, msg)
                else:
                    try:
                        with transaction.atomic():
                            stock_item.stock = F('stock') - quantity_request
                            stock_item.save()
                            add_to_cart(
                                request, self.object, quantity_request, stock_item.size, order_item)
                    except IntegrityError:
                        msg = 'An internal error has occurred. Please try your request again.'
                        messages.error(request, msg)
                        return redirect('/')
            else:
                messages.error(
                    request, 'This item is unavailable for this size.')

            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


def add_to_cart(request, item, quantity, size, order_item):

    if order_item.exists():
        order_item = order_item[0]
        order_item.quantity = F('quantity') + quantity
        order_item.save()
        messages.info(
            request, f"This item quantity for size {size.name} was updated.")

    else:
        order_item = OrderItem.objects.create(
            user=request.user,
            item=item,
            quantity=quantity,
            size=size,
            ordered=False
        )
        # We don't need to check if an order for this user and item exists
        # because if order_item does not exists then the order does not exists
        order = Order.objects.filter(user=request.user, ordered=False)
        if order.exists():
            order_item.order = order[0]
            order_item.save()
            messages.info(
                request, f"This item for size {size.name} was added to your cart.")
        else:
            order = Order.objects.create(user=request.user, ordered=False)
            order_item.order = order
            order_item.save()
            messages.info(
                request, f"This item for size {size.name} was added to your cart.")


class OrderSummary(LoginRequiredMixin, View):
    """Show the items with their details that are in the order of the user"""

    def get(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user, ordered=False)
        context = {}
        if not order.exists():
            context['empty'] = True
            return render(request, 'core/order_summary.html', context)

        order_items = OrderItem.objects.filter(order=order[0], ordered=False)
        # We could just do order.total_price() to have the 'price_include_discount'
        price_include_discount = 0
        price_without_discount = 0
        for order_item in order_items:
            price_include_discount += order_item.final_price()
            price_without_discount += order_item.total_item_price()

        context['order_items'] = order_items
        context['price_include_discount'] = price_include_discount
        context['price_without_discount'] = price_without_discount
        return render(request, 'core/order_summary.html', context)


@login_required
@transaction.atomic
def manage_order_item(request, pk):
    """
    Allow users to increase, decrease or
    delete an item in the order summary page
    """
    size = request.GET.get('size', None)
    operation = request.GET.get('op', None)

    size_item = get_object_or_404(Size, name=size)

    item = get_object_or_404(Item, pk=pk)
    order_item = get_object_or_404(
        OrderItem,
        user=request.user,
        item=item,
        size=size_item,
        ordered=False
    )
    stock_item = item.stockitem_set.filter(size=size_item)[0]
    # We don't need to check if an order for this user and item exists
    # because if order_item exists then the order exists
    if operation == 'plus':
        increase_item_quantity(request, order_item, stock_item)
        return redirect('core:order-summary')
    elif operation == 'minus':
        descrease_item_quantity(request, order_item, stock_item)
        return redirect('core:order-summary')
    elif operation == 'remove':
        remove_order_item_from_cart(request, order_item, stock_item)
        return redirect('core:order-summary')
    else:
        return redirect('/')


def increase_item_quantity(request, order_item, stock_item):
    if stock_item.stock == 0:
        messages.error(request, 'This product is out of stock for this size.')
    # Users cannot order more than 20 identical products
    elif order_item.quantity == 20:
        msg = 'You cannot add more than 20 identical products to the cart.'
        messages.error(request, msg)
    else:
        stock_item.stock = F('stock') - 1
        stock_item.save()
        order_item.quantity = F('quantity') + 1
        order_item.save()
        messages.info(request, "This item quantity was updated.")


def descrease_item_quantity(request, order_item, stock_item):
    # If quantity == 1 the user can't decrease it
    if order_item.quantity == 1:
        pass
    else:
        stock_item.stock = F('stock') + 1
        stock_item.save()
        order_item.quantity = F('quantity') - 1
        order_item.save()
        messages.info(request, "This item quantity was updated.")


def remove_order_item_from_cart(request, order_item, stock_item):
    order = Order.objects.get(
        user=request.user,
        ordered=False
    )
    stock_item.stock = F('stock') + order_item.quantity
    stock_item.save()
    order_item.delete()
    # If there is no order item in the order we delete the order
    order_items = OrderItem.objects.filter(
        user=request.user, order=order, ordered=False)
    if not order_items.exists():
        order.delete()
    messages.info(request, "This item was removed from your cart.")


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'core/checkout.html'
    form_class = CheckoutForm
    extra_context = {}

    def get(self, request, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered=False)
        if not order.exists():
            messages.error(self.request, 'You do not have an active order.')
            return redirect('/')

        form = CheckoutForm()
        order_items = OrderItem.objects.filter(order=order[0], ordered=False)
        address = Address.objects.filter(user=request.user)

        self.extra_context['order'] = order[0]
        self.extra_context['order_items'] = order_items
        self.extra_context['form'] = form
        if address.exists():
            self.extra_context['address'] = address[0]

        return self.render_to_response(self.extra_context)

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)

        shipping_address = form.cleaned_data.get('shipping_address')
        billing_address = form.cleaned_data.get('billing_address')
        shipping_zip = form.cleaned_data.get('shipping_zip')
        billing_zip = form.cleaned_data.get('billing_zip')
        country_shipping = form.cleaned_data.get('country_shipping')
        country_billing = form.cleaned_data.get('country_billing')
        billing_same_as_shipping = form.cleaned_data.get(
            'billing_same_as_shipping')
        set_default_shipping = form.cleaned_data.get('set_default_shipping')
        set_default_billing = form.cleaned_data.get('set_default_billing')
        use_default_shipping = form.cleaned_data.get('use_default_shipping')
        use_default_billing = form.cleaned_data.get('use_default_billing')
        payment_option = form.cleaned_data.get('payment_option')

        if use_default_shipping:
            address = Address.objects.filter(
                user=self.request.user,
                default_shipping_address=True
            )
            if not address.exists():
                return self.render_to_response(context)
        elif shipping_address and country_shipping and shipping_zip:
            address, created = Address.objects.get_or_create(
                user=self.request.user,
            )
            address.shipping_address = shipping_address
            address.shipping_zip = shipping_zip
            if set_default_shipping:
                address.default_shipping_address = True
            else:
                address.default_shipping_address = False
            address.save()

        else:
            if not billing_address or not country_billing or not billing_zip:
                msg = 'Please fill in the required shipping and billing address fields.'
            else:
                msg = 'Please fill in the required shipping address fields.'
            messages.error(self.request, msg)
            return self.render_to_response(context)

        if use_default_billing:
            address = Address.objects.filter(
                user=self.request.user,
                default_billing_address=True
            )
            if not address.exists():
                return self.render_to_response(context)
        elif billing_same_as_shipping:
            if use_default_shipping:
                address = Address.objects.filter(
                    user=self.request.user,
                    default_shipping_address=True
                )
                if address.exists():
                    address = address[0]
                    if set_default_billing:
                        address.default_billing_address = True
                    else:
                        address.default_billing_address = False
                    address.billing_address = address.shipping_address
                    address.billing_zip = address.shipping_zip
                    address.save()
                else:
                    return self.render_to_response(context)

            elif shipping_address and country_shipping and shipping_zip:
                address = Address.objects.get(user=self.request.user)
                if set_default_billing:
                    address.default_billing_address = True
                else:
                    address.default_billing_address = False
                address.billing_address = shipping_address
                address.billing_zip = shipping_zip
                address.save()

        elif billing_address and country_billing and billing_zip:
            address = Address.objects.get(user=self.request.user)
            if set_default_billing:
                address.default_billing_address = True
            else:
                address.default_billing_address = False
            address.billing_address = billing_address
            address.country_billing = country_billing
            address.billing_zip = billing_zip
            address.save()
        else:
            msg = 'Please fill in the required billing address fields.'
            messages.error(self.request, msg)
            return self.render_to_response(context)

        if payment_option == 'ST':
            return redirect('payment:create-payment')
        else:
            return self.render_to_response(context)
