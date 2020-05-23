from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import stripe

from core.models import Order, OrderItem


stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
endpoint_secret = settings.ENDPOINT_SECRET


class CreatePaymentVIew(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                intent = stripe.PaymentIntent.create(
                    amount=100,
                    currency='usd'
                )
                return JsonResponse({
                    'clientSecret': intent['client_secret']
                })
            except stripe.error.CardError as e:
                print('********************ERROOOOOOOOOOR1**********************')
                print('Status is: %s' % e.http_status)
                print('Type is: %s' % e.error.type)
                print('Code is: %s' % e.error.code)
                # param is '' in this case
                print('Param is: %s' % e.error.param)
                print('Message is: %s' % e.error.message)
            except stripe.error.RateLimitError as e:
                print('********************ERROOOOOOOOOOR2**********************')
                # Too many requests made to the API too quickly
            except stripe.error.InvalidRequestError as e:
                print('********************ERROOOOOOOOOOR3**********************')
                # Invalid parameters were supplied to Stripe's API
            except stripe.error.AuthenticationError as e:
                print('********************ERROOOOOOOOOOR4**********************')
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)

            except stripe.error.APIConnectionError as e:
                print('********************ERROOOOOOOOOOR5**********************')
                # Network communication with Stripe failed
            except stripe.error.StripeError as e:
                print('********************ERROOOOOOOOOOR6**********************')
                # Display a very generic error to the user, and maybe send
                # yourself an email
            except Exception as e:
                print('********************ERROOOOOOOOOOR7**********************')
                # Something else happened, completely unrelated to Stripe

        order = Order.objects.filter(user=request.user, ordered=False)
        order_items = OrderItem.objects.filter(order=order[0], ordered=False)
        context = {
            'order': order[0],
            'order_items': order_items,
            'pk_key': settings.STRIPE_PUBLISHABLE_KEY_TEST
        }
        return render(request, 'payment/create_payment.html', context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.is_ajax():
            print('***********************************************************************************')
            print(request.POST.get('order_complete'))
            print(request.POST)
            print('*********************************************************************************')

# Stripe can send webhook events to my server
# to notify me when the status of a PaymentIntent changes
# See https://stripe.com/docs/payments/payment-intents/verifying-status for more info
@require_POST
@csrf_exempt
def webhook(request):
    payload = request.body.decode('utf-8')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    endpoint_secret = 'whsec_JVN5v6f0PqItxJf5Jgbdz2WBmkVWIIiw'
    print('"payload": ', payload)
    print(type(payload))
    print('"sig_header": ', sig_header)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        print('"event: "', event)
    except ValueError as e:
        # Invalid payload
        print("ValueError")
        raise(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('stripe.error.SignatureVerificationError')
        raise(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object  # contains a stripe.PaymentIntent
        print('PaymentIntent was successful!')
    elif event.type == 'payment_intent.payment_failed':
        payment_intent = event.data.object  # contains a stripe.PaymentMethod
        if payment_intent.get('last_payment_error'):
            error_message = payment_intent['last_payment_error']['message'] 
        else:
            error_message = None

        print('FAILEDFAILEDFAILEDFAILEDFAILEDFAILEDFAILEDFAILEDFAILEDFAILEDFAILED')
    # ... handle other event types
    else:
        # Unexpected event type
        print('"Unexpected event typeUnexpected event typeUnexpected event type"')
        return HttpResponse(status=400)

    
    
    return HttpResponse(status=200)