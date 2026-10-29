from flask import Flask, render_template, request, redirect, session
from database_connection import DatabaseConnection
from book_repository import BookRepository
from film import Film
from userRepository import UserRepository
from authenticated import is_authenticated
from login_required import login_required
from werkzeug.security import generate_password_hash, check_password_hash
# instantiate a Flask app object
app = Flask(__name__)
app.secret_key = "some_really_secret_key"


# make the server run in response to `python app.py`
# on port 5001 (you'll learn more about what this means later)
# and use debug mode so that changing code restarts the app
@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello to you too'

@app.route('/books', methods=['GET'])
@login_required
def books():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    books = book_repository.all()
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

@app.route('/books/add', methods=['GET'])
@login_required
def add_book_page():
    return render_template("add_book.html")

@app.route("/books/add", methods=['POST'])
@login_required
def create_book():

    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    book_details = request.form
    book_repository.create(book_details)
    return redirect("/books")

@app.route('/films', methods=['GET'])
@login_required
def get_films():
    connection = DatabaseConnection()
    connection.connect()
    films = connection.execute('SELECT * FROM films')
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
    username = user_details['username']
    password = generate_password_hash(user_details['password'])
    user_repo.save(username, password)

    return redirect('/')

@app.route('/sessions/new', methods=['GET'])
def get_login_form():
    return render_template('login.html')

@app.route('/sessions', methods=['POST'])
def check_user():
    connection = DatabaseConnection()
    connection.connect()
    user_repo = UserRepository(connection)
    user_details = request.form
    username = user_details['username']
    user_found = user_repo.find(username)
    if user_found and check_password_hash(user_found['password'], user_details['password']):
        session.clear()
        session['username'] = user_details['username']
        session['user_id'] = user_found['id']
        return redirect('/books')
    return redirect('/sessions/new')
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
