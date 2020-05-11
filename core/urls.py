from django.urls import path
from .views import ItemDetailView, OrderSummary, manage_order_item


urlpatterns = [
    path('product/<pk>/<slug:slug>/', ItemDetailView.as_view(), name='product'),
    path('order-summary/', OrderSummary.as_view(), name='order-summary'),
    path('manage-order-item/<pk>/', manage_order_item, name='manage-order-item')
]
