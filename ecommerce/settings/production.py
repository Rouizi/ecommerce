from .base import *
import dj_database_url

print('*****************************************************************************************')
print(config('SECRET_KEY'))
print('*****************************************************************************************')
SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ["rouizi-commerce.herokuapp.com"]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DATABASES['default'] = dj_database_url.config(
    conn_max_age=600, ssl_require=True)

# Stripe API keys
# In production I am going to use my test keys same as in development
STRIPE_PUBLISHABLE_KEY_TEST = config('STRIPE_PUBLISHABLE_KEY_TEST')
STRIPE_SECRET_KEY_TEST = config('STRIPE_SECRET_KEY_TEST')
# Stripe endpoint's secret for webhooks
ENDPOINT_SECRET = config('ENDPOINT_SECRET')

# Send email with sendgrid
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

# Media
# Amazon Simple Storage Service (S3) to store media file
# see https://devcenter.heroku.com/articles/s3 for more details

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = config("S3_BUCKET_NAME", "")
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = config("AWS_S3_CUSTOM_DOMAIN", "")

# aws settings
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# s3 static settings
STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
STATICFILES_STORAGE = 'ecommerce.storage_backends.StaticStorage'
# s3 public media settings
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'ecommerce.storage_backends.PublicMediaStorage'
