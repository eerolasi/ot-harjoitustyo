import unittest
from repositories.user_repository import user_repository
from repositories.transaction_repository import transaction_repository
from entities.user import User
from entities.transaction import Transaction
from services.budget_service import budget_service


class TestUser(unittest.TestCase):
    def setUp(self):
        user_repository.clear_table()
        transaction_repository.clear_table()
        self.user = User("user", "123")
        self.transaction = Transaction(self.user.username, 3)

    def test_add_transaction(self):
        transaction = budget_service.add_transaction(
            self.user.username, self.transaction.amount)
        self.assertEqual(3, transaction)

    def test_get_transactions_sum(self):
        budget_service.add_transaction(
            self.transaction.username, self.transaction.amount)
        budget_service.add_transaction(self.user.username, 5)
        sum = budget_service.get_transactions_sum(self.user.username)
        self.assertEqual(sum, 8)
