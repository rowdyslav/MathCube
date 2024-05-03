import random

from flask import Flask, flash, redirect, render_template, request, session
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from forms.category import ProductForm
from forms.problems import AnswerForm
from misc import quadratic_equation, sample
from misc.gia import get_problem, take_categories, take_problems, get_analogs

app = Flask(__name__)
app.secret_key = "your_secret_key"
# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route("/")
def index():
    return render_template("pages/home.html")


@app.route("/generator", methods=["GET", "POST"])
# @login_required
def generator():
    category = request.args.get("category", default="sample", type=str)
    if request.method == "POST":
        user_answer1 = float(request.form.get("answer1"))
        user_answer2 = request.form.get("answer2")
        if user_answer2:
            user_answer2 = float(user_answer2)

        correct_answer = request.form.get("correct_answer")

        if category == "sample":
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
            "pages/index.html",
            correct_answer=correct_answer,
            category=category,
        )
    elif request.method == "GET":
        if category == "sample":
            problem = sample.generate()
            correct_answer = eval(problem)

            return render_template(
                "pages/index.html",
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
                "pages/index.html",
                problem=problem,
                correct_answer=correct_answer,
                category=category,
                difficulty=difficulty,
            )
        else:
            raise ValueError("Invalid category")


@app.route("/from_gia", methods=["GET", "POST"])
def from_gia():
    form = ProductForm(data=take_categories())
    if form.validate_on_submit():
        return redirect(f"from_gia/{form.type.data}")
    return render_template("pages/from_gia.html", form=form)


@app.route("/from_gia/<string:catecory_id>", methods=["GET", "POST"])
def from_gia_catecory_id(catecory_id):
    form = AnswerForm()
    if request.method == "GET":
        if not session.get('turn'):
            main_problem = random.choice(take_problems(catecory_id))
            turn = get_analogs(main_problem)
            random.shuffle(turn)
            session["turn"] = turn
        elif len(session.get('turn')):
            main_problem = random.choice(take_problems(catecory_id))
            turn = get_analogs(main_problem)
            random.shuffle(turn)
            session["turn"] = turn
        session["problem_id"] = session['turn'].pop(0)

    problem = get_problem(session["problem_id"])
    answer = problem["answer"]
    while not len(answer):
        session["problem_id"] = session['turn'].pop(0)
        problem = get_problem(session["problem_id"])
        answer = problem["answer"]

    if form.validate_on_submit():
        if str(problem["answer"]) == str(form.answer.data):
            get_problem(session["problem_id"])
            return redirect(f"/from_gia/{catecory_id}")
        else:
                return render_template(
        "pages/task.html", form=form, img=problem['condition']['images'][0], answer=answer, message='Неверно, попробуй ещё'
    )


    return render_template(
        "pages/task.html", form=form, img=problem['condition']['images'][0], answer=answer
    )


if __name__ == "__main__":
    app.run(debug=True)
