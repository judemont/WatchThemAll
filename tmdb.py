import re
from bs4 import BeautifulSoup
import requests

from models.movie import Movie

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
}


def extractMovie(tmdbUrl, langCode) -> Movie:
    CK = {"tmdb.prefs": f"%7B%22locale%22%3A%22{langCode}%22%7D"}

    page = requests.get(tmdbUrl, headers=HEADERS, cookies=CK)
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find("div", {"class": "title"}).find("a").getText()
    isSeries = "/tv/" in tmdbUrl
    description = soup.find("div", {"class": "overview"}).getText()

    trailerHref = soup.find_all("a", {"class": "play_trailer"})[1].get("href")
    youtubeTrailerID = re.findall(r"key=([^&]+)", trailerHref)[0]

    imageUrl = soup.find("img", {"class": "poster w-[100%]"}).get("src")

    return Movie(
        title=title,
        description=description,
        language_code=langCode,
        trailer_YTB_ID=youtubeTrailerID,
        image_url=imageUrl,
        tmdb_url=tmdbUrl,
        isSeries=isSeries,
    )
