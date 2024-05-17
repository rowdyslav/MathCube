import random
from typing import Literal

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flask_session import Session

from config import MONGO_URI, SECRET_KEY
from database.user import User
from misc import gia, quadratic_equation, sample

# from icecream import ic


app = Flask('MathCube')
app.secret_key = SECRET_KEY
app.config["MONGO_URI"] = MONGO_URI
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: str):
    return User._get(user_id)


@app.route("/")
def index():
    return render_template("pages/index.html")

@app.route("/signup", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if "signup" in request.path:
            result = User.signup(username, password)
        else:
            result = User.login(username, password)
        if isinstance(result, User):
            login_user(result, remember=True)
        elif isinstance(result, str):
            flash(result)
        return redirect(url_for("index"))
    elif request.method == "GET":
        if "signup" in request.path:
            return render_template("pages/signup.html")
        else:
            return render_template("pages/login.html")

    return redirect(url_for("index"))


@app.errorhandler(401)
def unauthorized(e):
    flash('Требуется авторизация')
    return redirect('/signup')

@app.route("/profile")
@login_required
def profile():
    return render_template("pages/profile.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/leaderboard")
def leaderboard():
    all_users = User._getall()

    def get_percentage(user: User) -> float:
        a = sum((statistic['correct'] for _, statistic in user.statistic.items()))
        b = sum((statistic['all'] for _, statistic in user.statistic.items()))
        return round(a / b * 100, 2) if b != 0 else 0

    def get_quantity(user: User) -> int:
        return sum((statistic['correct'] for _, statistic in user.statistic.items()))

    percentage = [
        (user.username, get_percentage(user)) for user in sorted(all_users, key=get_percentage, reverse=True)
    ]
    quantity = [
        (user.username, get_quantity(user)) for user in sorted(all_users, key=get_quantity, reverse=True)
    ]

    return render_template(
        "pages/leaderboard.html",
        percentage=percentage,
        quantity=quantity,
    )

@app.route("/generator", methods=["POST"])
@login_required
def generator_post():
    category = request.args.get("category", default="sample", type=str)
    user_answer1: str = request.form.get("answer1") # type: ignore
    user_answer2: str | None = request.form.get("answer2")

    correct_answer: str = request.form.get("correct_answer") # type: ignore

    if category == "sample":
        match request.form["submit_btn"]:
            case 'answer': 
                is_correct = user_answer1 == correct_answer
            case 'apply':
                opers = []
                if request.form.get('sumCheck'):
                    opers.append('+')
                if request.form.get('difCheck'):
                    opers.append('-')
                if  request.form.get('mulCheck'):
                    opers.append('*')
                if request.form.get('divCheck'):
                    opers.append('/')
                session['sample_opers'] = opers
    elif category == "quadratic_equation":
        correct_answers = {float(str_answer) for str_answer in correct_answer.split("|")}
        user_answers = {float(str_answer) for str_answer in (user_answer1, user_answer2) if str_answer}
        is_correct = correct_answers == user_answers
    inc_stat = {f"statistic.{category}.all": 1}

    if is_correct:
        flash("Верно!")
        inc_stat[f"statistic.{category}.correct"] = 1
    else:
        flash("Неправильно!")

    User._update(current_user._id, "$inc", **inc_stat)
    return redirect(url_for("generator_get", category=category))

@app.route("/generator")
@login_required
def generator_get():
    category = request.args.get("category", default="sample", type=str)
    if category == "sample":
        opers: list[Literal["+", "-", "*", "/"]] = session.get('sample_opers', ["+", "-", "*", "/"])
        problem, correct_answer = sample.generate(opers)
        return render_template(
            "pages/generator.html",
            problem=problem,
            correct_answer=correct_answer,
            category=category,
            sample_opers=opers
        )
    elif category == "quadratic_equation":
        difficulty = 2 # TODO получения с фронта
        a, b, c = quadratic_equation.generate_coefficients(difficulty)
        correct_answer = quadratic_equation.get_roots(a, b, c)
        problem = quadratic_equation.format(a, b, c)
        if isinstance(correct_answer, tuple):
            correct_answer = f"{correct_answer[0]}|{correct_answer[1]}"
        return render_template(
            "pages/generator.html",
            problem=problem,
            correct_answer=correct_answer,
            category=category,
            difficulty=difficulty,
        )
    return redirect("/", 400)



@app.route("/from_gia", methods=["GET", "POST"])
@login_required
def from_gia():
    categories = gia.get_categories()
    if request.method == "POST":
        return redirect(f"from_gia/{request.form.get("group")}")
    return render_template("pages/from_gia.html", categories=categories)


@app.route("/from_gia/<string:catecory_id>", methods=["GET", "POST"])
@login_required
def from_gia_catecory_id(catecory_id):
    if request.method == "GET":
        if not session.get("turn"):
            main_problem = random.choice(gia.get_category(catecory_id))
            turn = gia.get_analogs(main_problem)
            random.shuffle(turn)
            session["turn"] = turn
        elif len(session.get("turn")):
            main_problem = random.choice(gia.get_category(catecory_id))
            turn = gia.get_analogs(main_problem)
            random.shuffle(turn)
            session["turn"] = turn
        session["problem_id"] = session["turn"].pop(0)

    problem = gia.get_problem(session["problem_id"])
    answer = problem["answer"]
    while not len(answer) or answer == '.' or 'O' in answer or 'О' in answer:
        session["problem_id"] = session["turn"].pop(0)
        problem = gia.get_problem(session["problem_id"])
        answer = problem["answer"]

    if request.method == "POST":
        if float(problem["answer"].replace(',', '.')) == float(request.form.get("answer").replace(',', '.')):
            gia.get_problem(session["problem_id"])
            return redirect(f"/from_gia/{catecory_id}")
        else:
            return render_template(
                "pages/task.html",
                img=problem["condition"]["images"][0],
                answer=answer,
                message="Неверно, попробуй ещё",
            )

    return render_template(
        "pages/task.html",
        img=problem["condition"]["images"][0],
        problem_text=problem["condition"]["text"],
        answer=answer,
    )


if __name__ == "__main__":
    app.run(debug=True)
