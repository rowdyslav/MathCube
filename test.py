import math
import random


def generate_equation(difficulty):
    while True:
        if difficulty == "easy":
            a = random.randint(1, 5)
            b = random.randint(-20, 20)
            c = random.randint(-40, 40)
        elif difficulty == "medium":
            a = random.randint(1, 10)
            b = random.randint(-50, 50)
            c = random.randint(-100, 100)
        elif difficulty == "hard":
            a = random.randint(1, 20)
            b = random.randint(-100, 100)
            c = random.randint(-200, 200)
        else:
            raise ValueError("Invalid difficulty level")

        discriminant = b * b - 4 * a * c

        if discriminant >= 0 and (math.isqrt(discriminant) ** 2 == discriminant):
            return a, b, c


def equationroots(a, b, c):
    discriminant = b * b - 4 * a * c
    sqrt_d = math.sqrt(abs(discriminant))

    if discriminant > 0:
        print("real and two roots")
        print((-b + sqrt_d) / (2 * a))
        print((-b - sqrt_d) / (2 * a))
    elif discriminant == 0:
        print("real and one root")
        print(-b / (2 * a))


difficulty = input("Choose the difficulty level (easy, medium, hard): ")
a, b, c = generate_equation(difficulty)
if a == 0:
    print("Input correct quadratic equation")
else:
    print(
        f"Generated quadratic equation: {a if a != 1 else ''}x² {f'+ {b}' if b > 0 else f'- {abs(b)}'}x {f'+ {c}' if c > 0 else f'- {abs(c)}'} = 0"
    )

equationroots(a, b, c)
