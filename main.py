import random

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from icecream import ic

from config import MONGO_URL
from database.user import User
from misc import gia, quadratic_equation, sample

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["MONGO_URI"] = MONGO_URL

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: str):
    return User._get(user_id)


@app.route("/")
def index():
    return render_template("pages/index.html")


@app.route("/profile")
@login_required
def profile():
    return render_template("pages/profile.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.signup(username, password)
        if type(user) is User:
            login_user(user, remember=True)
    elif request.method == "GET":
        return render_template("pages/signup.html")

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.login(username, password)
        if type(user) is User:
            login_user(user, remember=True)
    elif request.method == "GET":
        return render_template("pages/login.html")

    return redirect("/")


@app.route("/generator", methods=["GET", "POST"])
@login_required
def generator():
    category = request.args.get("category", default="sample", type=str)
    if request.method == "POST":
        user_answer1 = float(request.form.get("answer1"))
        user_answer2 = request.form.get("answer2")
        if user_answer2:
            user_answer2 = float(user_answer2)

        correct_answer = request.form.get("correct_answer")

        if category == "sample":
            correct = user_answer1 == float(correct_answer)
        elif category == "quadratic":
            correct_answers = {float(x) for x in correct_answer.split("|")}
            correct = len(correct_answers & {user_answer1, user_answer2}) == len(
                correct_answers
            )

        if correct:
            flash("Верно!")
        else:
            flash("Неправильно!")
        return redirect(url_for("generator", category=category))

    elif request.method == "GET":
        if category == "sample":
            problem = sample.generate()
            correct_answer = eval(problem)

            return render_template(
                "pages/generator.html",
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
    while not len(answer):
        session["problem_id"] = session["turn"].pop(0)
        problem = gia.get_problem(session["problem_id"])
        answer = problem["answer"]

    if request.method == "POST":
        if str(problem["answer"]) == str(request.form.get("answer")):
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
        answer=answer,
    )


if __name__ == "__main__":
    app.run(debug=True)
