from user import User

class UserRepository:

    def __init__(self, connection):
        self.connection = connection

    def save(self, new_user):
        self.connection.execute("INSERT INTO users(username, password) VALUES(%s, %s)", [new_user['username'], new_user['password']])
        return None

    
    