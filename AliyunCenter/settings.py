"""
Django settings for AliyunCenter project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^e5^4ke_==y)9tu&(y^e(1nql%7sdau6i(-*m320=0(w5cor8l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['cmdb.godeng.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'aliecs',
    'django_celery_beat',
    'user',
    'ops',
    'tools',
    'worktickets',
    'gunicorn',
    'django_filters',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'AliyunCenter.middleware.SetRemoteAddrFromForwardedFor',
    'AliyunCenter.middleware.DisableCSRFCheck',
]

ROOT_URLCONF = 'AliyunCenter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'AliyunCenter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DB_OPTIONS = {}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oms',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'oms',
        'PASSWORD': '!@#$QWER000',
        'ATOMIC_REQUESTS': True,
    }
}

# Cache use redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:%(password)s@%(host)s:%(port)s/%(db)s' % {
            'password': '',
            'host': '127.0.0.1',
            'port': '6379',
            'db': '4',
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = '/opt/static/pstatic/'
STATIC_URL = '/pstatic/'

STATICFILES_DIRS = (
    os.path.join(os.path.join(BASE_DIR, 'static')),
)

# Celery
CELERY_BROKER_URL = 'redis://:%(password)s@%(host)s:%(port)s/%(db)s' % {
    'password': '',
    'host': '127.0.0.1',
    'port': '6379',
    'db': '6',
}
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_RESULT_EXPIRES = 3600
CELERY_CONCURRENCY = 1
CELERY_MAX_TASKS_PER_CHILD = 5
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_WORKER_REDIRECT_STDOUTS = True
CELERY_FORCE_EXECV = True
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# 修改默认用户表
AUTH_USER_MODEL = 'user.User'


# drf认证
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}


import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=2),
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=2),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}


# 用户验证重写
AUTHENTICATION_BACKENDS = (
    'user.views.CustomBackend',
)

