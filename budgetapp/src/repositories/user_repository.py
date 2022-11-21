from entities.user import User
from database_connection import get_database_connection

def get_user_by_row(row):
    return User(row["username"], row["password"]) if row else None

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def signup(self, user):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO Users (username, password) values (?, ?)",
                        [user.username, user.password])
        self._connection.commit()
        return user

    def find_by_username(self,username):
        cursor = self._connection.cursor()
        row = cursor.execute("SELECT * FROM Users WHERE username = ?",[username]).fetchone()
        return get_user_by_row(row)

    def find_all_users(self):
        cursor = self._connection.cursor()
        rows = cursor.execute("SELECT * FROM Users").fetchall()
        return list(map(get_user_by_row, rows))

    def clear_table(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM Users")
        self._connection.commit()

user_repository = UserRepository(get_database_connection())



