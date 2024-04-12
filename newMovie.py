import inquirer
import json
import requests
from bs4 import BeautifulSoup
import re
from database import Database
from models.movie import Movie

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
}

torrentMagnetLink = input("Torrent magnet link : ")

langQuestion = [
    inquirer.List(
        "langCode",
        message="Movie language",
        choices=[("English", "en-EN"), ("French", "fr-FR")],
    )
]

langAnswer = inquirer.prompt(langQuestion)
langCode = langAnswer["langCode"]
CK = {"tmdb.prefs": f"%7B%22locale%22%3A%22{langCode}%22%7D"}

tmdbUrl = ""

while not (
    tmdbUrl.startswith("https://themoviedb.org/")
    or tmdbUrl.startswith("https://www.themoviedb.org/")
):
    tmdbUrl = input("https://themoviedb.org movie URL : ")

page = requests.get(tmdbUrl, headers=HEADERS, cookies=CK)
soup = BeautifulSoup(page.content, "html.parser")

title = soup.find("div", {"class": "title"}).find("a").getText()

isSeries = "/tv/" in tmdbUrl

description = soup.find("div", {"class": "overview"}).getText()

trailerHref = soup.find_all("a", {"class": "play_trailer"})[1].get("href")
youtubeTrailerID = re.findall(r"key=([^&]+)", trailerHref)[0]

imageUrl = soup.find("img", {"class": "poster w-[100%]"}).get("src")

db: Database = Database()
db.init()

movie: Movie = Movie(
    title=title,
    description=description,
    magnet=torrentMagnetLink,
    language_code=langCode,
    trailer_YTB_ID=youtubeTrailerID,
    image_url=imageUrl,
    tmdb_url=tmdbUrl,
    isSeries=isSeries,
)

db.newMovie(movie)
