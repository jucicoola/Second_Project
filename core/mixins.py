from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class UserOwnershipMixin(LoginRequiredMixin):
    """
    본인 소유 객체만 접근 가능하도록 제한하는 믹스인.
    단, 관리자(Superuser)는 모든 데이터에 접근할 수 있습니다.
    """
    
    def get_queryset(self):
        # 1. 관리자(Superuser)인 경우 전체 데이터셋 반환
        if self.request.user.is_superuser:
            return super().get_queryset()
        # 2. 일반 사용자는 본인 데이터만 필터링
        return super().get_queryset().filter(user=self.request.user)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # 1. 관리자(Superuser)인 경우 즉시 객체 반환 (검증 패스)
        if self.request.user.is_superuser:
            return obj
            
        # 2. 일반 사용자는 객체의 소유권을 확인
        if hasattr(obj, 'user') and obj.user != self.request.user:
            raise PermissionDenied("이 데이터에 접근할 권한이 없습니다.")
            
        return obj