"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import re
import dj_database_url
import dj_email_url
from django.contrib import messages
from django.contrib.messages import ERROR
from django.core.exceptions import ImproperlyConfigured
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware

ADMIN_RE = re.compile("^([\w -]+) <([^>]+)>$")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "true").lower() == "true"
ENABLE_DEBUG_TOOLBAR = os.environ.get("ENABLE_DEBUG_TOOLBAR", "false").lower() == "true"
ENABLE_SILK = os.environ.get("ENABLE_SILK", "false").lower() == "true"


ENABLE_API = not os.environ.get("ENABLE_API", "y").lower() in ["n", "no", "false"]
ENABLE_FRONT = (
    os.environ.get("ENABLE_FRONT", "n").lower() in ["y", "yes", "true"] or DEBUG
)
ENABLE_MAP = os.environ.get("ENABLE_MAP", "n").lower() in ["y", "yes", "true"] or DEBUG

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEST_RUNNER = "agir.api.test_runner.TestRunner"

admins = os.environ.get("ADMINS")
if admins:
    admins = [ADMIN_RE.match(s.strip()) for s in admins.split(";")]
    if any(m is None for m in admins):
        raise ImproperlyConfigured(
            "ADMINS should be of the form 'Name 1 <address1@domain.fr>; Name 2 <address2@domain.fr>"
        )

    ADMINS = [m.groups() for m in admins]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET", "1d5a5&y9(220)phk0o9cqjwdpm$3+**d&+kru(2y)!5h-_qn4b"
)
SENDGRID_SES_WEBHOOK_USER = os.environ.get("SENDGRID_SES_WEBHOOK_USER", "fi")
SENDGRID_SES_WEBHOOK_PASSWORD = os.environ.get("SENDGRID_SES_WEBHOOK_PASSWORD", "prout")
MAILTRAIN_API_KEY = os.environ.get("MAILTRAIN_API_KEY", "prout")
SCANNER_API = os.environ.get("SCANNER_API", "http://agir.local:8000")
SCANNER_API_KEY = os.environ.get("SCANNER_API_KEY", "prout")
SCANNER_API_SECRET = os.environ.get("SCANNER_API_SECRET", "prout")

# these domain names are used when absolute URLs should be generated (e.g. to include in emails)
MAIN_DOMAIN = os.environ.get("MAIN_DOMAIN", "https://lafranceinsoumise.fr")
API_DOMAIN = os.environ.get(
    "API_DOMAIN",
    "http://agir.local:8000" if DEBUG else "https://api.lafranceinsoumise.fr",
)
FRONT_DOMAIN = os.environ.get(
    "FRONT_DOMAIN",
    "http://agir.local:8000" if DEBUG else "https://agir.lafranceinsoumise.fr",
)
MAP_DOMAIN = os.environ.get(
    "MAP_DOMAIN",
    "http://agir.local:8000" if DEBUG else "https://agir.lafranceinsoumise.fr",
)
MAILTRAIN_HOST = os.environ.get("MAILTRAIN_HOST", "http://agir.local:8000")
MAILTRAIN_LIST_ID = os.environ.get("MAILTRAIN_LIST_ID", "SyWda9pi")
MAILTRAIN_DISABLE = DEBUG

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,agir.local").split(",")

# Application definition

INSTALLED_APPS = [
    # before to override templates
    "agir.lib",
    # default contrib apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # sitemaps
    "django.contrib.sitemaps",
    # redirect
    "django.contrib.sites",
    "django.contrib.redirects",
    # humanize
    "django.contrib.humanize",
    # rest_framework
    "rest_framework",
    # OTP for admin
    "django_otp",
    "django_otp.plugins.otp_totp",
    # geodjango
    "django.contrib.gis",
    "rest_framework_gis",
    # rules
    "rules.apps.AutodiscoverRulesConfig",
    # crispy forms
    "crispy_forms",
    # django filters
    "django_filters",
    # django_countries
    "django_countries",
    # phone number field
    "phonenumber_field",
    # stdimage
    "stdimage",
    # webpack
    "webpack_loader",
    # fi apps
    "nuntius",
    "agir.authentication",
    "agir.people",
    "agir.events",
    "agir.groups",
    "agir.polls",
    "agir.clients",
    "agir.front",
    "agir.carte",
    "agir.webhooks",
    "agir.payments",
    "agir.donations",
    "agir.system_pay",
    "agir.checks",
    "agir.loans",
    "agir.mailing",
    # security
    "corsheaders",
    "oauth2_provider",
    "reversion",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "agir.lib.middleware.TurbolinksMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "agir.authentication.middleware.MailLinkMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]

