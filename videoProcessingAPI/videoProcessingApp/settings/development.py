from .base import *
from decouple import config

ALLOWED_HOSTS = []
DEBUG = config("DEBUG", cast=bool)

INSTALLED_APPS += []

MIDDLEWARE += []

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
