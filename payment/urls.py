from django.urls import path
from payment.views import CreatePaymentVIew, webhook


urlpatterns = [
    path('create-payment/', CreatePaymentVIew.as_view(), name='create-payment'),
    path('webhook/', webhook, name='webhook')
]