if ENABLE_SILK:
    INSTALLED_APPS += ["silk"]
    MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")


ROOT_URLCONF = "agir.api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "agir.api.context_processors.domain_names",
            ]
        },
    }
]

MESSAGE_TAGS = {ERROR: "danger"}
MESSAGE_LEVEL = messages.DEBUG if DEBUG else messages.INFO

WSGI_APPLICATION = "agir.api.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(default="postgis://api:password@localhost/api")
}

# Mails

# by default configured for mailhog sending
email_config = dj_email_url.parse(os.environ.get("SMTP_URL", "smtp://localhost:1025/"))

EMAIL_FILE_PATH = email_config["EMAIL_FILE_PATH"]
EMAIL_HOST_USER = email_config["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = email_config["EMAIL_HOST_PASSWORD"]
EMAIL_HOST = email_config["EMAIL_HOST"]
EMAIL_PORT = email_config["EMAIL_PORT"]
EMAIL_BACKEND = email_config["EMAIL_BACKEND"]
EMAIL_USE_TLS = email_config["EMAIL_USE_TLS"]
EMAIL_USE_SSL = email_config["EMAIL_USE_SSL"]

# fixed for now ==> maybe more flexible?
EMAIL_TEMPLATES = {
    # WELCOME_MESSAGE variables: [PROFILE_LINK]
    "WELCOME_MESSAGE": "https://mosaico.lafranceinsoumise.fr/emails/ac205f71-61a3-465b-8161-cec5729ecdbb.html",
    # CONFIRM_SUBSCRIPTION_MESSAGE variables: [CONFIRMATION_URL]
    "SUBSCRIPTION_CONFIRMATION_MESSAGE": "https://mosaico.lafranceinsoumise.fr/emails/cd878308-6fd7-4088-b525-a020c5bb3fe0.html",
    # ALREADY_SUBSCRIBED_MESSAGE: [AGO], [PANEL_LINK]
    "ALREADY_SUBSCRIBED_MESSAGE": "https://mosaico.lafranceinsoumise.fr/emails/d7040d22-703f-4ac7-883c-d2f04c13be1a.html",
    # INVITATION_SUBSCRIPTION_MESSAGE: [GROUP_NAME], [CONFIRMATION_URL] [SIGNAL_URL]
    "GROUP_INVITATION_WITH_SUBSCRIPTION_MESSAGE": "https://mosaico.lafranceinsoumise.fr/emails/1db59e8e-0ebd-4dab-8b2d-e7a2d679d6aa.html",
    # INVITATION_CONFIRMATION_MESSAGE: [GROUP_NAME], [CONFIRMATION_URL] [SIGNAL_URL]
    "GROUP_INVITATION_MESSAGE": "https://mosaico.lafranceinsoumise.fr/emails/4a704705-9b5d-4356-b799-285741e558c6.html",
    # GROUP_INVITATION_ABUSE_MESSAGE
    "GROUP_INVITATION_ABUSE_MESSAGE": "https://mosaico.lafranceinsoumise.fr/emails/b70f5728-c2fb-490e-aa25-1a678b6a5864.html",
    # DONATION_MESSAGE variables : [PROFILE_LINK]
    "DONATION_MESSAGE": "https://mosaico.lafranceinsoumise.fr/emails/cab3c2ee-9444-4c70-b16e-9f7dce7929b1.html",
    # DONATION_MESSAGE_EUROPEENNES variables : [PROFILE_LINK]
    "DONATION_MESSAGE_EUROPEENNES": "https://mosaico.lafranceinsoumise.fr/emails/4b0f0d0d-e0a9-4264-8e69-143e9ba9fd48.html",
    # UNSUBSCRIBE_CONFIRMATION variables [MANAGE_SUBSCRIPTIONS_LINK]
    "UNSUBSCRIBE_CONFIRMATION": "https://mosaico.lafranceinsoumise.fr/emails/51cbadd7-2226-482d-85d4-6dc758d2eb3a.html",
    # GROUP_CREATION variables: [GROUP_NAME], [CONTACT_{NAME,EMAIL,PHONE,PHONE_VISIBILITY], [LOCATION_{NAME,LOCATION}], [GROUP_LINK], [MANAGE_GROUP_LINK]
    "GROUP_CREATION": "https://mosaico.lafranceinsoumise.fr/emails/bc07d593-ff8f-470e-a8cb-9ba679fc5f59.html",
    # GROUP_CHANGED variables: GROUP_NAME, GROUP_CHANGES, GROUP_LINK
    "GROUP_CHANGED": "https://mosaico.lafranceinsoumise.fr/emails/3724b7ba-2a48-4954-9496-fc4c970a56b8.html",
    # GROUP_SOMEONE_JOINED_NOTIFICATION variables: GROUP_NAME, PERSON_INFORMATION, MANAGE_GROUP_LINK
    "GROUP_SOMEONE_JOINED_NOTIFICATION": "https://mosaico.lafranceinsoumise.fr/emails/e25c5123-6a7d-428f-89c6-3ddca4a65096.html",
    # GROUP_EXTERNAL_JOIN_OPTION variables: [GROUP_NAME], [JOIN_LINK]
    "GROUP_EXTERNAL_JOIN_OPTIN": "https://mosaico.lafranceinsoumise.fr/emails/5c106c1d-a46f-4072-9c4e-2e3bfbfea069.html",
    # EVENT_CREATION variables: [EVENT_NAME], [CONTACT_{NAME,EMAIL,PHONE,PHONE_VISIBILITY], [LOCATION_{NAME,LOCATION}], [EVENT_LINK], [MANAGE_EVENT_LINK]
    "EVENT_CREATION": "https://mosaico.lafranceinsoumise.fr/emails/f44ff2c1-1050-41c4-8973-15573eba2741.html",
    # EVENT_CHANGED variables: EVENT_NAME, EVENT_CHANGES, EVENT_LINK, EVENT_QUIT_LINK
    "EVENT_CHANGED": "https://mosaico.lafranceinsoumise.fr/emails/f8dfc882-4e7e-4ff2-bd8c-473fd41e54bf.html",
    # EVENT_RSVP_NOTIFICATION variables EVENT_NAME, PERSON_INFORMATION, MANAGE_EVENT_LINK
    "EVENT_RSVP_NOTIFICATION": "https://mosaico.lafranceinsoumise.fr/emails/6f2eb6f0-cf59-4e2e-ab62-a8d204c6166b.html",
    # EVENT_RSVP_CONFIRMATION variables EVENT_NAME  EVENT_SCHEDULE CONTACT_NAME CONTACT_EMAIL LOCATION_NAME LOCATION_ADDRESS EVENT_LINK
    "EVENT_RSVP_CONFIRMATION": "https://mosaico.lafranceinsoumise.fr/emails/71fa1bc8-1b94-4d88-98dc-27c5502b83f8.html",
    # EVENT_EXTERNAL_RSVP_OPTIN variables EVENT_NAME RSVP_LINK
    "EVENT_EXTERNAL_RSVP_OPTIN": "https://mosaico.lafranceinsoumise.fr/emails/e7c3e2f6-1089-4f49-82a7-608ab038e6d3.html",
    # EVENT_GUEST_CONFIRMATION variables EVENT_NAME  EVENT_SCHEDULE CONTACT_NAME CONTACT_EMAIL LOCATION_NAME LOCATION_ADDRESS EVENT_LINK
    "EVENT_GUEST_CONFIRMATION": "https://mosaico.lafranceinsoumise.fr/emails/eded7af1-8ded-4150-a33c-b4902b34d54c.html",
    # EVENT_CANCELLATION variables: EVENT_NAME
    "EVENT_CANCELLATION": "https://mosaico.lafranceinsoumise.fr/emails/94c7cbb3-afdc-4d14-a07a-cf9503db5b5f.html",
    # EVENT_SECRETARIAT_NOTIFICATION variables : EVENT_NAME EVENT_SCHEDULE CONTACT_NAME CONTACT_EMAIL LOCATION_NAME LOCATION_ADDRESS EVENT_LINK LEGAL_INFORMATIONS
    "EVENT_SECRETARIAT_NOTIFICATION": "https://mosaico.lafranceinsoumise.fr/emails/d7ebb6a3-f693-4c33-934f-df4335b23621.html",
    # EVENT_ORGANIZER_VALIDATION_NOTIFICATION variables : EVENT_NAME EVENT_SCHEDULE LOCATION_NAME LOCATION_ADDRESS EVENT_LINK MANAGE_EVENT_LINK
    "EVENT_ORGANIZER_VALIDATION_NOTIFICATION": "https://mosaico.lafranceinsoumise.fr/emails/668ac434-423b-43b8-9ae0-6d1f3d29c3d4.html",
    # FORM_CONFIRMATION variables : CONFIRMATION_NOTE
    "FORM_CONFIRMATION": "https://mosaico.lafranceinsoumise.fr/emails/6172a755-0459-4f01-b3e4-fcfa835224b0.html",
    # FORM_NOTIFICATION variables : PERSON_EMAIL, INFORMATIONS
    "FORM_NOTIFICATION": "https://mosaico.lafranceinsoumise.fr/emails/45cd8bc1-8fb6-4ab6-bb67-739fd7e2e68e.html",
    # LOGIN_MESSAGE variables: CODE, EXPIRY_TIME
    "LOGIN_MESSAGE": "https://mosaico.lafranceinsoumise.fr/emails/65cb8867-9d14-4448-bae8-8cf40c5fee78.html",
    # EVENT_REPORT variables: EVENT_NAME,EVENT_REPORT_SUMMARY, EVENT_REPORT_LINK, PREFERENCES_LINK, EMAIL
    "EVENT_REPORT": "https://mosaico.lafranceinsoumise.fr/emails/7b39830d-8cf5-4d01-abbd-ab41e77c444e.html",
    # CHANGE_MAIL_CONFIRMATION variables: CONFIRMATION_URL
    "CHANGE_MAIL_CONFIRMATION": "https://mosaico.lafranceinsoumise.fr/emails/55429415-6611-45a9-8667-929e445ff7c4.html",
    # MERGE_ACCOUNT_CONFIRMATION variables: CONFIRMATION_URL, REQUESTER_EMAIL
    "MERGE_ACCOUNT_CONFIRMATION": "https://mosaico.lafranceinsoumise.fr/emails/4d727c1c-5319-416d-a747-37117d957aa1.html",
    # CONTRACT_CONFIRMATION
    "CONTRACT_CONFIRMATION": "https://mosaico.lafranceinsoumise.fr/emails/c63e76d7-d8a1-434c-bdd6-75337312ca28.html",
    # CHECK INFORMATION
    "CHECK_INFORMATION": "https://mosaico.lafranceinsoumise.fr/emails/fbf5b074-5ffd-479c-bb2a-76cf6cbcee10.html",
}

EMAIL_FROM = os.environ.get(
    "EMAIL_FROM", "La France insoumise <noreply@lafranceinsoumise.fr>"
)
EMAIL_SECRETARIAT = os.environ.get("EMAIL_SECRETARIAT", "nospam@lafranceinsoumise.fr")

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.environ.get("STATIC_ROOT")

STATICFILES_DIRS = [os.path.join(os.path.dirname(BASE_DIR), "assets")]

WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "components/",
        "STATS_FILE": os.path.join(
            STATICFILES_DIRS[0], "components", "webpack-stats.json"
        ),
    }
}

