from user import User

class UserRepository:

    def __init__(self, connection):
        self.connection = connection

    def save(self, new_user):
        self.connection.execute("INSERT INTO users(username, password) VALUES(%s, %s)", [new_user['username'], new_user['password']])
        return None

    def find(self, user_details):
        row = self.connection.execute('SELECT id, username, password FROM users WHERE username = %s AND password = %s', [user_details['username'], user_details['password']])
        if row:
            return {'username': row[0]['username'], 'id': row[0]['id']}
        return False
    