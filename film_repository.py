from film import Film

class FilmRepository:
    def __init__(self, connection):
        self.connection = connection

    def all(self):
        rows = self.connection.execute("SELECT * FROM films")
        films = []
        for row in rows:
            item = Film(row['title'], row['year'])
            films.append(item)

        return films

    def create(self, new_film):
        self.connection.execute("INSERT INTO films(title, year) VALUES(%s, %s)", [new_film['title'], new_film['year']])