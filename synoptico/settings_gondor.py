import os
import urlparse

from .settings import *  # noqa

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    "jy682.gondor.co",
    "synopti.co"
]

if "GONDOR_DATABASE_URL" in os.environ:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["GONDOR_DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": {
                "postgres": "django.db.backends.postgresql_psycopg2"
            }[url.scheme],
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port
        }
    }

SITE_ID = 2

MEDIA_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "media")
STATIC_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "static")

MEDIA_URL = "/site_media/media/"  # make sure this maps inside of site_media_url
STATIC_URL = "/site_media/static/"  # make sure this maps inside of site_media_url
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

FILE_UPLOAD_PERMISSIONS = 0640

RAVEN_CONFIG = {
    "dsn": "https://7d8f3acc41d041609d51e850daf9c847:45d4fbf7ece5472abb29023fa1e384bd@app.getsentry.com/30564"
}
