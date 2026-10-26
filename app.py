from flask import Flask, render_template, request, redirect
from database_connection import DatabaseConnection
from book_repository import BookRepository
from film import Film
from userRepository import UserRepository
# instantiate a Flask app object
app = Flask(__name__)

# make the server run in response to `python app.py`
# on port 5001 (you'll learn more about what this means later)
# and use debug mode so that changing code restarts the app
@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello to you too'

@app.route('/books', methods=['GET'])
def books():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    books = book_repository.all()
    print(books)
    return render_template("books.html", books=books)

@app.route("/authors", methods=['GET'])
def authors():
    return [
  {
    "name": "Julia Donaldson",
    "dob": "1948-09-16"
  },
  {
    "name": "Andrea Beaty",
    "dob": "1961-10-08"
  },
  {
    "name": "Kelly Barnhill",
    "dob": "1973-01-01"
  },
  {
    "name": "Zetta Elliott",
    "dob": "1979-11-11"
  }
]

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/books", methods=['POST'])
def create_book():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    book_details = request.form
    book_repository.create(book_details)
    return redirect("/books")

@app.route('/films', methods=['GET'])
def get_films():
    connection = DatabaseConnection()
    connection.connect()
    films = connection.execute('SELECT * FROM films')
    print(films)
    return render_template("films.html",films = [Film(film['title'], film['year']) for film in films])


@app.route('/users/new', methods=['GET'])
def get_signup_form():
    return render_template('signup_form.html')


@app.route('/users', methods=['POST'])
def add_user():
    connection = DatabaseConnection()
    connection.connect()
    user_repo = UserRepository(connection)
    user_details = request.form
    user_repo.save(user_details)
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
