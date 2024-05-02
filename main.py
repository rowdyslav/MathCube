import random

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_answer = int(request.form.get("answer"))
        correct_answer = request.form.get("correct_answer")
        if user_answer == int(correct_answer):
            flash("Correct!", "success")
        else:
            flash("Incorrect!", "error")
    number1 = random.randint(1, 10)
    number2 = random.randint(1, 10)
    operation = random.choice(["+", "-", "*"])
    if operation == "+":
        correct_answer = number1 + number2
    elif operation == "-":
        correct_answer = number1 - number2
    else:
        correct_answer = number1 * number2
    return render_template(
        "index.html",
        number1=number1,
        number2=number2,
        operation=operation,
        correct_answer=correct_answer,
    )


if __name__ == "__main__":
    app.run(debug=True)
