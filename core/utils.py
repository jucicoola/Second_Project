def mask_account_number(account_number):
    """계좌번호 마스킹: 110-123-456789 -> 110-****-6789"""
    if not account_number:
        return ''
    
    parts = account_number.split('-')
    if len(parts) == 3:
        return f"{parts[0]}-****-{parts[2][-4:]}"
    
    if len(account_number) > 8:
        return account_number[:3] + '****' + account_number[-4:]
    
    return account_number

## 질문 : 실제 계좌번호 인증 API 연결을 어떻게 하지? PG사, Toss 에 연결