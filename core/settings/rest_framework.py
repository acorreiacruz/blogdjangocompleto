from datetime import timedelta
from .installed_apps import INSTALLED_APPS
import os

INSTALLED_APPS += ['rest_framework', 'rest_framework_simplejwt', 'corsheaders',]

REST_FRAMEWORK = {
    'DEFAULT_RENDERERS_CLASSES':[
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=180),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'SIGNING_KEY': os.environ.get('SECRET_KEY'),
    'AUTH_HEADER_TYPES': ('Bearer',)
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
]
