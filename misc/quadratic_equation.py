from math import isqrt, sqrt
from random import randint

from icecream import ic


def randcoef(a: int, b: int) -> int:
    "Аналог функции random.randint, который не допускает нули"
    result = randint(a, b)
    while result == 0:
        result = randint(a, b)
    ic(a, b, result)
    return result


def generate_coefficients(difficulty: int) -> tuple[int, int, int]:
    while True:
        match difficulty:
            case 0:
                a = randcoef(-2, 5)
                b = 0
                c = randcoef(-5, 5)
            case 1:
                a = randcoef(-2, 10)
                b = randcoef(-10, 10)
                c = 0
            case 2:
                a = randcoef(-10, 10)
                b = randcoef(-15, 15)
                c = randcoef(-20, 20)
            case _:
                raise ValueError("Invalid difficulty level")

        discriminant = b * b - 4 * a * c

        if discriminant >= 0 and (isqrt(discriminant) ** 2 == discriminant):
            return a, b, c


def get_roots(a: int, b: int, c: int) -> float | tuple[float, float]:
    discriminant = b * b - 4 * a * c
    sqrt_d = sqrt(abs(discriminant))

    if discriminant > 0:
        root1 = (-b + sqrt_d) / (2 * a)
        root2 = (-b - sqrt_d) / (2 * a)
        return root1, root2
    elif discriminant == 0:
        root = -b / (2 * a)
        return root
    else:
        raise ValueError("Попытка получить корни корни квадратного уравнения с D < 0")


def format(a: int, b: int, c: int) -> str:
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
        a = ""  # type: ignore
    if b == 1:
        b = ""  # type: ignore

    result = template.format(a, second, b, third, c)
    return result
