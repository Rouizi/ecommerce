from .base import *

# SECRET_KEY = '+&t^zh$1&^la7*el(%bww#p%vjb60n$ouylj!x@38@t-y^&5)k'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Stripe API keys
STRIPE_PUBLISHABLE_KEY_TEST = config('STRIPE_PUBLISHABLE_KEY_TEST')
STRIPE_SECRET_KEY_TEST = config('STRIPE_SECRET_KEY_TEST')
# Stripe endpoint's secret for webhooks
ENDPOINT_SECRET = config('ENDPOINT_SECRET')

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
