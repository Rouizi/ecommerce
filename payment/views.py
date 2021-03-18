from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives

import stripe
import logging

from payment.models import StripePayment
from core.models import Order, OrderItem
from users.models import User, Address


stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
endpoint_secret = settings.ENDPOINT_SECRET
stripe.max_network_retries = 7

logger = logging.getLogger(__name__)


class CreatePaymentView(LoginRequiredMixin, View):

    def send_email(
        self,
        html_content,
        subject='Dj-ecommerce report stripe payment',
        text_content='',
        from_email='cinorouizi@hotmail.fr',
        to='cinorouizi@gmail.com'
    ):
        message = EmailMultiAlternatives(
            subject, text_content, from_email, [to])
        message.attach_alternative(html_content, "text/html")
        message.send()

    def get(self, request, *args, **kwargs):
        logger.info(f'payment begin for user {request.user}')
        address = Address.objects.filter(user=request.user)
        if not address.exists():
            messages.error(
                request, 'You must have a shipping and billing address.')
            return redirect('/')
        order = Order.objects.filter(user=request.user, ordered=False)
        if not order.exists():
            messages.error(request, 'You do not have an active order.')
            return redirect('/')
        order = order[0]
        order_items = OrderItem.objects.filter(order=order, ordered=False)
        context = {
            'order': order,
            'order_items': order_items,
            'pk_key': settings.STRIPE_PUBLISHABLE_KEY_TEST
        }
        amount = int(order.total_price() * 100)

        if not request.is_ajax():
            return render(request, 'payment/create_payment.html', context)
        # TODO: Add save information of cart
        try:
            stripe_payment = StripePayment.objects.filter(
                user=request.user, order=order)
            if stripe_payment.exists():
                logger.info(f'stripe_payment exist for user {request.user}')
                payment_intent_id = stripe_payment[0].payment_intent_id
                intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                return JsonResponse({
                    'clientSecret': intent['client_secret']
                })
            else:
                logger.info(
                    f'stripe_payment does not exist for user {request.user}')
                customer = stripe.Customer.create(
                    email=request.user.email,
                    metadata={'user_id': request.user.id}
                )
                intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency='usd',
                    customer=customer['id'],
                    metadata={
                        'user_id': request.user.id,
                        'order_id': order.id
                    }
                )
                return JsonResponse({
                    'clientSecret': intent['client_secret']
                })
        except stripe.error.CardError as e:
            logger.exception('stripe.error.CardError')
            msg = 'Your card number is not valid.'
            return JsonResponse({'message': msg})
        except stripe.error.RateLimitError as e:
            logger.exception('stripe.error.RateLimitError')
            msg = 'Too many requests made to the API too quickly, please try again'
            return JsonResponse({'message': msg})
        except stripe.error.InvalidRequestError as e:
            logger.exception('stripe.error.InvalidRequestError')
            subject = 'stripe.error.InvalidRequestError'
            html_content = f"""
            <p>Report from Dj-ecommerce<br>The error occurred with stripe</p>
            <p><strong>Type</strong> is: {e.error.type}<br>
            <strong>Message</strong> is: {e.error.message}</p>
            """

            self.send_email(subject=subject, html_content=html_content)
            msg = 'A problem occurred please try again, if the error persists please try later.'

            return JsonResponse({'message': msg})
        except stripe.error.AuthenticationError as e:
            logger.exception('stripe.error.AuthenticationError')
            subject = 'stripe.error.AuthenticationError'
            html_content = f"""
            <p>Report from Dj-ecommerce<br>The error occurred with stripe</p>
            <p><strong>Type</strong> is: {e.error.type}<br>
            <strong>Message</strong> is: {e.error.message}</p>
            """
            self.send_email(subject=subject, html_content=html_content)
            msg = 'An internal problem occurred, we were notified. '\
                'Please try again. If the error persists please try later.'
            return JsonResponse({'message': msg})
        except stripe.error.APIConnectionError as e:
            # TODO: send email to myself and maybe an SMS
            logger.exception('stripe.error.APIConnectionError')
            msg = 'Network communication with stripe failed. You were not charged. please try later.'
            return JsonResponse({'message': msg})
        except stripe.error.StripeError as e:
            # TODO: send email to myself and maybe and SMS
            logger.exception('stripe.error.StripeError')
            msg = 'An internal problem occurred, we were notified. Please try later.'
            return JsonResponse({'message': msg})
        except Exception as e:
            # TODO: send email to myself
            logger.exception(e)
            msg = 'Something went wrong, please try again, if the error persits please contact us.'
            return JsonResponse({'message': msg})

# Stripe can send webhook events to my server
# to notify me when the status of a PaymentIntent changes
# See https://stripe.com/docs/payments/payment-intents/verifying-status for more info


@require_POST
@csrf_exempt
def webhook(request):
    """Handling events with stripe webhooks"""
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        logger.exception('ValueError in webhook')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.exception('stripe.error.SignatureVerificationError in webhook')
        return HttpResponse(status=400)

    # Create a reference to a PaymentIntent in my database
    if 'payment_intent' in event.type:
        user_id = int(event.data.object.metadata.user_id)
        user = User.objects.get(id=user_id)
        order_id = int(event.data.object.metadata.order_id)
        order = Order.objects.get(id=order_id)

        stripe_payment = StripePayment.objects.filter(
            user=user,
            order=order,
            payment_intent_id=event.data.object.id
        )
        if not stripe_payment.exists():
            stripe_payment = StripePayment.objects.create(
                user=user,
                order=order,
                payment_intent_id=event.data.object.id
            )
            stripe_payment.save()
            logger.info(
                f''' webhook says: reference created for PaymentIntent 
                for use {user} (stripe_payment = {stripe_payment})''')
    # Create a reference to a customer in my database
    elif 'customer' in event.type:
        customer_id = event.data.object.id
        user_id = int(event.data.object.metadata.user_id)
        user = User.objects.get(pk=user_id)
        if user.stripe_customer_id is None:
            user.stripe_customer_id = customer_id
            user.save()
            logger.info(
                f'''webhook says: reference created for Customer
                 for user {user} (customer_id = {customer_id})''')

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        # send email to the user manually or via stripe
        order = Order.objects.get(user=request.user, ordered=False)
        order.update(ordered=True)
        payment_intent = event.data.object
        logger.info('webhook says: PaymentIntent was successful!')
    elif event.type == 'payment_intent.payment_failed':
        # send email to the user manually or via stripe
        payment_intent = event.data.object
        if payment_intent.get('last_payment_error'):
            error_message = payment_intent['last_payment_error']['message']
        else:
            error_message = None

        logger.info(f'webhook says: payment failed with error message: {error_message}')
    else:
        # Unexpected event type
        logger.info(f'webhook says: Unexpected event {event.type}')

    return HttpResponse(status=200)
