import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    """파일 확장자 검증"""
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    if ext not in valid_extensions:
        raise ValidationError(
            f'허용되지 않는 파일 형식입니다. 허용: {", ".join(valid_extensions)}'
        )

def validate_file_size(value):
    """파일 크기 검증 (5MB 제한)"""
    filesize = value.size
    max_size = 5 * 1024 * 1024  # 5MB
    if filesize > max_size:
        raise ValidationError(
            f'파일 크기는 5MB를 초과할 수 없습니다. (현재: {filesize / 1024 / 1024:.2f}MB)'
        )
