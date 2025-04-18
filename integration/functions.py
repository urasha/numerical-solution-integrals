import math


def f_x2(x):
    return x ** 2


def f_sin(x):
    return math.sin(x)


def f_inv(x):
    if x == 0:
        raise ValueError("Discontinuity at x = 0")
    return 1 / x


def f_ln(x):
    if x <= 0:
        raise ValueError("ln(x) undefined for x <= 0")
    return math.log(x)


def f_inv_sqrt(x):
    if x <= 0:
        raise ValueError("1/sqrt(x) undefined for x <= 0")
    return 1 / math.sqrt(x)


FUNCTIONS = {
    "x^2": f_x2,
    "sin(x)": f_sin,
    "1/x": f_inv,
    "ln(x)": f_ln,
    "1/sqrt(x)": f_inv_sqrt
}
