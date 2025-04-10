from flask import Flask, request, redirect, url_for

from .db import app


@app.route("/")
def index():
    pass


@app.route("/create_quiz", methods=['POST', 'GET'])
def create_quiz():
    if request.method == "POST":
        name = request.form['name']


@app.route("/delete_quiz/<quiz_id>")
def delete_quiz():
    pass
