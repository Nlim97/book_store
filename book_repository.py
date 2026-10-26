from book import Book

class BookRepository:
    def __init__(self, connection):
        self.connection = connection

    def all(self):
        rows = self.connection.execute("SELECT * FROM books")
        books = []
        for row in rows:
            book = Book(row['id'], row['title'], row['author'])
            books.append(book)

        return books

    def create(self, new_book):
        self.connection.execute("INSERT INTO books(title, author) VALUES(%s, %s)", [new_book['title'], new_book['author']])