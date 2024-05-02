from random import choice, randint


def generate():
    number1 = randint(1, 10)
    number2 = randint(1, 10)
    operation = choice(["+", "-", "*"])

    problem = f"{number1} {operation} {number2}"
    return problem
