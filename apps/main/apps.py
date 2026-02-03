from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 'main'으로 되어 있다면 'apps.main'으로 수정해야 합니다.
    name = 'apps.main'
