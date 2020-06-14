from django.contrib import admin
from core.models import Item, OrderItem, Order, Size, StockItem


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'description')
    list_filter = ('name', 'category', 'price')
    ordering = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Item, ItemAdmin)
admin.site.register(Size)
admin.site.register(StockItem)
admin.site.register(OrderItem)
admin.site.register(Order)
