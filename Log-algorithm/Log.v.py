@public
def log(a: num, b: num) -> num:
    assert a > 0
    assert b > 1
    _a: num
    _a = a
    c: num
    c = 0
    for _ in range(256):
        if (_a < b): break
        _a /= b
        c += 1
    return c
