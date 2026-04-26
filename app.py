from flask import Flask, render_template, request
import os
import sqlite3
from datetime import datetime

from src.model import train_model, save_model, load_model

app = Flask(__name__)

# -------------------------
# Load or Train Model
# -------------------------
if not os.path.exists("model/similarity.pkl"):
    print("Training model...")
    similarity, movies = train_model()
    save_model(similarity, movies)
else:
    print("Loading model...")
    similarity, movies = load_model()

# -------------------------
# Recommendation Logic
# -------------------------
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

# -------------------------
# Database
# -------------------------
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

# -------------------------
# Routes
# -------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []

    if request.method == "POST":
        movie = request.form.get("movie")

        if movie:
            ip = request.remote_addr
            log_search(ip, movie)
            recommendations = get_recommendations(movie)

    return render_template("index.html", recommendations=recommendations)

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)