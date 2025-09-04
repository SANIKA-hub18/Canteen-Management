from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# BASE DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY
SECRET_KEY = 'django-insecure-c5)td6nx+c#n36_i_jn#&q7af98i#&^bxvr_rif!&+n9d9rt_+'

# DEBUG MODE
DEBUG = True

# ALLOWED HOSTS (for local and Render)
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'qr-code-scanner-and-generator.onrender.com',
    'canteen-management-wwmm.onrender.com'
]

# Load .env variables
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'qr',  # your app
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

ROOT_URLCONF = 'qrapp.urls'

# ✅ Templates Config for dashboard.html
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "qr" / "templates"],
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

WSGI_APPLICATION = 'qrapp.wsgi.application'

# ✅ Database Setup → MySQL (canteen_management)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'canteen_management',
        'USER': 'root',
        'PASSWORD': 'sanika',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# ✅ Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ Language and Time
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static files settings for Render + dashboard.html CSS/JS
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # development
STATIC_ROOT = BASE_DIR / 'staticfiles'    # production (collectstatic)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'shaligramsanika@gmail.com'
EMAIL_HOST_PASSWORD = 'rgnw gcjc lwib naja'  # Gmail App Password वापर
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
