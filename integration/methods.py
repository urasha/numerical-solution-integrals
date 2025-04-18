def rectangle_rule(f, a, b, n, variant="left"):
    h = (b - a) / n
    s = 0.0
    if variant == "left":
        for i in range(n):
            s += f(a + i * h)
    elif variant == "right":
        for i in range(1, n + 1):
            s += f(a + i * h)
    elif variant == "middle":
        for i in range(n):
            s += f(a + (i + 0.5) * h)
    else:
        raise ValueError("Unknown rectangle variant")
    return s * h


def trapezoidal_rule(f, a, b, n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h


def simpson_rule(f, a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        s += 4 * f(x) if i % 2 != 0 else 2 * f(x)
    return s * h / 3
