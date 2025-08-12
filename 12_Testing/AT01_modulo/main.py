def safe_modulo(a: int, b: int) -> int:
    if b == 0:
        return None
    return a % b