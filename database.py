import sqlite3
from models.movie import Movie


class Database:
    def __init__(self) -> None:
        pass

    def createTables(self):
        self.conn.cursor().execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY,
                title TEXT,
                isSeries BOOL,
                description TEXT,
                magnet TEXT,
                language_code TEXT,
                trailer_YTB_ID TEXT,
                image_url TEXT,
                tmdb_url TEXT
            )
        """
        )
        self.conn.commit()

    def newMovie(self, movie: Movie):
        data: tuple = (
            movie.title,
            movie.isSeries,
            movie.description,
            movie.magnet,
            movie.language_code,
            movie.trailer_YTB_ID,
            movie.image_url,
            movie.tmdb_url,
        )

        self.conn.cursor().execute(
            f"""
            INSERT INTO movies
            (title, isSeries, description, magnet, language_code, trailer_YTB_ID, image_url, tmdb_url)
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            data,
        )

        self.conn.commit()

    def getMovies(self, id: int | None = None) -> list[Movie]:
        cursor = self.conn.cursor()
        if id == None:
            print("SSSAA")
            cursor.execute(
                """
                SELECT * from movies
                """
            )
        else:
            cursor.execute(
                """
                SELECT * from movies WHERE id=(?)
                """,
                id,
            )

        results = cursor.fetchall()
        print(results)
        movies = []

        for result in results:
            movies.append(
                Movie(
                    id=result[0],
                    title=result[1],
                    isSeries=result[2],
                    description=result[3],
                    magnet=result[4],
                    language_code=result[5],
                    trailer_YTB_ID=result[6],
                    image_url=result[7],
                    tmdb_url=result[8],
                )
            )
        return movies

    def init(self) -> sqlite3.Cursor:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        self.conn: sqlite3.Connection = conn
        self.createTables()
