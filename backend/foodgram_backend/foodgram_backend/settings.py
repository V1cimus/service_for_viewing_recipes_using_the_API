import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure--vztlg$$te7_urbg$wm)4ard8fznt6^ehhnkgivo0vyvhi&h)g'

DEBUG = False

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'http://158.160.61.84',
    'http://127.0.0.1',
    'https://158.160.61.84',
    'https://127.0.0.1',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'colorfield',
    'djoser',

    'users',
    'posts',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default="django.db.backends.postgresql"),
        'NAME': os.getenv('DB_NAME', default=None),
        'USER': os.getenv('POSTGRES_USER', default=None),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default=None),
        'HOST': os.getenv('DB_HOST', default=None),
        'PORT': os.getenv('DB_PORT', default=None)
    }
}

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

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 6,
}

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_L10N = True

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'),)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = "users.User"

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SET_PASSWORD_RETYPE': False,
    'HIDE_USERS': False,
    'SEND_ACTIVATION_EMAIL': False,
    'TOKEN_MODEL': 'rest_framework.authtoken.models.Token',
    'TOKEN_CREATE_MODEL': 'rest_framework.authtoken.models.Token',
    'TOKEN_DESTROY_MODEL': 'rest_framework.authtoken.models.Token',
    'SERIALIZERS': {
        'user': 'api.serializers.UsersSerializer',
        'user_create': 'api.serializers.UserCreateSerializer',
        'current_user': 'api.serializers.UsersSerializer',
    },
    'PERMISSIONS': {
        'user': ['djoser.permissions.CurrentUserOrAdminOrReadOnly',],
        'user_list': ['rest_framework.permissions.IsAuthenticatedOrReadOnly',],
    }
}
