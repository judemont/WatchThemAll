from flask import Flask, render_template
import os
import json

app = Flask(__name__)


with open("./movies.json", "r") as file:
    moviesData = json.load(file)

@app.route('/')
def home():
    return render_template('home.html', moviesData=moviesData, moviesDataLength=len(moviesData))


@app.route('/movie/<index>/')
def movie(index):
    return render_template('movie.html', movieData=moviesData[int(index)])


