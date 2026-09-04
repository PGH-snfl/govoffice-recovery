"""소스화 전 기관 함수를 원본 호환 facade에 연결한다."""

def 실행(한컴, 기능, *args, **kwargs):
    메서드 = getattr(한컴, 기능)
    return 메서드(*args, **kwargs)
