from django.urls import path
from .views import ItemDetailView, add_to_cart


urlpatterns = [
    path('product/<pk>/<slug:slug>/', ItemDetailView.as_view(), name='product'),
]
