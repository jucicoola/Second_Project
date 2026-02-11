import os
from pathlib import Path
from decouple import config
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-me')
SECRET_KEY = (
    os.environ.get("DJANGO_SECRET_KEY")
    or os.environ.get("SECRET_KEY")
    or "ci-dev-secret-key"
    )
DEBUG = os.environ.get("DEBUG", "0") == "1"

# DEBUG = config('DEBUG', default=True, cast=bool)
# DEBUG = True
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
# ALLOWED_HOSTS = ["django-first2.fly.dev", "localhost", "127.0.0.1"]
# CSRF_TRUSTED_ORIGINS = ["https://django-first2.fly.dev"]

# 기존 설정은 주석 처리하거나 지우고 아래 내용을 넣으세요.
ALLOWED_HOSTS = ["django-second-project.fly.dev", "localhost", "127.0.0.1"]

# CSRF 설정을 반드시 해주어야 어드민 페이지 로그인이 가능합니다.
CSRF_TRUSTED_ORIGINS = ["https://django-second-project.fly.dev"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'apps.accounts',
    'apps.trips',
    'apps.transactions',
    'apps.dashboard',
    'apps.main',
    'django.contrib.humanize',  # 이 줄을 추가하세요!
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# 기존의 복잡한 DATABASES 설정 전체를 아래로 교체하세요.
DATABASES = {
    'default': dj_database_url.config(
        # DATABASE_URL 환경변수가 없을 때만 SQLite를 사용하도록 설정
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# Fly.io에서 제공하는 DATABASE_URL은 SSL 설정이 포함되어 있지 않을 수 있으므로
# 아래 설정을 추가하여 Postgres 연결 시 에러를 방지합니다.
if os.environ.get("DATABASE_URL"):
    DATABASES["default"]["OPTIONS"] = {"sslmode": "disable"}



# DATABASES = {
#     "default": dj_database_url.config(
#         default=f"postgresql://{os.environ.get('POSTGRES_USER','django_myuser')}:"
#                 f"{os.environ.get('POSTGRES_PASSWORD','strong-password')}@"
#                 f"{os.environ.get('POSTGRES_HOST','127.0.0.1')}:"
#                 f"{os.environ.get('POSTGRES_PORT','5432')}/"
#                 f"{os.environ.get('POSTGRES_DB','second_project_db')}",
#         conn_max_age=600,
#         ssl_require=bool(os.environ.get("DATABASE_URL")),
#     )
# }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("POSTGRES_DB", "second_project_db"),
#         "USER": os.environ.get("POSTGRES_USER", "django_myuser"),
#         "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "strong-password"),
#         "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
#         "PORT": os.environ.get("POSTGRES_PORT", "5432"),
#     },
#     conn_max_age=600,
#     ssl_require=bool(os.environ.get("DATABASE_URL")),  # Fly에서만 SSL 강제
    
# }


# # DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get('DATABASE_URL'),
#         conn_max_age=600
#     )
# }

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or "ci-dev-secret-key"


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'


if not DEBUG:
    # 이 줄을 반드시 추가하세요! (Fly.io 프록시 설정)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # 무한 루프 방지를 위해 일단 False로 바꾸거나 주석 처리하고 배포해 보세요.
    SECURE_SSL_REDIRECT = False  
    
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
# if not DEBUG:
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_HSTS_SECONDS = 31536000
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True