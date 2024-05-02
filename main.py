import math
import random

from flask import Flask, flash, render_template, request, redirect, url_for, session
from forms.category import ProductForm
from forms.problems import AnswerForm
from sdam_con import take_categories, take_problems, get_problem
app = Flask(__name__)
app.secret_key = "your_secret_key"


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


def equation_roots(a, b, c):
    discriminant = b * b - 4 * a * c
    sqrt_d = math.sqrt(abs(discriminant))

    if discriminant > 0:
        root1 = (-b + sqrt_d) / (2 * a)
        root2 = (-b - sqrt_d) / (2 * a)
        return root1, root2
    elif discriminant == 0:
        root = -b / (2 * a)
        return root


@app.route("/", methods=["GET", "POST"])
def index():
    category = request.args.get("category", default="simple", type=str)
    if request.method == "POST":
        user_answer1 = float(request.form.get("answer1"))
        user_answer2 = request.form.get("answer2")
        if user_answer2:
            user_answer2 = float(user_answer2)

        correct_answer = request.form.get("correct_answer")

        if category == "simple":
            if user_answer1 == float(correct_answer):
                flash("Correct!", "success")
            else:
                flash("Incorrect!", "error")
        elif category == "quadratic":
            correct_answers = {float(x) for x in correct_answer.split(", ")}
            if len(correct_answers & {user_answer1, user_answer2}) == len(
                correct_answers
            ):
                flash("Correct!", "success")
            else:
                flash("Incorrect!", "error")
        return render_template(
            "index.html",
            correct_answer=correct_answer,
            category=category,
        )
    elif request.method == "GET":
        if category == "simple":
            number1 = random.randint(1, 10)
            number2 = random.randint(1, 10)
            operation = random.choice(["+", "-", "*"])
            if operation == "+":
                correct_answer = number1 + number2
            elif operation == "-":
                correct_answer = number1 - number2
            else:
                correct_answer = number1 * number2
            problem = f"{number1} {operation} {number2}"
            return render_template(
                "index.html",
                problem=problem,
                correct_answer=correct_answer,
                category=category,
            )
        elif category == "quadratic":
            difficulty = request.args.get("difficulty", default="easy", type=str)
            a, b, c = generate_equation(difficulty)
            correct_answer = equation_roots(a, b, c)
            if isinstance(correct_answer, float):
                problem = f"{a}x² {f'+ {b}' if b > 0 else f'- {abs(b)}'}x {f'+ {c}' if c > 0 else f'- {abs(c)}'} = 0"
                correct_answer = correct_answer
            else:
                problem = f"{a}x² {f'+ {b}' if b > 0 else f'- {abs(b)}'}x {f'+ {c}' if c > 0 else f'- {abs(c)}'} = 0"
                correct_answer = f"{correct_answer[0]}, {correct_answer[1]}"
            return render_template(
                "index.html",
                problem=problem,
                correct_answer=correct_answer,
                category=category,
                difficulty=difficulty,
            )
        else:
            raise ValueError("Invalid category")
        

@app.route("/from_gia", methods=["GET", "POST"])
def from_gia():
    form =  ProductForm(data=take_categories())
    if form.validate_on_submit():
        return redirect(f'from_gia/{form.type.data}')
    return render_template('from_gia.html', form=form)

@app.route("/from_gia/<string:catecory_id>", methods=["GET", "POST"])
def from_gia_catecory_id(catecory_id):
    form = AnswerForm()
    if request.method == "GET":
        session['problem_id'] = random.choice(take_problems(catecory_id))
    problem = get_problem(session['problem_id'])
    problem_img, problem = problem['filename'], problem['data']
    if form.validate_on_submit():
        if str(problem['answer']) == str(form.answer.data):
            return 'True'
        return 'False'
    

    return render_template('task.html', form=form, img=problem_img, answer=problem['answer'])


if __name__ == "__main__":
    app.run(debug=True)
