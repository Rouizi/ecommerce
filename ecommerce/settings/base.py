import os
from decouple import config
import dj_database_url

SECRET_KEY = 'rzegzef-zef-ze-fzefzefzefzef'

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    'crispy_forms',

    'core',
    'users',
    'payment',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'context_processors.nb_of_items',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('NAME'),
        'USER': 'alfa',
        'PASSWORD': config('PASSWORD'),
        'HOST': '',
        'PORT': config('PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/accounts/login/'

# Django allauth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# django.contrib.sites
SITE_ID = 1

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': ''
#         }
#     }
# }

# CRISPY FORMS
CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'users.User'

# django-allauth
ACCOUNT_ADAPTER = 'users.adapter.AccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'verbose': {
#             'format': '%(asctime)s %(name)s  %(levelname)s %(message)s',
#         },
#     },
#     'handlers': {
#         'stripe': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'logs/stripe.log',
#             'formatter': 'verbose',
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'logs/all_logs.log',
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'payment': {
#             'level': 'DEBUG',
#             'handlers': ['stripe'],
#             'propagate': True,
#         }
#     }
# }


DEBUG = False

ALLOWED_HOSTS = ["rouizi-commerce.herokuapp.com"]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DATABASES['default'] = dj_database_url.config(
    conn_max_age=600, ssl_require=True)

# # Stripe API keys
# # In production I am going to use my test keys same as in development
# STRIPE_PUBLISHABLE_KEY_TEST = config('STRIPE_PUBLISHABLE_KEY_TEST')
# STRIPE_SECRET_KEY_TEST = config('STRIPE_SECRET_KEY_TEST')
# # Stripe endpoint's secret for webhooks
# ENDPOINT_SECRET = config('ENDPOINT_SECRET')

# # Send email with sendgrid
# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_PORT = config('EMAIL_PORT')
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = True

# Media
# Amazon Simple Storage Service (S3) to store media file
# see https://devcenter.heroku.com/articles/s3 for more details

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", "")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", "")
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
