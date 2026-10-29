import sys
import os

# this line is a bit of a hack which allows us to import app without changing anything else
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from playwright.sync_api import Page, expect
from flask import redirect
from database_connection import *

"""
# a descriptive test name
def test_get_books_returns_a_200():
    app.testing = True
    # here's where we make the test client
    client = app.test_client()

    # here's where we make the request
    response = client.get("/books")

    # here's where we assert that the response's status code is 200
    assert response.status_code == 200
  """

# a descriptive test name
""""
def test_get_books_returns_all_the_books():

    client = app.test_client()
    response = client.get("/books")

    # here's where we assert that the response body contains all the books
    # note that we need to call .json on the response
    assert response.json == [
      {
        "title": "The Gruffalo",
        "author": "Julia Donaldson"
      },
      {
        "title": "Ada Twist, Scientist",
        "author": "Andrea Beaty"
      },
      {
        "title": "The Girl Who Drank the Moon",
        "author": "Kelly Barnhill"
      },
      {
        "title": "Dragons in a Bag",
        "author": "Zetta Elliott"
      }
    ]
  """

def test_get_authors_returns_a_200():
    app.testing = True
    client = app.test_client()
    response = client.get("/authors")

    assert response.status_code == 200

def test_get_authors_returns_list_of_authors():
    client = app.test_client()
    response = client.get("/authors")

    assert response.json == [
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

def test_h1_on_landing_page(page : Page):
    page.goto("http://localhost:5001")

    h1 = page.locator("h1")

    expect(h1).to_have_text('Welcome to my Book Store')


def test_list_elements_in_books_page(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.seed('./seeds/books.sql')
    connection.seed('./seeds/user.sql')

    page.goto("http://localhost:5001/sessions/new")
    page.locator("#username").fill("test")
    page.locator("#password").fill('1234')
    page.get_by_role("button").click()



    page.goto('http://localhost:5001/books')


    expect(page.locator("li")).to_have_text([
        'The Gruffalo by Julia Donaldson',
        'Ada Twist, Scientist by Andrea Beaty',
        'The Girl Who Drank the Moon by Kelly Barnhill',
        'Dragons in a Bag by Zetta Elliott'
    ])

def test_form_post(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.seed('./seeds/books.sql')
    connection.seed('./seeds/user.sql')
    

    page.goto("http://localhost:5001/sessions/new")
    page.locator("#username").fill("test")
    page.locator("#password").fill('1234')
    page.get_by_role("button").click()


    
    page.goto('http://localhost:5001/books/add')
    page.locator("#title").fill("The Chroicles of Geronimo (the cat)")
    page.locator("#author").fill("Geronimo")
    page.get_by_role("button", name="Submit").click()

    books = page.locator("li")

    expected_books = [
        'The Gruffalo by Julia Donaldson',
        'Ada Twist, Scientist by Andrea Beaty',
        'The Girl Who Drank the Moon by Kelly Barnhill',
        'Dragons in a Bag by Zetta Elliott',
        'The Chroicles of Geronimo (the cat) by Geronimo'
    ]

    assert expected_books == books.all_inner_texts()

def test_list_elements_in_films_page(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.seed('./seeds/films.sql')
    connection.seed('./seeds/user.sql')

    page.goto("http://localhost:5001/sessions/new")
    page.locator("#username").fill("test")
    page.locator("#password").fill('1234')
    page.get_by_role("button").click()


    page.goto('http://localhost:5001/films')


    expect(page.locator("li")).to_have_text([
        'The Gruffalo released at 2009',
        'Ada Twist, Scientist released at 2021',
        'The Girl Who Drank the Moon released at 2020',
        'Dragons in a Bag released at 2019'
    ])

def test_auth_integration():
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect()

    response = client.post('/sessions', data={
        'username': 'test',
        'password': '1234'
    })

    assert response.status_code == 302
    # this assertion might be new to you :)
    assert response.headers['Location'].endswith('/books')



def test_auth_playwright(page: Page):

    connection = DatabaseConnection()
    connection.connect()

    page.goto("http://localhost:5001/sessions/new")
    page.locator("#username").fill("test")
    page.locator("#password").fill("1234")
    page.get_by_role("button").click()

    assert page.url == "http://localhost:5001/books"



