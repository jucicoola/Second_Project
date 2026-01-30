from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class UserOwnershipMixin(LoginRequiredMixin):
    """본인 소유 객체만 접근 가능"""
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if hasattr(obj, 'user') and obj.user != self.request.user:
            raise PermissionDenied("이 데이터에 접근할 권한이 없습니다.")
        return obj
