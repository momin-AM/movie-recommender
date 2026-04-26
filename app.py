from flask import Flask, render_template, request
from src.model import load_model
from src.recommend import recommend
import sqlite3
from datetime import datetime
from flask import request

app = Flask(__name__)

# load model once
movies, similarity = load_model()


def get_recommendations(movie):
    movie = movie.lower()
    matches = movies[movies['title'].str.lower().str.contains(movie)]

    if matches.empty:
        return ["Movie not found 😢"]

    movie_index = matches.index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return [movies.iloc[i[0]].title for i in movie_list]


@app.route("/", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []

    if request.method == "POST":
        movie = request.form["movie"]

        # 👇 get user IP
        ip = request.remote_addr

        # 👇 log search
        log_search(ip, movie)

        recommendations = get_recommendations(movie)

    return render_template("index.html", recommendations=recommendations)
def init_db():
    conn = sqlite3.connect("searches.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            movie TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

def log_search(ip, movie):
    conn = sqlite3.connect("searches.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO searches (ip, movie, timestamp) VALUES (?, ?, ?)",
        (ip, movie, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)