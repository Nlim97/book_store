import psycopg
from psycopg.rows import dict_row
import os

class DatabaseConnection():
    DATABASE_NAME = os.getenv("DATABASE_NAME", "book_store_test")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")

    def __init__(self):
        self.connection = None

    def connect(self):

        try:
            self.connection = psycopg.connect(
                f"postgresql://{self.DATABASE_HOST}/{self.DATABASE_NAME}",
                row_factory=dict_row)
        except psycopg.OperationalError:
            raise Exception(f"Couldn't connect to the database {self.DATABASE_NAME}! " \
                    f"Did you create it using `createdb {self.DATABASE_NAME}`?")


    def seed(self, sql_filename):
        self._check_connection()
        if not os.path.exists(sql_filename):
            raise Exception(f"File {sql_filename} does not exist")
        with self.connection.cursor() as cursor:
            cursor.execute(open(sql_filename, "r").read())
            self.connection.commit()

    def execute(self, query, params=[]):
        self._check_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description is not None:
                result = cursor.fetchall()
            else:
                result = None
            self.connection.commit()
            return result

    def _check_connection(self):
        if self.connection is None:
            raise Exception(self.CONNECTION_MESSAGE)