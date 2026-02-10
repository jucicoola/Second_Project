
# ## 질문 : 실제 계좌번호 인증 API 연결을 어떻게 하지? PG사, Toss 에 연결


def mask_account_number(account_number):
    """
    1. 하이픈(-)이 있는 경우: 두 번째 섹션(index 1)을 해당 길이만큼 마스킹
    2. 하이픈(-)이 없는 경우:
       - 앞 4자리 숫자 노출
       - 중간 최대 4자리를 '*'로 마스킹
       - 9번째 자리부터 나머지 숫자 노출
    """
    if not account_number:
        return ''

    # 1. 하이픈(-)이 있는 경우
    if '-' in account_number:
        parts = account_number.split('-')
        if len(parts) > 1:
            parts[1] = '*' * len(parts[1])   
            return '-'.join(parts)
        return account_number

    # 2. 하이픈(-)이 없는 경우
    else:
        length = len(account_number)
        if length <= 4:
            return account_number

        prefix = account_number[:4]                      # 앞 4자리
        masked = '*' * min(4, length - 4)                
        suffix = account_number[8:]                      # 9번째 자리부터 끝

        return f"{prefix}{masked}{suffix}"
