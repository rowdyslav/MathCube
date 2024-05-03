from math import isqrt, sqrt
from random import randint


def generate_coefficients(difficulty: int) -> tuple[int, int, int]:
    while True:
        match difficulty:
            case 0:
                a = randint(1, 5)
                b = randint(-20, 20)
                c = randint(-40, 40)
            case 1:
                a = randint(1, 10)
                b = randint(-50, 50)
                c = randint(-100, 100)
            case 2:
                a = randint(1, 20)
                b = randint(-100, 100)
                c = randint(-200, 200)
            case _:
                raise ValueError("Invalid difficulty level")

        discriminant = b * b - 4 * a * c

        if discriminant >= 0 and (isqrt(discriminant) ** 2 == discriminant):
            return a, b, c


def get_roots(a, b, c) -> float | tuple[float, float]:
    discriminant = b * b - 4 * a * c
    sqrt_d = sqrt(abs(discriminant))

    if discriminant > 0:
        root1 = (-b + sqrt_d) / (2 * a)
        root2 = (-b - sqrt_d) / (2 * a)
        return root1, root2
    elif discriminant == 0:
        root = -b / (2 * a)
        return root


def format(a, b, c) -> str:
    if b and c:
        template = "{0}x² {1} {2}x {3} {4} = 0"
    elif b and not c:
        template = "{0}x² {1} {2}x = 0"
    elif not b and c:
        template = "{0}x² {3} {4} = 0"
    if b > 0:
        second = "+"
    else:
        b *= -1
        second = "-"
    if c > 0:
        third = "+"
    else:
        c *= -1
        third = "-"
    if a == 1:
        a = ""
    if b in (0, 1):
        b = ""
    if c == 0:
        c = ""
    return template.format(a, second, b, third, c)