MEDIA_URL = "/media/"

MEDIA_ROOT = os.environ.get("MEDIA_ROOT", "media")

# Authentication

AUTH_USER_MODEL = "authentication.Role"

AUTHENTICATION_BACKENDS = [
    # Rules permission backend MUST be in first position
    "agir.clients.authentication.AccessTokenRulesPermissionBackend",
    # This backend is necessary to enforce database permissions
    "django.contrib.auth.backends.ModelBackend",
]

if ENABLE_API:
    # This backend is used to connect to the administration panel
    AUTHENTICATION_BACKENDS.append("agir.people.backend.PersonBackend")

if ENABLE_FRONT:
    AUTHENTICATION_BACKENDS.extend(
        [
            # This backend is used for email challenge connection
            "agir.authentication.backend.ShortCodeBackend",
            # This backend is used for connection through links found in emails
            "agir.authentication.backend.MailLinkBackend",
            # legacy backend only used to preserve currently connected sessions
            "agir.authentication.backend.OAuth2Backend",
        ]
    )
    LOGIN_URL = "short_code_login"

OAUTH2_PROVIDER_APPLICATION_MODEL = "clients.Client"
OAUTH2_PROVIDER = {"SCOPES_BACKEND_CLASS": "agir.clients.scopes.ScopesBackend"}

