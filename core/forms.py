from django import forms


class SizeForm(forms.Form):
    CHOICES = (
        ('S', 'SMALL'),
        ('M', 'MEDIUM'),
        ('L', 'LARGE'),
    )
    size = forms.ChoiceField(
        choices=CHOICES, label='Select size',
        widget=forms.RadioSelect()
    )
    quantity = forms.IntegerField(min_value=1, max_value=20)


class CheckoutForm(forms.Form):
    STRIPE = 'ST'
    PAYPAL = 'PY'
    PAYMENT_CHOICES = (
        (STRIPE, 'Stripe'),
        (PAYPAL, 'Paypal')
    )
    UNITED_STATES = 'US'
    COUNTRY_CHOICES = ((UNITED_STATES, 'United States'),)
    shipping_address = forms.CharField(max_length=255)
    billing_address = forms.CharField(max_length=255)
    shipping_zip = forms.CharField(max_length=50)
    billing_zip = forms.CharField(max_length=50)
    country = forms.ChoiceField(widget=forms.Select, choices=COUNTRY_CHOICES)
    billing_same_as_shipping = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
