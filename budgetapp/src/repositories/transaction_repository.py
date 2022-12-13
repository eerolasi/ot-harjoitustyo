from database_connection import get_database_connection


class TransactionRepository:
    """Luokka, joka vastaa menoihin liittyvistä tietokantaoperaatioista.
    """

    def __init__(self, connection):
        """Luokan konstruktori, joka muodostaa tietokantayhteyden

        Args:
            connection(object): Tietokantayhteys
        """
        self._connection = connection

    def add_transaction(self, transaction):
        """Tallentaa uuden menon tietokantaan

        Args:
            transaction(object): meno-olio

        Returns:
            Palauttaa menon summan
        """
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO Transactions (username, category, amount) VALUES (?, ?, ?)", [
                       transaction.username, transaction.category, transaction.amount])
        self._connection.commit()
        return transaction.amount

    def get_transactions(self, username):
        """Palauttaa käyttäjän menojen yhteissumman

        Args:
            username(str): käyttäjän käyttäjättunnus

        Returns:
            Palauttaa käyttäjätunnuksen perusteella yhteenlasketun summan
            kaikista käyttäjän menoista
        """
        cursor = self._connection.cursor()
        row = cursor.execute(
            "SELECT sum(amount) as sum FROM Transactions WHERE username=?", [username]).fetchone()
        return row["sum"]

    def get_transactions_by_category(self, username):
        """Palauttaa käyttäjän menojen jakauman kategorisoittain

        Args:
            username(str): käyttäjän käyttäjätunnus

        Returns:
            Palauttaa sanakirjan, jossa kategoriat ja niitä vastaavat menojen summat
        """
        cursor = self._connection.cursor()
        rows = cursor.execute(
            '''SELECT sum(amount) as amount, category FROM Transactions WHERE
            username=? group by category''', [username]).fetchall()
        return {i["category"]: i["amount"] for i in rows}

    def clear_transactions(self, username):
        """Tyhjentää kaikki käyttäjän menot

        Args:
            username(str): käyttäjän käyttäjätunnus
        """
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM Transactions WHERE username=?", [username])
        self._connection.commit()

    def clear_table(self):
        """Tyhjentää kaikkien käyttäjien kaikki menot tietokannasta
        """
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM Transactions")
        self._connection.commit()


transaction_repository = TransactionRepository(get_database_connection())
