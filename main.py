from flask import Flask, render_template, request, session, redirect
import os
import json

app = Flask(__name__)
app.secret_key = "suuuuuper secret key (;"

with open("./movies.json", "r") as file:
    moviesData = json.load(file)

@app.route('/')
def home():
    if(not "languageCode" in session):
        session["languageCode"] = "en-EN"
    print(session["languageCode"])

    moviesDataInLanguage = [movieData for movieData in moviesData if movieData["language_code"].startswith(session["languageCode"].split("-")[0])]

    return render_template('home.html', moviesData=moviesDataInLanguage, moviesDataLength=len(moviesDataInLanguage))


@app.route('/movie/<index>/')
def movie(index):
    return render_template('movie.html', movieData=moviesData[int(index)])


@app.route('/changeLanguage', methods=["GET"])
def changeLanguage():
    languageCode = request.args.get('languageCode')
    session["languageCode"] = languageCode
    return redirect("/")



if __name__ == "__main__":
    app.debug = True
    app.run()