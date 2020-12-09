from randutils import random_string

from .base import *  # noqa

DEBUG = False

#  NOTE: This random string is not safe for production
SECRET_KEY = random_string(20)

ALLOWED_HOSTS = []
DATABASES = {}
