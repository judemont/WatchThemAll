from flask import Flask, render_template, request, session, redirect
import os
import difflib

from database import Database
from models.movie import Movie
from tmdb import extractMovie


app = Flask(__name__)
app.secret_key = "suuuuuper secret key (;"


LANGUAGES = [
    ("en-US", "English"),
    # ("es-ES", "Spanish"),
    ("fr-FR", "French"),
    # ("de-DE", "German"),
    # ("it-IT", "Italian"),
    # ("zh-CN", "Chinese (Simplified)"),
    # ("ja-JP", "Japanese"),
    # ("ko-KR", "Korean"),
    # ("pt-BR", "Portuguese"),
    # ("ru-RU", "Russian"),
]


@app.route("/", methods=["GET"])
def home():
    db: Database = Database()
    db.init()
    moviesData = db.getMovies()

    if not "languageCode" in session:
        session["languageCode"] = "en-EN"

    moviesDataForLang = [
        movieData
        for movieData in moviesData
        if movieData.language_code.startswith(session["languageCode"].split("-")[0])
    ]

    if "q" in request.args:
        searchQuery = request.args.get("q")
        moviesSimilarity = {}
        for i in range(len(moviesDataForLang)):
            similarity = difflib.SequenceMatcher(
                None, moviesDataForLang[i].title, searchQuery
            ).ratio()
            moviesSimilarity[str(moviesDataForLang[i].id)] = similarity

        moviesData = sorted(
            moviesDataForLang, key=lambda x: moviesSimilarity[str(x.id)], reverse=True
        )

    return render_template(
        "home.html",
        moviesData=moviesDataForLang,
        moviesDataLength=len(moviesDataForLang),
        languages=LANGUAGES,
        languageCode=session["languageCode"],
    )


@app.route("/movie/<id>/")
def movie(id):
    db: Database = Database()
    db.init()
    moviesData: list[Movie] = db.getMovies()

    movieData = [movieData for movieData in moviesData if movieData.id == int(id)][0]
    return render_template(
        "movie.html",
        movieData=movieData,
    )


@app.route("/changeLanguage", methods=["GET"])
def changeLanguage():
    languageCode = request.args.get("languageCode")
    session["languageCode"] = languageCode
    return redirect("/")


@app.route("/new/")
def newMovie():
    return render_template(
        "newMovie.html",
        languages=LANGUAGES,
    )


@app.route("/saveNewMovie", methods=["GET"])
def saveNewMovie():
    magnet = request.args.get("magnet")
    tmdbUrl = request.args.get("tmdbUrl")
    movie: Movie = extractMovie(
        tmdbUrl=tmdbUrl, langCode=request.args.get("languageCode")
    )

    movie.magnet = magnet

    db: Database = Database()
    db.init()

    duplicatedMovie: list[Movie] = db.getMovies(tmdbUrl=tmdbUrl)
    if len(duplicatedMovie) <= 0:
        db.newMovie(movie)
        return redirect("/")
    else:
        return redirect("/")


if __name__ == "__main__":
    app.debug = True
    app.run()
