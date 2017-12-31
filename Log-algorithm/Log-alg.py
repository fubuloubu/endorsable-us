# Viper logarithm alg emulated in Python
# NOTE 107,707 gas when implemented in viper
def log(a, b):
    assert a > 0 # log_b(0) incomputable
    assert b > 1 # log_1(a) or log_0(a) incomputable
    c = 0
    # This algorithm handles log_2(MAX_NUM256)
    # Which is the largest possible iterations needed
    for _ in range(256):
        if (a < b):
            break
        a = a // b # Floor division (emulates EVM)
        c += 1
    return c

# Testing

import math
from hypothesis import given, example, settings
from hypothesis.strategies import data, integers
# a cannot be 0, b cannot be 0 or 1, neither can exceed num256 MAX
@given(a=integers(1, 2**255), b=integers(2, 2**255))
@example(3, 2) # Base case, should be 1 (actual is 1.58...)
@example(4, 3) # Base case, should be 1 (actual is 1.26...)
@example(10**30, 10) # Python approximates this to 29.9999..., our alg returns 30
@example(2**255, 2) # Maximum number of iterations
@example(78**13-1, 78**13) # Python rounds this to 1.0, our alg returns 0
@example(78**13+1, 78**13) # Python rounds this to 1.0, our alg returns 1
@settings(max_examples=1e6) # 1m examples
def test_log(a, b):
    alg = log(a, b)
    c = math.log(a, b) # Python's function isn't precise enough sometimes
    # The following ensures flt-pt errors for things like log_10(10**30) work out
    actual = round(c) if b**round(c) <= a else c-1 if c % 1 == 0 else math.floor(c)
    assert alg == actual, "{} != round({})".format(alg, c)

if __name__ == '__main__':
    test_log()