# Admin

OTP_TOTP_ISSUER = "api.lafranceinsoumise.fr"

# REST_FRAMEWORK

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        *(["rest_framework.renderers.BrowsableAPIRenderer"] if DEBUG else []),
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "agir.clients.authentication.AccessTokenAuthentication",
        "agir.clients.authentication.ClientAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("agir.lib.permissions.PermissionsOrReadOnly",),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework.renderers.MultiPartRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "EXCEPTION_HANDLER": "agir.api.handlers.exception_handler",
}

# Access tokens

AUTH_REDIS_URL = os.environ.get("AUTH_REDIS_URL", "redis://localhost?db=0")
AUTH_REDIS_MAX_CONNECTIONS = 5
AUTH_REDIS_PREFIX = os.environ.get("AUTH_REDIS_PREFIX", "AccessToken:")

LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING")
LOG_FILE = os.environ.get("LOG_FILE", "./errors.log")
LOG_DISABLE_JOURNALD = os.environ.get("LOG_DISABLE_JOURNALD", "").lower() in [
    "y",
    "yes",
    "true",
]

if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "journald": {
                "level": "DEBUG",
                "class": "systemd.journal.JournaldLogHandler"
                if not LOG_DISABLE_JOURNALD
                else "logging.StreamHandler",
            },
            "admins_mail": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
            },
        },
        "loggers": {
            "django.template": {
                "handlers": ["journald"],
                "level": "INFO",
                "propagate": False,
            },
            "django": {"handlers": ["journald"], "level": "DEBUG", "propagate": True},
            "celery": {"handlers": ["journald"], "level": "DEBUG", "propagate": True},
            "agir": {
                "handlers": ["journald", "admins_mail"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }

# CACHING
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("CACHING_REDIS_URL", "redis://localhost?db=0"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "caching_",
    }
}


# SECURITY
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIAL = False
CORS_URLS_REGEX = r"^/legacy/"

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

if not DEBUG:
    # should be useless, but we never know
    # SECURE_SSL_REDIRECT = True
    # removed because it created problems with direct HTTP connections on localhost
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

CRISPY_TEMPLATE_PACK = "bootstrap3"

# CELERY
CELERY_BROKER_URL = os.environ.get("BROKER_URL", "redis://")
# make sure there is a max_retries option
CELERY_BROKER_TRANSPORT_OPTIONS = {"max_retries": 2}
# make sure celery does not mess with the root logger
CELERY_WORKER_HIJACK_ROOT_LOGGER = DEBUG
# enable worker events to allow monitoring
CELERY_WORKER_SEND_TASK_EVENTS = True
# enable task events to allow monitoring
CELERY_TASK_SEND_SENT_EVENT = True

CELERY_RESULT_BACKEND = os.environ.get("BROKER_URL", "redis://")

DEFAULT_EVENT_IMAGE = "front/images/default_event_pic.jpg"

PHONENUMBER_DEFAULT_REGION = "FR"

CONNECTION_LINK_VALIDITY = 7

# allow insecure transports for OAUTHLIB in DEBUG mode
if DEBUG:
    os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "y")

