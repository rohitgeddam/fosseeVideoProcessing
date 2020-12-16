from .base import *
from decouple import config

ALLOWED_HOSTS = []
DEBUG = config("DEBUG", cast=bool)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
