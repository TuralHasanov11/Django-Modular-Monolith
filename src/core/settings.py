import os
from pathlib import Path

import dj_database_url
from django.contrib import messages
from django.utils.log import DEFAULT_LOGGING
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = int(os.environ.get("DEBUG", 0)) == 1

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",") or []
if DEBUG:
    ALLOWED_HOSTS += ["127.0.0.1", "localhost"]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "").split(",") or []
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SITE_ID = 1

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "rosetta",
    "log_viewer",
    "rest_framework",
    "corsheaders",
    "csp",
    'axes',
    'simple_history',
    "apps.shared",
    "apps.main",
    "apps.users",
    "apps.identity",
    "apps.blog"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'simple_history.middleware.HistoryRequestMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "csp.middleware.CSPMiddleware",
    
    "axes.middleware.AxesMiddleware", # should be last
]

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "csp.context_processors.nonce"
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

if int(os.environ.get("POSTGRES_DB_READY", 0)) == 1:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
    }

DATABASE_URL = os.environ.get("DATABASE_URL", None)
if DATABASE_URL:
    db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=1800)
    DATABASES["default"].update(db_from_env)

AUTH_USER_MODEL = "identity.IdentityUser"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 12,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LOGIN_URL = "identity:login"
LOGIN_REDIRECT_URL = "main:home"


TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGE_CODE = "en"

LANGUAGES = (
    ("en", _("English")),
    ("ru", _("Russian")),
)

LOCALE_PATHS = (BASE_DIR / "locale/",)

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = "/static/"
STATIC_ROOT: str = os.path.join(BASE_DIR, "static_cdn")

# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

if not DEBUG:
    STATIC_ROOT: str = os.path.join(BASE_DIR, "static_cdn")

MEDIA_URL = "/media/"
if not DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get("MEDIA_ROOT", "media"))
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOG_DIR = BASE_DIR / "logs"
LOG_FILE = "/main.log"
LOG_PATH = f"{LOG_DIR}/{LOG_FILE}"
CRON_LOG_FILE = "/cron.log"
CRON_LOG_PATH = f"{LOG_DIR}/{CRON_LOG_FILE}"

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

if not os.path.exists(LOG_PATH):
    f = open(LOG_PATH, "w").close()
else:
    f = open(LOG_PATH, "a").close()

if not os.path.exists(CRON_LOG_PATH):
    f = open(CRON_LOG_PATH, "w").close()
else:
    f = open(CRON_LOG_PATH, "a").close()

LOGGING_CONFIG = None
LOGLEVEL = os.environ.get("LOGLEVEL", "info").upper()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s at %(name)-2s in %(module)s with level %(levelname)-2s : %(message)s",
        },
        "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": LOGLEVEL,
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "level": LOGLEVEL,
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": LOG_PATH,
            "encoding": "utf8",
        },
        "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
    },
    "loggers": {
        "": {
            "level": LOGLEVEL,
            "handlers": ["file", "console"],
        },
        "django": {
            "handlers": ["file", "console"],
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
    },
}

LOG_VIEWER_FILES = ["main.log", "cron.log"]
LOG_VIEWER_FILES_PATTERN = "*.log*"
LOG_VIEWER_FILES_DIR = "logs/"
LOG_VIEWER_PAGE_LENGTH = 25
LOG_VIEWER_MAX_READ_LINES = 1000
LOG_VIEWER_FILE_LIST_MAX_ITEMS_PER_PAGE = 25
LOG_VIEWER_PATTERNS = ["[INFO]", "[DEBUG]", "[WARNING]", "[ERROR]", "[CRITICAL]"]
LOG_VIEWER_EXCLUDE_TEXT_PATTERN = None


MESSAGE_TAGS = {
    messages.constants.DEBUG: "alert-secondary",
    messages.constants.INFO: "alert-info",
    messages.constants.SUCCESS: "alert-success",
    messages.constants.WARNING: "alert-warning",
    messages.constants.ERROR: "alert-danger",
}

CORS_URLS_REGEX = r"^/api/.*$"
CORS_ALLOWED_ORIGIN_REGEXES = os.environ.get("ALLOWED_ORIGINS", "").split(",") or []

AXES_ENABLED = True
AXES_COOLOFF_TIME = float(os.environ.get("AXES_COOLOFF_TIME", 0.25))
AXES_FAILURE_LIMIT = int(os.environ.get("AXES_FAILURE_LIMIT", 10))
AXES_RESET_ON_SUCCESS = True
AXES_USERNAME_FORM_FIELD = "email"
AXES_LOCKOUT_CALLABLE = "apps.identity.views.lockout"
AXES_LOCKOUT_TEMPLATE = "apps.identity/lockout.html"
AXES_LOCKOUT_PARAMETERS = [["username", "user_agent"]]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")
EMAIL_BACKEND = "django_smtp_ssl.SSLEmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", "")
EMAIL_USE_TLS = int(os.environ.get("EMAIL_USE_TLS", 0)) == 1
EMAIL_USE_SSL = int(os.environ.get("EMAIL_USE_SSL", 0)) == 1
EMAIL_USE_LOCALTIME = True

SIMPLE_HISTORY_HISTORY_ID_USE_UUID = True
SIMPLE_HISTORY_ENFORCE_HISTORY_MODEL_PERMISSIONS = True
SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD=True

MAINTENANCE_MODE = int(os.environ.get("MAINTENANCE_MODE", 0))
MAINTENANCE_BYPASS_QUERY = os.environ.get("MAINTENANCE_BYPASS_QUERY")


CSP_NONE = "'none'"
CSP_SELF = "'self'"
CSP_STRICT_DYNAMIC = "'strict-dynamic'"
CSP_NONCE = "'nonce'"

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": [CSP_SELF],
        "frame-ancestors": [CSP_SELF],
        "form-action": [CSP_SELF],
        "script-src": [CSP_SELF, CSP_STRICT_DYNAMIC, CSP_NONCE],
        "style-src": [CSP_SELF],
        "report-uri": "/csp-report/",
        "img-src": [CSP_SELF, "data:"],
    },
}

CONTENT_SECURITY_POLICY_REPORT_ONLY = {
    "DIRECTIVES": {
        "default-src": [CSP_NONE],
        "connect-src": [CSP_SELF],
        "img-src": [CSP_SELF],
        "form-action": [CSP_SELF],
        "frame-ancestors": [CSP_SELF],
        "script-src": [CSP_SELF],
        "style-src": [CSP_SELF],
        "upgrade-insecure-requests": True,
        "report-uri": "/csp-report/",
    },
}
