# settings.py 

from pathlib import Path
import os
from dotenv import load_dotenv

# -------------------------------------------------------------------
# 기본 경로 & .env 로드
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# .env 파일 명시적으로 로드
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# 환경변수에서 DEBUG 가져오기 (기본값 True)
DEBUG = os.getenv("DEBUG", "True") == "True"

if not SECRET_KEY:
  raise ValueError("SECRET_KEY 환경 변수가 비어 있습니다. .env 파일을 확인하세요!")

ALLOWED_HOSTS: list[str] = []

# -------------------------------------------------------------------
# 앱 설정
# -------------------------------------------------------------------
INSTALLED_APPS = [
    # third-party
    'corsheaders',
    'rest_framework',
    'movies',

    # django 기본 앱들
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# -------------------------------------------------------------------
# 미들웨어
# -------------------------------------------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # 🔻 이 줄 주석 처리 or 삭제
    # 'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'my_movies.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_movies.wsgi.application'

# -------------------------------------------------------------------
# 데이터베이스
# -------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------------------------------------------------------
# 비밀번호 정책
# -------------------------------------------------------------------
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

# -------------------------------------------------------------------
# 국제화
# -------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'   # 원하면 'Asia/Seoul' 로 바꿔도 됨

USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# 정적 파일
# -------------------------------------------------------------------
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------------------
# DRF / JWT 설정
# -------------------------------------------------------------------
REST_FRAMEWORK = {
    # ✅ 세션/베이식 인증 제거 → CSRF 이슈 피함
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# -------------------------------------------------------------------
# CORS / CSRF 설정
# -------------------------------------------------------------------

# 프론트 개발 서버 도메인만 허용
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

# Origin 체크(403) 피하기 위해 신뢰 도메인 등록
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

# 필요하다면 쿠키 기반 CORS 옵션도 추가할 수 있지만
# 지금은 JWT 헤더만 쓰니까 기본 값 그대로 둬도 됨.
