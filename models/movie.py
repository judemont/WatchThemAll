class Movie:
    def __init__(
        self,
        title,
        description,
        magnet,
        language_code,
        trailer_YTB_ID,
        image_url,
        tmdb_url,
        isSeries=False,
        id=0,
    ):
        self.id = id
        self.title = title
        self.isSeries = isSeries
        self.description = description
        self.magnet = magnet
        self.language_code = language_code
        self.trailer_YTB_ID = trailer_YTB_ID
        self.image_url = image_url
        self.tmdb_url = tmdb_url

    def __str__(self):
        return f"Movie(id={self.id}, title='{self.title}', isSeries={self.isSeries}, description='{self.description}', magnet='{self.magnet}', language_code='{self.language_code}', trailer_YTB_ID='{self.trailer_YTB_ID}', image_url='{self.image_url}', tmdb_url='{self.tmdb_url}')"
