from .base import *


SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['my-web-site']

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Stripe API keys
# In production I am going to use my test keys same as in development
STRIPE_PUBLISHABLE_KEY_TEST = config('STRIPE_PUBLISHABLE_KEY_TEST')
STRIPE_SECRET_KEY_TEST = config('STRIPE_SECRET_KEY_TEST')
# Stripe endpoint's secret for webhooks
ENDPOINT_SECRET = config('ENDPOINT_SECRET')
