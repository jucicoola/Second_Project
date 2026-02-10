from django.apps import AppConfig # 앱 설정용 기본 클래스 

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # 모델에서 id 자동 생성할 때 기본 타입 지정
    name = 'apps.accounts' # 앱 경로 apps/accounts
    verbose_name = '계좌 관리' # Django Admin 화면에서 보이는 앱 이름