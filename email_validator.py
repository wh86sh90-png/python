import re

# (간단하면서 실무에서 흔히 쓰이는) 기본 이메일 정규식.
# 연속된 점(..)을 금지하는 전방탐색도 포함.
_pattern = re.compile(r"^(?!.*\.\.)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def is_valid_email(email: str) -> bool:
    """
    이메일이 유효하면 True, 아니면 False를 반환합니다.
    검사 규칙:
    - 전체 길이는 254자를 넘지 않음
    - 로컬파트(@ 앞)는 64자를 넘지 않음
    - 도메인 각 레이블은 63자를 넘지 않음, 빈 레이블이나 접두/접미 하이픈 금지
    - 연속된 점("..") 금지
    - 간단한 정규식으로 형식 확인(유효한 TLD 요구)
    """
    if not isinstance(email, str):
        return False
    if len(email) > 254:
        return False
    if not _pattern.fullmatch(email):
        return False

    try:
        local, domain = email.rsplit("@", 1)
    except ValueError:
        return False

    if len(local) > 64:
        return False
    if local.startswith(".") or local.endswith("."):
        return False
    # 도메인 전체 및 레이블 검사
    if domain.startswith("-") or domain.endswith("-"):
        return False
    labels = domain.split(".")
    for lbl in labels:
        if not lbl or len(lbl) > 63:
            return False
        if lbl.startswith("-") or lbl.endswith("-"):
            return False
    return True


def main():
    samples = [
        "alice@example.com",                                # valid
        "bob.smith+tag@sub.domain-example.co.uk",           # valid
        "charlie_123@domain.io",                            # valid
        ".startdot@domain.com",                             # invalid (로컬 시작 점)
        "enddot.@domain.com",                               # invalid (로컬 끝 점)
        "double..dot@domain.com",                           # invalid (연속 점)
        f'{"a"*65}@example.com',                            # invalid (로컬 길이 초과)
        "user@-domain.com",                                 # invalid (도메인 레이블 하이픈 시작)
        "user@domain..com",                                 # invalid (도메인 연속 점)
        "jane-doe@domain.co",                               # valid
    ]

    for e in samples:
        print(f"{e:40} -> {'VALID' if is_valid_email(e) else 'INVALID'}")


if __name__ == "__main__":
    main()