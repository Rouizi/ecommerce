from django.db import models
from django.conf import settings
from django.utils import timezone


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
        for item in self.stockitem_set.all():
            if item.stock > 0:
                return True
        return False


class StockItem(models.Model):
    stock = models.PositiveIntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.stock} product(s) "{self.item}" for size "{self.size}"'


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'OrderItem of {self.item.name}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(default=timezone.now)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'Order of user {self.user.username}'
