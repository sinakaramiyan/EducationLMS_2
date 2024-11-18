import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [

    # django-admin-interface
    "admin_interface",
    "colorfield",

    # main django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # whitenoise 
    'whitenoise.runserver_nostatic',
    
    # rosetta
    'rosetta',

    # django-extension
    'django_extensions',
    
    # django all-auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.microsoft',

    # Webpack Loader
    'webpack_loader',
    
    # apps
    'core',
    'role_management',
    'individual_course_management'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

if DEBUG:
    # Django debugger toolbar
    INSTALLED_APPS += ["debug_toolbar", ]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request'
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]


WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'education_LMS2', 
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# LANGUAGE_CODE = 'fa-ir'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    str(BASE_DIR.joinpath('static')),
    str(BASE_DIR.joinpath('static/static_build'))
]

STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))

MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.CustomUser'
DEFAULT_PROFILE_IMG = 'profile.png'

LOGIN_REDIRECT_URL = '/home'
LOGOUT_REDIRECT_URL = '/home'

# Whitenoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        # The directory where Webpack will output the bundled files
        'BUNDLE_DIR_NAME': 'static_build/', # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR.joinpath('static/static_build'),'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
        'LOADER_CLASS': 'webpack_loader.loader.WebpackLoader',
    }
}

# Django resized
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_SCALE = 0.5
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'WEBP'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".webp"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

# Django all-auth
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# This will allow you to test the signup process without actually 
# sending emails because in django all-auth when signup an email was sent to user
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Django all-auth custom forms
# ACCOUNT_FORMS = {'signup': 'core.forms.UserRegistrationForm'}

# Django-admin-interface
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]


# django-extension => graph models
GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}

# Rosetta
LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Persian')),
    # other languages
]

# Specify the paths where your translation files will be stored
LOCALE_PATHS = [
    str(BASE_DIR.joinpath('static/static_src/translations'))
]