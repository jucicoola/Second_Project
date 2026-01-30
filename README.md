# TravelBank - 여행 경비 관리 시스템

Django 기반의 개인 여행 경비 관리 웹 애플리케이션입니다.

## 주요 기능

- ✅ 사용자 인증 (회원가입, 로그인, 로그아웃)
- ✅ 계좌 관리 (생성, 조회, 수정, 삭제)
- ✅ 여행 관리 (생성, 조회, 수정, 삭제)
- ✅ 거래 관리 (입출금 내역 기록, 필터링, 검색)
- ✅ 영수증 첨부 (이미지/PDF 업로드)
- ✅ 대시보드 (월별/카테고리별 통계)
- ✅ 계좌번호 마스킹 (보안 처리)
- ✅ 본인 데이터 접근 제한

## 기술 스택

- **Backend**: Django 5.0
- **Frontend**: HTML, CSS (JavaScript 미사용)
- **Database**: SQLite (개발), PostgreSQL 지원 가능
- **파일 처리**: Pillow (이미지 처리)

## 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd travelbank
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정

```bash
cp .env.example .env
# .env 파일을 열어 SECRET_KEY 등 설정 수정
```

### 5. 데이터베이스 마이그레이션

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 초기 카테고리 데이터 생성

```bash
python scripts/init_categories.py
```

### 7. 관리자 계정 생성

```bash
python manage.py createsuperuser
```

### 8. 개발 서버 실행

```bash
python manage.py runserver
```

브라우저에서 `http://localhost:8000` 접속

## 프로젝트 구조

```
travelbank/
├── config/                 # 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                   # Django 앱
│   ├── accounts/          # 사용자 인증 및 계좌 관리
│   ├── trips/             # 여행 관리
│   ├── transactions/      # 거래 관리
│   └── dashboard/         # 대시보드
├── core/                  # 공통 유틸리티
│   ├── mixins.py
│   ├── validators.py
│   └── templatetags/
├── static/                # 정적 파일 (CSS)
├── media/                 # 업로드 파일 (영수증)
├── templates/             # HTML 템플릿
├── scripts/               # 유틸리티 스크립트
└── manage.py
```

## 주요 URL

- `/` - 대시보드 (로그인 후 리다이렉트)
- `/accounts/signup/` - 회원가입
- `/accounts/login/` - 로그인
- `/accounts/` - 계좌 목록
- `/trips/` - 여행 목록
- `/transactions/` - 거래 목록
- `/dashboard/` - 대시보드
- `/admin/` - 관리자 페이지

## 보안 기능

1. **비밀번호 암호화**: Django PBKDF2 해시 사용
2. **CSRF 보호**: 모든 POST 요청에 CSRF 토큰 적용
3. **계좌번호 마스킹**: 화면/로그에서 자동 마스킹
4. **본인 데이터 접근 제한**: UserOwnershipMixin 적용
5. **파일 업로드 검증**: 확장자, 크기 제한

## 테스트

```bash
# 전체 테스트 실행
python manage.py test

# 특정 앱 테스트
python manage.py test apps.accounts
python manage.py test apps.trips
python manage.py test apps.transactions
```

## 배포

### 프로덕션 설정

1. `.env` 파일 수정:
```
DEBUG=False
SECRET_KEY=<강력한-시크릿-키>
ALLOWED_HOSTS=yourdomain.com
```

2. 정적 파일 수집:
```bash
python manage.py collectstatic
```

3. 데이터베이스 설정 (PostgreSQL 권장):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travelbank',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 문제 해결

### 마이그레이션 충돌
```bash
python manage.py makemigrations --merge
python manage.py migrate
```

### 정적 파일이 로드되지 않을 때
```bash
python manage.py collectstatic --clear
```

### 데이터베이스 초기화
```bash
rm db.sqlite3
python manage.py migrate
python scripts/init_categories.py
```

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트는 언제든 환영합니다!

## 개발 로드맵

- [ ] 다중 통화 지원
- [ ] CSV 내보내기 기능
- [ ] 예산 설정 및 알림
- [ ] 영수증 OCR 기능
- [ ] 모바일 앱 개발

## 문의

프로젝트 관련 문의사항은 이슈를 통해 남겨주세요.