# Get the promo
PROMO_CODE_KEY = os.environb.get(b"PROMO_CODE_KEY", b"prout")
PROMO_CODE_TAG = os.environ.get("PROMO_CODE_TAG", "Code promo matériel")
CERTIFIED_GROUP_SUBTYPES = os.environ.get(
    "CERTIFIED_GROUP_SUBTYPES", "certifié,thématique certifié"
).split(",")
if os.environ.get("PROMO_CODE_DELAY") is not None:
    year, month, day = (
        int(value) for value in os.environ.get("PROMO_CODE_DELAY").split("-")
    )
    PROMO_CODE_DELAY = make_aware(datetime(year, month, day))
else:
    PROMO_CODE_DELAY = None
CERTIFIABLE_GROUP_TYPES = ["L", "B"]  # groupes locaux  # groupes thématiques
CERTIFIABLE_GROUP_SUBTYPES = ["comité d'appui"]

# HTML settings
USER_ALLOWED_TAGS = [
    "a",
    "abbr",
    "acronym",
    "b",
    "br",
    "blockquote",
    "code",
    "em",
    "i",
    "li",
    "ol",
    "p",
    "strong",
    "ul",
    "h2",
    "h3",
    "h4",
]
ADMIN_ALLOWED_TAGS = USER_ALLOWED_TAGS + ["table", "tr", "td", "th"]

