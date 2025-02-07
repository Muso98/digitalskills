from pathlib import Path
from dotenv import load_dotenv
import os
from django.utils.translation import gettext_lazy as _
import dj_database_url
# .env faylni yuklash
load_dotenv()



BASE_DIR = Path(__file__).resolve().parent.parent


ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'modeltranslation',  # Django Model Translation
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'courses',
    'users',
    'rest_framework',
    'ckeditor',
    'ckeditor_uploader',  # Fayl yuklashni qo'llab-quvvatlash uchun

]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',  # Tilni aniqlash uchun middleware
    'django.middleware.security.SecurityMiddleware',
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



DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'postgres://digitalskills:12345@localhost:5432/digitalskills')
    )
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
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

LOGIN_REDIRECT_URL = '/users/'  # Login bo'lgandan keyin bosh sahifaga yo'naltiradi

#LOGIN_URL = '/users/login/'  # Tizimga kirish sahifasining URL'ini belgilang
