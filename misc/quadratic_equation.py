from math import isqrt, sqrt
from random import randint
from typing import Literal

# from icecream import ic


def _randcoef(a: int, b: int) -> int:
    "Аналог функции random.randint, который не допускает нули"

    result = randint(a, b)
    while result == 0:
        result = randint(a, b)
    return result


def generate_coefficients(
    difficulty: Literal["Легкая", "Средняя", "Сложная"]
) -> tuple[int, int, int]:
    "Возвращает коэффициенты для квадратного уравнения заданной сложности Легкая, Средняя, Сложная"

    while True:
        match difficulty:
            case "Легкая":
                a = _randcoef(-2, 5)
                b = 0
                c = _randcoef(-5, 5)
            case "Средняя":
                a = _randcoef(-2, 10)
                b = _randcoef(-10, 10)
                c = 0
            case "Сложная":
                a = _randcoef(-10, 10)
                b = _randcoef(-15, 15)
                c = _randcoef(-20, 20)
            case _:
                raise ValueError("Invalid difficulty level")

        discriminant = b * b - 4 * a * c

        if discriminant >= 0 and (isqrt(discriminant) ** 2 == discriminant):
            return a, b, c


def get_roots(a: int, b: int, c: int) -> float | tuple[float, float]:
    "Возвращает корень или кортеж из двух корней для квадратного уравнения"

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
    "Форматирует квадратное уравнение по математическим правилам записи"

    if b and c:
        template = "{0}x² {1} {2}x {3} {4} = 0"
    elif b and not c:
        template = "{0}x² {1} {2}x = 0"
    elif c and not b:
        template = "{0}x² {3} {4} = 0"

    second = "+" if b > 0 else "-"
    third = "+" if c > 0 else "-"

    if a == 1:
        a = ""  # type: ignore
    if b == 1:
        b = ""  # type: ignore

    return template.format(
        a, second, abs(b), third, abs(c)
    )  # TODO Переписать, пока будет ерор если b станет пусттой ковычкой
