from typing import Callable
import math


def midpoint(a: float, b: float) -> float:
    return (a + b) / 2

def simpsons_rule(f: Callable[[float], float], N: int, a: float, b: float) -> float:

    delta_x = (b - a) / N
    xs = list(map(
        lambda i: a + delta_x * i,
        range(N + 1)
    ))

    return (b - a) / (6 * N) * sum(
        [f(xs[i]) + 4 * f(midpoint(xs[i], xs[i + 1])) + f(xs[i + 1]) for i in range(N)]
    )

if __name__ == '__main__':
    # example usage for 3i
    integrand = lambda x: x ** 2
    N = 10
    a, b = (0, 1)
    value = simpsons_rule(integrand, N, a, b)
    print (f'{value:.10f}') # rounds to 10 decimal places
