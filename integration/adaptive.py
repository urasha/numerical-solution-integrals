from integration.methods import rectangle_rule, trapezoidal_rule, simpson_rule


def runge_error(approx_integral_n, approx_integral_2n, order):
    return abs(approx_integral_2n - approx_integral_n) / (2 ** order - 1)


def adaptive_integration(f, a, b, tol, method, variant="left"):
    n = 4
    while True:
        if method == "rectangle":
            approx_integral_n = rectangle_rule(f, a, b, n, variant)
            approx_integral_2n = rectangle_rule(f, a, b, n * 2, variant)
            order = 1 if variant in ["left", "right"] else 2
        elif method == "trapezoidal":
            approx_integral_n = trapezoidal_rule(f, a, b, n)
            approx_integral_2n = trapezoidal_rule(f, a, b, n * 2)
            order = 2
        elif method == "simpson":
            approx_integral_n = simpson_rule(f, a, b, n)
            approx_integral_2n = simpson_rule(f, a, b, n * 2)
            order = 4
        else:
            raise ValueError("Unknown integration method")

        runge_estimate = runge_error(approx_integral_n, approx_integral_2n, order)
        if runge_estimate < tol:
            return approx_integral_2n, n * 2
        n *= 2
        if n > 1e7:
            raise ValueError("Max subdivisions reached. Desired accuracy may be unattainable.")


def handle_improper_integral(f, a, b, tol, method, variant="left"):
    # Handling discontinuities for 1/x case
    if f.__name__ == "f_inv" and a < 0 < b:
        delta = min(abs(a), b)

        # If the interval is symmetric
        if abs(delta - abs(a)) < 1e-9 and abs(delta - b) < 1e-9:
            return 0, None
        else:
            if abs(a) < b:
                new_a, new_b = delta, b
            else:
                new_a, new_b = a, -delta

            approx_integral, subdivisions_used = adaptive_integration(f, new_a, new_b, tol, method, variant)

            if new_b < 0:
                approx_integral = -approx_integral

            return approx_integral, subdivisions_used

    try:
        return adaptive_integration(f, a, b, tol, method, variant)
    except Exception as ex:
        raise ValueError("Integration error: " + str(ex))
