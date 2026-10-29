from user import User

class UserRepository:

    def __init__(self, connection):
        self.connection = connection

    def save(self, username, password):
        self.connection.execute("INSERT INTO users(username, password) VALUES(%s, %s)", [username, password])
        return None

    def find(self, username):
        row = self.connection.execute('SELECT id, username, password FROM users WHERE username = %s' , [username,])
        if row:
            return {'username': row[0]['username'], 'id': row[0]['id'], 'password': row[0]['password']}
        print('false')
        return False
    