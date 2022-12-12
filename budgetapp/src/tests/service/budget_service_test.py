import unittest
from repositories.user_repository import user_repository
from repositories.transaction_repository import transaction_repository
from entities.user import User
from entities.transaction import Transaction
from services.budget_service import budget_service, InvalidInputError, UserExitsError, LoginError


class TestUser(unittest.TestCase):
    def setUp(self):
        user_repository.clear_table()
        transaction_repository.clear_table()
        self.user = User("user", "123", 100)
        self.transaction = Transaction(self.user.username,"muu", 2)
        self.transaction2 = Transaction(self.user.username, "ruoka", 3)

    def login_user(self):
        budget_service.signup(self.user.username,self.user.password)

    def test_signup(self):
        signed = budget_service.signup(self.user.username, self.user.password)
        budget_service.login(signed.username, signed.password)
        with self.assertRaises(UserExitsError):
            budget_service.signup("user", "1223")

    def test_login_fail(self):
        with self.assertRaises(LoginError):
            budget_service.login(self.user.username, "124")

    def test_get_logged_user(self):
        budget_service.signup(self.user.username, self.user.password)
        logged = budget_service.get_logged_user()
        self.assertEqual(logged.username, self.user.username)

    def test_add_budget(self):
        self.login_user()
        with self.assertRaises(InvalidInputError):
            budget_service.add_budget(-1)
        budget = budget_service.add_budget(100)
        self.assertEqual(100, budget)

    def test_add_transaction(self):
        self.login_user()
        with self.assertRaises(InvalidInputError):
            budget_service.add_transaction("muu", -1)
        transaction = budget_service.add_transaction(
            self.transaction2.category, self.transaction2.amount)
        self.assertEqual(3, transaction)

    def test_get_transactions_sum(self):
        budget_service.get_transactions_sum()
        budget_service.add_transaction(
            self.transaction.category, self.transaction2.amount)
        budget_service.add_transaction( "muu", 5)
        sum = budget_service.get_transactions_sum()
        self.assertEqual(sum, 8)
