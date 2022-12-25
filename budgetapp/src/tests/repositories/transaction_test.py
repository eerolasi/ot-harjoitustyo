import unittest
from repositories.user_repository import user_repository
from repositories.transaction_repository import transaction_repository
from entities.user import User
from entities.transaction import Transaction


class TestTransactions(unittest.TestCase):
    def setUp(self):
        user_repository.clear_table()
        transaction_repository.clear_table()
        self.user = User("user", "123")
        self.transcation = Transaction(self.user.username, "muu", 10)
        self.transcation2 = Transaction(self.user.username, "sijoitukset", 3)

    def test_add_transaction(self):
        transaction_repository.add_transaction(self.transcation)
        self.assertEqual(10, self.transcation.amount)

    def test_get_transactions(self):
        transaction_repository.add_transaction(self.transcation)
        transaction_repository.add_transaction(self.transcation2)
        sum = transaction_repository.get_transactions(self.user.username)
        self.assertEqual(sum, 13)

    def test_get_transactions_by_category(self):
        transaction_repository.add_transaction(self.transcation)
        category = transaction_repository.get_transactions_sum_by_category(
            self.user.username)
        self.assertEqual(
            category, {self.transcation.category: self.transcation.amount})

    def test_clear_transactions(self):
        transaction_repository.add_transaction(self.transcation)
        transaction_repository.clear_transactions(self.user.username)
        sum = transaction_repository.get_transactions(self.user.username)
        self.assertIsNone(sum)