SITE_ID = 1

FILE_UPLOAD_PERMISSIONS = 0o644

PROMETHEUS_USER = os.environ.get("PROMETHEUS_USER", "prometheus")
PROMETHEUS_PASSWORD = os.environ.get("PROMETHEUS_PASSWORD", "password")

# Systempay
SYSTEMPAY_SITE_ID = os.environ.get("SYSTEMPAY_SITE_ID", 0)
SYSTEMPAY_PRODUCTION = os.environ.get("SYSTEMPAY_PRODUCTION", "false").lower() == "true"
SYSTEMPAY_CURRENCY = os.environ.get("SYSTEMPAY_CURRENCY", 978)
SYSTEMPAY_CERTIFICATE = os.environ.get("SYSTEMPAY_CERTIFICATE", "arbitrarystring")

SYSTEMPAY_AFCE_SITE_ID = os.environ.get("SYSTEMPAY_AFCE_SITE_ID", 0)
SYSTEMPAY_AFCE_PRODUCTION = (
    os.environ.get("SYSTEMPAY_AFCE_PRODUCTION", "false").lower() == "true"
)
SYSTEMPAY_AFCE_CERTIFICATE = os.environ.get(
    "SYSTEMPAY_AFCE_CERTIFICATE", "arbitrarystring"
)

SYSTEMPAY_AFCE_LOANS_SITE_ID = os.environ.get("SYSTEMPAY_AFCE_LOANS_SITE_ID", 0)
SYSTEMPAY_AFCE_LOANS_PRODUCTION = (
    os.environ.get("SYSTEMPAY_AFCE_LOANS_PRODUCTION", "false").lower() == "true"
)
SYSTEMPAY_AFCE_LOANS_CERTIFICATE = os.environ.get(
    "SYSTEMPAY_AFCE_LOANS_CERTIFICATE", "arbitrarystring"
)


DONATION_MINIMUM = 1
DONATION_MAXIMUM = 1000

