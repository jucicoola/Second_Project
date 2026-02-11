# 1. 아규먼트 유지로 유연한 버전 관리
ARG PYTHON_VERSION=3.12-slim
FROM python:${PYTHON_VERSION}

# 2. 파이썬 환경 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. [수정] 필수 시스템 패키지 추가 (psycopg2 및 Pillow 대응)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# 4. [수정] 캐시 최적화: 소스 복사 전 패키지 설치 완료
# 이렇게 하면 소스 코드를 고쳐도 패키지 설치 단계를 건너뜁니다.
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. 소스 코드 복사
COPY . /code/

# 6. 정적 파일 수집 (fly.toml의 statics 설정과 연동)
# 빌드 타임용 임시 키 주입
ENV SECRET_KEY="build-time-secret-key-only"
RUN python manage.py collectstatic --noinput

# 7. 포트 설정 (fly.toml의 internal_port=8000과 일치)
EXPOSE 8000

# 8. [수정] 실행 명령 최적화 (0.0.0.0 바인딩 명시)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "config.wsgi:application"]