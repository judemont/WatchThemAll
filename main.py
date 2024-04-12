from flask import Flask, render_template, request, session, redirect
import os
import json
import difflib


app = Flask(__name__)
app.secret_key = "suuuuuper secret key (;"


LANGUAGES = [
    ('en-US', 'English'),
    ('es-ES', 'Spanish'),
    ('fr-FR', 'French'),
    ('de-DE', 'German'),
    ('it-IT', 'Italian'),
    ('zh-CN', 'Chinese (Simplified)'),
    ('ja-JP', 'Japanese'),
    ('ko-KR', 'Korean'),
    ('pt-BR', 'Portuguese'),
    ('ru-RU', 'Russian')
]



@app.route('/', methods=["GET"])
def home():

    with open("./movies.json", "r") as file:
        moviesData = json.load(file)


    if(not "languageCode" in session):
        session["languageCode"] = "en-EN"

    moviesData = [movieData for movieData in moviesData if movieData["language_code"].startswith(session["languageCode"].split("-")[0])]

    if("q" in request.args):
        searchQuery = request.args.get('q')

        for i in range(len(moviesData)):
            similarity = difflib.SequenceMatcher(None, moviesData[i]["title"], searchQuery).ratio()
            moviesData[i]["searchSimilarity"] = similarity
        
        moviesData = sorted(moviesData, key=lambda x: x["searchSimilarity"], reverse=True)
        print(moviesData)


    return render_template('home.html', moviesData=moviesData, moviesDataLength=len(moviesData), languages=LANGUAGES, languageCode=session["languageCode"])


@app.route('/movie/<index>/')
def movie(index):
    with open("./movies.json", "r") as file:
        moviesData = json.load(file)
    return render_template('movie.html', movieData=moviesData[int(index)])


@app.route('/changeLanguage', methods=["GET"])
def changeLanguage():
    languageCode = request.args.get('languageCode')
    session["languageCode"] = languageCode
    return redirect("/")



if __name__ == "__main__":
    app.debug = True
    app.run()