LOAN_MINIMUM = 400
LOAN_MAXIMUM = 100000
LOAN_MAXIMUM_TOTAL = 207119700
LOAN_MAXIMUM_THANK_YOU_PAGE = (
    "https://lafranceinsoumise.fr/2019/04/07/succes-de-lemprunt-populaire/"
)

# France + most numerous communities in France
COUNTRIES_FIRST = ["FR", "PT", "DZ", "MA", "TR", "IT", "GB", "ES"]
COUNTRIES_FIRST_REPEAT = True

# allows the administrator to temporarily disable sending to specific domains
EMAIL_DISABLED_DOMAINS = (
    [d.lower() for d in os.environ.get("EMAIL_DISABLED_DOMAINS").split(",")]
    if "EMAIL_DISABLED_DOMAINS" in os.environ
    else []
)


# The first one will be the default one
PAYMENT_MODES = ["agir.system_pay.SystemPayPaymentMode", "agir.checks.CheckPaymentMode"]

# OVH Settings
OVH_SMS_DISABLE = os.environ.get("OVH_SMS_DISABLE", "true").lower() == "true"
OVH_SMS_SERVICE = os.environ.get("OVH_SMS_SERVICE")
OVH_APPLICATION_KEY = os.environ.get("OVH_APPLICATION_KEY")
OVH_APPLICATION_SECRET = os.environ.get("OVH_APPLICATION_SECRET")
OVH_CONSUMER_KEY = os.environ.get("OVH_CONSUMER_KEY")
SMS_BUCKET_MAX = 3
SMS_BUCKET_INTERVAL = 600
SMS_BUCKET_IP_MAX = 10
SMS_BUCKET_IP_INTERVAL = 600


# Short login codes settings
SHORT_CODE_VALIDITY = 90
MAX_CONCURRENT_SHORT_CODES = 3

CALENDAR_MAXIMAL_DEPTH = 3

# configuration PRESSERO
PRESSERO_API_URL = os.environ.get("PRESSERO_API_URL", "").rstrip("/")
PRESSERO_USER_NAME = os.environ.get("PRESSERO_USER_NAME")
PRESSERO_SUBSCRIBER_ID = os.environ.get("PRESSERO_SUBSCRIBER_ID")
PRESSERO_CONSUMER_ID = os.environ.get("PRESSERO_CONSUMER_ID")
PRESSERO_PASSWORD = os.environ.get("PRESSERO_PASSWORD")
PRESSERO_SITE = os.environ.get("PRESSERO_SITE", "").rstrip("/")
PRESSERO_APPROBATOR_ID = os.environ.get("PRESSERO_APPROBATOR_ID")
PRESSERO_GROUP_ID = os.environ.get("PRESSERO_GROUP_ID")

# nuntius
NUNTIUS_PUBLIC_URL = FRONT_DOMAIN
NUNTIUS_SUBSCRIBER_MODEL = "people.Person"
NUNTIUS_SEGMENT_MODELS = ["mailing.segment"]
NUNTIUS_CELERY_BROKER_URL = "redis://"
NUNTIUS_EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"
NUNTIUS_MOSAICO_TEMPLATES = [
    (
        "/static/mosaico_templates/versafix-blank/template.html",
        "Template sans bannière",
    ),
    ("/static/mosaico_templates/versafix-fi/template.html", "Template LFI"),
]

ANYMAIL = {
    "AMAZON_SES_CLIENT_PARAMS": {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_FOR_ANYMAIL_SES"),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_KEY_FOR_ANYMAIL_SES"),
        "region_name": "eu-west-1",
        "config": {"connect_timeout": 30, "read_timeout": 30},
    },
    "WEBHOOK_SECRET": os.environ.get("SENDGRID_SES_WEBHOOK_USER", "fi")
    + ":"
    + os.environ.get("SENDGRID_SES_WEBHOOK_PASSWORD", "fi"),
}

BANNER_CONFIG = {"thumbnail": (400, 250), "banner": (1200, 400)}

JITSI_GROUP_SIZE = 5
JITSI_SERVERS = os.environ.get("JITSI_SERVERS", "jitsi1.lafranceinsoumise.fr").split(
    ","
)
