from django.urls import path
from payment.views import CreatePaymentView, webhook


urlpatterns = [
    path('create-payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('webhook/', webhook, name='webhook')
]
