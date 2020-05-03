from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import IntegrityError, transaction

from core.models import Item, OrderItem, Order
from .forms import SizeForm


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

        if order_by:
            items = Item.objects.order_by(order_by)
            if filter_by:
                if filter_by == 'N' or filter_by == 'BS':
                    items = Item.objects.filter(label=filter_by).order_by(order_by)
                elif filter_by == 'discount':
                    items = Item.objects.exclude(discount_price__isnull=True).order_by(order_by)
                context['filter_by'] = filter_by
            if category:
                items = Item.objects.filter(category=category).order_by(order_by)
                context['category'] = category

            paginator = self.paginator_class(items, self.paginate_by)
            list_items = paginator.page(page)
            context['order_by'] = order_by

        if filter_by:
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

        if category:
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

        if order_by and filter_by and category:
            if filter_by == 'N' or filter_by == 'BS':
                items = Item.objects.filter(category=category, label=filter_by).order_by(order_by)
            elif filter_by == 'discount':
                items = Item.objects.filter(
                    category=category
                ).exclude(discount_price__isnull=True).order_by(order_by)

            paginator = self.paginator_class(items, self.paginate_by)
            list_items = paginator.page(page)
            context['order_by'] = order_by
            context['filter_by'] = filter_by
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
            self.object = self.get_object()

            size_request = form.cleaned_data.get('size')
            quantity_request = form.cleaned_data.get('quantity')
            sizes = {'S': 'SMALL', 'M': 'MEDIUM', 'L': 'LARGE'}

            for item_by_size in self.object.stockitem_set.all():
                print(item_by_size)
                # We check the stock for the size the user requested
                if str(item_by_size.size) == size_request:
                    if item_by_size.stock == 0:
                        messages.error(
                            request, f'This product is out of stock for {sizes[size_request]} size.')
                    elif quantity_request > item_by_size.stock:
                        messages.error(
                            request, f'There are only {item_by_size.stock} product(s) of this size in stock.')
                    else:
                        item_by_size.stock -= quantity_request
                        item_by_size.save()
                        add_to_cart(request, self.object, quantity_request)

            return self.render_to_response(context=context)

        return self.render_to_response(context=context)


def add_to_cart(request, item, quantity):
    order_item = OrderItem.objects.filter(
        user=request.user, item=item, ordered=False)
    if order_item.exists():
        order_item = order_item[0]
        order_item.quantity += quantity
        order_item.save()
    else:
        order_item = OrderItem.objects.create(
            user=request.user, item=item, quantity=quantity, ordered=False)

    order = Order.objects.filter(user=request.user, ordered=False)
    if order.exists():
        order = order[0]
        if order.items.filter(item=item).exists():
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            messages.info(request, "This item quantity was updated.")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        print('CCCCCCCCCCCCCCCCCCCCCCCCCCCC')


@login_required
def remove_order_item_from_cart(request):
    pass


@login_required
def remove_order_from_cart(request):
    pass
