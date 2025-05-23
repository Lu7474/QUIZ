from flask import Flask, request, redirect, url_for, render_template

from .db import app, del_quiz, save_quiz, get_quiz, get_questions, save_ques


@app.route("/")
def index():
    search = request.args.get("search")
    quizes = get_quiz(search=search)
    return render_template("index.html", quizes=quizes)


@app.route("/create_quiz", methods=["POST", "GET"])
def create_quiz():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form.get("description")
        save_quiz(name, description)
        return redirect(url_for("index"))
    return render_template("create_quiz.html")


@app.route("/delete_quiz/<int:id>", methods=["POST"])
def delete_quiz(id):
    del_quiz(id)
    return redirect(url_for("index"))


@app.route("/quiz/<int:quiz_id>", methods=["GET"])
def perform_quiz(quiz_id):
    questions = get_questions(quiz_id)
    return render_template("quiz.html", questions=questions)


@app.route("/create_ques", methods=["POST", "GET"])
def create_ques():
    if request.method == "POST":

        save_ques()
        return redirect(url_for("index"))
    return render_template("add_question.html")


# @app.route("/submit/<quiz_id>) - обработка результатов
