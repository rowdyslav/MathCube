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
    """Форматирует квадратное уравнение по математическим правилам записи"""

    sign_b = "+" if b > 0 else "-"
    sign_c = "+" if c > 0 else "-"

    abs_b = abs(b)
    abs_c = abs(c)

    a_str = "" if a == 1 else a
    b_str = "" if abs_b == 1 else abs_b

    if b and c:
        equation = f"{a_str}x² {sign_b} {b_str}x {sign_c} {abs_c} = 0"
    elif b:
        equation = f"{a_str}x² {sign_b} {b_str}x = 0"
    elif c:
        equation = f"{a_str}x² {sign_c} {abs_c} = 0"

    if equation.startswith("+"):
        equation = equation[1:].strip()

    return equation
