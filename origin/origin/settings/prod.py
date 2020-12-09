from safe_environ import from_env

from .base import *  # noqa

DEBUG = False
SECRET_KEY = from_env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = []

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": from_env("POSTGRES_NAME"),
        "USER": from_env("POSTGRES_USER"),
        "PASSWORD": from_env("POSTGRES_PASSWORD"),
        "HOST": from_env("POSTGRES_HOST"),
        "PORT": from_env("POSTGRES_PORT"),
    }
}

memcached_host = (from_env("MEMCACHED_HOST"),)
memcached_port = (from_env("MEMCACHED_PORT"),)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": f"{memcached_host}{memcached_port}",
    }
}
