from flask import Flask, render_template, request, session, redirect
import os
import difflib

from database import Database


app = Flask(__name__)
app.secret_key = "suuuuuper secret key (;"


LANGUAGES = [
    ("en-US", "English"),
    ("es-ES", "Spanish"),
    ("fr-FR", "French"),
    ("de-DE", "German"),
    ("it-IT", "Italian"),
    ("zh-CN", "Chinese (Simplified)"),
    ("ja-JP", "Japanese"),
    ("ko-KR", "Korean"),
    ("pt-BR", "Portuguese"),
    ("ru-RU", "Russian"),
]


@app.route("/", methods=["GET"])
def home():
    db: Database = Database()
    db.init()
    moviesData = db.getMovies()
    print(moviesData)

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


@app.route("/movie/<index>/")
def movie(index):
    with open("./movies.json", "r") as file:
        moviesData = json.load(file)
    return render_template("movie.html", movieData=moviesData[int(index)])


@app.route("/changeLanguage", methods=["GET"])
def changeLanguage():
    languageCode = request.args.get("languageCode")
    session["languageCode"] = languageCode
    return redirect("/")


if __name__ == "__main__":
    app.debug = True
    app.run()
