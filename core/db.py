import sqlite3
from flask import Flask, render_template, url_for

app = Flask(__name__)


quizes = """
    CREATE TABLE IF NOT EXISTS quizes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL
    );
"""
questions = """
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text VARCHAR(100) NOT NULL,
        quiz_id INTEGER REFERENCES quizes(id)
    );
"""
answers = """
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text VARCHAR(100) NOT NULL,
        is_correct BOOLEAN NOT NULL,
        question_id INTEGER REFERENCES questions(id)
    );
"""


def get_db_connection():
    return sqlite3.connect("quiz.db")


with get_db_connection() as connection:
    cursor = connection.cursor()

    cursor.execute(quizes)
    cursor.execute(questions)
    cursor.execute(answers)
