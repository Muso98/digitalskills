from pathlib import Path
from dotenv import load_dotenv
import os
from django.utils.translation import gettext_lazy as _
import dj_database_url
# .env faylni yuklash
load_dotenv()

DEBUG=False


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-default-key")


ALLOWED_HOSTS = ['digitalskills.onrender.com', 'localhost', '127.0.0.1']


CSRF_TRUSTED_ORIGINS = [
    "https://digitalskills.onrender.com",  # Render yoki hosting domeningiz
]

INSTALLED_APPS = [
    'modeltranslation',  # Django Model Translation
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',  # Whitenoise statik fayllarni xizmat qilish uchun
    'courses',
    'users',
    'rest_framework',
    'ckeditor',
    'ckeditor_uploader',  # Fayl yuklashni qo'llab-quvvatlash uchun

]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',  # Tilni aniqlash uchun middleware
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'digitalskills.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'digitalskills.wsgi.application'



DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
else:
    print("⚠️ WARNING: DATABASE_URL environment variable is not set!")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'digitalskills'),
            'USER': os.getenv('DB_USER', 'digitalskills'),
            'PASSWORD': os.getenv('DB_PASSWORD', '12345'),
            'HOST': 'localhost',
            'PORT': '5432',

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

LANGUAGES = [
    ('uz', _('O‘zbekcha')),
    ('ru', _('Русский')),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
MODELTRANSLATION_LANGUAGES = ('uz', 'ru')

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'UTC'

USE_I18N = True

# Django'ga tarjimalarni qayerdan olishni aytish
LOCALE_PATHS = [BASE_DIR / 'locale']


USE_TZ = True

CKEDITOR_UPLOAD_PATH = "uploads/"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

LOGIN_REDIRECT_URL = '/users/'  # Login bo'lgandan keyin bosh sahifaga yo'naltiradi

#LOGIN_URL = '/users/login/'  # Tizimga kirish sahifasining URL'ini belgilang
