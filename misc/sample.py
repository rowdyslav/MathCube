def generate():
    number1 = randint(1, 10)
    number2 = randint(1, 10)
    operation = choice(["+", "-", "*"])
    if operation == "+":
        correct_answer = number1 + number2
    elif operation == "-":
        correct_answer = number1 - number2
    else:
        correct_answer = number1 * number2
    problem = f"{number1} {operation} {number2}"
