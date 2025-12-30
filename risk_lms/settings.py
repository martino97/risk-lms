# Session timeout: expire after 5 minutes (300 seconds) of inactivity
SESSION_COOKIE_AGE = 300  # 5 minutes
SESSION_SAVE_EVERY_REQUEST = True
"""
Django settings for Risk LMS project.
Co-operative Bank of Tanzania PLC - Risk Department LMS
"""
from pathlib import Path
import os
import secrets

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# ENVIRONMENT DETECTION
# =============================================================================
# Set DJANGO_ENV to 'production' on the server, defaults to 'development'
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'development')
IS_PRODUCTION = ENVIRONMENT == 'production'

# =============================================================================
# SECURITY SETTINGS
# =============================================================================
# Generate a secure key or use from environment
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-temp-key-for-development-only')

# Debug mode - ALWAYS False in production
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes') if not IS_PRODUCTION else False

# Allowed hosts for the application
ALLOWED_HOSTS_STR = os.environ.get('ALLOWED_HOSTS', 'localhost, 127.0.0.1, cooplms.coopbank.co.tz')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR.split(',')]

# Add common development hosts if not in production
if not IS_PRODUCTION:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '*'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Local apps
    'accounts',
    'courses',
    'videos',
    'quizzes',
    'progress',
    'certificates',
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

ROOT_URLCONF = 'risk_lms.urls'

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

WSGI_APPLICATION = 'risk_lms.wsgi.application'

# Database Configuration
# Using Microsoft SQL Server for production

# Get database settings from environment variables or use defaults
DB_ENGINE = os.environ.get('DB_ENGINE', 'mssql')
DB_NAME = os.environ.get('DB_NAME', 'risk_lms')
DB_HOST = os.environ.get('DB_HOST', 'KCBLSMS-GATEWAY\\MSSQLSERVER02')
DB_USER = os.environ.get('DB_USER', 'sa2')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Pondrch@999')

if DB_ENGINE == 'mssql':
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': '',
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
                'TrustServerCertificate': 'yes',
            },
        }
    }

elif DB_ENGINE == 'sqlite':
    # SQLite for local development/testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # PostgreSQL (alternative)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': DB_HOST,
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Authentication Backends
# Order matters: LDAP first, then Django's default for local users
AUTHENTICATION_BACKENDS = [
    'accounts.ldap_backend.LDAPBackend',  # Active Directory authentication
    'django.contrib.auth.backends.ModelBackend',  # Fallback for local users
]

# LDAP/Active Directory Configuration
LDAP_CONFIG = {
    'DOMAIN': 'KCBLTZ.CRDBBANKPLC.COM',
    'SERVERS': [
        '192.168.10.50',  # Primary DNS
        '192.168.10.10',  # Alternate DNS
    ],
    'BASE_DN': 'DC=KCBLTZ,DC=CRDBBANKPLC,DC=COM',
    'PORT': 389,
    'USE_SSL': False,  # Set to True for LDAPS (port 636)
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Use WhiteNoise for static file serving in production
if IS_PRODUCTION:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# JWT Settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 2147483648  # 2GB
DATA_UPLOAD_MAX_MEMORY_SIZE = 2147483648

# Celery Configuration (for video processing)
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Video processing settings
VIDEO_ALLOWED_EXTENSIONS = ['mp4', 'mov', 'avi', 'mkv']
SUBTITLE_ALLOWED_EXTENSIONS = ['vtt', 'srt']

# Certificate settings
CERTIFICATE_QR_SIZE = 200
CERTIFICATE_BASE_URL = os.environ.get('CERTIFICATE_BASE_URL', 'http://localhost:8000')

# Email settings (for certificate delivery)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Login URL
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Allow iframe embedding for interactive courses
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Security settings for development
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

# =============================================================================
# PRODUCTION SECURITY SETTINGS
# =============================================================================
if IS_PRODUCTION:
    # HTTPS/SSL Settings
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() in ('true', '1', 'yes')
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Session Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_AGE = 28800  # 8 hours
    
    # CSRF Security
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_TRUSTED_ORIGINS = [
        'https://risklms.cbtbank.co.tz',
        'https://localhost',
    ]
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Content Security
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    
    # Logging configuration for production
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR / 'logs' / 'django_error.log',
                'formatter': 'verbose',
            },
            'security_file': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR / 'logs' / 'security.log',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.security': {
                'handlers': ['security_file'],
                'level': 'WARNING',
                'propagate': False,
            },
        },
    }
