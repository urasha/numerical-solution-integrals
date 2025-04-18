def f1(x):
    return -x ** 3 - x ** 2 - 2 * x + 1


def f2(x):
    return -3 * x ** 3 - 5 * x ** 2 + 4 * x - 2


def f3(x):
    return -2 * x ** 3 - 4 * x ** 2 + 8 * x - 4


def f4(x):
    return 3 * x ** 3 + 5 * x ** 2 + 3 * x - 6


def f5(x):
    return 4 * x ** 3 - 5 * x ** 2 + 6 * x - 7


FUNCTIONS = {
    "-x³ - x² - 2x + 1": f1,
    "-3x³ - 5x² + 4x - 2": f2,
    "-2x³ - 4x² + 8x - 4": f3,
    "3x³ + 5x² + 3x - 6": f4,
    "4x³ - 5x² + 6x - 7": f5
}
