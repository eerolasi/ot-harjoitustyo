from database_connection import get_database_connection


class TransactionRepository:
    def __init__(self, connection):
        self._connection = connection

    def add_transaction(self, transaction):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO Transactions (username, amount) VALUES (?, ?)", [
                       transaction.username, transaction.amount])
        self._connection.commit()
        return transaction.amount

    def get_transactions(self, user):
        cursor = self._connection.cursor()
        row = cursor.execute(
            "SELECT sum(amount) as sum FROM Transactions WHERE username=?", [user]).fetchone()
        return row["sum"]

    def clear_table(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM Transactions")
        self._connection.commit()


transaction_repository = TransactionRepository(get_database_connection())
