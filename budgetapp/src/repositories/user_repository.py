from entities.user import User
from database_connection import get_database_connection


def get_user_by_row(row):
    return User(row["username"], row["password"]) if row else None


class UserRepository:
    """Luokka, joka vastaa käyttäjiin liittyvistä tietokantaoperaatioista.
    """

    def __init__(self, connection):
        """Luokan konstruktori, joka muodostaa tietokantayhteyden

        Args:
            connection(object): tietokantayhteys
        """
        self._connection = connection

    def signup(self, user):
        """Tallentaa uuden käyttäjän tietokantaan.

        Args:
            user(object):käyttäjä

        Returns:
            Tallennettu käyttäjä
        """
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO Users (username, password) values (?, ?)",
                       [user.username, user.password])
        self._connection.commit()
        return user

    def find_by_username(self, username):
        """Palauttaa käyttäjän käyttäjätunnuksen perusteella

        Args:
            username(str): käyttäjän käyttäjätunnus

        Returns:
            Jos käyttäjätunnus löytyy tietokannasta palauttaa sen User-oliona,
            jos ei löydy niin None
        """
        cursor = self._connection.cursor()
        row = cursor.execute(
            "SELECT * FROM Users WHERE username = ?", [username]).fetchone()
        return get_user_by_row(row)

    def find_all_users(self):
        """Palauttaa kaikki käyttäjät

        Returns:
            Tietokannasta löytyvät käyttäjät listana
        """
        cursor = self._connection.cursor()
        rows = cursor.execute("SELECT * FROM Users").fetchall()
        return list(map(get_user_by_row, rows))

    def clear_table(self):
        """Tyhjentää kaikki käyttäjät tietokannasta
        """
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM Users")
        self._connection.commit()

    def add_budget(self, budget, username):
        """Lisää käyttäjälle uuden budjetin

        Args:
            budget(int): käyttäjän antama budjetti
            username(str): käyttäjän käyttäjätunnus

        Returns:
            Päivitetyn budjetin pyöristettynä kahden desimaalin tarkkuudelle
        """
        cursor = self._connection.cursor()

        cursor.execute("UPDATE Users SET budget=? WHERE username=?", [
                       budget, username])
        self._connection.commit()
        return round(budget, 2)

    def get_budget(self, username):
        """Palauttaa käyttäjän budjetin

        Args:
            username(str): käyttäjän käyttäjätunnus

        Returns:
            Käyttäjän budjetin pyöristettynä
            kahden desimaalin tarkkuudella jos budjetti on asetettu muuten None
        """
        cursor = self._connection.cursor()
        row = cursor.execute(
            "SELECT budget FROM Users WHERE username=?", [username]).fetchone()
        return round(row["budget"], 2) if row["budget"] else None


user_repository = UserRepository(get_database_connection())
