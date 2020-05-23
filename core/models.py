from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.models import Address


class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Item(models.Model):
    SHIRT = 'S'
    SPORT_WEAR = 'SW'
    OUTWEAR = 'OW'
    DENIM = 'D'
    CATEGORY = [
        (SHIRT, 'Shirt'),
        (SPORT_WEAR, 'Sport Wear'),
        (OUTWEAR, 'OutWear'),
        (DENIM, 'Denim'),
    ]
    NEW = 'N'
    BESTSELLER = 'BS'
    LABEL = [(NEW, 'New'), (BESTSELLER, 'bestseller')]
    PRIMARY = 'primary-color'
    DANGER = 'danger-color'
    COLOR_LABEL = [(PRIMARY, 'primary'), (DANGER, 'danger')]
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=2, choices=CATEGORY)
    label = models.CharField(max_length=2, choices=LABEL, blank=True, null=True)
    color_label = models.CharField(
        max_length=15, choices=COLOR_LABEL, blank=True, null=True)
    size = models.ManyToManyField(Size, through='StockItem')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image1 = models.ImageField(upload_to='clothes')
    image2 = models.ImageField(upload_to='clothes', blank=True, null=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    def in_stock(self):
        # Return True if we have at least 1 product in stock of any size
        for item in self.stockitem_set.all():
            if item.stock > 0:
                return True
        return False

    def clean(self):
        # raise a ValidationError if discount_price is bigger then price
        if self.discount_price is not None:
            if self.discount_price >= self.price:
                raise ValidationError(
                    {'discount_price': 'Discount price must be less then Price.'}
                )

    def save(self, *args, **kwargs):
        self.full_clean
        return super(Item, self).save(*args, **kwargs)


class StockItem(models.Model):
    stock = models.PositiveIntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.stock} product(s) of "{self.item}" for size "{self.size}"'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(default=timezone.now)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey(
        Address, on_delete=models.SET, null=True, blank=True)

    def __str__(self):
        return f'Order of user {self.user.username}'

    def total_price(self):
        total = 0
        for order_item in self.orderitem_set.all():
            total += order_item.final_price()
        return total


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'OrderItem of {self.item.name}'

    def total_item_price(self):
        return self.quantity * self.item.price

    def total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def amount_saved(self):
        return self.total_item_price() - self.total_discount_item_price()

    def final_price(self):
        if self.item.discount_price:
            return self.total_discount_item_price()
        return self.total_item_price()
