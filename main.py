import random

from flask import Flask, flash, render_template, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from misc import quadratic_equation

app = Flask(__name__)
app.secret_key = "your_secret_key"
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/", methods=["GET", "POST"])
@login_required
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

            return render_template(
                "index.html",
                problem=problem,
                correct_answer=correct_answer,
                category=category,
            )
        elif category == "quadratic":
            difficulty = request.args.get("difficulty", default=0, type=int)

            a, b, c = quadratic_equation.generate_coefficients(difficulty)
            correct_answer = quadratic_equation.get_roots(a, b, c)
            problem = quadratic_equation.format(a, b, c)

            if isinstance(correct_answer, float):
                correct_answer = correct_answer
            else:
                correct_answer = f"{correct_answer[0]}|{correct_answer[1]}"

            return render_template(
                "index.html",
                problem=problem,
                correct_answer=correct_answer,
                category=category,
                difficulty=difficulty,
            )
        else:
            raise ValueError("Invalid category")


if __name__ == "__main__":
    app.run(debug=True)
