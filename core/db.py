import sqlite3
from flask import Flask, render_template, url_for

app = Flask(__name__)


quizes = """
    CREATE TABLE IF NOT EXISTS quizes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        description VARCHAR(100) NOT NULL
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


def get_quiz(search=None):
    with get_db_connection() as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        if search:
            cursor.execute(
                """
                SELECT quizes.id, name, description FROM quizes WHERE name LIKE ?;
                """,
                (f"%{search}%",),
            )
        else:
            cursor.execute(
                """
                SELECT quizes.id, name, description FROM quizes;
                """
            )
        quizes = cursor.fetchall()
        return [dict(row) for row in quizes]


def del_quiz(quiz_id):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            DELETE FROM quizes WHERE id = ?;
            """,
            (quiz_id,),
        )
        connection.commit()


def save_quiz(name, description):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO quizes (name, description)
            VALUES (?, ?);
            """,
            (name, description),
        )
        connection.commit()


def get_questions(quiz_id):
    with get_db_connection() as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT 
                questions.id AS question_id, 
                questions.text AS question_text, 
                answers.id AS answer_id, 
                answers.text AS answer_text, 
                answers.is_correct 
            FROM questions
            LEFT JOIN answers ON questions.id = answers.question_id
            WHERE questions.quiz_id = ?;
            """,
            (quiz_id,),
        )
        rows = cursor.fetchall()

        # Группируем ответы по вопросам
        questions = {}
        for row in rows:
            question_id = row["question_id"]
            if question_id not in questions:
                questions[question_id] = {
                    "id": question_id,
                    "text": row["question_text"],
                    "answers": [],
                }
            questions[question_id]["answers"].append({
                "id": row["answer_id"],
                "text": row["answer_text"],
                "is_correct": row["is_correct"],
            })

        return list(questions.values())
